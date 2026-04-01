import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import random
import json

st.set_page_config(page_title="OpsClarity", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
.stApp{background:#0a0a0f;font-family:'DM Sans',sans-serif;}
.main .block-container{padding:2rem 3rem;max-width:1400px;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
.hero{text-align:center;padding:3rem 2rem 2rem;}
.hero-badge{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.3);padding:5px 14px;border-radius:20px;margin-bottom:1.5rem;background:rgba(200,255,87,.05);}
.hero-title{font-family:'DM Serif Display',serif;font-size:clamp(2.5rem,6vw,5rem);color:#f0ede8;line-height:1.05;letter-spacing:-.02em;margin-bottom:1rem;}
.hero-title span{color:#c8ff57;font-style:italic;}
.hero-sub{font-size:1.1rem;color:#6b6b7a;max-width:520px;margin:0 auto 2.5rem;line-height:1.7;font-weight:300;}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:2rem 0;}
.metric-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:1.4rem 1.6rem;position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:14px 14px 0 0;}
.metric-card.green::before{background:linear-gradient(90deg,#c8ff57,transparent);}
.metric-card.red::before{background:linear-gradient(90deg,#ff5757,transparent);}
.metric-card.amber::before{background:linear-gradient(90deg,#ffb557,transparent);}
.metric-card.blue::before{background:linear-gradient(90deg,#57b8ff,transparent);}
.metric-label{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#4a4a5a;margin-bottom:8px;}
.metric-value{font-family:'DM Serif Display',serif;font-size:2rem;color:#f0ede8;line-height:1;margin-bottom:4px;}
.metric-delta{font-size:12px;color:#c8ff57;font-weight:500;}
.metric-delta.neg{color:#ff5757;}
.section-header{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#f0ede8;margin:2.5rem 0 1rem;letter-spacing:-.01em;}
.insight-card{background:rgba(200,255,87,.05);border:1px solid rgba(200,255,87,.15);border-radius:12px;padding:1rem 1.25rem;margin-bottom:10px;}
.insight-icon{font-size:18px;margin-bottom:6px;}
.insight-text{font-size:14px;color:#c8c8d4;line-height:1.6;}
.insight-text strong{color:#c8ff57;font-weight:600;}
.action-box{background:rgba(255,255,255,.03);border-left:3px solid #c8ff57;border-radius:0 8px 8px 0;padding:8px 12px;margin-top:8px;font-size:13px;color:#9494a8;line-height:1.5;}
.action-box strong{color:#c8ff57;}
.alert-card{border-radius:12px;padding:1rem 1.25rem;margin-bottom:10px;}
.alert-card.warn{background:rgba(255,181,87,.08);border:1px solid rgba(255,181,87,.25);}
.alert-card.danger{background:rgba(255,87,87,.08);border:1px solid rgba(255,87,87,.25);}
.alert-text{font-size:14px;color:#c8c8d4;line-height:1.6;}
.alert-text strong{color:#ffb557;font-weight:600;}
.alert-card.danger .alert-text strong{color:#ff5757;}
.health-score-wrap{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1.5rem 2rem;margin:1.5rem 0;}
.health-score-num{font-family:'DM Serif Display',serif;font-size:4rem;line-height:1;margin-bottom:4px;}
.health-breakdown{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:1rem;}
.health-item{background:rgba(255,255,255,.02);border-radius:8px;padding:8px 12px;}
.health-item-label{font-size:11px;color:#4a4a5a;margin-bottom:4px;}
.health-item-bar{height:4px;background:rgba(255,255,255,.08);border-radius:2px;overflow:hidden;}
.health-item-fill{height:100%;border-radius:2px;}
.health-item-score{font-size:12px;color:#9494a8;margin-top:3px;}
.paywall{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1px solid rgba(200,255,87,.2);border-radius:20px;padding:3rem;text-align:center;margin:2rem 0;}
.paywall-title{font-family:'DM Serif Display',serif;font-size:2rem;color:#f0ede8;margin-bottom:.75rem;}
.paywall-sub{color:#6b6b7a;font-size:14px;margin-bottom:2rem;font-weight:300;}
.price-tag{font-family:'DM Serif Display',serif;font-size:3rem;color:#c8ff57;line-height:1;}
.price-tag span{font-size:1.2rem;color:#6b6b7a;font-family:'DM Sans',sans-serif;font-weight:300;}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin:2rem 0;}
.stButton>button{background:#c8ff57!important;color:#0a0a0f!important;border:none!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:14px!important;padding:.6rem 2rem!important;letter-spacing:.02em!important;}
[data-testid="stFileUploader"]{background:rgba(255,255,255,.02)!important;border:1.5px dashed rgba(200,255,87,.25)!important;border-radius:16px!important;padding:1rem!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;border:1px solid rgba(255,255,255,.06)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#6b6b7a!important;border-radius:8px!important;font-weight:500!important;font-size:13px!important;}
.stTabs [aria-selected="true"]{background:rgba(200,255,87,.1)!important;color:#c8ff57!important;}
h1,h2,h3{color:#f0ede8!important;}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────

def fmt_inr(val):
    val = float(val)
    if val >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif val >= 1_00_000: return f"₹{val/1_00_000:.1f}L"
    elif val >= 1000: return f"₹{val/1000:.1f}k"
    return f"₹{val:.0f}"


# ── SAMPLE DATA ──────────────────────────────────────────────────────────────

def make_df(records):
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

def generate_restaurant_data():
    random.seed(42); np.random.seed(42)
    customers = ["Ravi Enterprises","Meena Stores","Krishna Traders","Sunita Foods",
                 "Ramesh & Sons","Lakshmi Textiles","Suresh Auto Parts","Priya Catering",
                 "Deepak Electronics","Anita Pharmacy"]
    expense_cats = ["Raw Materials","Staff Salary","Rent","Electricity","Transport","Marketing","Misc Expenses","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(15, 30)):
            records.append({"Date": month - timedelta(days=random.randint(0,28)),
                "Type":"Sales","Category":random.choice(["Food Sales","Beverage Sales","Catering"]),
                "Party":random.choice(customers),"Amount":round(random.uniform(5000,85000),0),
                "Status":random.choice(["Paid","Paid","Paid","Overdue","Pending"]),
                "Invoice_No":f"INV-{random.randint(1000,9999)}","GST_Rate":random.choice([5,12,18])})
        for cat in expense_cats:
            amt = round(random.uniform(2000,45000),0)
            if cat=="Electricity" and month.month in [4,5,6]: amt*=2.5
            if cat=="Raw Materials": amt*=1.4
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Expense","Category":cat,"Party":"Vendor",
                "Amount":round(amt,0),"Status":"Paid",
                "Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_clinic_data():
    random.seed(10); np.random.seed(10)
    patients = ["Apollo Health","MedCare Trust","Sharma Family","Reddy Clinic Ref",
                "City Hospital Ref","Patel Family","Gupta Diagnostics","Iyer Wellness","Kumar Family","Nair Health"]
    expense_cats = ["Doctor Salaries","Medicines & Supplies","Rent","Electricity",
                    "Equipment Maintenance","Lab Reagents","Admin Staff","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(20,40)):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Sales","Category":random.choice(["Consultation","Lab Tests","Procedures","Health Packages"]),
                "Party":random.choice(patients),"Amount":round(random.uniform(800,45000),0),
                "Status":random.choice(["Paid","Paid","Paid","Paid","Overdue"]),
                "Invoice_No":f"RX-{random.randint(1000,9999)}","GST_Rate":0})
        for cat in expense_cats:
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Expense","Category":cat,"Party":"Vendor",
                "Amount":round(random.uniform(5000,80000),0),"Status":"Paid",
                "Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_retail_data():
    random.seed(20); np.random.seed(20)
    customers = ["Wholesale Hub","Metro Traders","Quick Mart","Singh Distributors","Raj Superstore",
                 "City Bazaar","Fresh Mart","Daily Needs Co","Star Retail","Budget Store"]
    expense_cats = ["Inventory Purchase","Staff Wages","Rent","Electricity","Transport & Delivery",
                    "Marketing","Shrinkage/Loss","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        n = random.randint(30,60) if month.month in [10,11,12] else random.randint(15,30)
        for _ in range(n):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Sales","Category":random.choice(["FMCG","Electronics","Apparel","Home & Kitchen"]),
                "Party":random.choice(customers),"Amount":round(random.uniform(2000,120000),0),
                "Status":random.choice(["Paid","Paid","Paid","Overdue","Pending"]),
                "Invoice_No":f"RTL-{random.randint(1000,9999)}","GST_Rate":random.choice([5,12,18])})
        for cat in expense_cats:
            amt = round(random.uniform(10000,90000),0)
            if cat=="Inventory Purchase" and month.month in [9,10]: amt*=1.8
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Expense","Category":cat,"Party":"Vendor",
                "Amount":round(amt,0),"Status":"Paid",
                "Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_agency_data():
    random.seed(30); np.random.seed(30)
    clients = ["TechStart Pvt Ltd","Growfast Brands","UrbanEats Chain","BuildRight Infra",
               "FinEdge Solutions","MegaMart Retail","HealthPlus Network","EduWorld Pvt Ltd",
               "TravelLux India","AutoNext Motors"]
    expense_cats = ["Salaries","Software Subscriptions","Rent","Electricity",
                    "Freelancer Payments","Client Servicing","Marketing","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(8,18)):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Sales","Category":random.choice(["Retainer","Project Fee","Consulting","Performance Bonus"]),
                "Party":random.choice(clients),"Amount":round(random.uniform(25000,350000),0),
                "Status":random.choice(["Paid","Paid","Overdue","Pending"]),
                "Invoice_No":f"AGY-{random.randint(1000,9999)}","GST_Rate":18})
        for cat in expense_cats:
            records.append({"Date":month-timedelta(days=random.randint(0,28)),
                "Type":"Expense","Category":cat,"Party":"Vendor",
                "Amount":round(random.uniform(15000,200000),0),"Status":"Paid",
                "Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

INDUSTRY_MAP = {
    "Restaurant / Cafe": ("restaurant", generate_restaurant_data),
    "Clinic / Diagnostic Lab": ("clinic", generate_clinic_data),
    "Retail / Distribution": ("retail", generate_retail_data),
    "Agency / Consulting": ("agency", generate_agency_data),
}


# ── MESSY FILE PARSER ────────────────────────────────────────────────────────

def parse_uploaded_file(file):
    try:
        # Try multiple encodings
        try:
            df = pd.read_csv(file) if file.name.lower().endswith(".csv") else pd.read_excel(file)
        except Exception:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin1") if file.name.lower().endswith(".csv") else pd.read_excel(file, header=1)

        # Drop fully empty rows/cols
        df = df.dropna(how="all").dropna(axis=1, how="all")

        # Smart column mapping
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher date","txn date"]): col_map[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","net","inr","rs","rupee"]): col_map[col]="Amount"
            elif any(x in cl for x in ["type","txn type","transaction type","dr/cr","dr cr","nature"]): col_map[col]="Type"
            elif any(x in cl for x in ["category","cat","head","narration","description","particulars","ledger","account"]): col_map[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","payee","client","supplier"]): col_map[col]="Party"
            elif any(x in cl for x in ["status","paid","payment status","cleared"]): col_map[col]="Status"
            elif any(x in cl for x in ["invoice","bill no","voucher","ref"]): col_map[col]="Invoice_No"

        df = df.rename(columns=col_map)

        # Parse dates flexibly
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True, errors="coerce", dayfirst=True)
            df = df.dropna(subset=["Date"])

        # Parse amounts — handle strings like "1,23,456" or "(45,000)" negatives
        if "Amount" in df.columns:
            df["Amount"] = df["Amount"].astype(str).str.replace(",","").str.replace("(","–").str.replace(")","")
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)

        # Infer Type if missing (debit=expense, credit=sales)
        if "Type" not in df.columns:
            raw_cols = [c.lower() for c in df.columns]
            if "debit" in raw_cols and "credit" in raw_cols:
                df["Type"] = df.apply(lambda r: "Expense" if pd.notna(r.get("debit","")) and float(str(r.get("debit",0)).replace(",","") or 0)>0 else "Sales", axis=1)
            else:
                df["Type"] = "Sales"

        # Normalise Type values
        if "Type" in df.columns:
            df["Type"] = df["Type"].astype(str).str.strip().str.title()
            df["Type"] = df["Type"].replace({
                "Dr":"Expense","Cr":"Sales","Debit":"Expense","Credit":"Sales",
                "Out":"Expense","In":"Sales","Payment":"Expense","Receipt":"Sales",
                "Purchase":"Expense","Sale":"Sales"
            })
            df.loc[~df["Type"].isin(["Sales","Expense"]), "Type"] = "Sales"

        # Fill missing cols
        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","–")]:
            if col not in df.columns: df[col] = default

        # Remove duplicates
        df = df.drop_duplicates()

        if "Month" not in df.columns and "Date" in df.columns:
            df["Month"] = df["Date"].dt.to_period("M").astype(str)

        return df, True, f"Loaded {len(df)} transactions successfully"
    except Exception as e:
        return None, False, str(e)


# ── BUSINESS HEALTH SCORE ────────────────────────────────────────────────────

def compute_health_score(df, industry):
    scores = {}
    sales = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    total_rev = sales["Amount"].sum()
    total_exp = expenses["Amount"].sum()
    profit = total_rev - total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0

    # 1) Profit margin
    if margin > 25: scores["Profit Margin"] = (95, "#c8ff57")
    elif margin > 15: scores["Profit Margin"] = (75, "#c8ff57")
    elif margin > 5: scores["Profit Margin"] = (55, "#ffb557")
    elif margin > 0: scores["Profit Margin"] = (35, "#ffb557")
    else: scores["Profit Margin"] = (10, "#ff5757")

    # 2) Revenue trend
    sales_m = sales.groupby("Month")["Amount"].sum().sort_index()
    if len(sales_m) >= 3:
        trend = (sales_m.iloc[-1] - sales_m.iloc[-3]) / max(sales_m.iloc[-3], 1) * 100
        if trend > 10: scores["Revenue Trend"] = (90, "#c8ff57")
        elif trend > 0: scores["Revenue Trend"] = (70, "#c8ff57")
        elif trend > -10: scores["Revenue Trend"] = (45, "#ffb557")
        else: scores["Revenue Trend"] = (20, "#ff5757")
    else:
        scores["Revenue Trend"] = (60, "#ffb557")

    # 3) Expense stability
    exp_m = expenses.groupby("Month")["Amount"].sum()
    if len(exp_m) >= 3:
        cv = exp_m.std() / max(exp_m.mean(), 1)
        if cv < 0.1: scores["Expense Stability"] = (90, "#c8ff57")
        elif cv < 0.2: scores["Expense Stability"] = (70, "#c8ff57")
        elif cv < 0.35: scores["Expense Stability"] = (50, "#ffb557")
        else: scores["Expense Stability"] = (25, "#ff5757")
    else:
        scores["Expense Stability"] = (60, "#ffb557")

    # 4) Overdue risk
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overdue_pct = (overdue/total_rev*100) if total_rev>0 else 0
    if overdue_pct < 2: scores["Collections"] = (95, "#c8ff57")
    elif overdue_pct < 8: scores["Collections"] = (70, "#c8ff57")
    elif overdue_pct < 15: scores["Collections"] = (45, "#ffb557")
    else: scores["Collections"] = (20, "#ff5757")

    # 5) Revenue concentration
    if len(sales) > 0:
        top_cust_rev = sales.groupby("Party")["Amount"].sum().max()
        conc = (top_cust_rev/total_rev*100) if total_rev>0 else 0
        if conc < 20: scores["Revenue Diversity"] = (90, "#c8ff57")
        elif conc < 35: scores["Revenue Diversity"] = (70, "#c8ff57")
        elif conc < 50: scores["Revenue Diversity"] = (45, "#ffb557")
        else: scores["Revenue Diversity"] = (20, "#ff5757")
    else:
        scores["Revenue Diversity"] = (50, "#ffb557")

    # 6) Cost ratio
    cost_ratio = (total_exp/total_rev*100) if total_rev>0 else 100
    if cost_ratio < 60: scores["Cost Efficiency"] = (90, "#c8ff57")
    elif cost_ratio < 75: scores["Cost Efficiency"] = (65, "#c8ff57")
    elif cost_ratio < 90: scores["Cost Efficiency"] = (40, "#ffb557")
    else: scores["Cost Efficiency"] = (15, "#ff5757")

    overall = int(sum(v for v,_ in scores.values()) / len(scores))
    if overall >= 75: color = "#c8ff57"
    elif overall >= 50: color = "#ffb557"
    else: color = "#ff5757"

    return overall, color, scores


# ── INDUSTRY INSIGHTS + ACTIONS ──────────────────────────────────────────────

def generate_insights_with_actions(df, industry):
    insights = []
    sales = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    total_rev = sales["Amount"].sum()
    total_exp = expenses["Amount"].sum()
    profit = total_rev - total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overdue_pct = (overdue/total_rev*100) if total_rev>0 else 0

    top_exp_series = expenses.groupby("Category")["Amount"].sum() if len(expenses)>0 else pd.Series()
    top_exp = top_exp_series.idxmax() if len(top_exp_series)>0 else "N/A"
    top_exp_pct = (top_exp_series.max()/total_exp*100) if total_exp>0 and len(top_exp_series)>0 else 0
    best_cust = sales.groupby("Party")["Amount"].sum().idxmax() if len(sales)>0 else "N/A"
    best_cust_rev = sales.groupby("Party")["Amount"].sum().max() if len(sales)>0 else 0
    best_cust_pct = (best_cust_rev/total_rev*100) if total_rev>0 else 0

    # Margin insight
    if margin > 20:
        insights.append(("◈",
            f"Profit margin is <strong>{margin:.1f}%</strong> — healthy for an SME.",
            f"Maintain this by keeping <strong>{top_exp}</strong> below {top_exp_pct:.0f}% of expenses. Reinvest surplus into marketing or inventory."))
    elif margin > 0:
        insights.append(("▲",
            f"Margin is thin at <strong>{margin:.1f}%</strong>. Biggest cost: <strong>{top_exp} ({top_exp_pct:.0f}%)</strong>.",
            f"Review {top_exp} line items this week. Even a 10% reduction here adds {fmt_inr(total_exp * top_exp_pct/100 * 0.1)} back to profit."))
    else:
        insights.append(("⚠",
            f"Running at a <strong>loss of {fmt_inr(abs(profit))}</strong>. Expenses exceed revenue by {abs(margin):.1f}%.",
            f"Immediate action needed: freeze discretionary spending, prioritise collecting {fmt_inr(overdue)} in overdue invoices, and review if {top_exp} can be renegotiated."))

    # Customer concentration
    if best_cust_pct > 40:
        insights.append(("◉",
            f"<strong>{best_cust}</strong> contributes <strong>{best_cust_pct:.0f}%</strong> of total revenue — dangerously high concentration.",
            f"Start acquiring at least 2–3 new clients this month. If {best_cust} slows down, your revenue drops immediately."))
    else:
        insights.append(("◆",
            f"<strong>{best_cust}</strong> is your top customer at <strong>{fmt_inr(best_cust_rev)}</strong> ({best_cust_pct:.0f}% of revenue).",
            f"Upsell or cross-sell to {best_cust} — it costs 5x less to grow an existing customer than acquire a new one."))

    # Overdue
    if overdue > 0:
        insights.append(("◉",
            f"<strong>{fmt_inr(overdue)} stuck in overdue invoices</strong> ({overdue_pct:.0f}% of revenue).",
            f"Send payment reminders today. Offer a 2% early payment discount if needed — recovering {fmt_inr(overdue)} is better than waiting."))

    # Industry-specific
    if industry == "restaurant":
        food_cost = expenses[expenses["Category"]=="Raw Materials"]["Amount"].sum()
        food_ratio = (food_cost/total_rev*100) if total_rev>0 else 0
        if food_ratio > 35:
            insights.append(("◐",
                f"Food cost ratio is <strong>{food_ratio:.0f}%</strong> — above the 30% industry benchmark.",
                "Review supplier contracts, reduce waste, and audit portion sizes. A 5% reduction in food cost directly improves your bottom line."))
        elec = expenses[expenses["Category"]=="Electricity"]["Amount"].sum()
        elec_ratio = (elec/total_exp*100) if total_exp>0 else 0
        if elec_ratio > 8:
            insights.append(("◐",
                f"Electricity is <strong>{elec_ratio:.0f}%</strong> of expenses — high for a restaurant.",
                "Check if ACs, refrigerators, or kitchen equipment are energy-inefficient. Switch to LED lighting and off-peak equipment usage."))

    elif industry == "clinic":
        lab_rev = sales[sales["Category"]=="Lab Tests"]["Amount"].sum()
        consult_rev = sales[sales["Category"]=="Consultation"]["Amount"].sum()
        if consult_rev > 0 and lab_rev / max(consult_rev,1) < 0.3:
            insights.append(("◐",
                "Lab revenue is <strong>low relative to consultations</strong>.",
                "Recommend in-house lab tests during consultations. This is a high-margin revenue stream — even 20% conversion improves revenue significantly."))
        doc_sal = expenses[expenses["Category"]=="Doctor Salaries"]["Amount"].sum()
        doc_pct = (doc_sal/total_exp*100) if total_exp>0 else 0
        if doc_pct > 45:
            insights.append(("◐",
                f"Doctor salaries are <strong>{doc_pct:.0f}%</strong> of expenses.",
                "Review whether patient volume justifies current staffing. Consider part-time specialist arrangements to reduce fixed salary costs."))

    elif industry == "retail":
        inv_cost = expenses[expenses["Category"]=="Inventory Purchase"]["Amount"].sum()
        inv_ratio = (inv_cost/total_exp*100) if total_exp>0 else 0
        if inv_ratio > 60:
            insights.append(("◐",
                f"Inventory is <strong>{inv_ratio:.0f}%</strong> of expenses — high working capital locked in stock.",
                "Move to just-in-time ordering for slow-moving SKUs. Identify items with >60 days of stock and run a clearance cycle."))
        shrink = expenses[expenses["Category"]=="Shrinkage/Loss"]["Amount"].sum()
        if shrink > 0:
            shrink_pct = shrink/total_rev*100
            insights.append(("◐",
                f"Shrinkage/losses are <strong>{fmt_inr(shrink)} ({shrink_pct:.1f}% of revenue)</strong>.",
                "Install basic CCTV, tighten stock audits, and do weekly physical counts. Even 50% reduction in shrinkage adds directly to profit."))

    elif industry == "agency":
        sal = expenses[expenses["Category"]=="Salaries"]["Amount"].sum()
        sal_pct = (sal/total_rev*100) if total_rev>0 else 0
        if sal_pct > 50:
            insights.append(("◐",
                f"Salaries are <strong>{sal_pct:.0f}%</strong> of revenue — above the 40–45% agency benchmark.",
                "Review utilisation rates per team member. If billable hours are below 70%, either reduce bench or convert fixed costs to variable (freelancers)."))
        software = expenses[expenses["Category"]=="Software Subscriptions"]["Amount"].sum()
        if software > 0:
            insights.append(("◐",
                f"Software subscriptions: <strong>{fmt_inr(software)}</strong>.",
                "Audit all subscriptions quarterly. Cancel tools with <50% team usage. Many agencies find 20–30% of software spend is on unused tools."))

    return insights


# ── ANOMALY DETECTION ────────────────────────────────────────────────────────

def detect_anomalies(df):
    alerts = []
    expenses = df[df["Type"]=="Expense"]
    for cat in expenses["Category"].unique():
        cat_df = expenses[expenses["Category"]==cat].groupby("Month")["Amount"].sum()
        if len(cat_df)<3: continue
        mean,std = cat_df.mean(), cat_df.std()
        if std==0: continue
        last_val = cat_df.iloc[-1]
        z = (last_val-mean)/std
        if z>1.5:
            alerts.append(("danger",f"<strong>{cat}</strong> last month: <strong>{fmt_inr(last_val)}</strong> — {((last_val/mean-1)*100):.0f}% above average ({fmt_inr(mean)}/month).",
                f"Check invoices for {cat}. Could be a billing error, price increase, or one-off event."))
        elif z>1.0:
            alerts.append(("warn",f"<strong>{cat}</strong> slightly elevated at <strong>{fmt_inr(last_val)}</strong> vs avg {fmt_inr(mean)}.",
                "Monitor next month — if it continues rising, investigate the cause."))
    sales_m = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum().sort_index()
    if len(sales_m)>=2:
        prev,last = sales_m.iloc[-2], sales_m.iloc[-1]
        drop = (prev-last)/prev*100 if prev>0 else 0
        if drop>20:
            alerts.append(("danger",f"Revenue dropped <strong>{drop:.0f}%</strong> last month ({fmt_inr(prev)} → {fmt_inr(last)}).",
                "Urgent: identify if this is seasonal, customer loss, or collections delay. Check overdue invoices first."))
    return alerts


# ── GST + FORECAST + EXPORTS ─────────────────────────────────────────────────

def gst_summary(df):
    sales = df[df["Type"]=="Sales"].copy()
    total_sales = sales["Amount"].sum()
    if "GST_Rate" in sales.columns:
        sales["GST_Amt"] = sales.apply(lambda r: r["Amount"]*r["GST_Rate"]/(100+max(r["GST_Rate"],1)) if r["GST_Rate"]>0 else 0, axis=1)
        output_gst = sales["GST_Amt"].sum()
    else:
        output_gst = total_sales*0.18/1.18
    expenses = df[df["Type"]=="Expense"].copy()
    gst_exp = expenses[expenses["Category"]=="GST Paid"]["Amount"].sum()
    input_gst = gst_exp if gst_exp>0 else expenses["Amount"].sum()*0.05
    net_gst = output_gst-input_gst
    return {"output_gst":output_gst,"input_gst":input_gst,"net_payable":max(net_gst,0),
            "cgst":output_gst/2,"sgst":output_gst/2,"total_sales":total_sales}

def cash_flow_forecast(df, months_ahead=3):
    sales_m = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum().sort_index()
    exp_m = df[df["Type"]=="Expense"].groupby("Month")["Amount"].sum().sort_index()
    avg_rev = sales_m.tail(3).mean() if len(sales_m)>=3 else sales_m.mean()
    avg_exp = exp_m.tail(3).mean() if len(exp_m)>=3 else exp_m.mean()
    rev_trend = (sales_m.iloc[-1]-sales_m.iloc[-3])/3 if len(sales_m)>=3 else 0
    exp_trend = (exp_m.iloc[-1]-exp_m.iloc[-3])/3 if len(exp_m)>=3 else 0
    forecast = []
    for i in range(1,months_ahead+1):
        label = (datetime.now()+timedelta(days=30*i)).strftime("%b %Y")
        pr = max(avg_rev+rev_trend*i,0)
        pe = max(avg_exp+exp_trend*i,0)
        forecast.append({"Month":label,"Projected Revenue":round(pr,0),"Projected Expenses":round(pe,0),"Projected Profit":round(pr-pe,0)})
    return pd.DataFrame(forecast)

def generate_whatsapp_summary(df):
    total_rev = df[df["Type"]=="Sales"]["Amount"].sum()
    total_exp = df[df["Type"]=="Expense"]["Amount"].sum()
    profit = total_rev-total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    top_exp = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().idxmax() if len(df[df["Type"]=="Expense"])>0 else "N/A"
    top_cust = df[df["Type"]=="Sales"].groupby("Party")["Amount"].sum().idxmax() if len(df[df["Type"]=="Sales"])>0 else "N/A"
    return f"""*OpsClarity Business Summary*
Revenue: {fmt_inr(total_rev)}
Expenses: {fmt_inr(total_exp)}
Net Profit: {fmt_inr(profit)} ({margin:.1f}% margin)
Overdue: {fmt_inr(overdue)}
Top Cost: {top_exp}
Best Customer: {top_cust}
_Generated by OpsClarity_
Try free: https://opscalarity.streamlit.app"""

def generate_report_csv(df):
    total_rev = df[df["Type"]=="Sales"]["Amount"].sum()
    total_exp = df[df["Type"]=="Expense"]["Amount"].sum()
    profit = total_rev-total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    exp_b = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().reset_index()
    exp_b["Share %"] = (exp_b["Amount"]/total_exp*100).round(1)
    top_c = df[df["Type"]=="Sales"].groupby("Party")["Amount"].sum().reset_index().sort_values("Amount",ascending=False).head(5)
    out = io.StringIO()
    out.write(f"OpsClarity Business Report\nGenerated: {datetime.now().strftime('%d %b %Y %H:%M')}\n\n")
    out.write("P&L SUMMARY\n")
    out.write(f"Total Revenue,{fmt_inr(total_rev)}\nTotal Expenses,{fmt_inr(total_exp)}\n")
    out.write(f"Net Profit,{fmt_inr(profit)}\nProfit Margin,{margin:.1f}%\nOverdue Invoices,{fmt_inr(overdue)}\n\n")
    out.write("EXPENSE BREAKDOWN\n"); out.write(exp_b.to_csv(index=False))
    out.write("\nTOP CUSTOMERS\n"); out.write(top_c.to_csv(index=False))
    out.write("\nALL TRANSACTIONS\n"); out.write(df.to_csv(index=False))
    return out.getvalue().encode()

def ask_ai(question, df):
    total_rev = df[df["Type"]=="Sales"]["Amount"].sum()
    total_exp = df[df["Type"]=="Expense"]["Amount"].sum()
    profit = total_rev-total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    top_exp = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().to_dict()
    top_cust = df[df["Type"]=="Sales"].groupby("Party")["Amount"].sum().nlargest(5).to_dict()
    context = f"""You are a sharp Indian SME financial advisor. Answer in plain language, be specific with numbers, give actionable advice. Keep it under 150 words.
Business data: Revenue={fmt_inr(total_rev)}, Expenses={fmt_inr(total_exp)}, Profit={fmt_inr(profit)} ({margin:.1f}% margin), Overdue={fmt_inr(overdue)}
Expense breakdown: {json.dumps({k:fmt_inr(v) for k,v in top_exp.items()})}
Top customers: {json.dumps({k:fmt_inr(v) for k,v in top_cust.items()})}
Question: {question}"""
    import urllib.request
    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":300,"messages":[{"role":"user","content":context}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=payload,
        headers={"Content-Type":"application/json","anthropic-version":"2023-06-01"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=15) as resp:
            return json.loads(resp.read())["content"][0]["text"]
    except Exception:
        return "AI Q&A needs ANTHROPIC_API_KEY in Streamlit secrets. Add it under Settings → Secrets."


# ── MAIN APP ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-badge">◈ OpsClarity — SME Intelligence</div>
    <h1 class="hero-title">Upload your numbers.<br><span>Understand your business.</span></h1>
    <p class="hero-sub">Tally export, Excel, bank statement — any format. Instant P&L, health score, anomaly alerts, GST summary, and AI-powered action recommendations.</p>
</div>
""", unsafe_allow_html=True)

for key,default in [("df",None),("industry","restaurant"),("unlocked",False),("chat_history",[])]:
    if key not in st.session_state: st.session_state[key]=default

# Upload
col1,col2,col3 = st.columns([1,2,1])
with col2:
    uploaded_file = st.file_uploader("Drop your file here — CSV, Excel, Tally export, bank statement",type=["csv","xlsx","xls"])
    st.markdown("<div style='text-align:center;margin:.5rem 0;color:#3a3a4a;font-size:13px;'>— or try a sample —</div>",unsafe_allow_html=True)
    industry_name = st.selectbox("Choose industry",list(INDUSTRY_MAP.keys()),label_visibility="collapsed")
    if st.button(f"Load {industry_name} sample data",use_container_width=True):
        ind_key, gen_fn = INDUSTRY_MAP[industry_name]
        st.session_state.df = gen_fn()
        st.session_state.industry = ind_key

if uploaded_file:
    df_up,ok,msg = parse_uploaded_file(uploaded_file)
    if ok:
        st.session_state.df = df_up
        st.session_state.industry = "restaurant"
        st.success(msg)
    else:
        st.error(f"Could not parse file: {msg}. Try saving as CSV and re-uploading.")

# Dashboard
if st.session_state.df is not None:
    df = st.session_state.df.copy()
    industry = st.session_state.industry

    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)

    # Date filter
    if "Date" in df.columns and df["Date"].notna().any():
        min_d,max_d = df["Date"].min().date(), df["Date"].max().date()
        fc1,fc2,fc3 = st.columns([2,2,4])
        with fc1: start_d = st.date_input("From",value=min_d,min_value=min_d,max_value=max_d)
        with fc2: end_d = st.date_input("To",value=max_d,min_value=min_d,max_value=max_d)
        df = df[(df["Date"].dt.date>=start_d)&(df["Date"].dt.date<=end_d)]
        with fc3: st.markdown(f"<div style='padding-top:1.8rem;font-size:13px;color:#4a4a5a;'>{len(df)} transactions • {start_d.strftime('%d %b %Y')} to {end_d.strftime('%d %b %Y')}</div>",unsafe_allow_html=True)

    # KPIs
    total_rev = df[df["Type"]=="Sales"]["Amount"].sum()
    total_exp = df[df["Type"]=="Expense"]["Amount"].sum()
    profit = total_rev-total_exp
    margin = (profit/total_rev*100) if total_rev>0 else 0
    overdue_amt = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green"><div class="metric-label">Total Revenue</div><div class="metric-value">{fmt_inr(total_rev)}</div><div class="metric-delta">Selected period</div></div>
        <div class="metric-card red"><div class="metric-label">Total Expenses</div><div class="metric-value">{fmt_inr(total_exp)}</div><div class="metric-delta neg">Review top costs</div></div>
        <div class="metric-card {'green' if profit>=0 else 'red'}"><div class="metric-label">Net Profit</div><div class="metric-value">{fmt_inr(abs(profit))}</div><div class="metric-delta {'neg' if profit<0 else ''}">{'▲' if profit>=0 else '▼'} {abs(margin):.1f}% margin</div></div>
        <div class="metric-card amber"><div class="metric-label">Overdue Invoices</div><div class="metric-value">{fmt_inr(overdue_amt)}</div><div class="metric-delta neg">Collect now</div></div>
    </div>
    """,unsafe_allow_html=True)

    # Health Score
    st.markdown("<div class='section-header'>◈ Business Health Score</div>",unsafe_allow_html=True)
    overall,color,scores = compute_health_score(df,industry)
    label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs attention" if overall>=45 else "Critical"

    score_html = f"""<div class="health-score-wrap">
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:6px;">
        <div class="health-score-num" style="color:{color}">{overall}</div>
        <div style="font-size:1.1rem;color:#6b6b7a;">/ 100 — <span style="color:{color}">{label}</span></div>
    </div>
    <div class="health-breakdown">"""
    for name,(score,sc) in scores.items():
        score_html += f"""<div class="health-item">
        <div class="health-item-label">{name}</div>
        <div class="health-item-bar"><div class="health-item-fill" style="width:{score}%;background:{sc}"></div></div>
        <div class="health-item-score" style="color:{sc}">{score}/100</div></div>"""
    score_html += "</div></div>"
    st.markdown(score_html,unsafe_allow_html=True)

    # Insights + Actions
    st.markdown("<div class='section-header'>◈ Insights & recommended actions</div>",unsafe_allow_html=True)
    for icon,text,action in generate_insights_with_actions(df,industry):
        st.markdown(f"""<div class="insight-card">
        <div class="insight-icon">{icon}</div>
        <div class="insight-text">{text}</div>
        <div class="action-box"><strong>Action:</strong> {action}</div>
        </div>""",unsafe_allow_html=True)

    # Anomaly Alerts
    alerts = detect_anomalies(df)
    if alerts:
        st.markdown("<div class='section-header'>Anomaly alerts</div>",unsafe_allow_html=True)
        for level,text,action in alerts:
            st.markdown(f"""<div class="alert-card {level}">
            <div class="alert-text">{text}</div>
            <div class="action-box"><strong>Action:</strong> {action}</div>
            </div>""",unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)

    # Charts
    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "Revenue & Expenses","Expense Breakdown","Top Customers",
        "Monthly Profit","GST Summary","Cash Flow Forecast","Invoice Tracker"])

    with tab1:
        st.markdown("<div class='section-header'>Revenue vs Expenses trend</div>",unsafe_allow_html=True)
        sales_m = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum()
        exp_m = df[df["Type"]=="Expense"].groupby("Month")["Amount"].sum()
        st.line_chart(pd.DataFrame({"Revenue":sales_m,"Expenses":exp_m}).fillna(0).sort_index(),use_container_width=True)

    with tab2:
        ca,cb = st.columns([1,1])
        with ca:
            st.markdown("<div class='section-header'>Where money is going</div>",unsafe_allow_html=True)
            st.bar_chart(df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False),use_container_width=True)
        with cb:
            st.markdown("<div class='section-header'>Breakdown</div>",unsafe_allow_html=True)
            et = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().reset_index().sort_values("Amount",ascending=False)
            et["Share %"] = (et["Amount"]/et["Amount"].sum()*100).round(1)
            et["Amount"] = et["Amount"].apply(fmt_inr)
            st.dataframe(et[["Category","Amount","Share %"]],hide_index=True,use_container_width=True)

    with tab3:
        st.markdown("<div class='section-header'>Top customers by revenue</div>",unsafe_allow_html=True)
        st.bar_chart(df[df["Type"]=="Sales"].groupby("Party")["Amount"].sum().sort_values(ascending=False).head(8),use_container_width=True)

    with tab4:
        st.markdown("<div class='section-header'>Monthly profit / loss</div>",unsafe_allow_html=True)
        sm = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum()
        em = df[df["Type"]=="Expense"].groupby("Month")["Amount"].sum()
        st.bar_chart(pd.DataFrame({"Profit":(sm-em).fillna(0).sort_index()}),use_container_width=True)

    with tab5:
        st.markdown("<div class='section-header'>GST Summary</div>",unsafe_allow_html=True)
        gst = gst_summary(df)
        g1,g2,g3,g4 = st.columns(4)
        g1.metric("Output GST",fmt_inr(gst["output_gst"]))
        g2.metric("Input GST Credit",fmt_inr(gst["input_gst"]))
        g3.metric("Net GST Payable",fmt_inr(gst["net_payable"]))
        g4.metric("Taxable Sales",fmt_inr(gst["total_sales"]))
        gc1,gc2 = st.columns(2)
        gc1.metric("CGST (50%)",fmt_inr(gst["cgst"]))
        gc2.metric("SGST (50%)",fmt_inr(gst["sgst"]))
        st.info("Estimates only. Verify with your CA before filing.")

    with tab6:
        st.markdown("<div class='section-header'>Cash Flow Forecast</div>",unsafe_allow_html=True)
        ma = st.slider("Forecast months ahead",1,6,3)
        fdf = cash_flow_forecast(df,ma)
        st.line_chart(fdf.set_index("Month")[["Projected Revenue","Projected Expenses"]],use_container_width=True)
        disp = fdf.copy()
        for c in ["Projected Revenue","Projected Expenses","Projected Profit"]: disp[c]=disp[c].apply(fmt_inr)
        st.dataframe(disp,hide_index=True,use_container_width=True)

    with tab7:
        st.markdown("<div class='section-header'>Invoice Tracker</div>",unsafe_allow_html=True)
        if "Status" in df.columns:
            cols = ["Date","Party","Amount","Status"]
            if "Invoice_No" in df.columns: cols = ["Date","Invoice_No"]+cols[1:]
            inv = df[df["Type"]=="Sales"][cols].copy().sort_values("Status").head(25)
            sf = st.selectbox("Filter",["All","Overdue","Pending","Paid"])
            if sf!="All": inv=inv[inv["Status"]==sf]
            st.dataframe(inv.assign(Amount=inv["Amount"].apply(fmt_inr)),hide_index=True,use_container_width=True)

    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)

    # AI Q&A
    st.markdown("<div class='section-header'>Ask your data anything</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#6b6b7a;font-size:14px;margin-bottom:1rem;'>\"Why did profit drop?\", \"Which expense should I cut first?\", \"How do I improve my margin?\"</p>",unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if question := st.chat_input("Ask about your business..."):
        st.session_state.chat_history.append({"role":"user","content":question})
        with st.chat_message("user"): st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Analysing..."): answer = ask_ai(question,df)
            st.write(answer)
            st.session_state.chat_history.append({"role":"assistant","content":answer})

    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)

    # Exports
    st.markdown("<div class='section-header'>Export</div>",unsafe_allow_html=True)
    ex1,ex2,ex3 = st.columns(3)
    with ex1:
        st.markdown("**Report for CA**")
        st.download_button("Download Report (CSV)",data=generate_report_csv(df),
            file_name=f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",use_container_width=True)
    with ex2:
        st.markdown("**WhatsApp Summary**")
        st.text_area("Copy & send:",value=generate_whatsapp_summary(df),height=160,label_visibility="collapsed")
    with ex3:
        st.markdown("**Raw Data**")
        st.download_button("Download All Transactions",data=df.to_csv(index=False).encode(),
            file_name=f"OpsClarity_Data_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",use_container_width=True)

    # Paywall
    if not st.session_state.unlocked:
        st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
        st.markdown("""<div class="paywall">
        <div class="paywall-title">You've seen what clarity feels like.</div>
        <div class="paywall-sub">Unlock monthly auto-reports, AI advisor, GST filing prep, and priority support.</div>
        <div class="price-tag">₹2,999 <span>/ month</span></div>
        <div style="margin-top:.5rem;font-size:12px;color:#3a3a4a;">Cancel anytime. No contracts.</div>
        </div>""",unsafe_allow_html=True)
        _,cp,_ = st.columns([1,1,1])
        with cp:
            if st.button("Unlock full access — Rs 2,999/mo",use_container_width=True):
                st.session_state.unlocked=True
                st.success("Add your Razorpay key to enable payments!")

else:
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:2rem 0;">
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.5rem;">
            <div style="font-size:22px;margin-bottom:10px;">◈</div>
            <div style="font-weight:500;color:#f0ede8;margin-bottom:6px;font-size:14px;">Instant P&L</div>
            <div style="font-size:13px;color:#4a4a5a;line-height:1.6;">Revenue, expenses, and net profit in 30 seconds.</div>
        </div>
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.5rem;">
            <div style="font-size:22px;margin-bottom:10px;">74</div>
            <div style="font-weight:500;color:#f0ede8;margin-bottom:6px;font-size:14px;">Health Score</div>
            <div style="font-size:13px;color:#4a4a5a;line-height:1.6;">One number that tells you how your business is doing.</div>
        </div>
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.5rem;">
            <div style="font-size:22px;margin-bottom:10px;">!</div>
            <div style="font-weight:500;color:#f0ede8;margin-bottom:6px;font-size:14px;">Action Recommendations</div>
            <div style="font-size:13px;color:#4a4a5a;line-height:1.6;">Not just what's wrong — exactly what to do about it.</div>
        </div>
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.5rem;">
            <div style="font-size:22px;margin-bottom:10px;">AI</div>
            <div style="font-weight:500;color:#f0ede8;margin-bottom:6px;font-size:14px;">AI Q&A</div>
            <div style="font-size:13px;color:#4a4a5a;line-height:1.6;">Ask anything about your numbers in plain English.</div>
        </div>
    </div>""",unsafe_allow_html=True)
