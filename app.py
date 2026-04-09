"""
OpsClarity v3.1 - AI Finance Control Tower for Indian CAs and SMEs

""",
        unsafe_allow_html=True,
    )


def render_pricing_block() -> None:
    st.markdown(
        """
<div class="grid3" style="margin-top:1rem">
  <div class="card">
    <span class="tag">Starter</span>
    <div class="title" style="margin-top:.5rem">Rs 1,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For single operators and small firms managing up to 10 clients.</div>
    <div class="part-v" style="margin-top:.8rem">Includes health scoring, decision dashboard, action inbox, GST checks, cash forecast, and branded reports.</div>
  </div>
  <div class="card" style="border-color:rgba(201,168,76,.35);background:#0F1008">
    <span class="tag">Growth</span>
    <div class="title" style="margin-top:.5rem">Rs 4,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For CA firms managing active client portfolios every month.</div>
    <div class="part-v" style="margin-top:.8rem">Adds multi-client portfolio view, recurring advisory workflow, GST follow-up depth, and automation queue support.</div>
  </div>
  <div class="card">
    <span class="tag">Partner</span>
    <div class="title" style="margin-top:.5rem">Rs 9,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For firms standardizing advisory workflows across a larger team.</div>
    <div class="part-v" style="margin-top:.8rem">Adds white-label operating cadence, higher-volume portfolio usage, and premium onboarding support.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
Run:
  pip install -r requirements.txt
  streamlit run app.py
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

APP_VERSION = "3.1"
DATA_DIR = Path(".opsclarity_data")
CLIENTS_FILE = DATA_DIR / "clients.json"
ACTIONS_FILE = DATA_DIR / "actions.json"
AUTOMATIONS_FILE = DATA_DIR / "automations.json"
HISTORY_FILE = DATA_DIR / "client_history.json"
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "916362319163")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
RAZORPAY_PAYMENT_LINK = os.environ.get("RAZORPAY_PAYMENT_LINK", "")
ADMIN_MODE = os.environ.get("OPSCLARITY_ADMIN_MODE", "0") == "1"

try:
    OPENAI_KEY = OPENAI_KEY or st.secrets.get("OPENAI_API_KEY", "")
    WHATSAPP_NUMBER = st.secrets.get("WHATSAPP_NUMBER", WHATSAPP_NUMBER)
    RAZORPAY_PAYMENT_LINK = st.secrets.get("RAZORPAY_PAYMENT_LINK", RAZORPAY_PAYMENT_LINK)
    ADMIN_MODE = bool(st.secrets.get("OPSCLARITY_ADMIN_MODE", ADMIN_MODE))
except Exception:
    pass

st.set_page_config(
    page_title="OpsClarity - AI CFO for Indian SMEs & CA Firms",
    page_icon="OC",
    layout="wide",
    initial_sidebar_state="collapsed",
)


INDUSTRY_MAP = {
    "Manufacturing": "manufacturing",
    "Restaurant / Cafe": "restaurant",
    "Clinic / Diagnostic": "clinic",
    "Retail / Distribution": "retail",
    "Agency / Consulting": "agency",
    "Logistics / Transport": "logistics",
    "Construction": "construction",
    "Textile / Garments": "textile",
    "Pharma / Medical": "pharma",
    "Print / Packaging": "printing",
}

INDUSTRY_BENCHMARKS = {
    "manufacturing": 18,
    "restaurant": 15,
    "clinic": 25,
    "retail": 12,
    "agency": 35,
    "logistics": 10,
    "construction": 20,
    "textile": 14,
    "pharma": 22,
    "printing": 16,
}

GST_RATES = {
    "Raw Materials": 18,
    "Labor": 0,
    "Rent": 18,
    "Logistics": 12,
    "Packaging": 18,
    "Technology": 18,
    "Electricity": 18,
    "Professional Fees": 18,
    "Operations": 18,
    "General": 18,
    "Manufacturing": 18,
    "Travel": 5,
    "Bank Charges": 18,
    "Internet": 18,
    "Salary": 0,
    "Sales": 18,
}


def ensure_store() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for path in [CLIENTS_FILE, ACTIONS_FILE, AUTOMATIONS_FILE, HISTORY_FILE]:
        if not path.exists():
            path.write_text("{}", encoding="utf-8")


def read_json(path: Path) -> dict:
    ensure_store()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, data: dict) -> None:
    ensure_store()
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def sid(*parts) -> str:
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def fmt(v) -> str:
    v = float(v or 0)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1e7:
        return f"{sign}Rs {v/1e7:.1f}Cr"
    if v >= 1e5:
        return f"{sign}Rs {v/1e5:.1f}L"
    if v >= 1000:
        return f"{sign}Rs {v/1000:.0f}K"
    return f"{sign}Rs {v:.0f}"


def fmt_exact(v) -> str:
    return f"Rs {int(float(v or 0)):,}"


def pct(part, whole) -> float:
    return float(part or 0) / max(float(whole or 0), 1) * 100


def wa_link(message: str, number: str = "") -> str:
    return f"https://wa.me/{number or WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"


def clean_status(s: pd.Series) -> pd.Series:
    return s.astype(str).str.lower().str.strip()


def split_books(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return df[df["Type"].astype(str).str.title() == "Sales"].copy(), df[df["Type"].astype(str).str.title() == "Expense"].copy()


def classify_expense(text) -> str:
    d = str(text).lower()
    rules = [
        ("Rent", ["rent", "lease"]),
        ("Salary", ["salary", "wage", "payroll"]),
        ("Technology", ["software", "laptop", "cloud", "saas"]),
        ("Internet", ["internet", "wifi", "broadband"]),
        ("Electricity", ["electricity", "power"]),
        ("Professional Fees", ["ca", "audit", "legal", "consult"]),
        ("Travel", ["travel", "uber", "ola", "flight", "hotel"]),
        ("Raw Materials", ["raw", "material", "steel", "inventory"]),
        ("Logistics", ["logistics", "freight", "courier", "transport"]),
        ("Packaging", ["pack", "box", "carton"]),
        ("Bank Charges", ["bank", "charge", "fee"]),
    ]
    for name, keys in rules:
        if any(k in d for k in keys):
            return name
    return "Operations"


def coerce_amount(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("Rs.", "", regex=False)
        .str.replace("Rs", "", regex=False)
        .str.replace(" Dr", "", regex=False)
        .str.replace(" Cr", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False),
        errors="coerce",
    ).abs().fillna(0)


def infer_type(row: pd.Series) -> str:
    raw = " ".join(str(row.get(c, "")) for c in ["Type", "Category", "Party", "Narration"]).lower()
    if any(k in raw for k in ["expense", "purchase", "payment", "debit", "salary", "rent", "raw", "logistics"]):
        return "Expense"
    return "Sales"


def is_design_aid(raw: pd.DataFrame) -> bool:
    cells = []
    for r in range(min(3, len(raw))):
        for c in range(min(16, len(raw.columns))):
            cells.append(str(raw.iloc[r, c]).lower().strip())
    text = " ".join(cells)
    return "months" in text and ("investors" in text or "expenses" in text or "madhu" in text or "deepak" in text)


def parse_design_aid(file) -> tuple[pd.DataFrame | None, bool, str]:
    file.seek(0)
    raw = pd.read_csv(file, header=None, dtype=str).fillna("")
    month_map = {
        "august": "2024-08", "aug": "2024-08",
        "sept": "2024-09", "sep": "2024-09", "september": "2024-09",
        "oct": "2024-10", "october": "2024-10",
        "nov": "2024-11", "november": "2024-11",
        "dec": "2024-12", "december": "2024-12",
        "jan": "2025-01", "january": "2025-01",
        "feb": "2025-02", "february": "2025-02",
        "mar": "2025-03", "march": "2025-03",
        "apr": "2025-04", "april": "2025-04",
        "may": "2025-05", "jun": "2025-06", "june": "2025-06",
        "jul": "2025-07", "july": "2025-07",
    }
    skip = {"total", "grand total", "each", "sub total", "-", ""}
    records = []
    for _, row in raw.iterrows():
        mk = str(row.iloc[0]).strip().lower()
        if mk not in month_map:
            continue
        dt = pd.Timestamp(month_map[mk] + "-01")
        for col_i, party, typ in [(1, "Madhu", "Sales"), (2, "Deepak", "Sales"), (5, "Ashok", "Expense"), (6, "Office", "Expense"), (9, "Praveen", "Expense")]:
            if col_i >= len(row):
                continue
            try:
                v = float(str(row.iloc[col_i]).replace(",", "").strip())
                if v > 0:
                    records.append({"Date": dt, "Type": typ, "Party": party, "Category": "Investment/Capital" if typ == "Sales" else "Operations", "Amount": v, "Status": "Paid", "Invoice_No": "-", "GSTIN": ""})
            except Exception:
                pass
    cur_m, cur_d = None, None
    for _, row in raw.iterrows():
        c11 = str(row.iloc[11]).strip().lower() if len(row) > 11 else ""
        c14 = str(row.iloc[14]).strip().lower() if len(row) > 14 else ""
        if c11 in month_map:
            cur_m = month_map[c11]
        if c14 in month_map:
            cur_d = month_map[c14]
        for period, amount_i, desc_i, party in [(cur_m, 11, 12, "Madhu"), (cur_d, 14, 15, "Deepak")]:
            if not period or len(row) <= desc_i:
                continue
            desc = str(row.iloc[desc_i]).strip()
            if desc.lower() in skip:
                continue
            try:
                v = float(str(row.iloc[amount_i]).replace(",", "").strip())
                if v > 0:
                    records.append({"Date": pd.Timestamp(period + "-01"), "Type": "Expense", "Party": party, "Category": classify_expense(desc), "Amount": v, "Status": "Paid", "Invoice_No": "-", "GSTIN": ""})
            except Exception:
                pass
    if not records:
        return None, False, "No transactions found in Design AID format."
    df = pd.DataFrame(records).drop_duplicates()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df, True, f"{len(df):,} Design AID transactions loaded"


def parse_file(file) -> tuple[pd.DataFrame | None, bool, str]:
    try:
        name = file.name.lower()
        if name.endswith((".xlsx", ".xls")):
            try:
                raw = pd.read_excel(file, header=None, engine="openpyxl").fillna("")
                file.seek(0)
                df = pd.read_excel(file, engine="openpyxl")
            except Exception:
                file.seek(0)
                raw = pd.read_excel(file, header=None, engine="xlrd").fillna("")
                file.seek(0)
                df = pd.read_excel(file, engine="xlrd")
        elif name.endswith(".csv"):
            try:
                raw = pd.read_csv(file, header=None, dtype=str).fillna("")
                file.seek(0)
                df = pd.read_csv(file)
            except Exception:
                file.seek(0)
                raw = pd.read_csv(file, header=None, encoding="latin1", dtype=str).fillna("")
                file.seek(0)
                df = pd.read_csv(file, encoding="latin1")
        else:
            return None, False, "Use .csv, .xlsx, or .xls"
        if name.endswith(".csv") and is_design_aid(raw):
            return parse_design_aid(file)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        rename = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date", "dt", "day"]):
                rename[col] = "Date"
            elif any(x in cl for x in ["amount", "amt", "value", "total", "debit", "credit", "rs", "₹"]):
                rename[col] = "Amount"
            elif any(x in cl for x in ["type", "txn", "dr/cr", "nature"]):
                rename[col] = "Type"
            elif any(x in cl for x in ["particular", "category", "head", "narration", "ledger"]):
                rename[col] = "Category"
            elif any(x in cl for x in ["party", "customer", "vendor", "name", "client"]):
                rename[col] = "Party"
            elif any(x in cl for x in ["status", "paid", "pending", "overdue", "due"]):
                rename[col] = "Status"
            elif any(x in cl for x in ["bill", "invoice", "voucher", "ref", "num", "no"]):
                rename[col] = "Invoice_No"
            elif "gst" in cl:
                rename[col] = "GSTIN"
        df = df.rename(columns=rename)
        if "Date" not in df.columns or "Amount" not in df.columns:
            return None, False, "Could not find Date and Amount columns."
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["Date"])
        df["Amount"] = coerce_amount(df["Amount"])
        if "Type" not in df.columns:
            df["Type"] = ""
        df["Type"] = df["Type"].astype(str).str.strip().str.title().replace(
            {"Dr": "Expense", "Debit": "Expense", "Payment": "Expense", "Purchase": "Expense", "Cr": "Sales", "Credit": "Sales", "Receipt": "Sales", "Sale": "Sales", "Revenue": "Sales"}
        )
        mask = ~df["Type"].isin(["Sales", "Expense"])
        df.loc[mask, "Type"] = df.loc[mask].apply(infer_type, axis=1)
        for col, default in [("Status", "Paid"), ("Category", "General"), ("Party", "Unknown"), ("Invoice_No", "-"), ("GSTIN", "")]:
            if col not in df.columns:
                df[col] = default
        expense_mask = df["Type"] == "Expense"
        df.loc[expense_mask & df["Category"].astype(str).isin(["", "General", "nan"]), "Category"] = df.loc[
            expense_mask & df["Category"].astype(str).isin(["", "General", "nan"]), "Party"
        ].apply(classify_expense)
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        df = df[df["Amount"] > 0].copy()
        return df, True, f"{len(df):,} transactions loaded ({df['Date'].min():%b %Y} to {df['Date'].max():%b %Y})"
    except Exception as e:
        return None, False, f"Error: {e}. Try saving as CSV UTF-8."


def make_demo_data(client_name: str = "Demo Client") -> pd.DataFrame:
    seed = abs(hash(client_name)) % (2**32)
    np.random.seed(seed)
    dates = pd.date_range(datetime.now() - timedelta(days=365), datetime.now(), freq="D")
    customers = ["ABC Corp", "XYZ Industries", "PQR Mfg", "LMN Traders", "DEF Enterprises"]
    vendors = ["Steel Supplier A", "Steel Supplier B", "Raw Material Co", "Logistics Ltd", "Packaging Inc", "Payroll"]
    rows = []
    for d in dates:
        if np.random.random() > 0.35:
            rows.append(
                {
                    "Date": d,
                    "Type": "Sales",
                    "Party": np.random.choice(customers, p=[0.42, 0.22, 0.16, 0.10, 0.10]),
                    "Amount": round(float(np.random.uniform(55000, 240000)), 2),
                    "Status": np.random.choice(["Paid", "Paid", "Overdue", "Pending"], p=[0.55, 0.25, 0.12, 0.08]),
                    "Category": "Sales",
                    "Invoice_No": f"INV-{np.random.randint(1000, 9999)}",
                    "GSTIN": "29ABCDE1234F1Z5",
                }
            )
        for _ in range(np.random.randint(1, 4)):
            rows.append(
                {
                    "Date": d,
                    "Type": "Expense",
                    "Party": np.random.choice(vendors),
                    "Amount": round(float(np.random.uniform(9000, 85000)), 2),
                    "Status": "Paid",
                    "Category": np.random.choice(["Raw Materials", "Labor", "Rent", "Logistics", "Packaging", "Technology"], p=[0.38, 0.18, 0.10, 0.14, 0.12, 0.08]),
                    "Invoice_No": f"BILL-{np.random.randint(1000, 9999)}",
                    "GSTIN": "" if np.random.random() < 0.18 else "29ABCDE1234F1Z5",
                }
            )
    demo = pd.DataFrame(rows)
    demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
    return demo


@st.cache_data(ttl=300, show_spinner=False)
def find_leaks(df_json: str, industry: str) -> list[dict]:
    df = pd.read_json(io.StringIO(df_json))
    df["Date"] = pd.to_datetime(df["Date"])
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    expense_total = float(expenses["Amount"].sum())
    profit = revenue - expense_total
    margin = pct(profit, revenue)
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    leaks = []

    if len(sales) and "Status" in sales.columns:
        od = sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "due", "outstanding", "unpaid"])]
        od_amt = float(od["Amount"].sum())
        if od_amt > max(10000, revenue * 0.04):
            debtors = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_name = str(debtors.index[0]) if len(debtors) else "Top Customer"
            top_amt = float(debtors.iloc[0]) if len(debtors) else od_amt
            leaks.append(
                {
                    "id": "cash_stuck",
                    "severity": "critical",
                    "priority": 1,
                    "category": "Collections",
                    "rupee_impact": od_amt,
                    "annual_impact": od_amt * 0.18,
                    "headline": f"{fmt_exact(od_amt)} stuck in unpaid invoices",
                    "sub": f"{len(debtors)} customers overdue",
                    "problem": f"{len(debtors)} customers owe {fmt_exact(od_amt)}",
                    "reason": "Top overdue accounts: " + " | ".join([f"{n}: {fmt_exact(a)}" for n, a in debtors.head(5).items()]),
                    "action": f"Call {top_name} today and offer 2% discount for payment within 48 hours",
                    "benchmark": f"Healthy SMEs keep overdue below 5% of revenue. Yours is {pct(od_amt, revenue):.1f}%.",
                    "next_action": f"Call {top_name} and send WhatsApp reminder",
                    "owner": "Collections owner",
                    "channel": "WhatsApp",
                    "template": f"Hi {top_name}, invoice of {fmt(top_amt)} is overdue. We can offer 2% off if settled within 48 hours. Can you confirm payment date?",
                }
            )

    for category in expenses["Category"].dropna().astype(str).unique() if len(expenses) else []:
        ce = expenses[expenses["Category"].astype(str) == category]
        vendors = ce.groupby("Party")["Amount"].agg(["mean", "count", "sum"])
        vendors = vendors[vendors["count"] >= 2]
        if len(vendors) < 2:
            continue
        cheapest = float(vendors["mean"].min())
        expensive_vendor = str(vendors["mean"].idxmax())
        expensive_price = float(vendors["mean"].max())
        annual_volume = float(vendors.loc[expensive_vendor, "sum"])
        if cheapest > 0 and expensive_price > cheapest * 1.14:
            annual_waste = (expensive_price - cheapest) * (annual_volume / max(expensive_price, 1))
            if annual_waste > 15000:
                leaks.append(
                    {
                        "id": f"cost_bleed_{sid(category)}",
                        "severity": "warning",
                        "priority": 2,
                        "category": "Vendor Costs",
                        "rupee_impact": annual_waste,
                        "annual_impact": annual_waste,
                        "headline": f"{fmt_exact(annual_waste)} overpaid on {category}/year",
                        "sub": f"{expensive_vendor} is {((expensive_price / cheapest) - 1) * 100:.0f}% above cheapest vendor",
                        "problem": f"{expensive_vendor} average transaction is {fmt_exact(expensive_price)}",
                        "reason": f"Cheapest alternative average is {fmt_exact(cheapest)} for similar category",
                        "action": f"Get 2 quotes for {category} and renegotiate {expensive_vendor}",
                        "benchmark": "Best SMEs run annual vendor quote checks on top 3 costs.",
                        "next_action": f"Send vendor quote request for {category}",
                        "owner": "Founder / Procurement",
                        "channel": "Email",
                        "template": f"We are reviewing {category} suppliers for a 12-month contract. Please share your best rate for our current volume this week.",
                    }
                )
                break

    if margin < benchmark - 3 and revenue > 0:
        gap = ((benchmark - margin) / 100) * revenue
        if gap > 25000:
            leaks.append(
                {
                    "id": "margin_gap",
                    "severity": "critical" if margin < 5 else "warning",
                    "priority": 3,
                    "category": "Profitability",
                    "rupee_impact": gap,
                    "annual_impact": gap,
                    "headline": f"{fmt_exact(gap)} margin gap vs peers",
                    "sub": f"Your margin {margin:.1f}% vs {benchmark}% benchmark",
                    "problem": f"Net profit is {fmt_exact(profit)} on {fmt_exact(revenue)} revenue",
                    "reason": "Pricing, vendor costs, or collections are pulling margin below peer benchmark",
                    "action": "Raise prices 5% on top 3 offerings and cut largest recurring cost by 10%",
                    "benchmark": f"{industry.title()} benchmark net margin is {benchmark}%.",
                    "next_action": "Run pricing review and top-cost audit",
                    "owner": "Founder / CA",
                    "channel": "Internal",
                    "template": "Review top offerings for a 5% price increase and renegotiate the biggest recurring cost.",
                }
            )

    if revenue > 0 and len(sales):
        concentration = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(concentration) and pct(float(concentration.iloc[0]), revenue) > 28:
            top_customer = str(concentration.index[0])
            leaks.append(
                {
                    "id": "concentration",
                    "severity": "warning",
                    "priority": 4,
                    "category": "Revenue Risk",
                    "rupee_impact": float(concentration.iloc[0]) * 0.3,
                    "annual_impact": float(concentration.iloc[0]) * 0.3,
                    "headline": f"{top_customer} is {pct(float(concentration.iloc[0]), revenue):.0f}% of revenue",
                    "sub": "Single-client dependency risk",
                    "problem": f"{top_customer} contributes {fmt_exact(concentration.iloc[0])}",
                    "reason": "If this customer delays payment, cash flow can break even when P&L looks healthy",
                    "action": "Close 2 new customers and set a 25% single-client cap",
                    "benchmark": "Healthy SMEs keep any one customer below 25% of revenue.",
                    "next_action": "Start 10-account outbound list",
                    "owner": "Sales owner",
                    "channel": "Email",
                    "template": "Hi, we are expanding capacity this month. If you know a business that needs reliable supply or service support, we can offer a referral benefit. Happy to share details.",
                }
            )

    monthly_exp = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    if len(monthly_exp) >= 4:
        recent, prior = float(monthly_exp.tail(3).mean()), float(monthly_exp.iloc[:-3].mean())
        if prior > 0 and recent > prior * 1.18:
            spike = (recent - prior) * 12
            leaks.append(
                {
                    "id": "expense_spike",
                    "severity": "warning",
                    "priority": 5,
                    "category": "Cost Control",
                    "rupee_impact": spike,
                    "annual_impact": spike,
                    "headline": f"Monthly costs up {((recent / prior) - 1) * 100:.0f}%",
                    "sub": f"{fmt(recent - prior)} extra per month",
                    "problem": f"Monthly spend moved from {fmt(prior)} to {fmt(recent)}",
                    "reason": "Expense base expanded faster than revenue trend",
                    "action": "Freeze non-essential spend and audit all recurring vendors",
                    "benchmark": "Expenses should not rise faster than revenue for 3 straight months.",
                    "next_action": "Approve-only policy for new expenses this week",
                    "owner": "Finance owner",
                    "channel": "Internal",
                    "template": "Effective today, all non-essential expenses are paused pending review of recurring vendors and subscriptions.",
                }
            )

    eligible = expenses[(expenses["Amount"] > 25000) & (expenses["Category"].map(lambda c: GST_RATES.get(str(c), 18) > 0))] if len(expenses) else pd.DataFrame()
    missed_itc = float(eligible["Amount"].sum()) * 0.18 * 0.09 if len(eligible) else 0
    if missed_itc > 8000:
        leaks.append(
            {
                "id": "tax_gst",
                "severity": "info",
                "priority": 6,
                "category": "Tax Recovery",
                "rupee_impact": missed_itc,
                "annual_impact": missed_itc,
                "headline": f"~{fmt_exact(missed_itc)} GST ITC to verify",
                "sub": "Estimated Input Tax Credit opportunity",
                "problem": f"Eligible purchases above Rs 25K total {fmt_exact(float(eligible['Amount'].sum()))}",
                "reason": "Large invoices without tight GSTR-2B reconciliation often lead to missed ITC",
                "action": "Ask CA to review ITC eligibility and GSTR-2B matching before next GSTR-3B",
                "benchmark": "Monthly 2B reconciliation prevents ITC leakage and reversals.",
                "next_action": "Email CA for ITC review",
                "owner": "CA",
                "channel": "Email",
                "template": "Please review ITC eligibility and GSTR-2B matching for all purchase invoices above Rs 25K before the next GSTR-3B filing.",
            }
        )
    return sorted(leaks, key=lambda x: (x["priority"], -x["rupee_impact"]))


def alerts_engine(df: pd.DataFrame, industry: str) -> list[dict]:
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    alerts = []
    if len(sales) and "Status" in sales.columns:
        overdue = sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "outstanding", "unpaid"])]
        od_amt = float(overdue["Amount"].sum())
        if od_amt > revenue * 0.08:
            alerts.append({"severity": "critical", "title": f"Cash risk - {fmt(od_amt)} overdue", "body": f"{pct(od_amt, revenue):.1f}% of revenue is unpaid.", "action": "Launch collections today", "impact": od_amt})
    monthly_exp = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    if len(monthly_exp) >= 4:
        recent, prior = float(monthly_exp.tail(2).mean()), float(monthly_exp.iloc[:-2].mean())
        if prior > 0 and recent > prior * 1.22:
            alerts.append({"severity": "warning", "title": f"Expenses spiked {((recent / prior) - 1) * 100:.0f}%", "body": f"Costs moved from {fmt(prior)} to {fmt(recent)}.", "action": "Audit new recurring expenses", "impact": (recent - prior) * 12})
    margin = pct(float(sales["Amount"].sum() - expenses["Amount"].sum()), revenue)
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    if revenue > 0 and margin < benchmark - 5:
        alerts.append({"severity": "warning", "title": f"Margin {benchmark - margin:.0f}pp below peers", "body": f"{margin:.1f}% vs {benchmark}% benchmark.", "action": "Run pricing and top-cost review", "impact": ((benchmark - margin) / 100) * revenue})
    return sorted(alerts, key=lambda x: x["impact"], reverse=True)


def gst_intelligence(df: pd.DataFrame) -> dict:
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    by_cat = {}
    for cat, group in expenses.groupby("Category"):
        rate = GST_RATES.get(str(cat), 18)
        if rate <= 0:
            continue
        expense = float(group["Amount"].sum())
        itc_estimate = expense * (rate / (100 + rate))
        gstin = group["GSTIN"].astype(str) if "GSTIN" in group else pd.Series([""] * len(group))
        missing_gstin = int((gstin.str.len() < 10).sum())
        risk_discount = min(0.35, missing_gstin / max(len(group), 1) * 0.35)
        by_cat[str(cat)] = {
            "expense": expense,
            "rate": rate,
            "itc_estimate": itc_estimate,
            "claimable": max(0, itc_estimate * (0.9 - risk_discount)),
            "missing_gstin": missing_gstin,
            "invoice_count": int(len(group)),
        }
    total_itc = sum(v["itc_estimate"] for v in by_cat.values())
    claimable = sum(v["claimable"] for v in by_cat.values())
    missed = max(0, total_itc - claimable)
    vendor_risk = []
    for vendor, group in expenses.groupby("Party") if len(expenses) else []:
        spend = float(group["Amount"].sum())
        if spend < 50000:
            continue
        gstin = group["GSTIN"].astype(str) if "GSTIN" in group else pd.Series([""] * len(group))
        blank_pct = pct((gstin.str.len() < 10).sum(), len(group))
        dup_bills = int(group["Invoice_No"].astype(str).duplicated().sum()) if "Invoice_No" in group else 0
        risk_points = blank_pct + dup_bills * 10
        if risk_points > 20:
            vendor_risk.append({"vendor": str(vendor), "spend": spend, "risk": "High" if risk_points > 45 else "Medium", "reason": f"{blank_pct:.0f}% missing GSTIN; {dup_bills} duplicate bill refs"})
    vendor_risk = sorted(vendor_risk, key=lambda x: x["spend"], reverse=True)[:8]
    vendor_comply = max(35, 100 - len(vendor_risk) * 9)
    itc_claimed = min(95, pct(claimable, max(total_itc, 1)) if total_itc else 90)
    filing = 88 if revenue > 0 else 70
    score = int((itc_claimed * 0.42) + (vendor_comply * 0.36) + (filing * 0.22))
    return {
        "itc_by_cat": by_cat,
        "total_itc": total_itc,
        "claimable": claimable,
        "missed_est": missed,
        "gst_on_sales": revenue * 0.18,
        "risk_vendors": vendor_risk,
        "compliance_score": max(5, min(99, score)),
        "mismatch_count": sum(v["missing_gstin"] for v in by_cat.values()),
        "mismatch_value": missed,
    }


def cash_flow_forecast(df: pd.DataFrame) -> dict:
    sales, expenses = split_books(df)
    ms = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum() if len(sales) else pd.Series(dtype=float)
    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    avg_rev = float(ms.tail(3).mean()) if len(ms) >= 3 else float(ms.mean() if len(ms) else 0)
    avg_exp = float(me.tail(3).mean()) if len(me) >= 3 else float(me.mean() if len(me) else 0)
    trend = float(ms.tail(3).mean() / ms.iloc[-6:-3].mean()) if len(ms) >= 6 and float(ms.iloc[-6:-3].mean()) > 0 else 1.0
    od_amt = float(sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "outstanding", "unpaid"])]["Amount"].sum()) if len(sales) and "Status" in sales.columns else 0
    scenarios = {}
    for label, rev_mult, exp_mult, collect_rate in [("Best Case", 1.15 * trend, 0.95, 0.75), ("Expected", 1.0 * trend, 1.00, 0.50), ("Worst Case", 0.82 * trend, 1.05, 0.25)]:
        monthly_in = avg_rev * rev_mult
        monthly_out = avg_exp * exp_mult
        od_collect = od_amt * collect_rate
        net = monthly_in - monthly_out
        scenarios[label] = {"monthly_in": monthly_in, "monthly_out": monthly_out, "od_collect": od_collect, "cf_30": net + od_collect, "cf_60": net * 2 + od_collect, "cf_90": net * 3 + od_collect}
    cash_proxy = max(0, float(ms.tail(1).sum()) - float(me.tail(1).sum()))
    return {"scenarios": scenarios, "avg_rev": avg_rev, "avg_exp": avg_exp, "runway": cash_proxy / max(avg_exp, 1), "od_amt": od_amt, "trend": trend}


def reconciliation_engine(df: pd.DataFrame) -> dict:
    sales, expenses = split_books(df)
    duplicates = df[df.duplicated(subset=["Date", "Party", "Amount", "Type"], keep=False)].copy()
    duplicate_payments = expenses[expenses.duplicated(subset=["Party", "Amount", "Invoice_No"], keep=False)].copy() if len(expenses) else pd.DataFrame()
    unmatched = sales[clean_status(sales["Status"]).isin(["pending", "overdue", "not paid", "outstanding", "unpaid"])].copy() if len(sales) and "Status" in sales.columns else pd.DataFrame()
    possible = []
    paid = sales[clean_status(sales["Status"]).isin(["paid", "received"])] if len(sales) and "Status" in sales.columns else sales.iloc[0:0]
    for _, inv in unmatched.head(20).iterrows():
        near = paid[(paid["Party"].astype(str) == str(inv["Party"])) & ((paid["Amount"] - inv["Amount"]).abs() <= max(100, inv["Amount"] * 0.03))]
        if len(near):
            possible.append({"invoice": str(inv.get("Invoice_No", "-")), "party": str(inv["Party"]), "amount": float(inv["Amount"]), "match_count": int(len(near)), "action": "Verify whether payment was received but status not updated"})
    return {"duplicate_rows": duplicates, "duplicate_payments": duplicate_payments, "unmatched_invoices": unmatched, "possible_matches": possible, "risk_score": min(99, int(len(duplicates) * 2 + len(duplicate_payments) * 4 + len(unmatched) * 1.5))}


def health_score(df: pd.DataFrame, industry: str) -> int:
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    margin = pct(revenue - float(expenses["Amount"].sum()), revenue)
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    overdue = float(sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "outstanding", "unpaid"])]["Amount"].sum()) if len(sales) and "Status" in sales.columns else 0
    monthly_exp = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    trend = float(monthly_exp.tail(2).mean() / monthly_exp.iloc[:-2].mean()) if len(monthly_exp) >= 4 and float(monthly_exp.iloc[:-2].mean()) > 0 else 1.0
    gst_score = gst_intelligence(df)["compliance_score"]
    score = 58 + min(22, (margin / max(benchmark, 1)) * 22) - min(22, pct(overdue, revenue) * 1.8) - min(14, max(0, (trend - 1.1) * 55)) + min(8, max(0, gst_score - 70) / 4)
    return max(5, min(99, int(score)))


def upsert_actions(leaks: list[dict], tenant_id: str, client_id: str) -> list[dict]:
    store = read_json(ACTIONS_FILE)
    key = f"{tenant_id}:{client_id}"
    existing = {a["id"]: a for a in store.get(key, [])}
    for leak in leaks[:8]:
        action_id = sid(tenant_id, client_id, leak["id"], leak["next_action"])
        existing.setdefault(
            action_id,
            {
                "id": action_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "leak_id": leak["id"],
                "title": leak["next_action"],
                "owner": leak.get("owner", "Finance owner"),
                "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "impact": float(leak.get("rupee_impact", 0)),
                "status": "Open",
                "channel": leak.get("channel", "Internal"),
                "template": leak.get("template", ""),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            },
        )
    store[key] = list(existing.values())
    write_json(ACTIONS_FILE, store)
    return sorted(store[key], key=lambda x: (x["status"] != "Open", -x["impact"]))


def update_action(action_id: str, status: str, tenant_id: str, client_id: str) -> None:
    store = read_json(ACTIONS_FILE)
    key = f"{tenant_id}:{client_id}"
    for item in store.get(key, []):
        if item["id"] == action_id:
            item["status"] = status
    write_json(ACTIONS_FILE, store)


def queue_automation(action: dict) -> None:
    store = read_json(AUTOMATIONS_FILE)
    key = f"{action['tenant_id']}:{action['client_id']}"
    job_id = sid(action["id"], action["channel"], datetime.now().date())
    jobs = {j["id"]: j for j in store.get(key, [])}
    jobs[job_id] = {
        "id": job_id,
        "tenant_id": action["tenant_id"],
        "client_id": action["client_id"],
        "kind": "collections" if action["channel"] == "WhatsApp" else "follow_up",
        "channel": action["channel"],
        "recipient": action["owner"],
        "message": action.get("template") or action["title"],
        "scheduled_for": (datetime.now() + timedelta(hours=2)).isoformat(timespec="seconds"),
        "status": "Queued",
        "source_action_id": action["id"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    store[key] = list(jobs.values())
    write_json(AUTOMATIONS_FILE, store)


def copilot_answer(question: str, df: pd.DataFrame, leaks: list[dict], industry: str, history: list[dict]) -> str:
    business_terms = [
        "cash", "overdue", "invoice", "profit", "margin", "expense", "cost", "vendor", "gst", "itc",
        "tax", "reconcile", "reconciliation", "runway", "forecast", "revenue", "client", "customer",
        "debtor", "payable", "receivable", "collect", "payment", "risk", "leak", "fix", "tally",
        "what should", "who owes", "money", "business", "ca", "report"
    ]
    if not any(term in question.lower() for term in business_terms):
        return "I can help with finance questions only - cash flow, overdue invoices, GST/ITC, expenses, vendor costs, reconciliation, runway, and client actions. Try asking: **What should I fix first?** or **Who owes me money?**"
    if OPENAI_KEY:
        try:
            from openai import OpenAI

            sales, expenses = split_books(df)
            revenue = float(sales["Amount"].sum())
            exp_tot = float(expenses["Amount"].sum())
            margin = pct(revenue - exp_tot, revenue)
            prompt = "\n".join([f"- {l['headline']}: {l['action']} ({fmt(l['rupee_impact'])})" for l in leaks[:5]])
            client = OpenAI(api_key=OPENAI_KEY)
            messages = [
                {"role": "system", "content": f"You are OpsClarity AI, a CFO assistant for Indian CAs and SMEs. Use rupee numbers, give 2-3 specific actions, and stay under 180 words. Industry={industry}, Revenue={fmt(revenue)}, Expenses={fmt(exp_tot)}, Margin={margin:.1f}%. Leaks:\n{prompt}"}
            ]
            for h in history[-6:]:
                messages.append({"role": h["role"], "content": h["msg"]})
            messages.append({"role": "user", "content": question})
            return client.chat.completions.create(model=OPENAI_MODEL, messages=messages, max_tokens=420, temperature=0.35).choices[0].message.content
        except Exception:
            pass
    q = question.lower()
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    exp_tot = float(expenses["Amount"].sum())
    margin = pct(revenue - exp_tot, revenue)
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    if "gst" in q or "itc" in q:
        gst = gst_intelligence(df)
        return f"Estimated claimable ITC is **{fmt(gst['claimable'])}**. Risky or missed ITC is **{fmt(gst['missed_est'])}** across **{gst['mismatch_count']}** mismatch-risk invoices. Action: ask CA to reconcile GSTR-2B before GSTR-3B and verify high-spend vendor GSTINs."
    if any(x in q for x in ["cash", "overdue", "collect", "debtor"]):
        overdue = sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "outstanding", "unpaid"])] if "Status" in sales.columns else pd.DataFrame()
        od_amt = float(overdue["Amount"].sum()) if len(overdue) else 0
        if od_amt <= 0:
            return "Collections look healthy. No major overdue invoices are detected."
        top = overdue.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        return f"**{fmt_exact(od_amt)}** is unpaid. Biggest debtor: **{top.index[0]}** at **{fmt_exact(top.iloc[0])}**. Action: call today, offer 2% discount for 48-hour payment, and move future invoices to Net-15."
    if any(x in q for x in ["forecast", "runway"]):
        fc = cash_flow_forecast(df)
        exp = fc["scenarios"]["Expected"]
        return f"30-day expected cash flow is **{fmt(exp['cf_30'])}**. Avg revenue: {fmt(fc['avg_rev'])}, avg burn: {fmt(fc['avg_exp'])}, runway: **{fc['runway']:.1f} months**."
    top = leaks[:3]
    lines = "\n".join([f"{i+1}. **{l['headline']}** - {l['next_action']} ({fmt(l['rupee_impact'])})" for i, l in enumerate(top)])
    return f"Your margin is **{margin:.1f}%** vs **{benchmark}%** benchmark.\n\nHighest-impact actions:\n{lines}"


def save_client_snapshot(df: pd.DataFrame, tenant_id: str, client_id: str, client_name: str, industry: str) -> None:
    store = read_json(CLIENTS_FILE)
    clients = store.get(tenant_id, {})
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    exp_tot = float(expenses["Amount"].sum())
    leaks = find_leaks(df.to_json(date_format="iso"), industry)
    gst = gst_intelligence(df)
    fc = cash_flow_forecast(df)
    clients[client_id] = {
        "client_id": client_id,
        "client_name": client_name,
        "industry": industry,
        "revenue": revenue,
        "expenses": exp_tot,
        "margin": pct(revenue - exp_tot, revenue),
        "leak_impact": sum(float(l["rupee_impact"]) for l in leaks),
        "health_score": health_score(df, industry),
        "gst_score": gst["compliance_score"],
        "runway": fc["runway"],
        "records": int(len(df)),
        "last_scan": datetime.now().isoformat(timespec="seconds"),
    }
    store[tenant_id] = clients
    write_json(CLIENTS_FILE, store)
    history = read_json(HISTORY_FILE)
    hkey = f"{tenant_id}:{client_id}"
    history.setdefault(hkey, [])
    history[hkey].append(clients[client_id])
    history[hkey] = history[hkey][-12:]
    write_json(HISTORY_FILE, history)


def client_language_for_leak(leak: dict) -> str:
    if leak["category"] == "Collections":
        return "Your cash problem is not only sales. This money is already earned but not collected. If we collect the top overdue invoices this week, cash improves without taking a loan."
    if leak["category"] == "Vendor Costs":
        return "You may be paying more than needed for the same category of spend. We should use your current volume to negotiate better rates or get alternate supplier quotes."
    if leak["category"] == "Profitability":
        return "Revenue is coming in, but not enough is staying as profit. We should fix pricing and your largest cost category before growth hides the margin issue."
    if leak["category"] == "Tax Recovery":
        return "There may be GST input credit that needs verification. This is not confirmed recovery yet, but it is worth reviewing before the next filing cycle."
    if leak["category"] == "Revenue Risk":
        return "One customer is carrying too much revenue. If they delay payment or reduce orders, cash flow can break even if the business looks profitable."
    return "This issue can affect cash flow or profit. The safest next step is to act on the recommended task this week and review the result next month."


def gst_followup_checklist(df: pd.DataFrame) -> list[str]:
    gst = gst_intelligence(df)
    tasks = []
    for cat, item in sorted(gst["itc_by_cat"].items(), key=lambda x: x[1]["claimable"], reverse=True)[:5]:
        if item["claimable"] > 0:
            tasks.append(f"Verify ITC eligibility for {cat}: estimated claimable {fmt(item['claimable'])}.")
        if item["missing_gstin"] > 0:
            tasks.append(f"Ask client/vendor for GSTIN or tax invoice details for {item['missing_gstin']} {cat} invoices.")
    for vendor in gst["risk_vendors"][:3]:
        tasks.append(f"Cross-check GST compliance for {vendor['vendor']} ({fmt(vendor['spend'])} spend): {vendor['reason']}.")
    if not tasks:
        tasks.append("No major GST follow-up detected. Still reconcile purchase register with GSTR-2B before filing.")
    return tasks[:8]


def ca_client_brief(df: pd.DataFrame, industry: str, client_name: str) -> dict:
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    exp_tot = float(expenses["Amount"].sum())
    leaks = find_leaks(df.to_json(date_format="iso"), industry)
    gst = gst_intelligence(df)
    fc = cash_flow_forecast(df)
    score = health_score(df, industry)
    status = "Healthy" if score >= 75 else "Monitor" if score >= 50 else "At Risk"
    top = leaks[0] if leaks else None
    tell = client_language_for_leak(top) if top else "The client looks stable this month. Use the report to confirm collections, GST, and cash flow remain under control."
    actions = [l["next_action"] for l in leaks[:3]] or ["Review month-end collections", "Reconcile GST purchase invoices", "Confirm next month's cash runway"]
    return {
        "client": client_name,
        "health_score": score,
        "status": status,
        "revenue": revenue,
        "expenses": exp_tot,
        "margin": pct(revenue - exp_tot, revenue),
        "main_issue": top["headline"] if top else "No critical issue detected",
        "why_it_matters": tell,
        "actions": actions,
        "gst_followup": gst_followup_checklist(df)[:3],
        "runway": fc["runway"],
        "gst_score": gst["compliance_score"],
    }


def before_after_summary(tenant_id: str, client_id: str) -> dict:
    history = read_json(HISTORY_FILE).get(f"{tenant_id}:{client_id}", [])
    if len(history) < 2:
        return {"has_history": False}
    prev, latest = history[-2], history[-1]
    return {
        "has_history": True,
        "prev": prev,
        "latest": latest,
        "leak_delta": float(prev.get("leak_impact", 0)) - float(latest.get("leak_impact", 0)),
        "score_delta": float(latest.get("health_score", 0)) - float(prev.get("health_score", 0)),
        "gst_delta": float(latest.get("gst_score", 0)) - float(prev.get("gst_score", 0)),
        "runway_delta": float(latest.get("runway", 0)) - float(prev.get("runway", 0)),
    }


def gstr2b_match(purchases: pd.DataFrame, gstr2b: pd.DataFrame | None) -> pd.DataFrame:
    if gstr2b is None or len(gstr2b) == 0:
        return pd.DataFrame()
    p = purchases.copy()
    g = gstr2b.copy()
    if "Amount" not in g.columns:
        amount_cols = [c for c in g.columns if any(x in str(c).lower() for x in ["amount", "taxable", "invoice value", "value"])]
        if amount_cols:
            g = g.rename(columns={amount_cols[0]: "Amount"})
    if "GSTIN" not in g.columns:
        gst_cols = [c for c in g.columns if "gst" in str(c).lower()]
        if gst_cols:
            g = g.rename(columns={gst_cols[0]: "GSTIN"})
    if "Amount" not in g.columns:
        return pd.DataFrame()
    g["Amount"] = coerce_amount(g["Amount"])
    if "GSTIN" not in g.columns:
        g["GSTIN"] = ""
    p["match_key"] = p.get("GSTIN", "").astype(str).str[:10] + "_" + (p["Amount"].round(-1)).astype(str)
    g["match_key"] = g["GSTIN"].astype(str).str[:10] + "_" + (g["Amount"].round(-1)).astype(str)
    p["GSTR2B_Matched"] = p["match_key"].isin(set(g["match_key"]))
    return p[["Date", "Party", "Category", "Amount", "GSTIN", "Invoice_No", "GSTR2B_Matched"]].sort_values("GSTR2B_Matched")


def client_risk_label(row: pd.Series) -> tuple[str, str]:
    score = float(row.get("health_score", 0))
    margin = float(row.get("margin", 0))
    runway = float(row.get("runway", 0))
    leak_impact = float(row.get("leak_impact", 0))
    revenue = float(row.get("revenue", 0))
    if score < 45 or margin < 0 or runway < 1 or leak_impact > revenue * 0.35:
        return "Critical", "bad"
    if score < 70 or runway < 3 or leak_impact > revenue * 0.15:
        return "Monitor", "warn"
    return "Healthy", "good"


def payment_cta_url(plan: str = "OpsClarity Subscription") -> str:
    if RAZORPAY_PAYMENT_LINK:
        return RAZORPAY_PAYMENT_LINK
    return wa_link(f"Hi, I want to activate the {plan} for OpsClarity.")


def tally_export_xml(from_date: datetime, to_date: datetime, report_name: str = "Day Book") -> str:
    return f"""<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>{report_name}</REPORTNAME>
        <STATICVARIABLES>
          <SVFROMDATE>{from_date:%Y%m%d}</SVFROMDATE>
          <SVTODATE>{to_date:%Y%m%d}</SVTODATE>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>"""


def next_review_date() -> str:
    return (datetime.now() + timedelta(days=30)).strftime("%d %b %Y")
def sample_tally_xml() -> str:
    return """<ENVELOPE>
  <BODY>
    <DATA>
      <TALLYMESSAGE>
        <VOUCHER>
          <DATE>20260401</DATE>
          <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
          <VOUCHERNUMBER>INV-1001</VOUCHERNUMBER>
          <PARTYLEDGERNAME>ABC Corp</PARTYLEDGERNAME>
          <PARTYGSTIN>29ABCDE1234F1Z5</PARTYGSTIN>
          <ALLLEDGERENTRIES.LIST>
            <LEDGERNAME>ABC Corp</LEDGERNAME>
            <AMOUNT>-118000</AMOUNT>
          </ALLLEDGERENTRIES.LIST>
          <ALLLEDGERENTRIES.LIST>
            <LEDGERNAME>Sales</LEDGERNAME>
            <AMOUNT>100000</AMOUNT>
          </ALLLEDGERENTRIES.LIST>
        </VOUCHER>
      </TALLYMESSAGE>
      <TALLYMESSAGE>
        <VOUCHER>
          <DATE>20260402</DATE>
          <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
          <VOUCHERNUMBER>BILL-2001</VOUCHERNUMBER>
          <PARTYLEDGERNAME>Steel Supplier A</PARTYLEDGERNAME>
          <PARTYGSTIN>29XYZDE1234F1Z5</PARTYGSTIN>
          <ALLLEDGERENTRIES.LIST>
            <LEDGERNAME>Raw Materials</LEDGERNAME>
            <AMOUNT>59000</AMOUNT>
          </ALLLEDGERENTRIES.LIST>
          <ALLLEDGERENTRIES.LIST>
            <LEDGERNAME>Steel Supplier A</LEDGERNAME>
            <AMOUNT>-59000</AMOUNT>
          </ALLLEDGERENTRIES.LIST>
        </VOUCHER>
      </TALLYMESSAGE>
    </DATA>
  </BODY>
</ENVELOPE>"""


def _local_tag(tag: str) -> str:
    return tag.split("}", 1)[-1].upper()


def _child_text(node: ET.Element, names: set[str], default: str = "") -> str:
    for child in node.iter():
        if _local_tag(child.tag) in names and child.text:
            return child.text.strip()
    return default


def _parse_tally_amount(value: str) -> float:
    clean = str(value or "").replace(",", "").replace("₹", "").replace("Rs", "").strip()
    try:
        return float(clean)
    except Exception:
        return 0.0


def parse_tally_vouchers(xml_text: str) -> pd.DataFrame:
    root = ET.fromstring(xml_text)
    rows = []
    for voucher in [node for node in root.iter() if _local_tag(node.tag) == "VOUCHER"]:
        vtype = _child_text(voucher, {"VOUCHERTYPENAME"}, "Voucher")
        party = _child_text(voucher, {"PARTYLEDGERNAME", "BASICBUYERNAME", "BASICBASEPARTYNAME"}, "Unknown")
        invoice_no = _child_text(voucher, {"VOUCHERNUMBER", "REFERENCE"}, "-")
        gstin = _child_text(voucher, {"PARTYGSTIN", "GSTIN"}, "")
        raw_date = _child_text(voucher, {"DATE"}, "")
        try:
            date = pd.to_datetime(raw_date, format="%Y%m%d", errors="raise")
        except Exception:
            date = pd.to_datetime(raw_date, errors="coerce")
        ledger_names, amounts = [], []
        for ledger in [node for node in voucher.iter() if _local_tag(node.tag) == "ALLLEDGERENTRIES.LIST"]:
            lname = _child_text(ledger, {"LEDGERNAME"}, "")
            amt = _parse_tally_amount(_child_text(ledger, {"AMOUNT"}, "0"))
            if lname:
                ledger_names.append(lname)
            if amt:
                amounts.append(amt)
        if not amounts:
            continue
        amount = max(abs(a) for a in amounts)
        vt = vtype.lower()
        txn_type = "Sales" if any(x in vt for x in ["sales", "receipt", "credit note"]) else "Expense" if any(x in vt for x in ["purchase", "payment", "debit note", "journal"]) else ("Sales" if sum(amounts) < 0 else "Expense")
        category = vtype if txn_type == "Expense" else "Sales"
        rows.append({"Date": date, "Type": txn_type, "Party": party, "Amount": amount, "Status": "Paid", "Category": category, "Invoice_No": invoice_no, "GSTIN": gstin, "Tally_Voucher_Type": vtype, "Tally_Ledgers": ", ".join(ledger_names[:4])})
    df = pd.DataFrame(rows)
    if len(df):
        df = df.dropna(subset=["Date"])
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


def import_from_tally(tally_url: str, from_date: datetime, to_date: datetime, report_name: str) -> tuple[pd.DataFrame | None, bool, str]:
    try:
        import requests
    except ImportError:
        return None, False, "Install requests first: pip install requests"
    try:
        response = requests.post(tally_url, data=tally_export_xml(from_date, to_date, report_name), headers={"Content-Type": "text/xml"}, timeout=20)
        response.raise_for_status()
        df = parse_tally_vouchers(response.text)
        if df is None or len(df) == 0:
            return None, False, "Tally responded, but no vouchers were parsed. Check that Tally is open, company is loaded, and the report/date range has vouchers."
        return df, True, f"{len(df):,} vouchers imported from Tally {report_name}"
    except Exception as exc:
        return None, False, f"Could not connect/import from Tally: {exc}"


def gst_gsp_request(base_url: str, path: str, api_key: str = "", params: dict | None = None, method: str = "GET", payload: dict | None = None) -> tuple[dict | str | None, bool, str]:
    try:
        import requests
    except ImportError:
        return None, False, "Install requests first: pip install requests"
    try:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        headers = {"Accept": "application/json"}
        if api_key:
            headers["x-api-key"] = api_key
            headers["Authorization"] = f"Bearer {api_key}"
        if method == "POST":
            response = requests.post(url, headers=headers, params=params or {}, json=payload or {}, timeout=25)
        else:
            response = requests.get(url, headers=headers, params=params or {}, timeout=25)
        content_type = response.headers.get("content-type", "")
        data = response.json() if "json" in content_type.lower() else response.text[:5000]
        if response.ok:
            return data, True, f"GST API request succeeded ({response.status_code})"
        return data, False, f"GST API request failed ({response.status_code})"
    except Exception as exc:
        return None, False, f"GST API connection failed: {exc}"


def generate_pdf_report(df: pd.DataFrame, leaks: list[dict], industry: str, firm_name: str) -> bytes | None:
    try:
        from fpdf import FPDF
    except ImportError:
        return None
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    exp_tot = float(expenses["Amount"].sum())
    profit = revenue - exp_tot
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "OpsClarity Business Health Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Prepared by: {firm_name} | {datetime.now():%d %B %Y}", ln=True)
    pdf.cell(0, 6, f"Industry: {industry.title()} | Powered by OpsClarity", ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Executive Summary", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for label, value in [("Revenue", fmt(revenue)), ("Expenses", fmt(exp_tot)), ("Profit", fmt(profit)), ("Margin", f"{pct(profit, revenue):.1f}%"), ("Visible recoverable impact", fmt(sum(l["rupee_impact"] for l in leaks)))]:
        pdf.cell(60, 7, label + ":", ln=False)
        pdf.cell(0, 7, value, ln=True)
    pdf.ln(3)
    brief = ca_client_brief(df, industry, "Client")
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Advisory Brief", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, f"Health: {brief['health_score']} - {brief['status']}")
    pdf.multi_cell(0, 5, f"Main issue: {brief['main_issue']}")
    pdf.multi_cell(0, 5, f"Advisory summary: {brief['why_it_matters']}")
    pdf.multi_cell(0, 5, "This week's actions: " + " | ".join(brief["actions"][:3]))
    pdf.multi_cell(0, 5, "GST follow-up: " + " | ".join(brief["gst_followup"][:3]))
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top Decisions For This Week", ln=True)
    for i, leak in enumerate(leaks[:6], 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, f"{i}. {leak['headline']} [{leak['severity'].upper()}]")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, f"Problem: {leak['problem']}")
        pdf.multi_cell(0, 5, f"Action: {leak['action']}")
        pdf.multi_cell(0, 5, f"Impact: {fmt_exact(leak['rupee_impact'])}")
        pdf.ln(1)
    raw = pdf.output(dest="S")
    return bytes(raw) if isinstance(raw, bytearray) else raw.encode("latin-1")


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--ink:#07090D;--ink2:#0C0F15;--ink3:#12161E;--paper:#EAE6DF;--paper2:#B0ACA5;--gold:#C9A84C;--green:#0EA371;--red:#E05050;--amber:#D4820A;--blue:#4A8FD4;--border:#1A1F28;--muted:#6B7280;--card:#0C1018}
.stApp{background:var(--ink);color:var(--paper);font-family:'DM Sans',sans-serif}.main .block-container{padding:0!important;max-width:100%!important}#MainMenu,footer,header{visibility:hidden}
html,body,[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stToolbar"],.stApp,.main,section.main{background:#07090D!important}
.topbar{position:sticky;top:0;z-index:99;background:var(--ink2);border-bottom:1px solid var(--border);padding:.85rem 3rem;display:flex;justify-content:space-between;align-items:center}.brand{font-family:'DM Serif Display';color:var(--gold);font-size:1.45rem}.pill{border:1px solid rgba(201,168,76,.25);background:rgba(201,168,76,.08);color:var(--gold);border-radius:999px;padding:.25rem .65rem;font-size:.65rem;font-weight:700;text-transform:uppercase}.cta{background:var(--gold);color:#000!important;text-decoration:none;border-radius:7px;padding:.5rem .9rem;font-size:.75rem;font-weight:800}
.hero{padding:4rem 3rem;border-bottom:1px solid var(--border);background:radial-gradient(ellipse 70% 50% at 75% 10%,rgba(201,168,76,.08),transparent 55%),var(--ink)}.hero-grid{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:1fr 420px;gap:4rem;align-items:center}.eyebrow{color:var(--gold);font-size:.7rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase}.h1{font-family:'DM Serif Display';font-size:clamp(2.7rem,5vw,4.6rem);line-height:1.02;margin:.8rem 0}.h1 em{color:var(--gold)}.sub{max-width:620px;color:var(--paper2);line-height:1.8}
.section{padding:2.25rem 3rem}.section-head{font-family:'DM Serif Display';font-size:2rem;margin-bottom:.3rem}.section-sub{color:var(--muted);font-size:.84rem;line-height:1.7;margin-bottom:1.3rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem}.card,.kpi,.leak{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.15rem}.kpi-label{color:var(--muted);font-size:.62rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase}.kpi-val{font-family:'DM Serif Display';font-size:1.9rem;line-height:1.1}.kpi-sub{color:var(--muted);font-size:.72rem}.leak{margin-bottom:.85rem;border-left:4px solid var(--gold)}.critical{border-left-color:var(--red)}.warning{border-left-color:var(--amber)}.info{border-left-color:var(--blue)}.tag{display:inline-block;border-radius:999px;padding:.2rem .55rem;font-size:.58rem;font-weight:800;text-transform:uppercase;background:rgba(201,168,76,.1);color:var(--gold)}.title{font-family:'DM Serif Display';font-size:1.25rem}.muted{color:var(--muted)}.mono{font-family:'JetBrains Mono'}.gold{color:var(--gold)}.good{color:var(--green)}.bad{color:var(--red)}.warn{color:var(--amber)}
.parts{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border-radius:9px;overflow:hidden;margin-top:1rem}.part{background:#0E1219;padding:.9rem}.part-l{color:var(--muted);font-size:.58rem;font-weight:800;text-transform:uppercase}.part-v{color:var(--paper2);font-size:.78rem;line-height:1.6}.money{background:linear-gradient(135deg,var(--card),#0F1208);border:1px solid rgba(201,168,76,.18);border-radius:18px;padding:2rem;margin:1rem 0 1.3rem}.money-total{font-family:'DM Serif Display';color:var(--gold);font-size:4rem;line-height:1}
.stTabs [data-baseweb="tab-list"]{background:var(--ink2);border-bottom:1px solid var(--border);padding:0 3rem;gap:0}.stTabs [data-baseweb="tab"]{color:var(--muted)!important;font-size:.7rem;font-weight:800;text-transform:uppercase;padding:1rem}.stTabs [aria-selected="true"]{color:var(--gold)!important;border-bottom:2px solid var(--gold)!important}.stButton>button{background:var(--gold)!important;color:#000!important;border:none!important;border-radius:8px!important;font-weight:800!important}
.footer{padding:1.75rem 3rem;border-top:1px solid var(--border);background:#040608;color:var(--muted);font-size:.7rem}.wa{position:fixed;right:24px;bottom:24px;background:#25D366;color:white!important;text-decoration:none;padding:.75rem 1rem;border-radius:999px;font-weight:800;z-index:9999}@media(max-width:900px){.hero-grid,.grid4,.grid3,.parts{grid-template-columns:1fr}.section,.hero,.topbar{padding-left:1.25rem;padding-right:1.25rem}}
</style>
""",
    unsafe_allow_html=True,
)

