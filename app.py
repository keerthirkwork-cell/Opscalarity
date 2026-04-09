"""
╔══════════════════════════════════════════════════════════════╗
║          OpsClarity - AI CFO for Indian CAs & SMEs           ║
║                    SINGLE FILE VERSION                        ║
║                                                              ║
║  To run:  streamlit run app.py                               ║
║  To install: pip install streamlit pandas numpy openpyxl     ║
╚══════════════════════════════════════════════════════════════╝
"""

# ── IMPORTS ──────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import os
import hashlib
import hmac
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

# ── PAGE CONFIG (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="OpsClarity – AI CFO",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
DATA_DIR = Path(".opsclarity_data")
USERS_FILE  = DATA_DIR / "users.json"
CLIENTS_FILE = DATA_DIR / "clients.json"
SCANS_FILE  = DATA_DIR / "scans.json"
ACTIONS_FILE = DATA_DIR / "actions.json"

INDUSTRY_BENCHMARKS = {
    "Manufacturing": 18, "Restaurant / Cafe": 15, "Clinic / Diagnostic": 25,
    "Retail / Distribution": 12, "Agency / Consulting": 35, "Logistics / Transport": 10,
    "Construction": 20, "Textile / Garments": 14, "Pharma / Medical": 22,
    "Print / Packaging": 16,
}
GST_RATES = {
    "Raw Materials": 18, "Labor": 0, "Rent": 18, "Logistics": 12,
    "Packaging": 18, "Technology": 18, "Electricity": 18,
    "Professional Fees": 18, "Operations": 18, "General": 18,
    "Manufacturing": 18, "Travel": 5, "Bank Charges": 18,
    "Internet": 18, "Salary": 0, "Sales": 18,
}

# ── DATA STORE HELPERS ────────────────────────────────────────────────────────
def ensure_store():
    DATA_DIR.mkdir(exist_ok=True)
    for f in [USERS_FILE, CLIENTS_FILE, SCANS_FILE, ACTIONS_FILE]:
        if not f.exists():
            f.write_text("{}", encoding="utf-8")

def read_json(path):
    ensure_store()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

def write_json(path, data):
    ensure_store()
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def make_id(*parts):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:16]

# ── AUTH HELPERS ──────────────────────────────────────────────────────────────
def get_user(email):
    return read_json(USERS_FILE).get(email)

def create_user(firm_name, name, email, password, city=""):
    users = read_json(USERS_FILE)
    if email in users:
        return False, "Email already registered"
    users[email] = {
        "email": email,
        "name": name,
        "firm_name": firm_name,
        "city": city,
        "password_hash": hash_password(password),
        "plan": "trial",        # trial / starter / growth / partner
        "trial_ends": (datetime.now() + timedelta(days=90)).isoformat(),
        "created_at": datetime.now().isoformat(),
    }
    write_json(USERS_FILE, users)
    return True, "Account created"

def verify_login(email, password):
    user = get_user(email)
    if not user:
        return False, "Email not found"
    if user["password_hash"] != hash_password(password):
        return False, "Wrong password"
    return True, user

def is_trial_active(user):
    try:
        return datetime.fromisoformat(user["trial_ends"]) > datetime.now()
    except:
        return False

def plan_client_limit(user):
    limits = {"trial": 9999, "free": 3, "starter": 10, "growth": 50, "partner": 9999}
    return limits.get(user.get("plan","free"), 3)

# ── CLIENT HELPERS ────────────────────────────────────────────────────────────
def get_clients(email):
    return read_json(CLIENTS_FILE).get(email, {})

def save_client(email, client_id, data):
    store = read_json(CLIENTS_FILE)
    if email not in store:
        store[email] = {}
    store[email][client_id] = data
    write_json(CLIENTS_FILE, store)

def delete_client(email, client_id):
    store = read_json(CLIENTS_FILE)
    if email in store and client_id in store[email]:
        del store[email][client_id]
    write_json(CLIENTS_FILE, store)

def get_scan(email, client_id):
    return read_json(SCANS_FILE).get(f"{email}:{client_id}")

def save_scan(email, client_id, data):
    store = read_json(SCANS_FILE)
    key = f"{email}:{client_id}"
    if key not in store:
        store[key] = []
    store[key].insert(0, data)
    store[key] = store[key][:12]   # keep last 12 scans
    write_json(SCANS_FILE, store)

# ── FORMAT HELPERS ────────────────────────────────────────────────────────────
def fmt(v):
    v = float(v or 0)
    neg = v < 0
    v = abs(v)
    s = "−" if neg else ""
    if v >= 1e7:  return f"{s}₹{v/1e7:.1f}Cr"
    if v >= 1e5:  return f"{s}₹{v/1e5:.1f}L"
    if v >= 1000: return f"{s}₹{v/1000:.0f}K"
    return f"{s}₹{v:.0f}"

def pct(part, whole):
    return float(part or 0) / max(float(whole or 0), 1) * 100

def score_color(score):
    if score >= 75: return "🟢"
    if score >= 50: return "🟡"
    return "🔴"

def risk_label(score):
    if score >= 75: return "Healthy", "green"
    if score >= 50: return "Monitor", "orange"
    return "At Risk", "red"

# ── DATA PARSING ──────────────────────────────────────────────────────────────
def classify_expense(text):
    d = str(text).lower()
    rules = [
        ("Rent", ["rent","lease"]),
        ("Salary", ["salary","wage","payroll"]),
        ("Technology", ["software","laptop","cloud","saas"]),
        ("Internet", ["internet","wifi","broadband"]),
        ("Electricity", ["electricity","power"]),
        ("Professional Fees", ["ca","audit","legal","consult"]),
        ("Travel", ["travel","uber","ola","flight","hotel"]),
        ("Raw Materials", ["raw","material","steel","inventory"]),
        ("Logistics", ["logistics","freight","courier","transport"]),
        ("Packaging", ["pack","box","carton"]),
        ("Bank Charges", ["bank","charge","fee"]),
    ]
    for name, keys in rules:
        if any(k in d for k in keys):
            return name
    return "Operations"

def coerce_amount(s):
    return pd.to_numeric(
        s.astype(str)
        .str.replace(",","",regex=False).str.replace("₹","",regex=False)
        .str.replace("Rs.","",regex=False).str.replace("Rs","",regex=False)
        .str.replace(" Dr","",regex=False).str.replace(" Cr","",regex=False)
        .str.replace("(", "-",regex=False).str.replace(")","",regex=False),
        errors="coerce"
    ).abs().fillna(0)

def infer_type(row):
    raw = " ".join(str(row.get(c,"")) for c in ["Type","Category","Party","Narration"]).lower()
    if any(k in raw for k in ["expense","purchase","payment","debit","salary","rent","raw","logistics"]):
        return "Expense"
    return "Sales"

