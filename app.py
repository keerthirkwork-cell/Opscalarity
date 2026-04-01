import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io, random, json

st.set_page_config(page_title="OpsClarity", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
.stApp{background:#0a0a0f;font-family:'DM Sans',sans-serif;}
.main .block-container{padding:2rem 3rem;max-width:1450px;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

.hero{text-align:center;padding:3rem 2rem 1.5rem;}
.hero-badge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.25);padding:6px 14px;border-radius:30px;background:rgba(200,255,87,.05);margin-bottom:1.4rem;}
.hero-title{font-family:'DM Serif Display',serif;font-size:clamp(2.7rem,6vw,5rem);line-height:1.03;color:#f4f1eb;letter-spacing:-.03em;margin-bottom:1rem;}
.hero-title span{color:#c8ff57;font-style:italic;}
.hero-sub{max-width:700px;margin:0 auto 2rem;font-size:1.05rem;color:#7f7f92;line-height:1.8;font-weight:300;}

.upload-wrap{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:22px;padding:1.5rem;margin:0 auto 2rem;backdrop-filter:blur(12px);}
.mini-note{text-align:center;color:#505062;font-size:12px;margin-top:8px;}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin:2rem 0;}
.section-title{font-family:'DM Serif Display',serif;font-size:1.65rem;color:#f4f1eb;margin:2.4rem 0 .5rem;letter-spacing:-.02em;}
.section-sub{color:#7f7f92;font-size:14px;margin-bottom:1rem;}

.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:1rem 0 2rem;}
.metric-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:1.4rem 1.5rem;position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.metric-card.green::before{background:linear-gradient(90deg,#c8ff57,transparent);}
.metric-card.red::before{background:linear-gradient(90deg,#ff5e5e,transparent);}
.metric-card.amber::before{background:linear-gradient(90deg,#ffb557,transparent);}
.metric-card.blue::before{background:linear-gradient(90deg,#57b8ff,transparent);}
.metric-label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b5b6f;font-weight:700;margin-bottom:8px;}
.metric-value{font-family:'DM Serif Display',serif;font-size:2rem;color:#f4f1eb;line-height:1;margin-bottom:5px;}
.metric-sub{font-size:12px;color:#9a9aae;}

.health-wrap{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:1.5rem 1.8rem;margin-top:1rem;}
.health-score{font-family:'DM Serif Display',serif;font-size:4rem;line-height:1;margin-bottom:6px;}
.health-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:1.2rem;}
.health-item{background:rgba(255,255,255,.02);border-radius:10px;padding:10px 12px;}
.health-label{font-size:11px;color:#616173;margin-bottom:6px;}
.health-bar{height:5px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden;}
.health-fill{height:100%;border-radius:99px;}
.health-score-small{font-size:12px;margin-top:6px;color:#9d9daf;}

.owner-summary{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1px solid rgba(200,255,87,.18);border-radius:20px;padding:1.6rem 1.8rem;margin-top:1rem;}
.owner-summary-label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#c8ff57;font-weight:700;margin-bottom:10px;}
.owner-summary-text{color:#f4f1eb;font-size:1rem;line-height:1.9;}
.owner-summary-text strong{color:#c8ff57;}

.problem-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:1rem;}
.problem-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:1.3rem;}
.problem-tag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border-radius:999px;margin-bottom:12px;}
.problem-tag.red{color:#ff7c7c;background:rgba(255,94,94,.08);border:1px solid rgba(255,94,94,.18);}
.problem-tag.amber{color:#ffcb7c;background:rgba(255,181,87,.08);border:1px solid rgba(255,181,87,.18);}
.problem-tag.green{color:#c8ff57;background:rgba(200,255,87,.08);border:1px solid rgba(200,255,87,.18);}
.problem-title{color:#f4f1eb;font-size:1.05rem;font-weight:700;margin-bottom:10px;}
.problem-text{color:#b0b0c1;font-size:14px;line-height:1.7;margin-bottom:14px;}
.problem-action{background:rgba(255,255,255,.03);border-left:3px solid #c8ff57;padding:10px 12px;border-radius:0 10px 10px 0;font-size:13px;color:#a0a0b4;line-height:1.6;}
.problem-action strong{color:#c8ff57;}

.panel{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:1.4rem 1.5rem;}
.panel-title{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#c8ff57;font-weight:700;margin-bottom:12px;}
.panel p{color:#b4b4c4;line-height:1.8;font-size:14px;margin-bottom:6px;}
.leak-item{border-top:1px solid rgba(255,255,255,.06);padding:12px 0;}
.leak-item:first-child{border-top:none;padding-top:0;}
.leak-title{color:#f4f1eb;font-weight:600;margin-bottom:4px;font-size:14px;}
.leak-sub{color:#8f8fa4;font-size:13px;line-height:1.7;}

.bench-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:1rem;}
.bench-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:1rem 1.2rem;}
.bench-label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#5b5b6f;font-weight:700;margin-bottom:8px;}
.bench-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}
.bench-yours{font-size:1.2rem;font-weight:700;font-family:'DM Serif Display',serif;}
.bench-avg{font-size:12px;color:#6b6b7a;margin-top:2px;}
.bench-bar-wrap{height:6px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden;margin-top:8px;}
.bench-bar-fill{height:100%;border-radius:99px;}

.collection-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:rgba(255,87,87,.05);border:1px solid rgba(255,87,87,.12);border-radius:10px;margin-bottom:8px;}
.collection-party{color:#f4f1eb;font-weight:600;font-size:14px;}
.collection-amt{color:#ff7c7c;font-weight:700;font-size:14px;}
.collection-days{font-size:11px;color:#8f8fa4;margin-top:2px;}

.alert-card{border-radius:12px;padding:1rem 1.25rem;margin-bottom:10px;}
.alert-card.warn{background:rgba(255,181,87,.08);border:1px solid rgba(255,181,87,.25);}
.alert-card.danger{background:rgba(255,87,87,.08);border:1px solid rgba(255,87,87,.25);}
.alert-text{font-size:14px;color:#c8c8d4;line-height:1.6;}
.alert-text strong{color:#ffb557;font-weight:600;}
.alert-card.danger .alert-text strong{color:#ff5757;}
.alert-action{background:rgba(255,255,255,.03);border-left:3px solid #ffb557;padding:8px 12px;border-radius:0 8px 8px 0;font-size:13px;color:#9a9aae;margin-top:8px;line-height:1.6;}
.alert-card.danger .alert-action{border-left-color:#ff5757;}

.trust-box{background:rgba(87,184,255,.06);border:1px solid rgba(87,184,255,.15);border-radius:14px;padding:1rem 1.4rem;margin-top:1.4rem;}
.trust-title{color:#57b8ff;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;}
.trust-text{color:#aab9c7;font-size:13px;line-height:1.8;}

.paywall{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1px solid rgba(200,255,87,.2);border-radius:20px;padding:3rem;text-align:center;margin:2rem 0;}
.paywall-title{font-family:'DM Serif Display',serif;font-size:2rem;color:#f4f1eb;margin-bottom:.75rem;}
.paywall-sub{color:#6b6b7a;font-size:14px;margin-bottom:2rem;font-weight:300;}
.price-tag{font-family:'DM Serif Display',serif;font-size:3rem;color:#c8ff57;line-height:1;}
.price-tag span{font-size:1.2rem;color:#6b6b7a;font-family:'DM Sans',sans-serif;font-weight:300;}

.stButton>button{background:#c8ff57!important;color:#0a0a0f!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:.65rem 1.6rem!important;}
.stDownloadButton>button{background:#c8ff57!important;color:#0a0a0f!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:.65rem 1.6rem!important;}
[data-testid="stFileUploader"]{background:rgba(255,255,255,.02)!important;border:1.5px dashed rgba(200,255,87,.25)!important;border-radius:18px!important;padding:1rem!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;border:1px solid rgba(255,255,255,.06)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#727285!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;}
.stTabs [aria-selected="true"]{background:rgba(200,255,87,.1)!important;color:#c8ff57!important;}
h1,h2,h3,h4{color:#f4f1eb!important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:10px!important;color:#f4f1eb!important;}
.stChatMessage{background:rgba(255,255,255,.03)!important;border:1px solid rgba(255,255,255,.07)!important;border-radius:12px!important;}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────

def fmt_inr(val):
    val = float(val)
    if val >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif val >= 1_00_000: return f"₹{val/1_00_000:.1f}L"
    elif val >= 1000: return f"₹{val/1000:.1f}k"
    return f"₹{val:.0f}"

def make_df(records):
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


# ── SAMPLE DATA ──────────────────────────────────────────────────────────────

def generate_restaurant_data():
    random.seed(42); np.random.seed(42)
    customers = ["Ravi Enterprises","Meena Stores","Krishna Traders","Sunita Foods","Ramesh & Sons","Lakshmi Textiles","Suresh Auto Parts","Priya Catering","Deepak Electronics","Anita Pharmacy"]
    expense_cats = ["Raw Materials","Staff Salary","Rent","Electricity","Transport","Marketing","Misc Expenses","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(15,30)):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Sales","Category":random.choice(["Food Sales","Beverage Sales","Catering"]),"Party":random.choice(customers),"Amount":round(random.uniform(5000,85000),0),"Status":random.choice(["Paid","Paid","Paid","Overdue","Pending"]),"Invoice_No":f"INV-{random.randint(1000,9999)}","GST_Rate":random.choice([5,12,18])})
        for cat in expense_cats:
            amt = round(random.uniform(2000,45000),0)
            if cat=="Electricity" and month.month in [4,5,6]: amt*=2.5
            if cat=="Raw Materials": amt*=1.4
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Expense","Category":cat,"Party":"Vendor","Amount":round(amt,0),"Status":"Paid","Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_clinic_data():
    random.seed(10); np.random.seed(10)
    patients = ["Apollo Health","MedCare Trust","Sharma Family","Reddy Clinic Ref","City Hospital Ref","Patel Family","Gupta Diagnostics","Iyer Wellness","Kumar Family","Nair Health"]
    expense_cats = ["Doctor Salaries","Medicines & Supplies","Rent","Electricity","Equipment Maintenance","Lab Reagents","Admin Staff","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(20,40)):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Sales","Category":random.choice(["Consultation","Lab Tests","Procedures","Health Packages"]),"Party":random.choice(patients),"Amount":round(random.uniform(800,45000),0),"Status":random.choice(["Paid","Paid","Paid","Paid","Overdue"]),"Invoice_No":f"RX-{random.randint(1000,9999)}","GST_Rate":0})
        for cat in expense_cats:
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Expense","Category":cat,"Party":"Vendor","Amount":round(random.uniform(5000,80000),0),"Status":"Paid","Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_retail_data():
    random.seed(20); np.random.seed(20)
    customers = ["Wholesale Hub","Metro Traders","Quick Mart","Singh Distributors","Raj Superstore","City Bazaar","Fresh Mart","Daily Needs Co","Star Retail","Budget Store"]
    expense_cats = ["Inventory Purchase","Staff Wages","Rent","Electricity","Transport & Delivery","Marketing","Shrinkage/Loss","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        n = random.randint(30,60) if month.month in [10,11,12] else random.randint(15,30)
        for _ in range(n):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Sales","Category":random.choice(["FMCG","Electronics","Apparel","Home & Kitchen"]),"Party":random.choice(customers),"Amount":round(random.uniform(2000,120000),0),"Status":random.choice(["Paid","Paid","Paid","Overdue","Pending"]),"Invoice_No":f"RTL-{random.randint(1000,9999)}","GST_Rate":random.choice([5,12,18])})
        for cat in expense_cats:
            amt = round(random.uniform(10000,90000),0)
            if cat=="Inventory Purchase" and month.month in [9,10]: amt*=1.8
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Expense","Category":cat,"Party":"Vendor","Amount":round(amt,0),"Status":"Paid","Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

def generate_agency_data():
    random.seed(30); np.random.seed(30)
    clients = ["TechStart Pvt Ltd","Growfast Brands","UrbanEats Chain","BuildRight Infra","FinEdge Solutions","MegaMart Retail","HealthPlus Network","EduWorld Pvt Ltd","TravelLux India","AutoNext Motors"]
    expense_cats = ["Salaries","Software Subscriptions","Rent","Electricity","Freelancer Payments","Client Servicing","Marketing","GST Paid"]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        for _ in range(random.randint(8,18)):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Sales","Category":random.choice(["Retainer","Project Fee","Consulting","Performance Bonus"]),"Party":random.choice(clients),"Amount":round(random.uniform(25000,350000),0),"Status":random.choice(["Paid","Paid","Overdue","Pending"]),"Invoice_No":f"AGY-{random.randint(1000,9999)}","GST_Rate":18})
        for cat in expense_cats:
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Expense","Category":cat,"Party":"Vendor","Amount":round(random.uniform(15000,200000),0),"Status":"Paid","Invoice_No":f"EXP-{random.randint(1000,9999)}","GST_Rate":18})
    return make_df(records)

INDUSTRY_MAP = {
    "🍽️  Restaurant / Cafe": ("restaurant", generate_restaurant_data),
    "🏥  Clinic / Diagnostic Lab": ("clinic", generate_clinic_data),
    "🛒  Retail / Distribution": ("retail", generate_retail_data),
    "💼  Agency / Consulting": ("agency", generate_agency_data),
}

INDUSTRY_BENCHMARKS = {
    "restaurant": {"Food Cost %": (38, 28, "lower is better"), "Staff Cost %": (30, 25, "lower is better"), "Rent %": (10, 8, "lower is better"), "Net Margin %": (12, 18, "higher is better")},
    "clinic": {"Doctor Salary %": (45, 38, "lower is better"), "Lab Revenue Mix %": (25, 35, "higher is better"), "Overdue %": (8, 3, "lower is better"), "Net Margin %": (18, 25, "higher is better")},
    "retail": {"Inventory Cost %": (60, 50, "lower is better"), "Shrinkage %": (3, 1.5, "lower is better"), "Staff Cost %": (12, 10, "lower is better"), "Net Margin %": (10, 15, "higher is better")},
    "agency": {"Salary % of Revenue": (55, 42, "lower is better"), "Freelancer Cost %": (15, 10, "lower is better"), "Software Cost %": (8, 5, "lower is better"), "Net Margin %": (22, 30, "higher is better")},
}


# ── FILE PARSER ──────────────────────────────────────────────────────────────

def parse_uploaded_file(file):
    try:
        try:
            df = pd.read_csv(file) if file.name.lower().endswith(".csv") else pd.read_excel(file)
        except Exception:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin1") if file.name.lower().endswith(".csv") else pd.read_excel(file, header=1)

        df = df.dropna(how="all").dropna(axis=1, how="all")
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher date","txn date"]): col_map[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","net","inr","rs","rupee"]): col_map[col]="Amount"
            elif any(x in cl for x in ["type","txn type","transaction type","dr/cr","nature"]): col_map[col]="Type"
            elif any(x in cl for x in ["category","cat","head","narration","description","particulars","ledger","account"]): col_map[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","payee","client","supplier"]): col_map[col]="Party"
            elif any(x in cl for x in ["status","paid","payment status","cleared"]): col_map[col]="Status"
            elif any(x in cl for x in ["invoice","bill no","voucher","ref"]): col_map[col]="Invoice_No"
        df = df.rename(columns=col_map)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
            df = df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"] = df["Amount"].astype(str).str.replace(",","",regex=False).str.replace("(","−",regex=False).str.replace(")","",regex=False)
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"] = "Sales"
        if "Type" in df.columns:
            df["Type"] = df["Type"].astype(str).str.strip().str.title()
            df["Type"] = df["Type"].replace({"Dr":"Expense","Cr":"Sales","Debit":"Expense","Credit":"Sales","Out":"Expense","In":"Sales","Payment":"Expense","Receipt":"Sales","Purchase":"Expense","Sale":"Sales"})
            df.loc[~df["Type"].isin(["Sales","Expense"]), "Type"] = "Sales"
        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","—")]:
            if col not in df.columns: df[col] = default
        df = df.drop_duplicates()
        if "Month" not in df.columns and "Date" in df.columns:
            df["Month"] = df["Date"].dt.to_period("M").astype(str)
        mapped = [c for c in ["Date","Amount","Type","Category","Party","Status","Invoice_No"] if c in df.columns]
        confidence = min(60 + len(mapped)*5, 95)
        return df, True, f"Loaded {len(df)} transactions", confidence, mapped
    except Exception as e:
        return None, False, str(e), 0, []


# ── ANALYTICS ────────────────────────────────────────────────────────────────

def compute_health_score(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    scores = {}
    if margin>25: scores["Profit Margin"]=(95,"#c8ff57")
    elif margin>15: scores["Profit Margin"]=(78,"#c8ff57")
    elif margin>5: scores["Profit Margin"]=(55,"#ffb557")
    elif margin>0: scores["Profit Margin"]=(35,"#ffb557")
    else: scores["Profit Margin"]=(12,"#ff5e5e")
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    if len(sm)>=3:
        t = (sm.iloc[-1]-sm.iloc[-3])/max(sm.iloc[-3],1)*100
        if t>10: scores["Revenue Trend"]=(90,"#c8ff57")
        elif t>0: scores["Revenue Trend"]=(72,"#c8ff57")
        elif t>-10: scores["Revenue Trend"]=(45,"#ffb557")
        else: scores["Revenue Trend"]=(20,"#ff5e5e")
    else: scores["Revenue Trend"]=(60,"#ffb557")
    em = e.groupby("Month")["Amount"].sum()
    if len(em)>=3:
        cv = em.std()/max(em.mean(),1)
        if cv<0.1: scores["Expense Stability"]=(90,"#c8ff57")
        elif cv<0.2: scores["Expense Stability"]=(72,"#c8ff57")
        elif cv<0.35: scores["Expense Stability"]=(48,"#ffb557")
        else: scores["Expense Stability"]=(25,"#ff5e5e")
    else: scores["Expense Stability"]=(60,"#ffb557")
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    op = (overdue/rev*100) if rev>0 else 0
    if op<2: scores["Collections"]=(95,"#c8ff57")
    elif op<8: scores["Collections"]=(72,"#c8ff57")
    elif op<15: scores["Collections"]=(45,"#ffb557")
    else: scores["Collections"]=(20,"#ff5e5e")
    if len(s)>0:
        tc = s.groupby("Party")["Amount"].sum().max()
        conc = (tc/rev*100) if rev>0 else 0
        if conc<20: scores["Revenue Diversity"]=(90,"#c8ff57")
        elif conc<35: scores["Revenue Diversity"]=(70,"#c8ff57")
        elif conc<50: scores["Revenue Diversity"]=(45,"#ffb557")
        else: scores["Revenue Diversity"]=(20,"#ff5e5e")
    else: scores["Revenue Diversity"]=(50,"#ffb557")
    cr = (exp/rev*100) if rev>0 else 100
    if cr<60: scores["Cost Efficiency"]=(90,"#c8ff57")
    elif cr<75: scores["Cost Efficiency"]=(68,"#c8ff57")
    elif cr<90: scores["Cost Efficiency"]=(42,"#ffb557")
    else: scores["Cost Efficiency"]=(15,"#ff5e5e")
    overall = int(sum(v for v,_ in scores.values())/len(scores))
    color = "#c8ff57" if overall>=75 else "#ffb557" if overall>=50 else "#ff5e5e"
    return overall, color, scores

def get_top_3_problems(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev-exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    op = (overdue/rev*100) if rev>0 else 0
    te = e.groupby("Category")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "Expenses"
    top_exp_pct = (te.max()/exp*100) if exp>0 and len(te)>0 else 0
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    top_cust = tc.idxmax() if len(tc)>0 else "Top Customer"
    top_cust_pct = (tc.max()/rev*100) if rev>0 and len(tc)>0 else 0
    problems = []
    if margin<5: problems.append({"severity":"red","title":"Profit margin is critically thin","text":f"Your margin is only <strong>{margin:.1f}%</strong>. You're working hard but keeping very little.","action":f"Review <strong>{top_exp}</strong> first — even a 10% cut there improves profit immediately."})
    else: problems.append({"severity":"green","title":"Profitability is healthy","text":f"Margin is <strong>{margin:.1f}%</strong> — a solid base.","action":f"Protect this by keeping <strong>{top_exp}</strong> under control and growing repeat revenue."})
    if overdue>0:
        sev = "red" if op>10 else "amber"
        problems.append({"severity":sev,"title":"Cash is stuck in overdue invoices","text":f"<strong>{fmt_inr(overdue)}</strong> overdue — <strong>{op:.1f}%</strong> of your revenue.","action":"Follow up on collections this week. Recovering overdue money is the fastest cash flow improvement."})
    else: problems.append({"severity":"green","title":"Collections are clean","text":"No meaningful overdue invoices right now.","action":"Keep invoice follow-ups disciplined so this stays healthy."})
    if top_cust_pct>35: problems.append({"severity":"amber","title":"Too dependent on one customer","text":f"<strong>{top_cust}</strong> is <strong>{top_cust_pct:.1f}%</strong> of your revenue.","action":"Add 2–3 more active revenue sources this quarter to reduce concentration risk."})
    else: problems.append({"severity":"amber" if top_exp_pct>28 else "green","title":f"{top_exp} is your biggest cost leak","text":f"Accounts for <strong>{top_exp_pct:.1f}%</strong> of all expenses.","action":"Audit this category line by line — highest-impact place to improve profitability."})
    return problems[:3]

def get_this_week_actions(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "largest cost category"
    actions = []
    if overdue>0: actions.append(f"Follow up on <strong>{fmt_inr(overdue)}</strong> in overdue invoices — call top 3 overdue parties today.")
    actions.append(f"Review last 10 entries under <strong>{top_exp}</strong> and flag anything avoidable.")
    actions.append("Identify one recurring expense you can reduce, renegotiate, or cut this month.")
    actions.append("Check your top 3 customers — can any be upsold, renewed, or billed earlier?")
    actions.append("Spend 15 minutes checking whether this month's revenue has actually turned into cash.")
    if industry=="restaurant": actions.append("Audit food wastage, supplier pricing, and kitchen electricity usage.")
    elif industry=="clinic": actions.append("Check if consultations are converting into lab tests or higher-value services.")
    elif industry=="retail": actions.append("Identify slow-moving inventory and clear dead stock before reordering.")
    elif industry=="agency": actions.append("Review if team salaries and freelancer spend are aligned with actual billable work.")
    return actions[:5]

def get_profit_leaks(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    leaks = []
    if len(e)>0:
        for cat, amt in e.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3).items():
            pct = (amt/exp*100) if exp>0 else 0
            leaks.append({"title":cat,"sub":f"{fmt_inr(amt)} spent — {pct:.1f}% of all expenses. High-impact area to review."})
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    if overdue>0: leaks.append({"title":"Delayed collections","sub":f"{fmt_inr(overdue)} earned but not yet in your account."})
    if len(s)>0:
        tc = s.groupby("Party")["Amount"].sum()
        top_pct = (tc.max()/rev*100) if rev>0 else 0
        if top_pct>35: leaks.append({"title":"Customer concentration risk","sub":f"Top customer = {top_pct:.1f}% of revenue. Hidden business risk."})
    return leaks[:5]

def get_benchmarks(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    results = []
    benchmarks = INDUSTRY_BENCHMARKS.get(industry, {})
    for metric, (your_typical, industry_avg, direction) in benchmarks.items():
        if metric == "Net Margin %":
            yours = (profit/rev*100) if rev>0 else 0
        elif "%" in metric:
            cat_name = metric.replace(" %","").replace(" of Revenue","")
            cat_spend = e[e["Category"].str.contains(cat_name.split()[0], case=False, na=False)]["Amount"].sum() if len(e)>0 else 0
            yours = (cat_spend/rev*100) if rev>0 else your_typical
        else:
            yours = your_typical
        if direction == "lower is better": good = yours <= industry_avg
        else: good = yours >= industry_avg
        results.append({"metric":metric,"yours":yours,"benchmark":industry_avg,"good":good,"direction":direction})
    return results

def get_collections(df):
    if "Status" not in df.columns: return []
    overdue = df[(df["Type"]=="Sales") & (df["Status"]=="Overdue")].copy()
    if len(overdue)==0: return []
    by_party = overdue.groupby("Party").agg(Amount=("Amount","sum"), Count=("Amount","count"), LastDate=("Date","max")).reset_index()
    by_party = by_party.sort_values("Amount", ascending=False).head(8)
    result = []
    for _, row in by_party.iterrows():
        days = (datetime.now() - pd.Timestamp(row["LastDate"])).days if pd.notna(row["LastDate"]) else 0
        result.append({"party":row["Party"],"amount":row["Amount"],"count":int(row["Count"]),"days":days})
    return result

def detect_anomalies(df):
    alerts = []
    e = df[df["Type"]=="Expense"]
    for cat in e["Category"].unique():
        cat_df = e[e["Category"]==cat].groupby("Month")["Amount"].sum()
        if len(cat_df)<3: continue
        mean, std = cat_df.mean(), cat_df.std()
        if std==0: continue
        last_val = cat_df.iloc[-1]; z = (last_val-mean)/std
        if z>1.5: alerts.append(("danger",f"<strong>{cat}</strong>: <strong>{fmt_inr(last_val)}</strong> last month — {((last_val/mean-1)*100):.0f}% above average ({fmt_inr(mean)}/mo).",f"Check {cat} invoices immediately. Could be pricing error or one-off spike."))
        elif z>1.0: alerts.append(("warn",f"<strong>{cat}</strong> slightly elevated at <strong>{fmt_inr(last_val)}</strong> vs avg {fmt_inr(mean)}.","Monitor next month — investigate if it keeps rising."))
    sm = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum().sort_index()
    if len(sm)>=2:
        prev, last = sm.iloc[-2], sm.iloc[-1]
        drop = (prev-last)/prev*100 if prev>0 else 0
        if drop>20: alerts.append(("danger",f"Revenue dropped <strong>{drop:.0f}%</strong> last month ({fmt_inr(prev)} → {fmt_inr(last)}).","Urgent: identify if this is seasonal, customer loss, or collections delay. Check overdue invoices first."))
    return alerts

def gst_summary(df):
    s = df[df["Type"]=="Sales"].copy()
    total_sales = s["Amount"].sum()
    if "GST_Rate" in s.columns:
        s["GST_Amt"] = s.apply(lambda r: r["Amount"]*r["GST_Rate"]/(100+max(r["GST_Rate"],1)) if r.get("GST_Rate",0)>0 else 0, axis=1)
        out_gst = s["GST_Amt"].sum()
    else: out_gst = total_sales*0.18/1.18
    e = df[df["Type"]=="Expense"].copy()
    gst_paid = e[e["Category"]=="GST Paid"]["Amount"].sum()
    in_gst = gst_paid if gst_paid>0 else e["Amount"].sum()*0.05
    net = out_gst - in_gst
    return {"output_gst":out_gst,"input_gst":in_gst,"net_payable":max(net,0),"cgst":out_gst/2,"sgst":out_gst/2,"total_sales":total_sales}

def cash_flow_forecast(df, months_ahead=3):
    sm = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum().sort_index()
    em = df[df["Type"]=="Expense"].groupby("Month")["Amount"].sum().sort_index()
    ar = sm.tail(3).mean() if len(sm)>=3 else sm.mean()
    ae = em.tail(3).mean() if len(em)>=3 else em.mean()
    rt = (sm.iloc[-1]-sm.iloc[-3])/3 if len(sm)>=3 else 0
    et = (em.iloc[-1]-em.iloc[-3])/3 if len(em)>=3 else 0
    rows = []
    for i in range(1,months_ahead+1):
        lbl = (datetime.now()+timedelta(days=30*i)).strftime("%b %Y")
        pr = max(ar+rt*i,0); pe = max(ae+et*i,0)
        rows.append({"Month":lbl,"Projected Revenue":round(pr,0),"Projected Expenses":round(pe,0),"Projected Profit":round(pr-pe,0)})
    return pd.DataFrame(rows)

def generate_owner_summary(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "costs"
    top_exp_amt = te.max() if len(te)>0 else 0
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    top_cust = tc.idxmax() if len(tc)>0 else "your top customer"
    top_cust_amt = tc.max() if len(tc)>0 else 0
    opening = f"This business generated <strong>{fmt_inr(profit)}</strong> in profit on <strong>{fmt_inr(rev)}</strong> revenue" if profit>=0 else f"This business is running at a <strong>loss of {fmt_inr(abs(profit))}</strong> on <strong>{fmt_inr(rev)}</strong> revenue"
    return f"{opening}, with a <strong>{margin:.1f}% margin</strong>. Biggest cost: <strong>{top_exp}</strong> at <strong>{fmt_inr(top_exp_amt)}</strong>. Strongest revenue contributor: <strong>{top_cust}</strong> at <strong>{fmt_inr(top_cust_amt)}</strong>. Cash stuck in overdue invoices: <strong>{fmt_inr(overdue)}</strong>. The fastest way to improve this business right now is better collections and tighter control of {top_exp}."

def generate_whatsapp_summary(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "N/A"
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    top_cust = tc.idxmax() if len(tc)>0 else "N/A"
    return f"""*OpsClarity Business Summary*
━━━━━━━━━━━━━━━━━━
Revenue: {fmt_inr(rev)}
Expenses: {fmt_inr(exp)}
Net Profit: {fmt_inr(profit)} ({margin:.1f}% margin)
Overdue: {fmt_inr(overdue)}
━━━━━━━━━━━━━━━━━━
Top Cost: {top_exp}
Best Customer: {top_cust}
━━━━━━━━━━━━━━━━━━
_Generated by OpsClarity_"""

def generate_report_csv(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    eb = e.groupby("Category")["Amount"].sum().reset_index() if len(e)>0 else pd.DataFrame()
    if len(eb)>0: eb["Share %"] = (eb["Amount"]/exp*100).round(1)
    tc = s.groupby("Party")["Amount"].sum().reset_index().sort_values("Amount",ascending=False).head(5) if len(s)>0 else pd.DataFrame()
    out = io.StringIO()
    out.write(f"OpsClarity Business Report\nGenerated: {datetime.now().strftime('%d %b %Y %H:%M')}\n\n")
    out.write(f"SUMMARY\nRevenue,{fmt_inr(rev)}\nExpenses,{fmt_inr(exp)}\nProfit,{fmt_inr(profit)}\nMargin,{margin:.1f}%\nOverdue,{fmt_inr(overdue)}\n\n")
    if len(eb)>0: out.write("EXPENSE BREAKDOWN\n"); out.write(eb.to_csv(index=False)); out.write("\n")
    if len(tc)>0: out.write("TOP CUSTOMERS\n"); out.write(tc.to_csv(index=False)); out.write("\n")
    out.write("ALL TRANSACTIONS\n"); out.write(df.to_csv(index=False))
    return out.getvalue().encode()


# ── MONTH VS MONTH COMPARISON ─────────────────────────────────────────────────

def month_vs_month(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    em = e.groupby("Month")["Amount"].sum().sort_index()
    if len(sm) < 2: return None
    months = sorted(set(sm.index) | set(em.index))
    if len(months) < 2: return None
    cur_m, prev_m = months[-1], months[-2]
    cur_rev = sm.get(cur_m, 0); prev_rev = sm.get(prev_m, 0)
    cur_exp = em.get(cur_m, 0); prev_exp = em.get(prev_m, 0)
    cur_profit = cur_rev - cur_exp; prev_profit = prev_rev - prev_exp
    def pct_chg(cur, prev):
        if prev == 0: return 0
        return ((cur - prev) / prev) * 100
    return {
        "cur_month": cur_m, "prev_month": prev_m,
        "rev": (cur_rev, prev_rev, pct_chg(cur_rev, prev_rev)),
        "exp": (cur_exp, prev_exp, pct_chg(cur_exp, prev_exp)),
        "profit": (cur_profit, prev_profit, pct_chg(cur_profit, prev_profit)),
    }


# ── CASH RUNWAY WARNING ────────────────────────────────────────────────────────

def cash_runway_warning(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    em = e.groupby("Month")["Amount"].sum().sort_index()
    avg_monthly_rev = sm.tail(3).mean() if len(sm) >= 3 else sm.mean()
    avg_monthly_exp = em.tail(3).mean() if len(em) >= 3 else em.mean()
    rev_trend = (sm.iloc[-1] - sm.iloc[-3]) / 3 if len(sm) >= 3 else 0
    next_30_rev = max(avg_monthly_rev + rev_trend, 0)
    next_30_exp = avg_monthly_exp
    net_next_30 = next_30_rev - next_30_exp
    stress_level = "safe"
    if net_next_30 < 0: stress_level = "critical"
    elif net_next_30 < avg_monthly_exp * 0.1: stress_level = "warning"
    elif overdue > avg_monthly_rev * 0.15: stress_level = "warning"
    return {
        "next_30_rev": next_30_rev,
        "next_30_exp": next_30_exp,
        "net_next_30": net_next_30,
        "overdue_risk": overdue,
        "stress_level": stress_level,
        "avg_monthly_exp": avg_monthly_exp,
    }


# ── COLLECTIONS WHATSAPP MESSAGES ──────────────────────────────────────────────

def get_collection_wa_message(party, amount, days):
    if days > 60:
        return f"Dear {party}, this is an urgent reminder that your payment of {fmt_inr(amount)} has been pending for over {days} days. Please settle this at the earliest to avoid any disruption. Contact us immediately to resolve. Thank you."
    elif days > 30:
        return f"Hi {party}, a gentle reminder that {fmt_inr(amount)} is overdue on your account. We would appreciate your payment at the earliest convenience. Please let us know if there are any issues. Thank you."
    else:
        return f"Hi {party}, this is a quick reminder about the outstanding payment of {fmt_inr(amount)} on your account. Request you to clear this at your earliest. Thank you for your continued business!"


# ── PDF-STYLE HTML REPORT ──────────────────────────────────────────────────────

def generate_html_report(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overall, color, scores = compute_health_score(df)
    health_label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs Attention" if overall>=45 else "Critical"
    te = e.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index() if len(e)>0 else pd.DataFrame(columns=["Category","Amount"])
    tc = s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(5).reset_index() if len(s)>0 else pd.DataFrame(columns=["Party","Amount"])
    probs = get_top_3_problems(df, industry)
    actions = get_this_week_actions(df, industry)
    date_str = datetime.now().strftime("%d %B %Y")

    exp_rows = "".join([f"<tr><td>{row.Category}</td><td style=\"text-align:right\">{fmt_inr(row.Amount)}</td><td style=\"text-align:right\">{row.Amount/exp*100:.1f}%</td></tr>" for _, row in te.iterrows()]) if len(te)>0 else ""
    cust_rows = "".join([f"<tr><td>{row.Party}</td><td style=\"text-align:right\">{fmt_inr(row.Amount)}</td></tr>" for _, row in tc.iterrows()]) if len(tc)>0 else ""
    prob_html = "".join([f"<div style=\"margin-bottom:12px;padding:10px 12px;border-left:3px solid {'#c8ff57' if p['severity']=='green' else '#ffb557' if p['severity']=='amber' else '#ff5e5e'};background:#f9f9f9;\"><strong>{p['title']}</strong><br><span style=\"font-size:13px;color:#555;\">{p['text'].replace('<strong>','').replace('</strong>','')}</span></div>" for p in probs])
    act_html = "".join([f"<li style=\"margin-bottom:6px;font-size:13px;\">{a.replace('<strong>','').replace('</strong>','')}</li>" for a in actions])

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
body{{font-family:Arial,sans-serif;color:#1a1a2e;margin:0;padding:0;background:#fff;}}
.page{{max-width:800px;margin:0 auto;padding:40px;}}
.header{{border-bottom:3px solid #0a0a0f;padding-bottom:20px;margin-bottom:30px;display:flex;justify-content:space-between;align-items:flex-end;}}
.logo{{font-size:24px;font-weight:900;color:#0a0a0f;letter-spacing:-.02em;}}
.logo span{{color:#6ab04c;}}
.date{{font-size:13px;color:#888;}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:30px;}}
.kpi{{background:#f5f5f0;border-radius:10px;padding:14px 16px;}}
.kpi-label{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#888;font-weight:700;margin-bottom:6px;}}
.kpi-value{{font-size:1.6rem;font-weight:900;color:#1a1a2e;}}
.kpi-sub{{font-size:11px;color:#aaa;margin-top:3px;}}
.health-box{{background:#0a0a0f;color:#f4f1eb;border-radius:12px;padding:20px 24px;margin-bottom:30px;display:flex;align-items:center;gap:24px;}}
.health-num{{font-size:4rem;font-weight:900;color:#c8ff57;line-height:1;}}
.health-label{{font-size:1.1rem;color:#c8ff57;margin-bottom:4px;}}
.health-sub{{font-size:13px;color:#9494a8;}}
.section{{margin-bottom:28px;}}
.section-title{{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:#888;font-weight:700;margin-bottom:14px;border-bottom:1px solid #eee;padding-bottom:6px;}}
table{{width:100%;border-collapse:collapse;font-size:13px;}}
th{{text-align:left;padding:8px 10px;background:#f5f5f0;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#888;}}
td{{padding:8px 10px;border-bottom:1px solid #f0f0f0;}}
.summary-box{{background:#f0fff4;border:1px solid #c8ff57;border-radius:10px;padding:16px 18px;margin-bottom:28px;font-size:14px;line-height:1.8;color:#1a1a2e;}}
.footer{{margin-top:40px;padding-top:16px;border-top:1px solid #eee;font-size:11px;color:#bbb;display:flex;justify-content:space-between;}}
</style></head><body><div class="page">
<div class="header">
  <div><div class="logo">Ops<span>Clarity</span></div><div style="font-size:12px;color:#888;margin-top:4px;">Business Intelligence Report</div></div>
  <div class="date">Generated: {date_str}</div>
</div>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Revenue</div><div class="kpi-value">{fmt_inr(rev)}</div><div class="kpi-sub">Total earned</div></div>
  <div class="kpi"><div class="kpi-label">Expenses</div><div class="kpi-value">{fmt_inr(exp)}</div><div class="kpi-sub">Total spent</div></div>
  <div class="kpi"><div class="kpi-label">Net Profit</div><div class="kpi-value">{fmt_inr(abs(profit))}</div><div class="kpi-sub">{'Profit' if profit>=0 else 'Loss'} · {abs(margin):.1f}%</div></div>
  <div class="kpi"><div class="kpi-label">Overdue</div><div class="kpi-value">{fmt_inr(overdue)}</div><div class="kpi-sub">Uncollected cash</div></div>
</div>
<div class="health-box">
  <div class="health-num">{overall}</div>
  <div><div class="health-label">Business Health Score — {health_label}</div><div class="health-sub">Based on profit margin, revenue trend, expense stability, collections, diversity &amp; cost efficiency.</div></div>
</div>
<div class="section"><div class="section-title">Business Summary</div>
<div class="summary-box">{generate_owner_summary(df, industry).replace('<strong>','<b>').replace('</strong>','</b>')}</div></div>
<div class="section"><div class="section-title">Top 3 Problems</div>{prob_html}</div>
<div class="section"><div class="section-title">Actions This Week</div><ul style="padding-left:18px;">{act_html}</ul></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
<div class="section"><div class="section-title">Expense Breakdown</div>
<table><tr><th>Category</th><th style="text-align:right">Amount</th><th style="text-align:right">Share</th></tr>{exp_rows}</table></div>
<div class="section"><div class="section-title">Top Customers</div>
<table><tr><th>Customer</th><th style="text-align:right">Revenue</th></tr>{cust_rows}</table></div>
</div>
<div class="footer"><div>OpsClarity — SME Intelligence</div><div>Confidential Business Report · {date_str}</div></div>
</div></body></html>"""
    return html.encode()

def ask_ai(question, df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = {k:fmt_inr(v) for k,v in e.groupby("Category")["Amount"].sum().to_dict().items()} if len(e)>0 else {}
    tc = {k:fmt_inr(v) for k,v in s.groupby("Party")["Amount"].sum().nlargest(5).to_dict().items()} if len(s)>0 else {}
    context = f"""You are a sharp Indian SME financial advisor. Be direct, specific, use numbers, give actionable advice. Max 150 words. No generic disclaimers.
Business: Revenue={fmt_inr(rev)}, Expenses={fmt_inr(exp)}, Profit={fmt_inr(profit)} ({margin:.1f}% margin), Overdue={fmt_inr(overdue)}
Expenses: {json.dumps(te)}
Top customers: {json.dumps(tc)}
Question: {question}"""
    import urllib.request
    api_key = st.secrets.get("ANTHROPIC_API_KEY","")
    if not api_key:
        return "Add ANTHROPIC_API_KEY to Streamlit secrets (Settings → Secrets) to enable AI Q&A."
    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":300,"messages":[{"role":"user","content":context}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=payload,
        headers={"Content-Type":"application/json","anthropic-version":"2023-06-01","x-api-key":api_key},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=15) as resp:
            return json.loads(resp.read())["content"][0]["text"]
    except Exception as e:
        return f"AI Q&A error: {str(e)}"


# ── SESSION STATE ─────────────────────────────────────────────────────────────

for k, v in [("df",None),("industry","restaurant"),("unlocked",False),("chat_history",[]),("confidence",95),("mapped_cols",[])]:
    if k not in st.session_state: st.session_state[k] = v


# ── HERO ─────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-badge">◈ OpsClarity — SME Intelligence</div>
    <h1 class="hero-title">Know where your business<br>is <span>leaking money</span> — in 30 seconds.</h1>
    <p class="hero-sub">Upload your Excel, Tally export, or bank statement. OpsClarity gives you instant P&L, health score, overdue alerts, GST summary, and plain-English actions. Works for restaurants, clinics, retail, agencies — any Indian SME.</p>
</div>
""", unsafe_allow_html=True)


# ── UPLOAD ────────────────────────────────────────────────────────────────────

st.markdown("<div class='upload-wrap'>", unsafe_allow_html=True)
col1, col2 = st.columns([1.6, 1])
with col1:
    uploaded_file = st.file_uploader("Drop your file — CSV, Excel, Tally export, bank statement", type=["csv","xlsx","xls"])
    st.markdown("<div class='mini-note'>No cleanup needed — works with Tally exports, bank CSVs, Excel sheets. <a href='#' style='color:#c8ff57;text-decoration:none;'>How to export from Tally ↗</a></div>", unsafe_allow_html=True)
with col2:
    industry_name = st.selectbox("Industry", list(INDUSTRY_MAP.keys()), label_visibility="collapsed")
    if st.button(f"Load sample data", use_container_width=True):
        ind_key, gen_fn = INDUSTRY_MAP[industry_name]
        st.session_state.df = gen_fn()
        st.session_state.industry = ind_key
        st.session_state.confidence = 95
        st.session_state.mapped_cols = ["Date","Amount","Type","Category","Party","Status","Invoice_No"]
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df_up, ok, msg, conf, mapped = parse_uploaded_file(uploaded_file)
    if ok:
        st.session_state.df = df_up; st.session_state.industry = "restaurant"
        st.session_state.confidence = conf; st.session_state.mapped_cols = mapped
        st.success(msg)
    else:
        st.error(f"Could not parse: {msg}. Try saving as CSV and re-uploading.")


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

if st.session_state.df is not None:
    df = st.session_state.df.copy()
    industry = st.session_state.industry

    # Date filter
    if "Date" in df.columns and df["Date"].notna().any():
        min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
        fc1,fc2,fc3 = st.columns([1,1,2])
        with fc1: start_d = st.date_input("From", value=min_d, min_value=min_d, max_value=max_d)
        with fc2: end_d = st.date_input("To", value=max_d, min_value=min_d, max_value=max_d)
        with fc3: st.markdown(f"<div style='padding-top:1.8rem;font-size:13px;color:#5a5a6d;'>{len(df)} transactions · {start_d.strftime('%d %b %Y')} to {end_d.strftime('%d %b %Y')}</div>", unsafe_allow_html=True)
        df = df[(df["Date"].dt.date>=start_d)&(df["Date"].dt.date<=end_d)]

    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev-exp; margin = (profit/rev*100) if rev>0 else 0
    overdue_amt = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0

    # ── KPI CARDS ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green"><div class="metric-label">Revenue</div><div class="metric-value">{fmt_inr(rev)}</div><div class="metric-sub">Total earned</div></div>
        <div class="metric-card red"><div class="metric-label">Expenses</div><div class="metric-value">{fmt_inr(exp)}</div><div class="metric-sub">Total spent</div></div>
        <div class="metric-card {'green' if profit>=0 else 'red'}"><div class="metric-label">Net Profit</div><div class="metric-value">{fmt_inr(abs(profit))}</div><div class="metric-sub">{'Profit' if profit>=0 else 'Loss'} · {abs(margin):.1f}% margin</div></div>
        <div class="metric-card amber"><div class="metric-label">Overdue</div><div class="metric-value">{fmt_inr(overdue_amt)}</div><div class="metric-sub">Cash not yet collected</div></div>
    </div>""", unsafe_allow_html=True)

    # ── MONTH VS MONTH ───────────────────────────────────────────────────────────
    mom = month_vs_month(df)
    if mom:
        st.markdown("<div class='section-title'>◈ This month vs last month</div>", unsafe_allow_html=True)
        m1,m2,m3 = st.columns(3)
        def delta_color(pct, higher_better=True):
            good = pct > 0 if higher_better else pct < 0
            return "#c8ff57" if good else "#ff5e5e"
        def delta_arrow(pct): return "▲" if pct > 0 else "▼"
        cur_r, prev_r, pct_r = mom["rev"]
        cur_e, prev_e, pct_e = mom["exp"]
        cur_p, prev_p, pct_p = mom["profit"]
        m1.markdown(f"""<div class="metric-card blue"><div class="metric-label">Revenue — {mom['cur_month']}</div><div class="metric-value">{fmt_inr(cur_r)}</div><div class="metric-sub" style="color:{delta_color(pct_r)}">{delta_arrow(pct_r)} {abs(pct_r):.1f}% vs {mom['prev_month']} ({fmt_inr(prev_r)})</div></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="metric-card amber"><div class="metric-label">Expenses — {mom['cur_month']}</div><div class="metric-value">{fmt_inr(cur_e)}</div><div class="metric-sub" style="color:{delta_color(pct_e, higher_better=False)}">{delta_arrow(pct_e)} {abs(pct_e):.1f}% vs {mom['prev_month']} ({fmt_inr(prev_e)})</div></div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="metric-card {'green' if cur_p>=0 else 'red'}"><div class="metric-label">Profit — {mom['cur_month']}</div><div class="metric-value">{fmt_inr(abs(cur_p))}</div><div class="metric-sub" style="color:{delta_color(pct_p)}">{delta_arrow(pct_p)} {abs(pct_p):.1f}% vs {mom['prev_month']} ({fmt_inr(abs(prev_p))})</div></div>""", unsafe_allow_html=True)

    # ── CASH RUNWAY WARNING ───────────────────────────────────────────────────────
    runway = cash_runway_warning(df)
    if runway["stress_level"] == "critical":
        st.error(f"🚨 **Cash flow warning:** Projected loss of **{fmt_inr(abs(runway['net_next_30']))}** next month based on current trends. Immediate action needed — review expenses and chase collections.")
    elif runway["stress_level"] == "warning":
        st.warning(f"⚠️ **Cash flow caution:** Next 30 days look tight — projected net: **{fmt_inr(runway['net_next_30'])}**. You have **{fmt_inr(runway['overdue_risk'])}** in overdue invoices that could ease this if collected.")
    else:
        st.success(f"✅ **Cash flow looks healthy** — projected next month surplus: **{fmt_inr(runway['net_next_30'])}**.")

        # ── HEALTH SCORE ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>◈ Business Health Score</div>", unsafe_allow_html=True)
    overall, color, scores = compute_health_score(df)
    label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs attention" if overall>=45 else "Critical"
    score_html = f"""<div class="health-wrap"><div style="display:flex;align-items:baseline;gap:12px;"><div class="health-score" style="color:{color}">{overall}</div><div style="font-size:1.05rem;color:#7f7f92;">/ 100 — <span style="color:{color}">{label}</span></div></div><div class="health-grid">"""
    for name,(sc,cl) in scores.items():
        score_html += f'<div class="health-item"><div class="health-label">{name}</div><div class="health-bar"><div class="health-fill" style="width:{sc}%;background:{cl};"></div></div><div class="health-score-small">{sc}/100</div></div>'
    score_html += "</div></div>"
    st.markdown(score_html, unsafe_allow_html=True)

    # ── OWNER SUMMARY ────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>◈ Owner Summary</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="owner-summary"><div class="owner-summary-label">Plain-English business snapshot</div><div class="owner-summary-text">{generate_owner_summary(df,industry)}</div></div>""", unsafe_allow_html=True)

    # ── TOP 3 PROBLEMS ───────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>◈ Top 3 problems right now</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Where this business needs attention first.</div>", unsafe_allow_html=True)
    probs = get_top_3_problems(df, industry)
    html = "<div class='problem-grid'>"
    for p in probs:
        html += f"""<div class="problem-card"><div class="problem-tag {p['severity']}">{p['severity'].upper()}</div><div class="problem-title">{p['title']}</div><div class="problem-text">{p['text']}</div><div class="problem-action"><strong>Action:</strong> {p['action']}</div></div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    # ── ACTIONS + LEAKS ──────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>◈ What to do this week</div>", unsafe_allow_html=True)
    colA, colB = st.columns([1.2, 0.8])
    with colA:
        st.markdown('<div class="panel"><div class="panel-title">Recommended actions</div>', unsafe_allow_html=True)
        for i, action in enumerate(get_this_week_actions(df, industry), 1):
            st.markdown(f"<p><strong>{i}.</strong> {action}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="panel"><div class="panel-title">Profit leak detector</div>', unsafe_allow_html=True)
        for leak in get_profit_leaks(df, industry):
            st.markdown(f'<div class="leak-item"><div class="leak-title">{leak["title"]}</div><div class="leak-sub">{leak["sub"]}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ANOMALY ALERTS ───────────────────────────────────────────────────────
    alerts = detect_anomalies(df)
    if alerts:
        st.markdown("<div class='section-title'>⚠️ Anomaly Alerts</div>", unsafe_allow_html=True)
        for level, text, action in alerts:
            st.markdown(f'<div class="alert-card {level}"><div class="alert-text">{text}</div><div class="alert-action"><strong>Action:</strong> {action}</div></div>', unsafe_allow_html=True)

    # ── TRUST LAYER ──────────────────────────────────────────────────────────
    conf = st.session_state.confidence
    mapped = st.session_state.mapped_cols
    st.markdown(f"""<div class="trust-box"><div class="trust-title">Data confidence</div><div class="trust-text">Parsed with <strong>{conf}%</strong> confidence. Detected fields: <strong>{", ".join(mapped) if mapped else "None"}</strong>. If any numbers look wrong, download the raw CSV and check the source data.</div></div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
        "📈 Revenue & Expenses","💸 Expense Breakdown","🏆 Top Customers",
        "📊 Monthly Profit","🏅 Benchmarks","🧾 GST","🔮 Forecast","📋 Collections & Invoices"])

    with tab1:
        st.markdown("<div class='section-title'>Revenue vs Expenses trend</div>", unsafe_allow_html=True)
        sm = s.groupby("Month")["Amount"].sum(); em = e.groupby("Month")["Amount"].sum()
        st.line_chart(pd.DataFrame({"Revenue":sm,"Expenses":em}).fillna(0).sort_index(), use_container_width=True)

    with tab2:
        ca,cb = st.columns([1,1])
        with ca:
            st.markdown("<div class='section-title'>Where money is going</div>", unsafe_allow_html=True)
            if len(e)>0: st.bar_chart(e.groupby("Category")["Amount"].sum().sort_values(ascending=False), use_container_width=True)
        with cb:
            st.markdown("<div class='section-title'>Breakdown</div>", unsafe_allow_html=True)
            if len(e)>0:
                et = e.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount",ascending=False)
                et["Share %"] = (et["Amount"]/et["Amount"].sum()*100).round(1)
                et["Amount"] = et["Amount"].apply(fmt_inr)
                st.dataframe(et[["Category","Amount","Share %"]], hide_index=True, use_container_width=True)

    with tab3:
        st.markdown("<div class='section-title'>Top customers by revenue</div>", unsafe_allow_html=True)
        if len(s)>0: st.bar_chart(s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(8), use_container_width=True)

    with tab4:
        st.markdown("<div class='section-title'>Monthly profit / loss</div>", unsafe_allow_html=True)
        sm2 = s.groupby("Month")["Amount"].sum(); em2 = e.groupby("Month")["Amount"].sum()
        st.bar_chart(pd.DataFrame({"Profit":(sm2-em2).fillna(0).sort_index()}), use_container_width=True)

    with tab5:
        st.markdown("<div class='section-title'>Industry Benchmarks</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-sub'>How your numbers compare to typical {industry} businesses in India.</div>", unsafe_allow_html=True)
        benchmarks = get_benchmarks(df, industry)
        bc1, bc2 = st.columns(2)
        for i, b in enumerate(benchmarks):
            col = bc1 if i%2==0 else bc2
            bar_color = "#c8ff57" if b["good"] else "#ff5e5e"
            bar_pct = min(b["yours"]/max(b["benchmark"]*2,1)*100, 100)
            with col:
                st.markdown(f"""
                <div class="bench-card">
                    <div class="bench-label">{b['metric']}</div>
                    <div class="bench-row">
                        <div><div class="bench-yours" style="color:{bar_color}">{b['yours']:.1f}%</div></div>
                        <div style="text-align:right"><div class="bench-avg">Industry avg: {b['benchmark']}%</div><div style="font-size:11px;color:{'#c8ff57' if b['good'] else '#ff7c7c'};margin-top:2px;">{'✓ Good' if b['good'] else '⚠ Needs work'}</div></div>
                    </div>
                    <div class="bench-bar-wrap"><div class="bench-bar-fill" style="width:{bar_pct}%;background:{bar_color};"></div></div>
                </div>
                """, unsafe_allow_html=True)

    with tab6:
        st.markdown("<div class='section-title'>GST Summary</div>", unsafe_allow_html=True)
        gst = gst_summary(df)
        g1,g2,g3,g4 = st.columns(4)
        g1.metric("Output GST", fmt_inr(gst["output_gst"]))
        g2.metric("Input GST Credit", fmt_inr(gst["input_gst"]))
        g3.metric("Net GST Payable", fmt_inr(gst["net_payable"]))
        g4.metric("Taxable Sales", fmt_inr(gst["total_sales"]))
        gc1,gc2 = st.columns(2)
        gc1.metric("CGST (50%)", fmt_inr(gst["cgst"]))
        gc2.metric("SGST (50%)", fmt_inr(gst["sgst"]))
        st.info("Estimates only. Always verify with your CA before filing.")

    with tab7:
        st.markdown("<div class='section-title'>Cash Flow Forecast</div>", unsafe_allow_html=True)
        ma = st.slider("Months ahead", 1, 6, 3)
        fdf = cash_flow_forecast(df, ma)
        st.line_chart(fdf.set_index("Month")[["Projected Revenue","Projected Expenses"]], use_container_width=True)
        disp = fdf.copy()
        for c in ["Projected Revenue","Projected Expenses","Projected Profit"]: disp[c]=disp[c].apply(fmt_inr)
        st.dataframe(disp, hide_index=True, use_container_width=True)
        avg_p = (fdf["Projected Revenue"]-fdf["Projected Expenses"]).mean()
        if avg_p>0: st.success(f"Forecast looks healthy — avg projected profit of {fmt_inr(avg_p)}/month.")
        else: st.warning(f"Projected losses ahead. Avg loss: {fmt_inr(abs(avg_p))}/month. Take action now.")

    with tab8:
        st.markdown("<div class='section-title'>Collections Recovery</div>", unsafe_allow_html=True)
        collections = get_collections(df)
        if collections:
            total_overdue = sum(c["amount"] for c in collections)
            st.markdown(f"<div class='section-sub'><strong style='color:#ff7c7c;'>{fmt_inr(total_overdue)}</strong> owed across {len(collections)} parties. Prioritised by amount.</div>", unsafe_allow_html=True)
            for c in collections:
                wa_msg = get_collection_wa_message(c["party"], c["amount"], c["days"])
                st.markdown(f"""
                <div class="collection-item">
                    <div><div class="collection-party">{c['party']}</div><div class="collection-days">{c['count']} invoice(s) · {c['days']} days overdue</div></div>
                    <div class="collection-amt">{fmt_inr(c['amount'])}</div>
                </div>""", unsafe_allow_html=True)
                with st.expander(f"📱 WhatsApp reminder for {c['party']}"):
                    st.text_area("Copy & send on WhatsApp:", value=wa_msg, height=100, key=f"wa_{c['party']}", label_visibility="collapsed")
        else:
            st.success("No overdue invoices — collections are clean!")
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Invoice Tracker</div>", unsafe_allow_html=True)
        if "Status" in df.columns:
            cols = ["Date","Party","Amount","Status"]
            if "Invoice_No" in df.columns: cols = ["Date","Invoice_No"]+cols[1:]
            inv = df[df["Type"]=="Sales"][cols].copy().sort_values("Status").head(25)
            sf = st.selectbox("Filter", ["All","Overdue","Pending","Paid"])
            if sf!="All": inv = inv[inv["Status"]==sf]
            st.dataframe(inv.assign(Amount=inv["Amount"].apply(fmt_inr)), hide_index=True, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── AI Q&A ────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🤖 Ask your data anything</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>\"Why did profit drop?\", \"Which expense should I cut first?\", \"How do I improve my margin?\"</div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if question := st.chat_input("Ask about your business..."):
        st.session_state.chat_history.append({"role":"user","content":question})
        with st.chat_message("user"): st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Analysing..."): answer = ask_ai(question, df)
            st.write(answer)
            st.session_state.chat_history.append({"role":"assistant","content":answer})

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── EXPORTS ──────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📤 Export</div>", unsafe_allow_html=True)
    ex1,ex2,ex3,ex4 = st.columns(4)
    with ex1:
        st.markdown("**📄 Report for CA**")
        st.download_button("⬇ Download CSV Report", data=generate_report_csv(df), file_name=f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    with ex2:
        st.markdown("**🌐 HTML Report**")
        st.download_button("⬇ Download HTML Report", data=generate_html_report(df, industry), file_name=f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
    with ex3:
        st.markdown("**📱 WhatsApp Summary**")
        st.text_area("Copy & send:", value=generate_whatsapp_summary(df), height=130, label_visibility="collapsed")
    with ex4:
        st.markdown("**📊 Raw Transactions**")
        st.download_button("⬇ Download All Data", data=df.to_csv(index=False).encode(), file_name=f"OpsClarity_Data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

    # ── PAYWALL ──────────────────────────────────────────────────────────────
    if not st.session_state.unlocked:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="paywall">
        <div class="paywall-title">You've seen what clarity feels like.</div>
        <div class="paywall-sub">Unlock monthly auto-reports, AI advisor, GST filing prep, benchmarks vs industry, and priority WhatsApp support.</div>
        <div class="price-tag">₹2,999 <span>/ month</span></div>
        <div style="margin-top:.5rem;font-size:12px;color:#3a3a4a;">Cancel anytime. No contracts. Less than ₹100/day.</div>
        </div>""", unsafe_allow_html=True)
        _,cp,_ = st.columns([1,1,1])
        with cp:
            if st.button("◈  Unlock full access — ₹2,999/mo", use_container_width=True):
                st.session_state.unlocked = True
                st.success("Payment integration coming soon! Add your Razorpay key in Streamlit secrets.")

else:
    st.markdown("""
    <div class="divider"></div>
    <div class="problem-grid">
        <div class="problem-card"><div class="problem-tag green">INSTANT</div><div class="problem-title">P&L in 30 seconds</div><div class="problem-text">Upload any messy file. See revenue, expenses, profit, and health score immediately.</div></div>
        <div class="problem-card"><div class="problem-tag amber">SMART</div><div class="problem-title">Not just charts — actions</div><div class="problem-text">OpsClarity tells you what's wrong and exactly what to do about it.</div></div>
        <div class="problem-card"><div class="problem-tag red">REAL</div><div class="problem-title">Built for actual SME pain</div><div class="problem-text">Profit leaks, overdue cash, rising costs, benchmarks, GST — all in one place.</div></div>
    </div>""", unsafe_allow_html=True)