ensure_store()
for k, v in {"df": None, "industry": "manufacturing", "city": "Bangalore", "chat": [], "ca_firm": "OpsClarity Workspace", "client_name": "Primary Client", "role": "OpsClarity Admin" if ADMIN_MODE else "CA"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(f'<div class="topbar"><div class="brand">OpsClarity <span class="muted" style="font-family:DM Sans;font-size:.7rem">AI Finance Control Tower</span></div><div style="display:flex;gap:.8rem;align-items:center"><span class="pill">Live</span><span class="pill">v{APP_VERSION}</span><a class="cta" href="{wa_link("Hi, I need help with OpsClarity")}" target="_blank">Support</a></div></div>', unsafe_allow_html=True)

with st.sidebar:
    if ADMIN_MODE:
        st.markdown("### Workspace")
        st.session_state.role = st.selectbox("Role", ["CA", "SME Owner", "OpsClarity Admin"], index=["CA", "SME Owner", "OpsClarity Admin"].index(st.session_state.role))
        st.session_state.ca_firm = st.text_input("Firm Name", st.session_state.ca_firm)
        st.session_state.client_name = st.text_input("Active Client", st.session_state.client_name)
        st.caption("Internal controls are visible only in admin mode.")
    else:
        st.session_state.role = "CA"

client_name = st.session_state.client_name
tenant_id = sid(st.session_state.ca_firm.lower().strip())
client_id = sid(tenant_id, client_name.lower().strip())

if st.session_state.df is not None:
    score = health_score(st.session_state.df, st.session_state.industry)
    label = "Healthy" if score >= 75 else "Monitor" if score >= 50 else "At Risk"
    card = f'<div class="card"><span class="tag">Business Health</span><div class="money-total">{score}</div><div class="title">{label}</div><div class="muted">Live from uploaded client data</div></div>'
else:
    card = '<div class="card" style="text-align:center"><div class="money-total">OC</div><div class="title">Your score appears here</div><div class="muted">Upload Tally, bank, sales, or purchase data.</div></div>'
st.markdown(f'<div class="hero"><div class="hero-grid"><div><div class="eyebrow">Built in Bangalore for Indian CAs and SMEs</div><div class="h1">Your business has a dashboard.<br>Now get a <em>CFO.</em></div><div class="sub">OpsClarity turns Tally and finance exports into client health reports with money leaks, overdue cash, GST ITC risk, reconciliation gaps, cash runway, and exact weekly actions.</div></div>{card}</div></div>', unsafe_allow_html=True)
render_trust_strip()

tabs = st.tabs(["Client Brief", "Scan", "Decision Dashboard", "Advisory Brief", "Action Inbox", "Alerts", "AI Copilot", "GST", "Reconciliation", "Cash Forecast", "Clients", "Reports & Automations", "Tally Import"])
tabs = st.tabs(["Overview", "Scan", "Decision Dashboard", "Advisory Brief", "Action Inbox", "Alerts", "AI Copilot", "GST", "Reconciliation", "Cash Forecast", "Clients", "Reports & Automations", "Tally Import"])

with tabs[0]:
st.markdown('<div class="section"><div class="section-head">Client Brief</div><div class="section-sub">Health score, top risk, recommended actions, GST follow-up, runway, and report export.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section"><div class="section-head">Overview</div><div class="section-sub">Your operating summary for this client: what matters now, what to do next, and what to review this month.</div>', unsafe_allow_html=True)
if st.session_state.df is None:
        st.info("No client data loaded yet. Start with a Tally export or finance file to generate the first brief.")
        render_getting_started()
""",
            unsafe_allow_html=True,
        )
        st.subheader("Subscriptions")
        render_pricing_block()
        st.info("Upload a client Tally/Excel file in the Scan tab to generate the client brief.")
if st.session_state.role == "OpsClarity Admin" and st.button("Load Example Client Data", use_container_width=True):
st.session_state.df = make_demo_data(client_name)
save_client_snapshot(st.session_state.df, tenant_id, client_id, client_name, st.session_state.industry)
            st.rerun()
    else:
        df, industry = st.session_state.df, st.session_state.industry
brief = ca_client_brief(df, industry, client_name)
leaks = find_leaks(df.to_json(date_format="iso"), industry)
fc = cash_flow_forecast(df)
        alerts = alerts_engine(df, industry)
        ba = before_after_summary(tenant_id, client_id)
top_leak = leaks[0] if leaks else None
st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Health Score</div><div class="kpi-val">{brief["health_score"]}</div><div class="kpi-sub">{brief["status"]}</div></div><div class="kpi"><div class="kpi-label">Top Leak</div><div class="kpi-val">{fmt(top_leak["rupee_impact"] if top_leak else 0)}</div><div class="kpi-sub">{top_leak["category"] if top_leak else "No critical leak"}</div></div><div class="kpi"><div class="kpi-label">Runway</div><div class="kpi-val">{fc["runway"]:.1f}</div><div class="kpi-sub">months</div></div><div class="kpi"><div class="kpi-label">GST Score</div><div class="kpi-val">{brief["gst_score"]}</div><div class="kpi-sub">ITC + vendor risk</div></div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="card" style="margin-top:1rem"><span class="tag">Advisory Summary</span><div class="title">{brief["main_issue"]}</div><div class="part-v" style="margin-top:.6rem">{brief["why_it_matters"]}</div></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="grid3" style="margin-top:1rem">
  <div class="card">
    <span class="tag">This Month</span>
    <div class="title" style="margin-top:.5rem">Priority Operating Rhythm</div>
    <div class="part-v" style="margin-top:.6rem">1. Upload latest books or Tally export</div>
    <div class="part-v">2. Resolve the top 3 actions in Action Inbox</div>
    <div class="part-v">3. Review GST mismatches and overdue invoices</div>
    <div class="part-v">4. Export report and schedule the next review for {next_review_date()}</div>
  </div>
  <div class="card">
    <span class="tag">Recurring Value</span>
    <div class="title" style="margin-top:.5rem">{fmt(sum(float(l["rupee_impact"]) for l in leaks[:3]))}</div>
    <div class="part-v" style="margin-top:.6rem">Visible opportunity across the top 3 decision items for this client right now.</div>
  </div>
  <div class="card">
    <span class="tag">Alert Load</span>
    <div class="title" style="margin-top:.5rem">{len(alerts)}</div>
    <div class="part-v" style="margin-top:.6rem">Open risk signals across collections, costs, cash, and margin performance.</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
c1, c2, c3 = st.columns(3)
with c1:
st.subheader("This Week")
            for i, action in enumerate(brief["actions"][:3], 1):
                st.markdown(f"{i}. {action}")
        with c2:
            st.subheader("GST Follow-up")
            for i, task in enumerate(brief["gst_followup"][:3], 1):
                st.markdown(f"{i}. {task}")
        with c3:
            st.subheader("Next Steps")
st.markdown("1. Review Advisory Brief")
st.markdown("2. Download PDF")
st.markdown("3. Queue follow-up actions")
        if ba["has_history"]:
            st.subheader("What Changed Since Last Review")
            st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Leak Change</div><div class="kpi-val">{fmt(ba["leak_delta"])}</div></div><div class="kpi"><div class="kpi-label">Health Change</div><div class="kpi-val">{ba["score_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">GST Change</div><div class="kpi-val">{ba["gst_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">Runway Change</div><div class="kpi-val">{ba["runway_delta"]:+.1f}</div></div></div>', unsafe_allow_html=True)
pdf = generate_pdf_report(df, leaks, industry, st.session_state.ca_firm)
if pdf:
st.download_button("Download Branded Report", pdf, file_name=f"OpsClarity_Report_{datetime.now():%Y%m%d}.pdf", mime="application/pdf", use_container_width=True)
        st.subheader("Subscriptions")
        render_pricing_block()
if RAZORPAY_PAYMENT_LINK:
st.link_button("Manage Subscription", payment_cta_url("OpsClarity Subscription"), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="section"><div class="section-head">Upload Finance Data</div><div class="section-sub">Upload CSV/Excel exports from Tally, bank statements, sales registers, or purchase ledgers.</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1:
        uploaded = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx", "xls"])
    with c2:
        st.session_state.industry = INDUSTRY_MAP[st.selectbox("Industry", list(INDUSTRY_MAP.keys()))]
    with c3:
        st.session_state.city = st.selectbox("City", ["Bangalore", "Mumbai", "Delhi", "Pune", "Chennai", "Hyderabad", "Ahmedabad", "Surat", "Other"])
    with c4:
        st.write("")
        st.write("")
        if st.session_state.role == "OpsClarity Admin" and st.button("Load Example Data", use_container_width=True):
            st.session_state.df = make_demo_data(client_name)
            save_client_snapshot(st.session_state.df, tenant_id, client_id, client_name, st.session_state.industry)
            st.rerun()
    if uploaded:
        parsed, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = parsed
            save_client_snapshot(parsed, tenant_id, client_id, client_name, st.session_state.industry)
            st.success(msg)
        else:
            st.error(msg)
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(60), use_container_width=True, height=360)
    else:
        st.info("Upload a client CSV/Excel file to begin.")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="section"><div class="section-head">Decision Dashboard</div><div class="section-sub">Top 5 leaks, rupee impact, and what to do this week.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        df, industry = st.session_state.df, st.session_state.industry
        leaks = find_leaks(df.to_json(date_format="iso"), industry)
        sales, expenses = split_books(df)
        revenue, exp_tot = float(sales["Amount"].sum()), float(expenses["Amount"].sum())
        overdue = float(sales[clean_status(sales["Status"]).isin(["overdue", "pending", "not paid", "outstanding", "unpaid"])]["Amount"].sum()) if "Status" in sales.columns else 0
        total_leak = sum(float(l["rupee_impact"]) for l in leaks)
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Revenue</div><div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales)} sales txns</div></div><div class="kpi"><div class="kpi-label">Net Margin</div><div class="kpi-val">{pct(revenue-exp_tot,revenue):.1f}%</div><div class="kpi-sub">Benchmark {INDUSTRY_BENCHMARKS.get(industry,15)}%</div></div><div class="kpi"><div class="kpi-label">Overdue</div><div class="kpi-val">{fmt(overdue)}</div><div class="kpi-sub">{pct(overdue,revenue):.1f}% revenue</div></div><div class="kpi"><div class="kpi-label">Recoverable</div><div class="kpi-val">{fmt(total_leak)}</div><div class="kpi-sub">{len(leaks)} leaks</div></div></div><div class="money"><div class="kpi-label">This week CFO decision</div><div class="money-total">{fmt(total_leak)}</div><div class="muted">Prioritize collections, vendor cost, margin, GST, then reconciliation.</div></div>', unsafe_allow_html=True)
        for leak in leaks[:5]:
            st.markdown(f'<div class="leak {leak["severity"]}"><span class="tag">{leak["category"]}</span><div style="display:flex;justify-content:space-between;gap:1rem"><div><div class="title">{leak["headline"]}</div><div class="muted">{leak["sub"]}</div></div><div class="mono gold" style="font-size:1.3rem">{fmt(leak["rupee_impact"])}</div></div><div class="parts"><div class="part"><div class="part-l">Problem</div><div class="part-v">{leak["problem"]}</div></div><div class="part"><div class="part-l">Reason</div><div class="part-v">{leak["reason"]}</div></div><div class="part"><div class="part-l">Action</div><div class="part-v gold">{leak["action"]}</div></div></div><div class="card" style="margin-top:.8rem;background:#0E1219"><span class="tag">Client Note</span><div class="part-v">{client_language_for_leak(leak)}</div></div><div class="muted" style="margin-top:.6rem">Benchmark: {leak["benchmark"]}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section"><div class="section-head">Advisory Brief</div><div class="section-sub">One-page summary of what happened, why it matters, and what actions come next.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        brief = ca_client_brief(st.session_state.df, st.session_state.industry, client_name)
        ba = before_after_summary(tenant_id, client_id)
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Health</div><div class="kpi-val">{brief["health_score"]}</div><div class="kpi-sub">{brief["status"]}</div></div><div class="kpi"><div class="kpi-label">Margin</div><div class="kpi-val">{brief["margin"]:.1f}%</div></div><div class="kpi"><div class="kpi-label">Runway</div><div class="kpi-val">{brief["runway"]:.1f}</div><div class="kpi-sub">months</div></div><div class="kpi"><div class="kpi-label">GST Score</div><div class="kpi-val">{brief["gst_score"]}</div></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card" style="margin-top:1rem"><span class="tag">Main Client Talking Point</span><div class="title">{brief["main_issue"]}</div><div class="part-v" style="margin-top:.6rem">{brief["why_it_matters"]}</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("This Week's Actions")
            for i, action in enumerate(brief["actions"], 1):
                st.markdown(f"{i}. {action}")
        with c2:
            st.subheader("GST Follow-up Checklist")
            for i, task in enumerate(brief["gst_followup"], 1):
                st.markdown(f"{i}. {task}")
        if ba["has_history"]:
            if any(abs(float(ba[k])) > 0.01 for k in ["leak_delta", "score_delta", "gst_delta", "runway_delta"]):
                st.subheader("Before vs After Tracker")
                st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Leak Reduction</div><div class="kpi-val">{fmt(ba["leak_delta"])}</div></div><div class="kpi"><div class="kpi-label">Health Change</div><div class="kpi-val">{ba["score_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">GST Change</div><div class="kpi-val">{ba["gst_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">Runway Change</div><div class="kpi-val">{ba["runway_delta"]:+.1f}</div></div></div>', unsafe_allow_html=True)
            else:
                st.info("Before/after tracking is ready. It will show meaningful changes after the next scan with updated client data.")
        else:
            st.info("Before/after tracking will appear after this client has at least two scans.")
        st.download_button("Download Client Brief (Text)", data=json.dumps(brief, indent=2, default=str), file_name=f"OpsClarity_Client_Brief_{datetime.now():%Y%m%d}.json", mime="application/json")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[4]:
    st.markdown('<div class="section"><div class="section-head">Action Inbox</div><div class="section-sub">Track whether client actions are open, queued, done, or blocked.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        actions = upsert_actions(find_leaks(st.session_state.df.to_json(date_format="iso"), st.session_state.industry), tenant_id, client_id)
        st.markdown(f'<div class="grid3"><div class="kpi"><div class="kpi-label">Open</div><div class="kpi-val">{sum(a["status"]=="Open" for a in actions)}</div></div><div class="kpi"><div class="kpi-label">Done</div><div class="kpi-val">{sum(a["status"]=="Done" for a in actions)}</div></div><div class="kpi"><div class="kpi-label">Open Impact</div><div class="kpi-val">{fmt(sum(a["impact"] for a in actions if a["status"]=="Open"))}</div></div></div>', unsafe_allow_html=True)
        for action in actions:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.markdown(f"**{action['title']}**")
                c1.caption(f"Owner: {action['owner']} | Due: {action['due_date']} | Channel: {action['channel']}")
                if action.get("template"):
                    c1.text_area("Message template", value=action["template"], height=110, key=f"template_{action['id']}", disabled=True)
                c2.metric("Impact", fmt(action["impact"]))
                new_status = c3.selectbox("Status", ["Open", "Queued", "Done", "Blocked"], index=["Open", "Queued", "Done", "Blocked"].index(action["status"]), key=f"status_{action['id']}")
                if new_status != action["status"]:
                    update_action(action["id"], new_status, tenant_id, client_id)
                    st.rerun()
                if c4.button("Queue", key=f"queue_{action['id']}"):
                    queue_automation(action)
                    update_action(action["id"], "Queued", tenant_id, client_id)
                    st.rerun()
                if action["channel"] == "WhatsApp":
                    c4.link_button("Open WA", wa_link(action.get("template", "")))
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:
    st.markdown('<div class="section"><div class="section-head">Alerts Engine</div><div class="section-sub">Overdue invoices, expense spikes, cash risk, and margin deterioration.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        alerts = alerts_engine(st.session_state.df, st.session_state.industry)
        if not alerts:
            st.success("No critical alerts detected. Keep monitoring monthly.")
        for alert in alerts:
            st.markdown(f'<div class="card" style="margin-bottom:.8rem"><span class="tag">{alert["severity"]}</span><div class="title">{alert["title"]}</div><div class="part-v">{alert["body"]}</div><div class="gold">Action: {alert["action"]}</div><div class="mono">Impact: {fmt(alert["impact"])}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[6]:
    st.markdown('<div class="section"><div class="section-head">AI Copilot</div><div class="section-sub">Ask finance questions about this client: cash flow, overdue invoices, GST, costs, runway, and actions.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        cols = st.columns(4)
        for i, q in enumerate(["What should I fix first?", "Who owes me money?", "What about GST?", "What is my runway?"]):
            if cols[i].button(q, key=f"q_{i}", use_container_width=True):
                leaks = find_leaks(st.session_state.df.to_json(date_format="iso"), st.session_state.industry)
                ans = copilot_answer(q, st.session_state.df, leaks, st.session_state.industry, st.session_state.chat)
                st.session_state.chat += [{"role": "user", "msg": q}, {"role": "assistant", "msg": ans}]
                st.rerun()
        for msg in st.session_state.chat[-10:]:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.markdown(msg["msg"])
        if st.session_state.chat and st.button("Clear conversation"):
            st.session_state.chat = []
            st.rerun()
        user_q = st.chat_input("Ask about your business...")
        if user_q:
            leaks = find_leaks(st.session_state.df.to_json(date_format="iso"), st.session_state.industry)
            ans = copilot_answer(user_q, st.session_state.df, leaks, st.session_state.industry, st.session_state.chat)
            st.session_state.chat += [{"role": "user", "msg": user_q}, {"role": "assistant", "msg": ans}]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[7]:
    st.markdown('<div class="section"><div class="section-head">GST Intelligence Engine</div><div class="section-sub">ITC missed detection, GSTR-2B mismatch proxy, vendor GST compliance risk.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        gst = gst_intelligence(st.session_state.df)
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">GST Score</div><div class="kpi-val">{gst["compliance_score"]}</div></div><div class="kpi"><div class="kpi-label">Claimable ITC</div><div class="kpi-val">{fmt(gst["claimable"])}</div></div><div class="kpi"><div class="kpi-label">Risky ITC</div><div class="kpi-val">{fmt(gst["missed_est"])}</div></div><div class="kpi"><div class="kpi-label">Mismatch Risk</div><div class="kpi-val">{gst["mismatch_count"]}</div><div class="kpi-sub">{fmt(gst["mismatch_value"])}</div></div></div>', unsafe_allow_html=True)
        itc_df = pd.DataFrame(gst["itc_by_cat"]).T.reset_index().rename(columns={"index": "Category"})
        st.subheader("ITC by category")
        st.dataframe(itc_df, use_container_width=True)
        st.subheader("GST Follow-up Checklist")
        for i, task in enumerate(gst_followup_checklist(st.session_state.df), 1):
            st.markdown(f"{i}. {task}")
        st.subheader("Optional GSTR-2B Match Check")
        gstr2b_file = st.file_uploader("Upload GSTR-2B CSV/Excel for purchase-register matching", type=["csv", "xlsx", "xls"], key="gstr2b_upload")
        if gstr2b_file:
            parsed_gstr, ok_gstr, msg_gstr = parse_file(gstr2b_file)
            if ok_gstr:
                purchases = st.session_state.df[st.session_state.df["Type"] == "Expense"].copy()
                matched = gstr2b_match(purchases, parsed_gstr)
                if len(matched):
                    st.caption("Matcher uses GSTIN + rounded amount to flag invoices for CA review.")
                    st.dataframe(matched, use_container_width=True)
                else:
                    st.warning("Could not match this GSTR-2B format. Try an export with GSTIN and invoice amount columns.")
            else:
                st.error(msg_gstr)
        st.subheader("Vendor GST risk")
        st.dataframe(pd.DataFrame(gst["risk_vendors"]), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[8]:
    st.markdown('<div class="section"><div class="section-head">Reconciliation Engine</div><div class="section-sub">Unmatched transactions, duplicate payments, invoice vs payment mapping hints.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        rec = reconciliation_engine(st.session_state.df)
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Risk</div><div class="kpi-val">{rec["risk_score"]}</div></div><div class="kpi"><div class="kpi-label">Duplicate Rows</div><div class="kpi-val">{len(rec["duplicate_rows"])}</div></div><div class="kpi"><div class="kpi-label">Duplicate Payments</div><div class="kpi-val">{len(rec["duplicate_payments"])}</div></div><div class="kpi"><div class="kpi-label">Unmatched</div><div class="kpi-val">{len(rec["unmatched_invoices"])}</div></div></div>', unsafe_allow_html=True)
        with st.expander("Duplicate payments"):
            st.dataframe(rec["duplicate_payments"], use_container_width=True)
        with st.expander("Unmatched invoices"):
            st.dataframe(rec["unmatched_invoices"], use_container_width=True)
        with st.expander("Possible matches"):
            st.dataframe(pd.DataFrame(rec["possible_matches"]), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[9]:
    st.markdown('<div class="section"><div class="section-head">Cash Flow Forecast</div><div class="section-sub">30 / 60 / 90-day scenario forecast and runway.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload data first.")
    else:
        fc = cash_flow_forecast(st.session_state.df)
        st.markdown(f'<div class="grid3"><div class="kpi"><div class="kpi-label">Avg Revenue</div><div class="kpi-val">{fmt(fc["avg_rev"])}</div></div><div class="kpi"><div class="kpi-label">Avg Burn</div><div class="kpi-val">{fmt(fc["avg_exp"])}</div></div><div class="kpi"><div class="kpi-label">Runway</div><div class="kpi-val">{fc["runway"]:.1f}</div><div class="kpi-sub">months</div></div></div>', unsafe_allow_html=True)
        rows = [{"Scenario": k, "30 days": fmt(v["cf_30"]), "60 days": fmt(v["cf_60"]), "90 days": fmt(v["cf_90"]), "Monthly In": fmt(v["monthly_in"]), "Monthly Out": fmt(v["monthly_out"]), "OD Collect": fmt(v["od_collect"])} for k, v in fc["scenarios"].items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[10]:
    st.markdown('<div class="section"><div class="section-head">Client Portfolio</div><div class="section-sub">Risk across clients, priority follow-ups, and recurring advisory workflow.</div>', unsafe_allow_html=True)
    if st.session_state.role == "OpsClarity Admin" and st.button("Load Example Client Portfolio"):
        for name, ind in [("Sharma Textiles", "textile"), ("Mehta Food", "restaurant"), ("Rajesh Diagnostics", "clinic"), ("Kapoor Steel", "manufacturing"), ("Green Pharma", "pharma"), ("SV Printers", "printing")]:
            demo = make_demo_data(name)
            save_client_snapshot(demo, tenant_id, sid(tenant_id, name), name, ind)
        st.rerun()
    clients = read_json(CLIENTS_FILE).get(tenant_id, {})
    if not clients:
        st.info("Upload a client file in the Scan tab to build the client portfolio.")
    else:
        cdf = pd.DataFrame(list(clients.values()))
        risk_info = cdf.apply(client_risk_label, axis=1)
        cdf["risk_status"] = [x[0] for x in risk_info]
        cdf["risk_class"] = [x[1] for x in risk_info]
        cdf["priority"] = cdf["risk_status"].map({"Critical": 1, "Monitor": 2, "Healthy": 3})
        critical_count = int((cdf["risk_status"] == "Critical").sum())
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Clients</div><div class="kpi-val">{len(cdf)}</div></div><div class="kpi"><div class="kpi-label">Total Exposure</div><div class="kpi-val">{fmt(cdf["leak_impact"].sum())}</div></div><div class="kpi"><div class="kpi-label">Critical Risk</div><div class="kpi-val bad">{critical_count}</div><div class="kpi-sub">Needs action first</div></div><div class="kpi"><div class="kpi-label">Average Health</div><div class="kpi-val">{int(cdf["health_score"].mean()) if len(cdf) else 0}</div><div class="kpi-sub">Across portfolio</div></div></div>', unsafe_allow_html=True)
        st.subheader("Client Risk Priority")
        for _, row in cdf.sort_values(["priority", "leak_impact"], ascending=[True, False]).iterrows():
            risk_class = row["risk_class"]
            st.markdown(f'<div class="leak {risk_class}"><span class="tag">{row["risk_status"]}</span><div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start"><div><div class="title">{row["client_name"]}</div><div class="muted">{row["industry"].title()} · Health {row["health_score"]} · GST {row["gst_score"]} · Runway {row["runway"]:.1f} months</div></div><div class="mono gold" style="font-size:1.3rem">{fmt(row["leak_impact"])}</div></div><div class="parts"><div class="part"><div class="part-l">Risk</div><div class="part-v">{row["risk_status"]}</div></div><div class="part"><div class="part-l">Margin</div><div class="part-v">{row["margin"]:.1f}%</div></div><div class="part"><div class="part-l">Action</div><div class="part-v gold">Review the advisory brief and prioritize this client if risk is Critical.</div></div></div></div>', unsafe_allow_html=True)
        if st.session_state.role == "OpsClarity Admin":
            with st.expander("Admin data table"):
                st.dataframe(cdf.drop(columns=["priority"]).sort_values("leak_impact", ascending=False), use_container_width=True)
        st.subheader("Subscription")
        if RAZORPAY_PAYMENT_LINK:
            st.link_button("Manage Subscription", payment_cta_url("OpsClarity Subscription"), use_container_width=True)
        else:
            st.link_button("Request Subscription Access", payment_cta_url("OpsClarity Subscription"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[11]:
    st.markdown('<div class="section"><div class="section-head">Reports & Automations</div><div class="section-sub">Collections reminders, vendor follow-ups, and branded report exports.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("Upload a client file in the Scan tab to generate reports and automation tasks.")
else:
leaks = find_leaks(st.session_state.df.to_json(date_format="iso"), st.session_state.industry)
pdf = generate_pdf_report(st.session_state.df, leaks, st.session_state.industry, st.session_state.ca_firm)
        if pdf:
if pdf:
st.download_button("Download Branded PDF", pdf, file_name=f"OpsClarity_Report_{datetime.now():%Y%m%d}.pdf", mime="application/pdf")
csv = io.StringIO()
st.session_state.df.to_csv(csv, index=False)
st.download_button("Export Cleaned CSV", csv.getvalue(), file_name=f"OpsClarity_Data_{datetime.now():%Y%m%d}.csv", mime="text/csv")
        csv = io.StringIO()
        st.session_state.df.to_csv(csv, index=False)
        st.download_button("Export Cleaned CSV", csv.getvalue(), file_name=f"OpsClarity_Data_{datetime.now():%Y%m%d}.csv", mime="text/csv")
jobs = read_json(AUTOMATIONS_FILE).get(f"{tenant_id}:{client_id}", [])
st.subheader("Automation Queue")
if jobs:
st.dataframe(pd.DataFrame(jobs), use_container_width=True)
else:
st.info("No automation tasks queued yet. Open the Execution tab and click Queue on an action.")
        if jobs:
            st.dataframe(pd.DataFrame(jobs), use_container_width=True)
        else:
            st.info("No automation tasks queued yet. Open the Execution tab and click Queue on an action.")
        st.markdown(
            f"""
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[12]:
    st.markdown('<div class="section"><div class="section-head">Tally Import</div><div class="section-sub">Upload Tally Excel/CSV exports or use connected local import where Tally access is enabled.</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="grid3">
  <div class="card"><span class="tag">Recommended</span><div class="title">Upload Tally Export</div><div class="part-v">Export Day Book, Sales Register, Purchase Register, or Ledger from Tally and upload it in the Scan tab.</div></div>
  <div class="card"><span class="tag">Connected Workflow</span><div class="title">Connected Tally Import</div><div class="part-v">On supported desktop setups, OpsClarity can import voucher XML into the same analysis engine.</div></div>
  <div class="card"><span class="tag">GST</span><div class="title">GSTR-2B Upload Match</div><div class="part-v">Use the GST tab to upload GSTR-2B and compare it against purchase entries.</div></div>
</div>
<div class="card" style="margin-top:1rem">
  <span class="tag">Monthly Delivery</span>
  <div class="part-v" style="margin-top:.6rem">Use this area at month-end to export the client report, hand off the action list, and maintain a recurring advisory cadence for the next review on {next_review_date()}.</div>
  <div class="title">Recommended Tally Export Flow</div>
  <div class="part-v">Tally Prime: Display More Reports -> Account Books -> Day Book -> Export -> Excel/CSV. Then upload the exported file in the Scan tab.</div>
</div>
""",
            unsafe_allow_html=True,
        )
""", unsafe_allow_html=True)
    if st.session_state.role == "OpsClarity Admin":
        st.subheader("Tally Parser Self-Test")
        st.caption("Admin tool: verify OpsClarity can parse Tally-style XML before connecting to a real Tally server.")
        if st.button("Test with sample Tally voucher XML", use_container_width=True):
            sample_df = parse_tally_vouchers(sample_tally_xml())
            if len(sample_df):
                st.success(f"Tally parser is working. Parsed {len(sample_df)} sample vouchers.")
                st.dataframe(sample_df, use_container_width=True)
                if st.button("Load example Tally data into app", use_container_width=True):
                    st.session_state.df = sample_df
                    save_client_snapshot(sample_df, tenant_id, client_id, client_name, st.session_state.industry)
                    st.rerun()
            else:
                st.error("Sample Tally parser test failed.")
    if st.session_state.role == "OpsClarity Admin" and st.toggle("Show developer integration settings", value=False):
        with st.expander("Direct Tally XML import", expanded=False):
            st.caption("Use only when OpsClarity is running on the same PC or local network that can access Tally directly.")
            tc1, tc2, tc3, tc4 = st.columns([2, 1, 1, 1])
            with tc1:
                tally_url = st.text_input("Tally Server URL", value="http://localhost:9000")
            with tc2:
                tally_report = st.selectbox("Report", ["Day Book", "Sales Register", "Purchase Register", "Ledger Vouchers"])
            with tc3:
                tally_from = st.date_input("From", value=datetime.now().date() - timedelta(days=90))
            with tc4:
                tally_to = st.date_input("To", value=datetime.now().date())
            if st.button("Import Directly From Tally", use_container_width=True):
                imported, ok, msg = import_from_tally(tally_url, pd.to_datetime(tally_from).to_pydatetime(), pd.to_datetime(tally_to).to_pydatetime(), tally_report)
                if ok:
                    st.session_state.df = imported
                    save_client_snapshot(imported, tenant_id, client_id, client_name, st.session_state.industry)
                    st.success(msg)
                    st.dataframe(imported.head(50), use_container_width=True)
                else:
                    st.error(msg)
                    st.info("This connection only works when OpsClarity can reach the Tally machine directly over the local network.")
        with st.expander("GST API / GSP connector", expanded=False):
            st.info("Official GST and GSTR-2B sync requires an authorized GSP or ASP provider account and taxpayer authorization.")
            provider = st.selectbox("GST API Provider", ["Custom GSP / ASP", "ClearTax", "Quicko", "Vayana", "FinAGG", "Other"], key="gst_provider")
            g1, g2 = st.columns([2, 1])
            with g1:
                gst_base_url = st.text_input("GSP Base URL", value="", placeholder="https://api.your-gsp.com", key="gst_base_url")
            with g2:
                gst_method = st.selectbox("Method", ["GET", "POST"], key="gst_method")
            gst_api_key = st.text_input("API Key / Bearer Token", value="", type="password", key="gst_api_key")
            gst_path = st.text_input("Endpoint Path", value="", placeholder="/gstin/search or provider-specific GSTR-2B endpoint", key="gst_path")
            gstin = st.text_input("GSTIN / Query Parameter", value="", placeholder="29ABCDE1234F1Z5", key="gstin_lookup")
            extra_params = st.text_input("Extra query params as JSON", value="{}", help='Example: {"action":"TP","ret_period":"032026"}', key="gst_extra_params")
            payload_text = st.text_area("POST payload as JSON", value="{}", height=90, key="gst_payload")
            if st.button("Test GST API Connector", use_container_width=True):
                if not gst_base_url or not gst_path:
                    st.error("Enter a GSP Base URL and endpoint path from your provider documentation.")
                else:
                    try:
                        params = json.loads(extra_params or "{}")
                        if gstin:
                            params.setdefault("gstin", gstin)
                        payload = json.loads(payload_text or "{}")
                    except Exception as exc:
                        st.error(f"Invalid JSON in params/payload: {exc}")
                    else:
                        data, ok, msg = gst_gsp_request(gst_base_url, gst_path, gst_api_key, params=params, method=gst_method, payload=payload)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                        st.code(json.dumps(data, indent=2, default=str) if isinstance(data, (dict, list)) else str(data), language="json")
            st.caption("Security note: do not store production GST tokens in plain JSON. Use Streamlit secrets or a proper encrypted backend when moving beyond pilots.")
    elif st.session_state.role != "OpsClarity Admin":
        pass
st.markdown("</div>", unsafe_allow_html=True)

with tabs[12]:
st.markdown(f'<div class="footer"><strong style="color:var(--gold)">OpsClarity</strong><br>AI Finance Control Tower for Indian CAs and SMEs · v{APP_VERSION}</div><a class="wa" href="{wa_link("Hi, I need help with OpsClarity")}" target="_blank">Support</a>', unsafe_allow_html=True)