def parse_file(uploaded_file):
    try:
        name = uploaded_file.name.lower()
        buf = io.BytesIO(uploaded_file.read())
        if name.endswith((".xlsx",".xls")):
            try:    df = pd.read_excel(buf, engine="openpyxl")
            except: buf.seek(0); df = pd.read_excel(buf, engine="xlrd")
        elif name.endswith(".csv"):
            try:    df = pd.read_csv(buf)
            except: buf.seek(0); df = pd.read_csv(buf, encoding="latin1")
        else:
            return None, "Unsupported format. Use .csv, .xlsx, or .xls"

        df = df.dropna(how="all").dropna(axis=1, how="all")
        rename = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if   any(x in cl for x in ["date","dt","day"]):                           rename[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","rs","₹"]): rename[col]="Amount"
            elif any(x in cl for x in ["type","txn","dr/cr","nature"]):               rename[col]="Type"
            elif any(x in cl for x in ["particular","category","head","narration","ledger"]): rename[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client"]): rename[col]="Party"
            elif any(x in cl for x in ["status","paid","pending","overdue","due"]):   rename[col]="Status"
            elif any(x in cl for x in ["bill","invoice","voucher","ref","num","no"]): rename[col]="Invoice_No"
            elif "gst" in cl:                                                          rename[col]="GSTIN"
        df = df.rename(columns=rename)

        if "Date" not in df.columns or "Amount" not in df.columns:
            return None, "Could not find Date and Amount columns. Check your file."

        df["Date"]   = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        df           = df.dropna(subset=["Date"])
        df["Amount"] = coerce_amount(df["Amount"])

        if "Type" not in df.columns:
            df["Type"] = ""
        df["Type"] = df["Type"].astype(str).str.strip().str.title().replace({
            "Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
            "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales","Revenue":"Sales",
        })
        mask = ~df["Type"].isin(["Sales","Expense"])
        df.loc[mask,"Type"] = df.loc[mask].apply(infer_type, axis=1)

        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","-"),("GSTIN","")]:
            if col not in df.columns: df[col] = default

        exp_mask = df["Type"] == "Expense"
        df.loc[exp_mask & df["Category"].astype(str).isin(["","General","nan"]), "Category"] = \
            df.loc[exp_mask & df["Category"].astype(str).isin(["","General","nan"]), "Party"].apply(classify_expense)

        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        df = df[df["Amount"] > 0].copy()
        msg = f"✅ {len(df):,} transactions loaded ({df['Date'].min():%b %Y} → {df['Date'].max():%b %Y})"
        return df, msg
    except Exception as e:
        return None, f"❌ Error reading file: {e}. Try saving as CSV (UTF-8) from Excel."

def make_demo_data(client_name="Demo Client"):
    np.random.seed(abs(hash(client_name)) % (2**32))
    dates = pd.date_range(datetime.now() - timedelta(days=365), datetime.now(), freq="D")
    customers = ["ABC Corp","XYZ Industries","PQR Mfg","LMN Traders","DEF Enterprises"]
    vendors   = ["Steel Supplier A","Steel Supplier B","Raw Material Co","Logistics Ltd","Packaging Inc"]
    rows = []
    for d in dates:
        if np.random.random() > 0.35:
            rows.append({"Date":d,"Type":"Sales","Party":np.random.choice(customers,p=[0.42,0.22,0.16,0.10,0.10]),
                "Amount":round(float(np.random.uniform(55000,240000)),2),
                "Status":np.random.choice(["Paid","Paid","Overdue","Pending"],p=[0.55,0.25,0.12,0.08]),
                "Category":"Sales","Invoice_No":f"INV-{np.random.randint(1000,9999)}","GSTIN":"29ABCDE1234F1Z5"})
        for _ in range(np.random.randint(1,4)):
            rows.append({"Date":d,"Type":"Expense","Party":np.random.choice(vendors),
                "Amount":round(float(np.random.uniform(9000,85000)),2),"Status":"Paid",
                "Category":np.random.choice(["Raw Materials","Labor","Rent","Logistics","Packaging","Technology"],
                    p=[0.38,0.18,0.10,0.14,0.12,0.08]),
                "Invoice_No":f"BILL-{np.random.randint(1000,9999)}",
                "GSTIN":"" if np.random.random()<0.18 else "29ABCDE1234F1Z5"})
    demo = pd.DataFrame(rows)
    demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
    return demo

# ── ANALYSIS ENGINE ───────────────────────────────────────────────────────────
def split_books(df):
    return df[df["Type"].str.title()=="Sales"].copy(), df[df["Type"].str.title()=="Expense"].copy()

def clean_status(s):
    return s.astype(str).str.lower().str.strip()

def find_leaks(df, industry):
    sales, expenses = split_books(df)
    revenue   = float(sales["Amount"].sum())
    exp_total = float(expenses["Amount"].sum())
    profit    = revenue - exp_total
    margin    = pct(profit, revenue)
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    leaks = []

    # 1 — Overdue receivables
    if len(sales) and "Status" in sales.columns:
        od = sales[clean_status(sales["Status"]).isin(["overdue","pending","not paid","due","outstanding","unpaid"])]
        od_amt = float(od["Amount"].sum())
        if od_amt > max(10000, revenue * 0.04):
            debtors = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_name = str(debtors.index[0]) if len(debtors) else "Top Customer"
            top_amt  = float(debtors.iloc[0]) if len(debtors) else od_amt
            leaks.append({
                "id":"cash_stuck","sev":"🔴 Critical","cat":"Collections",
                "impact": od_amt,
                "headline": f"{fmt(od_amt)} stuck in unpaid invoices",
                "sub": f"{len(debtors)} customers overdue ({pct(od_amt,revenue):.1f}% of revenue)",
                "action": f"Call {top_name} today. Offer 2% discount for payment within 48 hrs.",
                "template": f"Hi {top_name}, your invoice of {fmt(top_amt)} is overdue. We can offer 2% off if settled within 48 hours. Can you confirm payment date?",
                "channel": "WhatsApp",
            })

    # 2 — Vendor cost bleed
    for cat in (expenses["Category"].dropna().astype(str).unique() if len(expenses) else []):
        ce = expenses[expenses["Category"].astype(str) == cat]
        v  = ce.groupby("Party")["Amount"].agg(["mean","count","sum"])
        v  = v[v["count"] >= 2]
        if len(v) < 2: continue
        cheapest = float(v["mean"].min())
        top_v    = str(v["mean"].idxmax())
        top_p    = float(v["mean"].max())
        vol      = float(v.loc[top_v, "sum"])
        if cheapest > 0 and top_p > cheapest * 1.14:
            waste = (top_p - cheapest) * (vol / max(top_p, 1))
            if waste > 15000:
                leaks.append({
                    "id":f"vendor_{cat}","sev":"🟡 Warning","cat":"Vendor Costs",
                    "impact": waste,
                    "headline": f"{fmt(waste)}/yr overpaid on {cat}",
                    "sub": f"{top_v} is {((top_p/cheapest)-1)*100:.0f}% above cheapest vendor",
                    "action": f"Get 2 quotes for {cat} and renegotiate with {top_v}.",
                    "template": f"We are reviewing {cat} suppliers for a 12-month contract. Please share your best rate for our current volume.",
                    "channel": "Email",
                })
                break

    # 3 — Margin gap
    if margin < benchmark - 3 and revenue > 0:
        gap = ((benchmark - margin) / 100) * revenue
        if gap > 25000:
            leaks.append({
                "id":"margin_gap","sev":"🔴 Critical" if margin<5 else "🟡 Warning","cat":"Profitability",
                "impact": gap,
                "headline": f"{fmt(gap)} margin gap vs industry peers",
                "sub": f"Your margin {margin:.1f}% vs {benchmark}% benchmark for {industry}",
                "action": "Raise prices 5% on top 3 offerings. Cut largest recurring cost by 10%.",
                "template": "Review top offerings for a 5% price increase and renegotiate the biggest recurring cost.",
                "channel": "Internal",
            })

    # 4 — Revenue concentration
    if revenue > 0 and len(sales):
        conc = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(conc) and pct(float(conc.iloc[0]), revenue) > 28:
            top_c = str(conc.index[0])
            leaks.append({
                "id":"concentration","sev":"🟡 Warning","cat":"Revenue Risk",
                "impact": float(conc.iloc[0]) * 0.3,
                "headline": f"{top_c} is {pct(float(conc.iloc[0]),revenue):.0f}% of revenue",
                "sub": "Single-client dependency — if they delay, cash breaks even when P&L looks fine",
                "action": "Close 2 new clients this month. Set a 25% single-client cap.",
                "template": "Hi, we're expanding capacity this month. If you know a business needing our services, we can offer a referral benefit.",
                "channel": "Email",
            })

    # 5 — Expense spike
    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    if len(me) >= 4:
        recent, prior = float(me.tail(3).mean()), float(me.iloc[:-3].mean())
        if prior > 0 and recent > prior * 1.18:
            leaks.append({
                "id":"exp_spike","sev":"🟡 Warning","cat":"Cost Control",
                "impact": (recent - prior) * 12,
                "headline": f"Monthly costs up {((recent/prior)-1)*100:.0f}% — {fmt(recent-prior)} extra/month",
                "sub": f"Spend moved from {fmt(prior)} to {fmt(recent)} per month",
                "action": "Freeze non-essential spend. Audit all recurring vendors immediately.",
                "template": "Effective today, all non-essential expenses are paused pending review.",
                "channel": "Internal",
            })

    # 6 — GST ITC
    eligible = expenses[(expenses["Amount"]>25000) & (expenses["Category"].map(lambda c: GST_RATES.get(str(c),18)>0))] if len(expenses) else pd.DataFrame()
    missed_itc = float(eligible["Amount"].sum()) * 0.18 * 0.09 if len(eligible) else 0
    if missed_itc > 8000:
        leaks.append({
            "id":"gst_itc","sev":"🔵 Info","cat":"Tax Recovery",
            "impact": missed_itc,
            "headline": f"~{fmt(missed_itc)} GST ITC to verify",
            "sub": f"Eligible purchases >₹25K total {fmt(float(eligible['Amount'].sum()))}",
            "action": "Ask CA to review ITC eligibility and GSTR-2B matching before next GSTR-3B.",
            "template": "Please review ITC eligibility and GSTR-2B matching for all purchase invoices above ₹25K before the next GSTR-3B filing.",
            "channel": "Email",
        })

    return sorted(leaks, key=lambda x: -x["impact"])

def gst_summary(df):
    _, expenses = split_books(df)
    total_itc = 0; claimable = 0; mismatches = 0
    rows = []
    for cat, group in expenses.groupby("Category"):
        rate = GST_RATES.get(str(cat), 18)
        if rate <= 0: continue
        exp_amt  = float(group["Amount"].sum())
        itc_est  = exp_amt * (rate / (100 + rate))
        gstin    = group["GSTIN"].astype(str) if "GSTIN" in group else pd.Series([""]*len(group))
        missing  = int((gstin.str.len() < 10).sum())
        risk_d   = min(0.35, missing / max(len(group),1) * 0.35)
        claim    = max(0, itc_est * (0.9 - risk_d))
        total_itc += itc_est; claimable += claim; mismatches += missing
        rows.append({"Category":str(cat),"Expense":fmt(exp_amt),"GST Rate":f"{rate}%",
                     "Est. ITC":fmt(itc_est),"Claimable":fmt(claim),"Missing GSTINs":missing})
    score = max(5, min(99, int(90 - mismatches * 2 - max(0, total_itc - claimable) / max(total_itc,1) * 40)))
    return {"total_itc":total_itc,"claimable":claimable,"missed":max(0,total_itc-claimable),
            "mismatches":mismatches,"score":score,"rows":rows}

def cash_forecast(df):
    sales, expenses = split_books(df)
    ms = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum() if len(sales) else pd.Series(dtype=float)
    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    avg_r = float(ms.tail(3).mean()) if len(ms)>=3 else float(ms.mean() if len(ms) else 0)
    avg_e = float(me.tail(3).mean()) if len(me)>=3 else float(me.mean() if len(me) else 0)
    trend = float(ms.tail(3).mean()/ms.iloc[-6:-3].mean()) if len(ms)>=6 and float(ms.iloc[-6:-3].mean())>0 else 1.0
    od = float(sales[clean_status(sales["Status"]).isin(["overdue","pending","not paid","outstanding","unpaid"])]["Amount"].sum()) if len(sales) and "Status" in sales.columns else 0
    scenarios = {}
    for label, rm, em, cr in [("Best Case",1.15*trend,0.95,0.75),("Expected",trend,1.0,0.50),("Worst Case",0.82*trend,1.05,0.25)]:
        net = avg_r*rm - avg_e*em
        scenarios[label] = {"Monthly In":fmt(avg_r*rm),"Monthly Out":fmt(avg_e*em),
            "30 Days":fmt(net+od*cr),"60 Days":fmt(net*2+od*cr),"90 Days":fmt(net*3+od*cr)}
    runway = max(0, float(ms.tail(1).sum())-float(me.tail(1).sum())) / max(avg_e,1)
    return {"scenarios":scenarios,"avg_rev":avg_r,"avg_exp":avg_e,"runway":runway,"overdue":od}

def health_score(df, industry):
    sales, expenses = split_books(df)
    revenue = float(sales["Amount"].sum())
    margin  = pct(revenue - float(expenses["Amount"].sum()), revenue)
    bench   = INDUSTRY_BENCHMARKS.get(industry, 15)
    od      = float(sales[clean_status(sales["Status"]).isin(["overdue","pending","not paid","outstanding","unpaid"])]["Amount"].sum()) if len(sales) and "Status" in sales.columns else 0
    me      = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum() if len(expenses) else pd.Series(dtype=float)
    trend   = float(me.tail(2).mean()/me.iloc[:-2].mean()) if len(me)>=4 and float(me.iloc[:-2].mean())>0 else 1.0
    gst     = gst_summary(df)
    score   = (58 + min(22,(margin/max(bench,1))*22) - min(22,pct(od,revenue)*1.8)
               - min(14,max(0,(trend-1.1)*55)) + min(8,max(0,gst["score"]-70)/4))
    return max(5, min(99, int(score)))

def run_full_analysis(df, industry, client_name):
    sales, expenses = split_books(df)
    revenue   = float(sales["Amount"].sum())
    exp_total = float(expenses["Amount"].sum())
    leaks     = find_leaks(df, industry)
    gst       = gst_summary(df)
    fc        = cash_forecast(df)
    score     = health_score(df, industry)
    overdue   = float(sales[clean_status(sales["Status"]).isin(["overdue","pending","not paid","outstanding","unpaid"])]["Amount"].sum()) if "Status" in sales.columns else 0
    rl, _     = risk_label(score)
    return {
        "revenue": revenue, "expenses": exp_total, "profit": revenue-exp_total,
        "margin": pct(revenue-exp_total, revenue), "health_score": score,
        "risk": rl, "overdue": overdue, "leak_impact": sum(l["impact"] for l in leaks),
        "runway": fc["runway"], "gst_score": gst["score"],
        "leaks": leaks, "gst": gst, "forecast": fc,
        "scanned_at": datetime.now().isoformat(),
        "industry": industry, "client_name": client_name,
        "transactions": len(df),
        "date_from": str(df["Date"].min())[:10] if len(df) else "",
        "date_to":   str(df["Date"].max())[:10] if len(df) else "",
    }

# ── STYLES ────────────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink:#07090D; --ink2:#0C0F15; --ink3:#12161E;
    --paper:#EAE6DF; --paper2:#B0ACA5;
    --gold:#C9A84C; --gold-dim:rgba(201,168,76,.12);
    --green:#0EA371; --red:#E05050; --amber:#D4820A; --blue:#4A8FD4;
    --border:#1A1F28; --muted:#6B7280; --card:#0C1018;
}
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], section.main, .main {
    background:#07090D !important; color:#EAE6DF;
    font-family:'DM Sans',sans-serif;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility:hidden; }
.main .block-container { padding:0 !important; max-width:100% !important; }

/* ── Topbar ── */
.oc-topbar {
    position:sticky; top:0; z-index:99;
    background:#0C0F15; border-bottom:1px solid #1A1F28;
    padding:.75rem 2.5rem;
    display:flex; justify-content:space-between; align-items:center;
}
.oc-brand { font-family:'DM Serif Display'; color:#C9A84C; font-size:1.4rem; }
.oc-brand span { font-family:'DM Sans'; color:#6B7280; font-size:.7rem; margin-left:.5rem; }
.oc-pill {
    border:1px solid rgba(201,168,76,.3); background:rgba(201,168,76,.08);
    color:#C9A84C; border-radius:999px; padding:.2rem .6rem;
    font-size:.6rem; font-weight:800; text-transform:uppercase;
}

/* ── Cards ── */
.oc-card {
    background:#0C1018; border:1px solid #1A1F28;
    border-radius:16px; padding:1.25rem;
}
.oc-kpi { @extend .oc-card; }
.kpi-label {
    color:#6B7280; font-size:.6rem; font-weight:800;
    text-transform:uppercase; letter-spacing:.14em;
}
.kpi-val {
    font-family:'DM Serif Display'; font-size:1.9rem; line-height:1.1;
    color:#EAE6DF;
}
.kpi-sub { color:#6B7280; font-size:.7rem; }
.gold { color:#C9A84C !important; }
.green { color:#0EA371 !important; }
.red { color:#E05050 !important; }
.amber { color:#D4820A !important; }
.muted { color:#6B7280 !important; }

/* ── Leak cards ── */
.leak {
    background:#0C1018; border:1px solid #1A1F28;
    border-radius:14px; padding:1.1rem;
    margin-bottom:.75rem;
    border-left:4px solid #C9A84C;
}
.leak-critical { border-left-color:#E05050; }
.leak-warning  { border-left-color:#D4820A; }
.leak-info     { border-left-color:#4A8FD4; }

/* ── Buttons ── */
.stButton > button {
    background:#C9A84C !important; color:#000 !important;
    border:none !important; border-radius:8px !important;
    font-weight:800 !important; font-family:'DM Sans' !important;
}
.stButton > button:hover { background:#e0bc5e !important; }

/* ── Forms ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background:#0C1018 !important; border:1px solid #2A3040 !important;
    color:#EAE6DF !important; border-radius:8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color:#C9A84C !important; box-shadow:none !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#0C0F15; border-bottom:1px solid #1A1F28;
    padding:0 2.5rem; gap:0;
}
.stTabs [data-baseweb="tab"] {
    color:#6B7280 !important; font-size:.7rem; font-weight:800;
    text-transform:uppercase; padding:.9rem 1rem;
    background:transparent !important;
}
.stTabs [aria-selected="true"] {
    color:#C9A84C !important;
    border-bottom:2px solid #C9A84C !important;
}
.stTabs [data-baseweb="tab-panel"] { padding:0; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background:#0C1018 !important;
    border:2px dashed #2A3040 !important;
    border-radius:12px !important;
}

/* ── DataFrame ── */
.stDataFrame { background:#0C1018 !important; border-radius:10px; }
[data-testid="stDataFrame"] { border:1px solid #1A1F28; border-radius:10px; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background:#0C1018; border:1px solid #1A1F28;
    border-radius:12px; padding:.8rem 1rem;
}
[data-testid="stMetricLabel"] { color:#6B7280 !important; font-size:.65rem !important; text-transform:uppercase; }
[data-testid="stMetricValue"] { font-family:'DM Serif Display'; color:#EAE6DF; font-size:1.7rem; }

/* ── Misc ── */
.block-container { padding-left:0 !important; padding-right:0 !important; }
hr { border-color:#1A1F28; }
[data-testid="stSidebar"] { background:#0C0F15; border-right:1px solid #1A1F28; }
.stSuccess { background:rgba(14,163,113,.1); border:1px solid rgba(14,163,113,.3); border-radius:8px; }
.stError   { background:rgba(224,80,80,.1);  border:1px solid rgba(224,80,80,.3);  border-radius:8px; }
.stWarning { background:rgba(212,130,10,.1); border:1px solid rgba(212,130,10,.3); border-radius:8px; }
.stInfo    { background:rgba(74,143,212,.1); border:1px solid rgba(74,143,212,.3); border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# ── UI COMPONENT HELPERS ──────────────────────────────────────────────────────
def topbar(user=None):
    plan_text = ""
    if user:
        plan = user.get("plan","free").upper()
        trial_active = is_trial_active(user)
        plan_text = f'<span class="oc-pill">{"TRIAL" if trial_active else plan}</span>'
        if trial_active:
            days_left = (datetime.fromisoformat(user["trial_ends"]) - datetime.now()).days
            plan_text += f'<span class="oc-pill" style="margin-left:.4rem">{days_left}d left</span>'
    st.markdown(f"""
<div class="oc-topbar">
  <div class="oc-brand">OpsClarity<span>AI CFO for CAs & SMEs</span></div>
  <div style="display:flex;gap:.6rem;align-items:center">
    {plan_text}
    {'<span class="oc-pill" style="color:#0EA371;border-color:rgba(14,163,113,.3)">●&nbsp;Live</span>' if user else ""}
  </div>
</div>""", unsafe_allow_html=True)

def section(title, subtitle=""):
    st.markdown(f"""
<div style="padding:1.5rem 2.5rem .5rem">
  <div style="font-family:'DM Serif Display';font-size:1.75rem;color:#EAE6DF">{title}</div>
  {'<div style="color:#6B7280;font-size:.82rem;margin-top:.2rem">'+subtitle+'</div>' if subtitle else ""}
</div>""", unsafe_allow_html=True)

def kpi_row(items):
    """items = list of (label, value, sub, color)"""
    cols = st.columns(len(items))
    for col, (label, val, sub, color) in zip(cols, items):
        with col:
            color_style = {"gold":"#C9A84C","green":"#0EA371","red":"#E05050","amber":"#D4820A"}.get(color,"#EAE6DF")
            st.markdown(f"""
<div class="oc-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-val" style="color:{color_style}">{val}</div>
  <div class="kpi-sub">{sub}</div>
</div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

def leak_card(leak, idx):
    sev  = leak["sev"]
    cls  = "leak-critical" if "Critical" in sev else "leak-warning" if "Warning" in sev else "leak-info"
    st.markdown(f"""
<div class="leak {cls}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">
    <div>
      <div style="font-size:.62rem;font-weight:800;text-transform:uppercase;color:#6B7280;margin-bottom:.3rem">
        {sev} &nbsp;·&nbsp; {leak['cat']}
      </div>
      <div style="font-family:'DM Serif Display';font-size:1.15rem;color:#EAE6DF">{leak['headline']}</div>
      <div style="color:#6B7280;font-size:.78rem;margin-top:.25rem">{leak['sub']}</div>
    </div>
    <div style="font-family:'JetBrains Mono';color:#C9A84C;font-size:1.25rem;white-space:nowrap;font-weight:700">
      {fmt(leak['impact'])}
    </div>
  </div>
  <div style="margin-top:.8rem;padding:.7rem;background:#070a0f;border-radius:8px;border:1px solid #1A1F28">
    <div style="font-size:.6rem;font-weight:800;text-transform:uppercase;color:#6B7280;margin-bottom:.3rem">
      ✅ Recommended Action
    </div>
    <div style="color:#C9A84C;font-size:.82rem">{leak['action']}</div>
  </div>
</div>""", unsafe_allow_html=True)

def money_box(label, value, color="#C9A84C"):
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0C1018,#0F130A);border:1px solid rgba(201,168,76,.2);
border-radius:18px;padding:1.5rem 2rem;margin:.5rem 0">
  <div style="font-size:.6rem;font-weight:800;text-transform:uppercase;color:#6B7280;margin-bottom:.4rem">{label}</div>
  <div style="font-family:'DM Serif Display';color:{color};font-size:3rem;line-height:1">{value}</div>
</div>""", unsafe_allow_html=True)

# ── AUTH SCREENS ──────────────────────────────────────────────────────────────
def show_login():
    topbar()
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("""
<div style="text-align:center;padding:2rem 0 1.5rem">
  <div style="font-family:'DM Serif Display';font-size:2.5rem;color:#EAE6DF;line-height:1.1">
    Your business has a dashboard.<br>Now get a <span style="color:#C9A84C">CFO.</span>
  </div>
  <div style="color:#6B7280;font-size:.85rem;margin-top:.75rem">
    90-day free trial · No credit card required
  </div>
</div>""", unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            email    = st.text_input("Email address", key="li_email", placeholder="you@yourfirm.com")
            password = st.text_input("Password", type="password", key="li_pw")
            if st.button("Sign In →", use_container_width=True, key="li_btn"):
                if not email or not password:
                    st.error("Please fill in both fields.")
                else:
                    ok, result = verify_login(email.strip().lower(), password)
                    if ok:
                        st.session_state.user  = result
                        st.session_state.page  = "dashboard"
                        st.rerun()
                    else:
                        st.error(result)

        with tab_signup:
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            firm  = st.text_input("CA Firm / Company Name", key="su_firm", placeholder="Sharma & Associates")
            name  = st.text_input("Your Name", key="su_name", placeholder="Rajesh Sharma")
            email2 = st.text_input("Email", key="su_email", placeholder="rajesh@sharmaca.in")
            city  = st.text_input("City", key="su_city", placeholder="Bangalore")
            pw1   = st.text_input("Password (min 8 chars)", type="password", key="su_pw1")
            pw2   = st.text_input("Confirm Password", type="password", key="su_pw2")
            if st.button("Start Free Trial →", use_container_width=True, key="su_btn"):
                if not all([firm, name, email2, pw1, pw2]):
                    st.error("Please fill all fields.")
                elif pw1 != pw2:
                    st.error("Passwords do not match.")
                elif len(pw1) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    ok, msg = create_user(firm.strip(), name.strip(), email2.strip().lower(), pw1, city.strip())
                    if ok:
                        _, user = verify_login(email2.strip().lower(), pw1)
                        st.session_state.user = user
                        st.session_state.page = "onboarding"
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("""
<div style="text-align:center;color:#6B7280;font-size:.7rem;margin-top:1.5rem">
  Built for Indian CAs & SMEs · Data stored securely on your server
</div>""", unsafe_allow_html=True)

# ── ONBOARDING (first login) ──────────────────────────────────────────────────
def show_onboarding():
    user = st.session_state.user
    topbar(user)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
<div style="padding:2rem 0">
  <div style="color:#C9A84C;font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.2em">
    Welcome, {user['name']}
  </div>
  <div style="font-family:'DM Serif Display';font-size:2rem;color:#EAE6DF;margin:.5rem 0">
    Let's add your first client
  </div>
  <div style="color:#6B7280;font-size:.85rem">
    Add a client, upload their Tally/Excel export, and get a full financial health report in 30 seconds.
  </div>
</div>""", unsafe_allow_html=True)

        with st.form("onboarding_form"):
            client_name = st.text_input("Client Business Name *", placeholder="Sharma Textiles Pvt Ltd")
            industry    = st.selectbox("Industry *", list(INDUSTRY_BENCHMARKS.keys()))
            gstin       = st.text_input("GSTIN (optional)", placeholder="29ABCDE1234F1Z5")
            col_a, col_b = st.columns(2)
            with col_a: contact = st.text_input("Contact Person", placeholder="Mr. Vijay Sharma")
            with col_b: phone   = st.text_input("Phone", placeholder="+91 98765 43210")
            submitted = st.form_submit_button("Add Client →", use_container_width=True)

        if submitted:
            if not client_name:
                st.error("Client name is required.")
            else:
                cid = make_id(user["email"], client_name, datetime.now().isoformat())
                client_data = {
                    "id": cid, "name": client_name.strip(), "industry": industry,
                    "gstin": gstin.strip(), "contact_name": contact.strip(),
                    "contact_phone": phone.strip(), "created_at": datetime.now().isoformat(),
                }
                save_client(user["email"], cid, client_data)
                st.session_state.active_client_id = cid
                st.session_state.page = "scan"
                st.rerun()

        st.markdown("<div style='text-align:center;margin-top:1rem'>", unsafe_allow_html=True)
        if st.button("Skip — go to dashboard", use_container_width=False):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ── DASHBOARD (multi-client view) ─────────────────────────────────────────────
def show_dashboard():
    user    = st.session_state.user
    clients = get_clients(user["email"])
    topbar(user)
    section("Client Portfolio", f"{user['firm_name']} · {len(clients)} clients")

    # ── Topbar actions
    c1, c2, c3 = st.columns([3,1,1])
    with c1: st.markdown("<div style='padding:1rem 2.5rem 0'></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='padding:.5rem 0'></div>", unsafe_allow_html=True)
        if st.button("＋ Add Client", use_container_width=True):
            st.session_state.page = "add_client"
            st.rerun()
    with c3:
        st.markdown("<div style='padding:.5rem 0'></div>", unsafe_allow_html=True)
        if st.button("⚙ Settings", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()

    st.markdown("<div style='padding:0 2.5rem'>", unsafe_allow_html=True)

    if not clients:
        st.markdown("""
<div style="text-align:center;padding:4rem 2rem;background:#0C1018;border:2px dashed #2A3040;border-radius:16px;margin:2rem 2.5rem">
  <div style="font-size:2.5rem">📂</div>
  <div style="font-family:'DM Serif Display';font-size:1.5rem;margin:.5rem 0">No clients yet</div>
  <div style="color:#6B7280;font-size:.85rem">Add your first client and upload their Tally export to get started</div>
</div>""", unsafe_allow_html=True)
        return

    # ── Portfolio summary KPIs
    all_scans = [get_scan(user["email"], cid) for cid in clients]
    all_scans = [s[0] for s in all_scans if s]  # latest scan per client
    total_leaks = sum(s.get("leak_impact",0) for s in all_scans)
    critical    = sum(1 for s in all_scans if s.get("health_score",50) < 50)
    healthy     = sum(1 for s in all_scans if s.get("health_score",50) >= 75)

    kpi_row([
        ("Total Clients",      str(len(clients)),      f"{healthy} healthy · {critical} critical", "gold"),
        ("Total Leaks Found",  fmt(total_leaks),        "across all clients",                       "red" if total_leaks > 0 else "green"),
        ("Critical Risk",      str(critical),           "need immediate attention",                 "red" if critical > 0 else "green"),
        ("Plan",               user.get("plan","trial").upper(), "90-day trial active" if is_trial_active(user) else "Active", "gold"),
    ])

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    # ── Client cards
    for cid, client in clients.items():
        scan_list = get_scan(user["email"], cid)
        scan      = scan_list[0] if scan_list else None
        score     = scan["health_score"] if scan else None
        rl, rc    = risk_label(score) if score else ("No data", "muted")
        colors    = {"green":"#0EA371","orange":"#D4820A","red":"#E05050","muted":"#6B7280"}
        rcolor    = colors.get(rc,"#6B7280")
        border    = {"green":"rgba(14,163,113,.3)","orange":"rgba(212,130,10,.3)","red":"rgba(224,80,80,.3)","muted":"#2A3040"}.get(rc,"#2A3040")

        col_info, col_kpis, col_btn = st.columns([3,4,1])

        with col_info:
            st.markdown(f"""
<div style="padding:.8rem;background:#0C1018;border:1px solid {border};border-radius:12px;border-left:4px solid {rcolor}">
  <div style="font-family:'DM Serif Display';font-size:1.1rem;color:#EAE6DF">{client['name']}</div>
  <div style="color:#6B7280;font-size:.75rem;margin-top:.2rem">{client['industry']} · {client.get('contact_name','')}</div>
  <div style="color:{rcolor};font-size:.65rem;font-weight:800;text-transform:uppercase;margin-top:.4rem">
    {score_color(score) if score else "⬜"} {rl} {"· Score "+str(score) if score else "· No scan yet"}
  </div>
</div>""", unsafe_allow_html=True)

        with col_kpis:
            if scan:
                st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;padding:.3rem 0">
  <div style="background:#070a0f;border-radius:8px;padding:.5rem;text-align:center">
    <div style="font-size:.55rem;color:#6B7280;text-transform:uppercase">Revenue</div>
    <div style="font-family:'DM Serif Display';color:#EAE6DF;font-size:.9rem">{fmt(scan['revenue'])}</div>
  </div>
  <div style="background:#070a0f;border-radius:8px;padding:.5rem;text-align:center">
    <div style="font-size:.55rem;color:#6B7280;text-transform:uppercase">Margin</div>
    <div style="font-family:'DM Serif Display';color:#EAE6DF;font-size:.9rem">{scan['margin']:.1f}%</div>
  </div>
  <div style="background:#070a0f;border-radius:8px;padding:.5rem;text-align:center">
    <div style="font-size:.55rem;color:#6B7280;text-transform:uppercase">Leaks</div>
    <div style="font-family:'DM Serif Display';color:#E05050;font-size:.9rem">{fmt(scan['leak_impact'])}</div>
  </div>
  <div style="background:#070a0f;border-radius:8px;padding:.5rem;text-align:center">
    <div style="font-size:.55rem;color:#6B7280;text-transform:uppercase">Runway</div>
    <div style="font-family:'DM Serif Display';color:#EAE6DF;font-size:.9rem">{scan['runway']:.1f}m</div>
  </div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#6B7280;font-size:.8rem;padding:.9rem">Upload data to see analysis →</div>', unsafe_allow_html=True)

        with col_btn:
            st.markdown("<div style='padding:.2rem 0'></div>", unsafe_allow_html=True)
            if st.button("Open →", key=f"open_{cid}", use_container_width=True):
                st.session_state.active_client_id = cid
                st.session_state.page = "client"
                st.rerun()

        st.markdown("<div style='height:.1rem'></div>", unsafe_allow_html=True)

    # ── Upgrade CTA (if on free/trial with no payment)
    st.markdown("""
<div style="margin:1.5rem 0;background:linear-gradient(135deg,#0C1018,#100e07);border:1px solid rgba(201,168,76,.2);border-radius:16px;padding:1.5rem 2rem">
  <div style="font-family:'DM Serif Display';font-size:1.3rem;color:#EAE6DF">
    Upgrade to CA Partner Plan
  </div>
  <div style="color:#6B7280;font-size:.8rem;margin:.4rem 0 1rem">
    ₹1,999/month · Unlimited scans · CA-branded PDF reports · Priority support
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem">
    <div style="background:#0C1018;border:1px solid #1A1F28;border-radius:10px;padding:.8rem">
      <div style="color:#C9A84C;font-size:.75rem;font-weight:800">Starter — ₹1,999/mo</div>
      <div style="color:#6B7280;font-size:.7rem;margin-top:.3rem">Up to 10 clients · All features</div>
    </div>
    <div style="background:#0C1018;border:1px solid rgba(201,168,76,.3);border-radius:10px;padding:.8rem">
      <div style="color:#C9A84C;font-size:.75rem;font-weight:800">Growth — ₹4,999/mo ⭐ Popular</div>
      <div style="color:#6B7280;font-size:.7rem;margin-top:.3rem">Up to 50 clients · Tally agent</div>
    </div>
    <div style="background:#0C1018;border:1px solid #1A1F28;border-radius:10px;padding:.8rem">
      <div style="color:#C9A84C;font-size:.75rem;font-weight:800">Partner — ₹9,999/mo</div>
      <div style="color:#6B7280;font-size:.7rem;margin-top:.3rem">Unlimited · White-label PDF</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── ADD CLIENT SCREEN ─────────────────────────────────────────────────────────
def show_add_client():
    user = st.session_state.user
    topbar(user)
    section("Add New Client")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        clients = get_clients(user["email"])
        limit   = plan_client_limit(user)
        if len(clients) >= limit and not is_trial_active(user):
            st.warning(f"You've reached your plan limit of {limit} clients. Upgrade to add more.")
            if st.button("← Back to Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
            return

        with st.form("add_client_form"):
            st.markdown("<div style='padding:.5rem 0'>", unsafe_allow_html=True)
            client_name = st.text_input("Business Name *", placeholder="Mehta Foods Pvt Ltd")
            industry    = st.selectbox("Industry *", list(INDUSTRY_BENCHMARKS.keys()))
            col_a, col_b = st.columns(2)
            with col_a: gstin    = st.text_input("GSTIN", placeholder="29ABCDE1234F1Z5")
            with col_b: city     = st.text_input("City", placeholder="Mumbai")
            col_c, col_d = st.columns(2)
            with col_c: contact  = st.text_input("Contact Person", placeholder="Mr. Mehta")
            with col_d: phone    = st.text_input("Phone", placeholder="+91 9876543210")
            email_c = st.text_input("Client Email (for reports)", placeholder="mehta@mfoods.in")
            submitted = st.form_submit_button("Add Client →", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not client_name:
                st.error("Business name is required.")
            else:
                cid = make_id(user["email"], client_name, datetime.now().isoformat())
                save_client(user["email"], cid, {
                    "id": cid, "name": client_name.strip(), "industry": industry,
                    "gstin": gstin.strip(), "city": city.strip(),
                    "contact_name": contact.strip(), "contact_phone": phone.strip(),
                    "contact_email": email_c.strip(), "created_at": datetime.now().isoformat(),
                })
                st.success(f"Client '{client_name}' added!")
                st.session_state.active_client_id = cid
                st.session_state.page = "scan"
                st.rerun()

        if st.button("← Back to Dashboard", key="back_add"):
            st.session_state.page = "dashboard"
            st.rerun()

# ── SCAN (upload data) ────────────────────────────────────────────────────────
def show_scan():
    user    = st.session_state.user
    cid     = st.session_state.get("active_client_id")
    clients = get_clients(user["email"])
    client  = clients.get(cid)
    if not client:
        st.session_state.page = "dashboard"; st.rerun()

    topbar(user)
    section(f"Upload Data — {client['name']}", f"Industry: {client['industry']}")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
<div style="background:#0C1018;border:1px solid #1A1F28;border-radius:12px;padding:1.25rem;margin-bottom:1rem">
  <div style="font-weight:700;color:#EAE6DF;margin-bottom:.5rem">📂 What files can I upload?</div>
  <div style="color:#6B7280;font-size:.8rem;line-height:1.8">
    ✅ <b>Tally Export:</b> Display → Account Books → Day Book → Export as Excel/CSV<br>
    ✅ <b>Bank Statement:</b> Download from your bank in Excel/CSV format<br>
    ✅ <b>Sales Register:</b> Any Excel/CSV with Date, Amount, Party columns<br>
    ✅ <b>Purchase Ledger:</b> Same format — Date, Amount, Category
  </div>
</div>""", unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop your file here (CSV, Excel .xlsx, .xls)",
            type=["csv","xlsx","xls"], label_visibility="collapsed"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 Load Demo Data (see how it works)", use_container_width=True):
                with st.spinner("Loading demo data..."):
                    df   = make_demo_data(client["name"])
                    result = run_full_analysis(df, client["industry"], client["name"])
                    save_scan(user["email"], cid, result)
                    st.session_state.page = "client"
                    st.rerun()
        with col_b:
            if st.button("← Back to Dashboard", use_container_width=True, key="back_scan"):
                st.session_state.page = "dashboard"; st.rerun()

        if uploaded:
            with st.spinner("Analysing your data..."):
                df, msg = parse_file(uploaded)
                if df is None:
                    st.error(msg)
                else:
                    st.success(msg)
                    result = run_full_analysis(df, client["industry"], client["name"])
                    save_scan(user["email"], cid, result)
                    st.markdown(f"""
<div style="background:rgba(14,163,113,.1);border:1px solid rgba(14,163,113,.3);border-radius:10px;padding:1rem;margin-top:1rem">
  <div style="color:#0EA371;font-weight:800">Analysis Complete!</div>
  <div style="color:#B0ACA5;font-size:.8rem;margin-top:.3rem">
    Health Score: <b>{result['health_score']}/100</b> ·
    Leaks Found: <b>{fmt(result['leak_impact'])}</b> ·
    Transactions: <b>{result['transactions']:,}</b>
  </div>
</div>""", unsafe_allow_html=True)
                    time.sleep(1)
                    st.session_state.page = "client"
                    st.rerun()

# ── CLIENT DETAIL VIEW ────────────────────────────────────────────────────────
def show_client():
    user    = st.session_state.user
    cid     = st.session_state.get("active_client_id")
    clients = get_clients(user["email"])
    client  = clients.get(cid)
    if not client:
        st.session_state.page = "dashboard"; st.rerun()

    scan_list = get_scan(user["email"], cid)
    scan      = scan_list[0] if scan_list else None

    topbar(user)

    # ── Sub-nav
    st.markdown(f"""
<div style="background:#0C0F15;border-bottom:1px solid #1A1F28;padding:.5rem 2.5rem;
display:flex;align-items:center;gap:1rem">
  <div style="font-family:'DM Serif Display';color:#EAE6DF;font-size:1.1rem">{client['name']}</div>
  <div style="color:#6B7280;font-size:.72rem">{client['industry']}</div>
  {'<div style="margin-left:auto;font-size:.65rem;color:'+("rgb(14,163,113)" if (scan or {}).get("health_score",0)>=75 else "rgb(212,130,10)" if (scan or {}).get("health_score",0)>=50 else "rgb(224,80,80)")+';font-weight:800">'+score_color((scan or {}).get("health_score",50))+' Health '+str((scan or {}).get("health_score","—"))+'</div>' if scan else ""}
</div>""", unsafe_allow_html=True)

    # ── Action buttons
    st.markdown("<div style='padding:.75rem 2.5rem 0'>", unsafe_allow_html=True)
    b1,b2,b3,b4 = st.columns([1,1,1,3])
    with b1:
        if st.button("⬆ Upload New Data", use_container_width=True):
            st.session_state.page = "scan"; st.rerun()
    with b2:
        if st.button("← Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()
    with b3:
        if scan and st.button("🗑 Delete Client", use_container_width=True):
            delete_client(user["email"], cid)
            st.session_state.page = "dashboard"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if not scan:
        st.markdown("""
<div style="text-align:center;padding:4rem;background:#0C1018;border:2px dashed #2A3040;
border-radius:16px;margin:1rem 2.5rem">
  <div style="font-size:2rem">📂</div>
  <div style="font-family:'DM Serif Display';font-size:1.4rem;margin:.5rem 0">No data uploaded yet</div>
  <div style="color:#6B7280;font-size:.85rem">Upload a Tally/Excel export to see the analysis</div>
</div>""", unsafe_allow_html=True)
        return

    leaks = scan.get("leaks", [])
    gst   = scan.get("gst",   {})
    fc    = scan.get("forecast", {})

    # ── Main tabs
    tabs = st.tabs(["📊 Overview", "💸 Leaks & Actions", "🧾 GST Health", "📈 Cash Forecast", "📋 Brief & Report"])

    # ══ TAB 1: OVERVIEW ══════════════════════════════════════════════════════
    with tabs[0]:
        st.markdown("<div style='padding:1rem 2.5rem'>", unsafe_allow_html=True)
        score = scan["health_score"]
        rl, rc = risk_label(score)
        colors = {"green":"#0EA371","orange":"#D4820A","red":"#E05050"}
        sc = colors.get(rc, "#EAE6DF")

        money_box("Total Recoverable Opportunity Identified", fmt(scan["leak_impact"]))

        kpi_row([
            ("Health Score",   f"{score}/100",          rl,                                   rc),
            ("Revenue",        fmt(scan["revenue"]),    f"{scan['transactions']:,} transactions","gold"),
            ("Net Margin",     f"{scan['margin']:.1f}%",f"Benchmark {INDUSTRY_BENCHMARKS.get(client['industry'],15)}%","green" if scan["margin"]>INDUSTRY_BENCHMARKS.get(client["industry"],15) else "amber"),
            ("Overdue Cash",   fmt(scan["overdue"]),    f"{pct(scan['overdue'],scan['revenue']):.1f}% of revenue","red" if scan["overdue"]>0 else "green"),
        ])
        kpi_row([
            ("Expenses",       fmt(scan["expenses"]),   "total outflow",                      "amber"),
            ("Net Profit",     fmt(scan["profit"]),     f"{scan['margin']:.1f}% margin",      "green" if scan["profit"]>0 else "red"),
            ("Cash Runway",    f"{scan['runway']:.1f}m","months at current burn",             "green" if scan["runway"]>3 else "red"),
            ("GST Score",      f"{scan['gst_score']}/100","ITC + vendor compliance",          "green" if scan["gst_score"]>=75 else "amber"),
        ])

        st.markdown("---")
        st.markdown(f"<div style='color:#6B7280;font-size:.72rem;text-align:center'>Data: {scan.get('date_from','')} → {scan.get('date_to','')} · Scanned: {scan.get('scanned_at','')[:16]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ══ TAB 2: LEAKS ══════════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown("<div style='padding:1rem 2.5rem'>", unsafe_allow_html=True)
        if not leaks:
            st.success("No major leaks detected. Business looks financially healthy.")
        else:
            st.markdown(f"""
<div style="margin-bottom:1rem">
  <span style="font-size:.65rem;color:#6B7280;text-transform:uppercase;font-weight:800">
    {len(leaks)} issues found · Total impact:
  </span>
  <span style="font-family:'DM Serif Display';color:#E05050;font-size:1.4rem;margin-left:.5rem">
    {fmt(scan['leak_impact'])}
  </span>
</div>""", unsafe_allow_html=True)
            for i, leak in enumerate(leaks):
                leak_card(leak, i)
                # Message template button
                if leak.get("template"):
                    with st.expander(f"📱 {leak['channel']} Message Template", expanded=False):
                        st.text_area("Copy and send this message:", value=leak["template"],
                                     height=100, key=f"tmpl_{i}", disabled=False)
                        if leak["channel"] == "WhatsApp":
                            import urllib.parse
                            wa_url = f"https://wa.me/?text={urllib.parse.quote(leak['template'])}"
                            st.markdown(f'<a href="{wa_url}" target="_blank" style="color:#25D366;font-size:.8rem;font-weight:800">📱 Open in WhatsApp →</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ══ TAB 3: GST ════════════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown("<div style='padding:1rem 2.5rem'>", unsafe_allow_html=True)
        kpi_row([
            ("GST Score",     f"{gst.get('score',0)}/100",  "Overall compliance",        "green" if gst.get("score",0)>=75 else "amber"),
            ("Claimable ITC", fmt(gst.get("claimable",0)),  "Est. input credit",          "gold"),
            ("Risky ITC",     fmt(gst.get("missed",0)),     "May be lost if not claimed", "red" if gst.get("missed",0)>0 else "green"),
            ("GSTIN Missing", str(gst.get("mismatches",0)), "invoices with missing GSTIN","amber" if gst.get("mismatches",0)>0 else "green"),
        ])

        if gst.get("rows"):
            st.markdown("<div style='margin-top:1rem'><b>ITC by Category</b></div>", unsafe_allow_html=True)
            df_gst = pd.DataFrame(gst["rows"])
            st.dataframe(df_gst, use_container_width=True, hide_index=True)

        st.markdown("""
<div style="background:#0C1018;border:1px solid #1A1F28;border-radius:12px;padding:1rem;margin-top:1rem">
  <div style="font-weight:700;color:#EAE6DF;margin-bottom:.5rem">📋 GST Follow-up Checklist</div>
  <div style="color:#B0ACA5;font-size:.8rem;line-height:2">
    ☐ Reconcile GSTR-2B with purchase register before GSTR-3B filing<br>
    ☐ Collect missing GSTINs from vendors with large invoices<br>
    ☐ Verify ITC eligibility for top-3 expense categories<br>
    ☐ Check for duplicate invoice references in purchase entries<br>
    ☐ Confirm GST rate classification for inter-state supplies
  </div>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ══ TAB 4: FORECAST ═══════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown("<div style='padding:1rem 2.5rem'>", unsafe_allow_html=True)
        kpi_row([
            ("Avg Monthly Revenue", fmt(fc.get("avg_rev",0)), "Last 3 months", "gold"),
            ("Avg Monthly Burn",    fmt(fc.get("avg_exp",0)), "Last 3 months", "amber"),
            ("Cash Runway",         f"{fc.get('runway',0):.1f}m", "months at current burn", "green" if fc.get("runway",0)>3 else "red"),
            ("Overdue",             fmt(fc.get("overdue",0)), "pending collections", "red" if fc.get("overdue",0)>0 else "green"),
        ])

        if fc.get("scenarios"):
            df_fc = pd.DataFrame(fc["scenarios"]).T.reset_index()
            df_fc.columns = ["Scenario"] + list(df_fc.columns[1:])
            st.markdown("<div style='margin-top:1rem'><b>30 / 60 / 90 Day Cash Flow Scenarios</b></div>", unsafe_allow_html=True)
            st.dataframe(df_fc, use_container_width=True, hide_index=True)

        st.markdown("""
<div style="background:#0C1018;border:1px solid rgba(212,130,10,.2);border-radius:12px;padding:1rem;margin-top:1rem">
  <div style="color:#D4820A;font-size:.65rem;font-weight:800;text-transform:uppercase;margin-bottom:.4rem">⚠ Cash Flow Warning Signs</div>
  <div style="color:#B0ACA5;font-size:.8rem;line-height:1.8">
    If <b>Worst Case</b> is negative, you need to collect overdue invoices immediately.<br>
    If runway is below <b>2 months</b>, consider a working capital loan from Lendingkart or FlexiLoans.<br>
    If trend is below 1.0, revenue is declining — review pricing and client concentration.
  </div>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ══ TAB 5: BRIEF & REPORT ═════════════════════════════════════════════════
    with tabs[4]:
        st.markdown("<div style='padding:1rem 2.5rem'>", unsafe_allow_html=True)
        score = scan["health_score"]
        rl, _ = risk_label(score)

        # Client brief
        top_leak = leaks[0] if leaks else None
        st.markdown(f"""
<div class="oc-card" style="margin-bottom:1rem">
  <div style="font-size:.6rem;font-weight:800;text-transform:uppercase;color:#6B7280;margin-bottom:.5rem">
    CA Advisory Brief — {client['name']}
  </div>
  <div style="font-family:'DM Serif Display';font-size:1.35rem;color:#EAE6DF">
    {top_leak['headline'] if top_leak else 'No critical issues detected'}
  </div>
  <div style="color:#B0ACA5;font-size:.82rem;margin-top:.5rem;line-height:1.7">
    {_client_talking_point(top_leak)}
  </div>
</div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**This Week's Actions**")
            for i, leak in enumerate(leaks[:3], 1):
                st.markdown(f"{i}. {leak['action'][:80]}...")
        with c2:
            st.markdown("**GST Follow-up**")
            st.markdown("1. Reconcile GSTR-2B with purchase register")
            st.markdown("2. Collect missing GSTINs from vendors")
            st.markdown(f"3. Verify ITC for top categories ({fmt(gst.get('claimable',0))} claimable)")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        # PDF download
        pdf_bytes = _generate_pdf(scan, client, user)
        if pdf_bytes:
            st.download_button(
                "⬇ Download CA-Branded PDF Report",
                data=pdf_bytes,
                file_name=f"OpsClarity_{client['name'].replace(' ','_')}_{datetime.now():%Y%m%d}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("Install fpdf2 to enable PDF export: `pip install fpdf2`")

        # JSON export
        st.download_button(
            "⬇ Export Raw Analysis (JSON)",
            data=json.dumps(scan, indent=2, default=str),
            file_name=f"OpsClarity_Analysis_{datetime.now():%Y%m%d}.json",
            mime="application/json",
        )
        st.markdown("</div>", unsafe_allow_html=True)

def _client_talking_point(leak):
    if not leak: return "The client looks stable this month. Confirm collections, GST, and cash flow remain under control."
    cat = leak.get("cat","")
    m = {
        "Collections": "Your cash problem is not only sales. This money is already earned but not collected. If we collect the top overdue invoices this week, cash improves without taking a loan.",
        "Vendor Costs": "You may be paying more than needed for the same category of spend. We should use your current volume to negotiate better rates or get alternate supplier quotes.",
        "Profitability": "Revenue is coming in, but not enough is staying as profit. We should fix pricing and your largest cost category before growth hides the margin issue.",
        "Tax Recovery": "There may be GST input credit that needs verification. Worth reviewing before the next filing cycle.",
        "Revenue Risk": "One customer is carrying too much revenue. If they delay, cash flow can break even when P&L looks healthy.",
        "Cost Control": "Monthly expenses are rising faster than revenue. We need to audit recurring costs immediately.",
    }
    return m.get(cat, "This issue can affect cash flow or profit. The safest next step is to act on the recommended task this week.")

def _fmt_pdf(v):
    """PDF-safe format (no rupee symbol, use 'Rs' for latin-1 compatibility)"""
    v = float(v or 0)
    neg = v < 0; v = abs(v); s = "-" if neg else ""
    if v >= 1e7:  return f"{s}Rs {v/1e7:.1f}Cr"
    if v >= 1e5:  return f"{s}Rs {v/1e5:.1f}L"
    if v >= 1000: return f"{s}Rs {v/1000:.0f}K"
    return f"{s}Rs {v:.0f}"

def _ps(text):
    """PDF-safe: strip non-latin-1 characters (emojis, rupee sign, etc.)"""
    return str(text).encode("latin-1", errors="replace").decode("latin-1")

def _generate_pdf(scan, client, user):
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
        W   = 190   # usable page width
        leaks = scan.get("leaks", [])
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # ── Title ──
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(W, 12, "OpsClarity - Business Health Report",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(W, 6, _ps(f"CA Firm: {user['firm_name']}  |  Client: {client['name']}  |  {datetime.now():%d %B %Y}"),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

        # ── Summary table ──
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(W, 8, "Executive Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 10)
        for label, val in [
            ("Revenue",           _fmt_pdf(scan["revenue"])),
            ("Expenses",          _fmt_pdf(scan["expenses"])),
            ("Net Profit",        _fmt_pdf(scan["profit"])),
            ("Margin",            f"{scan['margin']:.1f}%"),
            ("Health Score",      f"{scan['health_score']}/100"),
            ("GST Score",         f"{scan.get('gst_score', 0)}/100"),
            ("Total Recoverable", _fmt_pdf(scan["leak_impact"])),
            ("Cash Runway",       f"{scan['runway']:.1f} months"),
        ]:
            pdf.cell(65, 6, _ps(f"{label}:"))
            pdf.cell(W - 65, 6, _ps(val), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

        # ── Leaks ──
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(W, 8, "Top Financial Decisions This Week",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        for i, leak in enumerate(leaks[:6], 1):
            sev = leak.get("sev","").replace("🔴","[CRITICAL]").replace("🟡","[WARNING]").replace("🔵","[INFO]")
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(W, 6, _ps(f"{i}. {leak.get('headline','')}  {sev}"))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(W, 5, _ps(f"Action: {leak.get('action','')}"))
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(W, 5, _ps(f"Impact: {_fmt_pdf(leak.get('impact', 0))}"))
            pdf.ln(1)

        # ── Footer ──
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 5, _ps(f"Generated by OpsClarity AI CFO for {user['firm_name']}. For advisory use only."))
        return bytes(pdf.output())
    except Exception:
        return None

# ── SETTINGS ──────────────────────────────────────────────────────────────────
def show_settings():
    user = st.session_state.user
    topbar(user)
    section("Settings & Account")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
<div class="oc-card" style="margin-bottom:1rem">
  <div style="font-weight:700;color:#EAE6DF;margin-bottom:.5rem">Account</div>
  <div style="color:#B0ACA5;font-size:.85rem;line-height:2">
    <b>Name:</b> {user['name']}<br>
    <b>Email:</b> {user['email']}<br>
    <b>Firm:</b> {user['firm_name']}<br>
    <b>Plan:</b> {user.get('plan','free').upper()}
    {"&nbsp;&nbsp;🟢 Trial active — " + str((datetime.fromisoformat(user['trial_ends'])-datetime.now()).days) + " days left" if is_trial_active(user) else ""}
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="oc-card" style="margin-bottom:1rem">
  <div style="font-weight:700;color:#EAE6DF;margin-bottom:.75rem">🔌 Tally Desktop Agent</div>
  <div style="color:#B0ACA5;font-size:.82rem;line-height:1.8;margin-bottom:.75rem">
    The Tally Agent runs on your PC and automatically syncs data to OpsClarity every night.
    This removes the need to manually export and upload files.
  </div>
  <div style="background:#070a0f;border-radius:8px;padding:.75rem;font-family:'JetBrains Mono';font-size:.72rem;color:#C9A84C;line-height:2">
    # Step 1: Download the agent<br>
    # (Ask your developer to run the tally-agent/agent.py file)<br><br>
    # Step 2: Run setup<br>
    python agent.py --setup<br><br>
    # Step 3: Test connection<br>
    python agent.py --test<br><br>
    # Step 4: Start nightly sync<br>
    python agent.py --schedule
  </div>
</div>""", unsafe_allow_html=True)

        # Upgrade
        st.markdown("""
<div class="oc-card">
  <div style="font-weight:700;color:#EAE6DF;margin-bottom:.5rem">⬆ Upgrade Plan</div>
  <div style="color:#B0ACA5;font-size:.82rem;margin-bottom:.75rem">Contact us on WhatsApp to upgrade:</div>
</div>""", unsafe_allow_html=True)

        if st.button("📱 WhatsApp to Upgrade", use_container_width=True):
            import urllib.parse
            msg = f"Hi! I'm using OpsClarity for my CA firm ({user['firm_name']}) and want to upgrade my plan."
            st.markdown(f'<a href="https://wa.me/916362319163?text={urllib.parse.quote(msg)}" target="_blank">Click here to open WhatsApp →</a>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"; st.rerun()

        if st.button("🚪 Sign Out"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ── MAIN ROUTER ───────────────────────────────────────────────────────────────
def main():
    ensure_store()
    inject_styles()

    # Session state defaults
    if "page"  not in st.session_state: st.session_state.page  = "login"
    if "user"  not in st.session_state: st.session_state.user  = None

    page = st.session_state.page
    user = st.session_state.user

    # Redirect to login if not authenticated
    if page not in ("login",) and not user:
        st.session_state.page = "login"
        st.rerun()

    routes = {
        "login":      show_login,
        "onboarding": show_onboarding,
        "dashboard":  show_dashboard,
        "add_client": show_add_client,
        "scan":       show_scan,
        "client":     show_client,
        "settings":   show_settings,
    }

    handler = routes.get(page, show_login)
    handler()


if __name__ == "__main__":
    main()
