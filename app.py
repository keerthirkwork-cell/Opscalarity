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
.tally-guide{background:rgba(200,255,87,.04);border:1px solid rgba(200,255,87,.15);border-radius:14px;padding:1rem 1.3rem;margin-top:1rem;}
.tally-guide-title{font-size:12px;font-weight:700;color:#c8ff57;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;}
.tally-guide-step{font-size:13px;color:#9494a8;line-height:1.8;padding-left:4px;}
.tally-guide-step strong{color:#f4f1eb;}
.mini-note{text-align:center;color:#505062;font-size:12px;margin-top:8px;}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin:2rem 0;}
.section-title{font-family:'DM Serif Display',serif;font-size:1.65rem;color:#f4f1eb;margin:2.4rem 0 .5rem;letter-spacing:-.02em;}
.section-sub{color:#7f7f92;font-size:14px;margin-bottom:1rem;}

.mode-toggle{display:flex;gap:8px;margin:1rem 0 1.5rem;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:5px;width:fit-content;}
.mode-btn{padding:8px 20px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;}
.mode-btn.active{background:rgba(200,255,87,.12);color:#c8ff57;}
.mode-btn.inactive{color:#5a5a6d;}

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

/* CA mode specific */
.ca-summary{background:rgba(87,184,255,.04);border:1px solid rgba(87,184,255,.15);border-radius:20px;padding:1.6rem 1.8rem;margin-top:1rem;}
.ca-summary-label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#57b8ff;font-weight:700;margin-bottom:10px;}
.ca-summary-text{color:#c8d8e8;font-size:.95rem;line-height:2;}
.ca-summary-text strong{color:#57b8ff;}
.ca-flag{display:inline-block;background:rgba(255,181,87,.1);border:1px solid rgba(255,181,87,.25);color:#ffb557;font-size:11px;font-weight:700;padding:3px 10px;border-radius:6px;margin:2px 3px;}
.ca-flag.red{background:rgba(255,87,87,.1);border-color:rgba(255,87,87,.25);color:#ff7c7c;}
.ca-flag.green{background:rgba(200,255,87,.08);border-color:rgba(200,255,87,.2);color:#c8ff57;}
.drill-box{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.8rem 1rem;margin-top:8px;font-size:12px;color:#6b6b7a;}
.drill-box strong{color:#9494a8;}

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

/* GST warning box */
.gst-disclaimer{background:rgba(255,181,87,.06);border:1px solid rgba(255,181,87,.2);border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.2rem;}
.gst-disclaimer-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#ffb557;margin-bottom:6px;}
.gst-disclaimer-text{font-size:13px;color:#b8a88a;line-height:1.7;}

.paywall{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1px solid rgba(200,255,87,.2);border-radius:20px;padding:3rem;text-align:center;margin:2rem 0;}
.paywall-title{font-family:'DM Serif Display',serif;font-size:2rem;color:#f4f1eb;margin-bottom:.75rem;}
.paywall-sub{color:#6b6b7a;font-size:14px;margin-bottom:2rem;font-weight:300;}
.price-tag{font-family:'DM Serif Display',serif;font-size:3rem;color:#c8ff57;line-height:1;}
.price-tag span{font-size:1.2rem;color:#6b6b7a;font-family:'DM Sans',sans-serif;font-weight:300;}

/* CA report styles */
.ca-report-section{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem;}
.ca-report-title{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#57b8ff;font-weight:700;margin-bottom:10px;}
.ca-table-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:13px;}
.ca-table-row:last-child{border-bottom:none;}
.ca-table-label{color:#7a7a8a;}
.ca-table-value{color:#f4f1eb;font-weight:600;}

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
    if margin<5: problems.append({"severity":"red","title":"Profit margin is critically thin","text":f"Your margin is only <strong>{margin:.1f}%</strong>. You're working hard but keeping very little.","action":f"Review <strong>{top_exp}</strong> first — even a 10% cut there improves profit immediately.","drill_type":"margin","drill_category":top_exp})
    else: problems.append({"severity":"green","title":"Profitability is healthy","text":f"Margin is <strong>{margin:.1f}%</strong> — a solid base.","action":f"Protect this by keeping <strong>{top_exp}</strong> under control and growing repeat revenue.","drill_type":"margin","drill_category":top_exp})
    if overdue>0:
        sev = "red" if op>10 else "amber"
        problems.append({"severity":sev,"title":"Cash is stuck in overdue invoices","text":f"<strong>{fmt_inr(overdue)}</strong> overdue — <strong>{op:.1f}%</strong> of your revenue.","action":"Follow up on collections this week. Recovering overdue money is the fastest cash flow improvement.","drill_type":"overdue","drill_category":None})
    else: problems.append({"severity":"green","title":"Collections are clean","text":"No meaningful overdue invoices right now.","action":"Keep invoice follow-ups disciplined so this stays healthy.","drill_type":"overdue","drill_category":None})
    if top_cust_pct>35: problems.append({"severity":"amber","title":"Too dependent on one customer","text":f"<strong>{top_cust}</strong> is <strong>{top_cust_pct:.1f}%</strong> of your revenue.","action":"Add 2–3 more active revenue sources this quarter to reduce concentration risk.","drill_type":"concentration","drill_category":top_cust})
    else: problems.append({"severity":"amber" if top_exp_pct>28 else "green","title":f"{top_exp} is your biggest cost","text":f"Accounts for <strong>{top_exp_pct:.1f}%</strong> of all expenses.","action":"Audit this category line by line — highest-impact place to improve profitability.","drill_type":"expense_category","drill_category":top_exp})
    return problems[:3]

def get_drill_transactions(df, drill_type, drill_category, limit=10):
    """Return the transactions that back up a specific insight."""
    if drill_type == "overdue":
        result = df[(df["Type"]=="Sales") & (df["Status"]=="Overdue")].copy()
    elif drill_type == "expense_category" and drill_category:
        result = df[(df["Type"]=="Expense") & (df["Category"]==drill_category)].copy()
    elif drill_type == "concentration" and drill_category:
        result = df[(df["Type"]=="Sales") & (df["Party"]==drill_category)].copy()
    elif drill_type == "margin":
        result = df[df["Type"]=="Expense"].copy().sort_values("Amount", ascending=False)
    else:
        return pd.DataFrame()
    cols = [c for c in ["Date","Invoice_No","Party","Category","Amount","Status"] if c in result.columns]
    result = result[cols].sort_values("Date", ascending=False).head(limit)
    result["Amount"] = result["Amount"].apply(fmt_inr)
    return result

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
        if z>1.5: alerts.append(("danger",cat,f"<strong>{cat}</strong>: <strong>{fmt_inr(last_val)}</strong> last month — {((last_val/mean-1)*100):.0f}% above average ({fmt_inr(mean)}/mo).",f"Check {cat} invoices immediately. Could be pricing error or one-off spike."))
        elif z>1.0: alerts.append(("warn",cat,f"<strong>{cat}</strong> slightly elevated at <strong>{fmt_inr(last_val)}</strong> vs avg {fmt_inr(mean)}.","Monitor next month — investigate if it keeps rising."))
    sm = df[df["Type"]=="Sales"].groupby("Month")["Amount"].sum().sort_index()
    if len(sm)>=2:
        prev, last = sm.iloc[-2], sm.iloc[-1]
        drop = (prev-last)/prev*100 if prev>0 else 0
        if drop>20: alerts.append(("danger","revenue_drop",f"Revenue dropped <strong>{drop:.0f}%</strong> last month ({fmt_inr(prev)} → {fmt_inr(last)}).","Urgent: identify if this is seasonal, customer loss, or collections delay. Check overdue invoices first."))
    return alerts

def gst_summary(df):
    """
    GST computation — management estimates only.
    Actual filing must be done by a qualified CA using verified data.
    Assumptions:
      - If GST_Rate tagged: extract GST from gross amount (amount * rate / (100 + rate))
      - If not tagged: conservative flat 5% estimate on sales
      - ITC: uses 'GST Paid' expense category if present, else 5% flat on expenses
    """
    s = df[df["Type"]=="Sales"].copy()
    total_sales = s["Amount"].sum()

    # Output GST — tagged rates preferred
    if "GST_Rate" in s.columns:
        s["GST_Amt"] = s.apply(
            lambda r: r["Amount"] * r["GST_Rate"] / (100 + max(r["GST_Rate"], 1))
            if pd.notna(r.get("GST_Rate")) and r.get("GST_Rate", 0) > 0 else 0,
            axis=1
        )
        out_gst = s["GST_Amt"].sum()
        rate_coverage = (s["GST_Rate"] > 0).mean()
    else:
        # No rates — use conservative 5% estimate
        out_gst = total_sales * 0.05
        rate_coverage = 0.0

    # Input GST (ITC)
    e = df[df["Type"]=="Expense"].copy()
    gst_paid_explicit = e[e["Category"]=="GST Paid"]["Amount"].sum() if len(e) > 0 else 0
    if gst_paid_explicit > 0:
        in_gst = gst_paid_explicit
        itc_source = "tagged"
    else:
        # Estimate: 18% GST on non-salary expenses (conservative)
        eligible_exp = e[~e["Category"].str.lower().str.contains("salary|wages|rent", na=False)]["Amount"].sum() if len(e) > 0 else 0
        in_gst = eligible_exp * 0.18 / 1.18
        itc_source = "estimated"

    net = out_gst - in_gst
    return {
        "output_gst": out_gst,
        "input_gst": in_gst,
        "net_payable": max(net, 0),
        "cgst": out_gst / 2,
        "sgst": out_gst / 2,
        "total_sales": total_sales,
        "rate_coverage": rate_coverage,
        "itc_source": itc_source,
        "has_gst_rates": "GST_Rate" in df.columns,
    }

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

def generate_ca_summary(df, industry):
    """Detailed CA-mode summary with flags and evidence."""
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev-exp
    margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overdue_pct = (overdue/rev*100) if rev>0 else 0
    te = e.groupby("Category")["Amount"].sum().sort_values(ascending=False) if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "costs"
    top_exp_pct = (te.max()/exp*100) if exp>0 and len(te)>0 else 0
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    rev_trend = "growing" if len(sm)>=3 and sm.iloc[-1]>sm.iloc[-3] else "declining" if len(sm)>=3 and sm.iloc[-1]<sm.iloc[-3] else "stable"
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    top_cust_pct = (tc.max()/rev*100) if rev>0 and len(tc)>0 else 0
    n_months = df["Month"].nunique() if "Month" in df.columns else 0
    n_txns = len(df)
    # Build flags
    flags = []
    if margin < 5: flags.append(("red", f"Margin critically thin at {margin:.1f}%"))
    elif margin < 15: flags.append(("amber", f"Margin below industry avg at {margin:.1f}%"))
    else: flags.append(("green", f"Healthy margin {margin:.1f}%"))
    if overdue_pct > 10: flags.append(("red", f"Overdue {overdue_pct:.0f}% of revenue"))
    elif overdue_pct > 0: flags.append(("amber", f"Overdue {overdue_pct:.0f}% of revenue"))
    if top_cust_pct > 40: flags.append(("red", f"Top customer = {top_cust_pct:.0f}% concentration"))
    elif top_cust_pct > 25: flags.append(("amber", f"Top customer = {top_cust_pct:.0f}% concentration"))
    if top_exp_pct > 35: flags.append(("amber", f"{top_exp} = {top_exp_pct:.0f}% of expenses"))
    flags_html = " ".join([f'<span class="ca-flag {f[0]}">{f[1]}</span>' for f in flags])
    return f"""<strong>Period:</strong> {n_months} months · {n_txns} transactions · <strong>Revenue:</strong> {fmt_inr(rev)} · <strong>Expenses:</strong> {fmt_inr(exp)} · <strong>Net:</strong> {fmt_inr(abs(profit))} ({'profit' if profit>=0 else 'loss'}) · <strong>Margin:</strong> {margin:.1f}%<br><br>
<strong>Revenue trend:</strong> {rev_trend.title()} · <strong>Biggest cost head:</strong> {top_exp} ({top_exp_pct:.1f}% of expenses) · <strong>Overdue:</strong> {fmt_inr(overdue)} ({overdue_pct:.1f}% of revenue)<br><br>
<strong>Risk flags:</strong> {flags_html}"""

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

def generate_ca_report_html(df, industry):
    """Clean, professional CA-grade HTML report."""
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
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    em = e.groupby("Month")["Amount"].sum().sort_index()
    gst = gst_summary(df)
    date_str = datetime.now().strftime("%d %B %Y")
    n_months = df["Month"].nunique() if "Month" in df.columns else "—"

    exp_rows = "".join([f"<tr><td>{row.Category}</td><td style='text-align:right'>{fmt_inr(row.Amount)}</td><td style='text-align:right'>{row.Amount/exp*100:.1f}%</td></tr>" for _, row in te.iterrows()]) if len(te)>0 else ""
    cust_rows = "".join([f"<tr><td>{row.Party}</td><td style='text-align:right'>{fmt_inr(row.Amount)}</td><td style='text-align:right'>{row.Amount/rev*100:.1f}%</td></tr>" for _, row in tc.iterrows()]) if len(tc)>0 else ""
    prob_html = "".join([f"<div style='margin-bottom:10px;padding:10px 14px;border-left:3px solid {'#2e7d32' if p['severity']=='green' else '#e65100' if p['severity']=='amber' else '#c62828'};background:#f9f9f9;border-radius:0 6px 6px 0;'><strong style='color:#1a1a1a'>{p['title']}</strong><br><span style='font-size:13px;color:#555'>{p['text'].replace('<strong>','').replace('</strong>','')}</span></div>" for p in probs])
    act_html = "".join([f"<li style='margin-bottom:6px;font-size:13px;color:#333'>{a.replace('<strong>','<b>').replace('</strong>','</b>')}</li>" for a in actions])
    # Monthly trend table
    months_sorted = sorted(set(sm.index) | set(em.index))
    trend_rows = ""
    for m in months_sorted[-6:]:
        r = sm.get(m, 0); ex = em.get(m, 0); p = r - ex
        trend_rows += f"<tr><td>{m}</td><td style='text-align:right'>₹{r:,.0f}</td><td style='text-align:right'>₹{ex:,.0f}</td><td style='text-align:right;color:{'#2e7d32' if p>=0 else '#c62828'}'>₹{p:,.0f}</td></tr>"

    score_bars = ""
    for name, (sc, cl) in scores.items():
        bar_color = "#2e7d32" if cl=="#c8ff57" else "#e65100" if cl=="#ffb557" else "#c62828"
        score_bars += f"<tr><td>{name}</td><td><div style='background:#eee;border-radius:4px;height:8px;width:100%;'><div style='background:{bar_color};height:8px;border-radius:4px;width:{sc}%'></div></div></td><td style='text-align:right;font-weight:600'>{sc}/100</td></tr>"

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>OpsClarity — CA Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  body{{font-family:'Inter',Arial,sans-serif;color:#1a1a2e;margin:0;padding:0;background:#fff;font-size:14px;}}
  .page{{max-width:860px;margin:0 auto;padding:48px 40px;}}
  .header{{border-bottom:2px solid #0a0a0f;padding-bottom:20px;margin-bottom:32px;display:flex;justify-content:space-between;align-items:flex-end;}}
  .logo{{font-size:22px;font-weight:800;color:#0a0a0f;letter-spacing:-.02em;}}
  .logo span{{color:#5a8f1c;}}
  .report-meta{{font-size:12px;color:#888;text-align:right;line-height:1.8;}}
  .disclaimer{{background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:12px 16px;margin-bottom:28px;font-size:12px;color:#5d4037;line-height:1.7;}}
  .disclaimer strong{{color:#e65100;}}
  .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px;}}
  .kpi{{background:#f8f8f6;border:1px solid #e8e8e8;border-radius:10px;padding:14px 16px;}}
  .kpi-label{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#888;font-weight:700;margin-bottom:6px;}}
  .kpi-value{{font-size:1.5rem;font-weight:800;color:#1a1a2e;line-height:1;}}
  .kpi-sub{{font-size:11px;color:#aaa;margin-top:4px;}}
  .health-box{{background:#0a0a0f;color:#f4f1eb;border-radius:12px;padding:20px 24px;margin-bottom:28px;display:flex;align-items:center;gap:24px;}}
  .health-num{{font-size:3.5rem;font-weight:800;line-height:1;}}
  .health-label-text{{font-size:1rem;margin-bottom:4px;font-weight:600;}}
  .health-sub{{font-size:12px;color:#9494a8;}}
  .section{{margin-bottom:28px;}}
  .section-title{{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#888;font-weight:700;margin-bottom:14px;border-bottom:1px solid #eee;padding-bottom:6px;}}
  .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:24px;}}
  table{{width:100%;border-collapse:collapse;}}
  th{{text-align:left;padding:8px 10px;background:#f5f5f0;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:#888;border-bottom:2px solid #e8e8e8;}}
  td{{padding:8px 10px;border-bottom:1px solid #f0f0f0;font-size:13px;}}
  tr:last-child td{{border-bottom:none;}}
  .highlight-box{{background:#f0fff4;border:1px solid #a5d6a7;border-radius:8px;padding:14px 16px;font-size:13px;line-height:1.8;color:#1a1a2e;}}
  .footer{{margin-top:40px;padding-top:16px;border-top:1px solid #eee;font-size:11px;color:#bbb;display:flex;justify-content:space-between;}}
</style></head><body>
<div class="page">
  <div class="header">
    <div>
      <div class="logo">Ops<span>Clarity</span></div>
      <div style="font-size:12px;color:#888;margin-top:3px;">Business Intelligence — CA Advisory Report</div>
    </div>
    <div class="report-meta">
      Generated: {date_str}<br>
      Industry: {industry.title()}<br>
      Period: {n_months} months · {len(df)} transactions
    </div>
  </div>

  <div class="disclaimer">
    <strong>Important:</strong> This report contains management estimates for advisory purposes only.
    GST figures are approximations and must be verified against GSTR-2A/2B before filing.
    All figures should be reconciled with the client's books of accounts, Tally data, and bank statements
    before any tax, compliance, or business decisions are made. This tool does not replace a CA's professional judgment.
  </div>

  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-label">Total Revenue</div><div class="kpi-value">{fmt_inr(rev)}</div><div class="kpi-sub">Gross earned</div></div>
    <div class="kpi"><div class="kpi-label">Total Expenses</div><div class="kpi-value">{fmt_inr(exp)}</div><div class="kpi-sub">Gross spent</div></div>
    <div class="kpi"><div class="kpi-label">Net {'Profit' if profit>=0 else 'Loss'}</div><div class="kpi-value" style="color:{'#2e7d32' if profit>=0 else '#c62828'}">{fmt_inr(abs(profit))}</div><div class="kpi-sub">{abs(margin):.1f}% margin</div></div>
    <div class="kpi"><div class="kpi-label">Overdue</div><div class="kpi-value" style="color:#e65100">{fmt_inr(overdue)}</div><div class="kpi-sub">Uncollected</div></div>
  </div>

  <div class="health-box">
    <div class="health-num" style="color:{'#c8ff57' if overall>=75 else '#ffb557' if overall>=50 else '#ff5e5e'}">{overall}</div>
    <div>
      <div class="health-label-text" style="color:{'#c8ff57' if overall>=75 else '#ffb557' if overall>=50 else '#ff5e5e'}">Business Health Score — {health_label}</div>
      <div class="health-sub">Scored across: profit margin, revenue trend, expense stability, collections, customer diversity, cost efficiency.</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Health Score Breakdown</div>
    <table><tr><th>Metric</th><th>Score</th><th style="text-align:right">Value</th></tr>{score_bars}</table>
  </div>

  <div class="section">
    <div class="section-title">Advisory Summary</div>
    <div class="highlight-box">{generate_owner_summary(df, industry).replace('<strong>','<b>').replace('</strong>','</b>')}</div>
  </div>

  <div class="section">
    <div class="section-title">Priority Issues</div>
    {prob_html}
  </div>

  <div class="section">
    <div class="section-title">Recommended Actions</div>
    <ul style="padding-left:18px;">{act_html}</ul>
  </div>

  <div class="section">
    <div class="section-title">Monthly Trend (Last 6 Months)</div>
    <table><tr><th>Month</th><th style="text-align:right">Revenue</th><th style="text-align:right">Expenses</th><th style="text-align:right">Profit/Loss</th></tr>{trend_rows}</table>
  </div>

  <div class="two-col">
    <div class="section">
      <div class="section-title">Expense Breakdown</div>
      <table><tr><th>Category</th><th style="text-align:right">Amount</th><th style="text-align:right">Share</th></tr>{exp_rows}</table>
    </div>
    <div class="section">
      <div class="section-title">Top Revenue Sources</div>
      <table><tr><th>Party / Customer</th><th style="text-align:right">Revenue</th><th style="text-align:right">Share</th></tr>{cust_rows}</table>
    </div>
  </div>

  <div class="section">
    <div class="section-title">GST Estimates (Management Use Only — Verify Before Filing)</div>
    <table>
      <tr><th>Item</th><th style="text-align:right">Amount</th><th>Note</th></tr>
      <tr><td>Output GST (collected)</td><td style="text-align:right">{fmt_inr(gst['output_gst'])}</td><td style="font-size:12px;color:#888">{'Based on tagged rates' if gst['has_gst_rates'] else 'Estimated at 5% — no rates tagged'}</td></tr>
      <tr><td>Input GST / ITC</td><td style="text-align:right">{fmt_inr(gst['input_gst'])}</td><td style="font-size:12px;color:#888">{'From GST Paid category' if gst['itc_source']=='tagged' else 'Estimated — verify GSTR-2A'}</td></tr>
      <tr><td><strong>Net GST Payable</strong></td><td style="text-align:right"><strong>{fmt_inr(gst['net_payable'])}</strong></td><td style="font-size:12px;color:#e65100"><strong>Estimate only. Reconcile with actual ledger.</strong></td></tr>
    </table>
  </div>

  <div class="footer">
    <div>OpsClarity — SME Advisory Intelligence · opscalarity.streamlit.app</div>
    <div>Confidential · Management Estimates Only · {date_str}</div>
  </div>
</div></body></html>"""
    return html.encode()

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

def generate_score_card_html(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overall, color, scores = compute_health_score(df)
    label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs Attention" if overall>=45 else "Critical"
    ind_label = {"restaurant":"Restaurant","clinic":"Clinic / Lab","retail":"Retail","agency":"Agency"}.get(industry,"SME")
    date_str = datetime.now().strftime("%B %Y")
    score_bars = ""
    for name,(sc,cl) in scores.items():
        score_bars += f"""<div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;font-size:11px;color:#9494a8;margin-bottom:4px;"><span>{name}</span><span style="color:{cl}">{sc}/100</span></div><div style="height:4px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden;"><div style="width:{sc}%;height:100%;background:{cl};border-radius:99px;"></div></div></div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{margin:0;padding:0;background:#0a0a0f;font-family:'Segoe UI',Arial,sans-serif;}}.card{{width:520px;padding:36px;background:#0a0a0f;color:#f4f1eb;}}.badge{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.25);padding:5px 12px;border-radius:20px;background:rgba(200,255,87,.05);margin-bottom:20px;}}.score-big{{font-size:96px;font-weight:900;line-height:1;color:{color};letter-spacing:-.04em;}}.kpi-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:20px 0;}}.kpi{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px 14px;}}.kpi-l{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#4a4a5a;font-weight:700;margin-bottom:4px;}}.kpi-v{{font-size:1.3rem;font-weight:900;color:#f4f1eb;}}.footer{{margin-top:24px;padding-top:16px;border-top:1px solid rgba(255,255,255,.06);display:flex;justify-content:space-between;align-items:center;}}.footer-brand{{font-size:14px;font-weight:900;color:#c8ff57;}}.footer-tag{{font-size:11px;color:#4a4a5a;}}</style></head><body><div class="card"><div class="badge">◈ OpsClarity · {ind_label} · {date_str}</div><div style="display:flex;align-items:flex-end;gap:16px;margin-bottom:8px;"><div class="score-big">{overall}</div><div style="padding-bottom:14px;"><div style="font-size:18px;color:{color};margin-bottom:4px;">{label}</div><div style="font-size:13px;color:#6b6b7a;">Business Health Score / 100</div></div></div><div class="kpi-row"><div class="kpi"><div class="kpi-l">Revenue</div><div class="kpi-v">{fmt_inr(rev)}</div></div><div class="kpi"><div class="kpi-l">Net Profit</div><div class="kpi-v" style="color:{'#c8ff57' if profit>=0 else '#ff5e5e'}">{fmt_inr(abs(profit))}</div></div><div class="kpi"><div class="kpi-l">Margin</div><div class="kpi-v">{margin:.1f}%</div></div></div><div style="margin-top:4px;">{score_bars}</div><div class="footer"><div class="footer-brand">OpsClarity</div><div class="footer-tag">opscalarity.streamlit.app</div></div></div></body></html>"""
    return html.encode()

def get_roast(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum().sort_values(ascending=False) if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "your expenses"
    top_exp_pct = (te.max()/exp*100) if exp>0 and len(te)>0 else 0
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    top_cust_pct = (tc.max()/rev*100) if rev>0 and len(tc)>0 else 0
    roasts = []
    if margin < 5: roasts.append(f"Your profit margin is {margin:.1f}%. You're basically running a charity. A very busy, very tired charity.")
    elif margin < 15: roasts.append(f"You make {margin:.1f}% margin. Your employees are doing better than the business.")
    else: roasts.append(f"{margin:.1f}% margin — not bad! You actually know what you're doing. Suspicious.")
    if top_exp_pct > 35: roasts.append(f"{top_exp_pct:.0f}% of your expenses go to {top_exp}. At this point just marry your vendor.")
    if overdue > 0:
        overdue_pct = (overdue/rev*100) if rev>0 else 0
        roasts.append(f"You have {fmt_inr(overdue)} in overdue invoices ({overdue_pct:.0f}% of revenue). Your customers are treating you like a free loan service.")
    if top_cust_pct > 40: roasts.append(f"One customer is {top_cust_pct:.0f}% of your revenue. That's not a business, that's a hostage situation.")
    if industry == "restaurant": roasts.append("You feed hundreds of people and somehow still worry about money. Gordon Ramsay would have something to say.")
    elif industry == "clinic": roasts.append("You heal patients all day but your own business financials need an ICU visit.")
    elif industry == "retail": roasts.append("Your shelves are full. Your cash flow is empty. Classic retail experience.")
    elif industry == "agency": roasts.append("You invoice clients ₹5L for strategy decks while paying your team in 'exposure'. Classic agency.")
    roasts.append("The good news? You uploaded your data. Most SME owners don't even know their numbers. You're already ahead.")
    return roasts[:4]

def bank_loan_readiness(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    overdue_pct = (overdue/rev*100) if rev>0 else 0
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    rev_stable = len(sm)>=6 and sm.std()/sm.mean() < 0.3 if len(sm)>=3 else False
    score = 0; checks = []
    if len(sm)>=6: score += 20; checks.append(("pass","6+ months of revenue history","Banks want to see consistent income history"))
    elif len(sm)>=3: score += 10; checks.append(("partial","3–5 months of revenue history","Ideally show 6+ months for better loan terms"))
    else: checks.append(("fail","Less than 3 months data","Need at least 6 months of financial history"))
    if margin > 15: score += 25; checks.append(("pass",f"Strong profit margin ({margin:.1f}%)","Banks prefer 15%+ margin"))
    elif margin > 5: score += 15; checks.append(("partial",f"Acceptable margin ({margin:.1f}%)","Improve to 15%+ for better loan rates"))
    else: checks.append(("fail",f"Thin margin ({margin:.1f}%)","Banks see thin margins as high risk"))
    if overdue_pct < 5: score += 20; checks.append(("pass","Clean collections (low overdue)","Good sign of business health"))
    elif overdue_pct < 15: score += 10; checks.append(("partial",f"Some overdue ({overdue_pct:.0f}% of revenue)","Recover overdue before applying"))
    else: checks.append(("fail",f"High overdue ({overdue_pct:.0f}% of revenue)","Clear overdue invoices first"))
    monthly_rev = sm.mean() if len(sm)>0 else 0
    if monthly_rev > 500000: score += 20; checks.append(("pass",f"Strong monthly revenue ({fmt_inr(monthly_rev)}/mo)","Qualifies for larger loan amounts"))
    elif monthly_rev > 100000: score += 10; checks.append(("partial",f"Moderate revenue ({fmt_inr(monthly_rev)}/mo)","May qualify for small business loans"))
    else: checks.append(("fail",f"Low monthly revenue ({fmt_inr(monthly_rev)}/mo)","Grow revenue before applying"))
    if rev_stable: score += 15; checks.append(("pass","Revenue is consistent month-to-month","Lenders love predictable businesses"))
    else: score += 5; checks.append(("partial","Revenue has some fluctuation","More stability = better loan terms"))
    loan_estimate = monthly_rev * 6 if score >= 60 else monthly_rev * 3 if score >= 40 else monthly_rev
    return {"score":score,"checks":checks,"loan_estimate":loan_estimate,"monthly_rev":monthly_rev}

def gst_readiness(df):
    checks = []; score = 0
    if "Date" in df.columns and df["Date"].notna().any(): score += 20; checks.append(("pass","Dates present on all transactions","Required for GST period mapping"))
    else: checks.append(("fail","Missing dates","Add dates to all entries"))
    if "Category" in df.columns and df["Category"].nunique() > 3: score += 20; checks.append(("pass","Transactions are categorised","Helps with HSN/SAC code mapping"))
    else: checks.append(("partial","Limited categorisation","Add more specific categories"))
    if "GST_Rate" in df.columns: score += 20; checks.append(("pass","GST rates are tagged","Ready for GSTR-1 computation"))
    else: checks.append(("fail","No GST rates on transactions","Tag each transaction with GST rate (0/5/12/18/28%)"))
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    if len(s)>0 and len(e)>0: score += 20; checks.append(("pass","Both sales and expenses present","Full P&L available for GST"))
    gst_paid = e[e["Category"]=="GST Paid"]["Amount"].sum() if len(e)>0 else 0
    if gst_paid>0: score += 20; checks.append(("pass","GST paid (ITC) is tracked","Input Tax Credit can be claimed"))
    else: checks.append(("partial","GST paid not separately tracked","Add 'GST Paid' as expense category for ITC claims"))
    return {"score":score,"checks":checks}

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
    def pct_chg(cur, prev): return ((cur - prev) / prev) * 100 if prev != 0 else 0
    return {"cur_month":cur_m,"prev_month":prev_m,"rev":(cur_rev,prev_rev,pct_chg(cur_rev,prev_rev)),"exp":(cur_exp,prev_exp,pct_chg(cur_exp,prev_exp)),"profit":(cur_profit,prev_profit,pct_chg(cur_profit,prev_profit))}

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
    return {"next_30_rev":next_30_rev,"next_30_exp":next_30_exp,"net_next_30":net_next_30,"overdue_risk":overdue,"stress_level":stress_level,"avg_monthly_exp":avg_monthly_exp}

def get_collection_wa_message(party, amount, days):
    if days > 60: return f"Dear {party}, this is an urgent reminder that your payment of {fmt_inr(amount)} has been pending for over {days} days. Please settle this at the earliest to avoid any disruption. Contact us immediately to resolve. Thank you."
    elif days > 30: return f"Hi {party}, a gentle reminder that {fmt_inr(amount)} is overdue on your account. We would appreciate your payment at the earliest convenience. Please let us know if there are any issues. Thank you."
    else: return f"Hi {party}, this is a quick reminder about the outstanding payment of {fmt_inr(amount)} on your account. Request you to clear this at your earliest. Thank you for your continued business!"

def get_ca_demo_clients():
    return [
        {"name":"Sharma Clinic","industry":"clinic","health":74,"revenue":"₹28L","revenue_raw":2800000,"profit_margin":"18%","margin_raw":18,"overdue":"₹1.2L","overdue_raw":120000,"status":"good","alert":None,"months":9,"trend":"stable"},
        {"name":"Metro Traders","industry":"retail","health":45,"revenue":"₹92L","revenue_raw":9200000,"profit_margin":"6%","margin_raw":6,"overdue":"₹8.4L","overdue_raw":840000,"status":"warning","alert":"High overdue — follow up urgently","months":12,"trend":"declining"},
        {"name":"Priya Catering","industry":"restaurant","health":82,"revenue":"₹41L","revenue_raw":4100000,"profit_margin":"24%","margin_raw":24,"overdue":"₹0","overdue_raw":0,"status":"excellent","alert":None,"months":8,"trend":"growing"},
        {"name":"BuildRight Infra","industry":"agency","health":31,"revenue":"₹1.2Cr","revenue_raw":12000000,"profit_margin":"2%","margin_raw":2,"overdue":"₹18L","overdue_raw":1800000,"status":"critical","alert":"Loss-making — immediate review needed","months":11,"trend":"declining"},
        {"name":"City Diagnostics","industry":"clinic","health":68,"revenue":"₹54L","revenue_raw":5400000,"profit_margin":"15%","margin_raw":15,"overdue":"₹3.1L","overdue_raw":310000,"status":"good","alert":"Overdue rising — check collections","months":12,"trend":"stable"},
        {"name":"Raj Electronics","industry":"retail","health":71,"revenue":"₹1.8Cr","revenue_raw":18000000,"profit_margin":"11%","margin_raw":11,"overdue":"₹6.2L","overdue_raw":620000,"status":"good","alert":None,"months":6,"trend":"growing"},
    ]

def ask_ai(question, df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit / rev * 100) if rev > 0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = {k: fmt_inr(v) for k, v in e.groupby("Category")["Amount"].sum().to_dict().items()} if len(e) > 0 else {}
    tc = {k: fmt_inr(v) for k, v in s.groupby("Party")["Amount"].sum().nlargest(5).to_dict().items()} if len(s) > 0 else {}
    context = f"""You are a sharp Indian SME financial advisor.
Be direct, specific, use numbers, and give practical business advice.
Keep the answer under 150 words.

Business Summary:
Revenue = {fmt_inr(rev)}
Expenses = {fmt_inr(exp)}
Profit = {fmt_inr(profit)}
Profit Margin = {margin:.1f}%
Overdue = {fmt_inr(overdue)}

Expense Breakdown:
{json.dumps(te)}

Top Customers:
{json.dumps(tc)}

Question:
{question}
"""
    import urllib.request, urllib.error
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key: return "Add ANTHROPIC_API_KEY in Streamlit Secrets to enable AI Q&A."
    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":300,"messages":[{"role":"user","content":context}]}).encode("utf-8")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload, headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"AI Q&A error: {e.read().decode('utf-8')}"
    except Exception as e:
        return f"AI Q&A error: {str(e)}"

FOUNDER_WHATSAPP = "916362319163"

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("df",None),("industry","restaurant"),("unlocked",False),("chat_history",[]),("confidence",95),("mapped_cols",[]),("view_mode","owner")]:
    if k not in st.session_state: st.session_state[k] = v


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">◈ OpsClarity — SME Intelligence</div>
    <h1 class="hero-title">Know where your business<br>is <span>leaking money</span> — in 30 seconds.</h1>
    <p class="hero-sub">Upload your Excel, Tally export, or bank statement. Instant P&L, health score, loan readiness, GST readiness, and plain-English actions. Free for any Indian SME.</p>
    <a href="https://wa.me/916362319163?text=Hi%2C%20I%20want%20to%20try%20OpsClarity" target="_blank" style="display:inline-block;margin-top:1rem;background:#25D366;color:#fff;font-size:13px;font-weight:700;padding:10px 22px;border-radius:10px;text-decoration:none;">Talk to the founder on WhatsApp</a>
</div>
""", unsafe_allow_html=True)


# ── UPLOAD + TALLY GUIDE ──────────────────────────────────────────────────────
st.markdown("<div class='upload-wrap'>", unsafe_allow_html=True)
col1, col2 = st.columns([1.6, 1])
with col1:
    uploaded_file = st.file_uploader(
        "Drop your file — CSV, Excel, Tally export, bank statement",
        type=["csv","xlsx","xls"]
    )
    with st.expander("📋 How to export from Tally (step-by-step)"):
        st.markdown("""
**Tally Prime / ERP9 → Export in 3 steps:**

1. Open Tally → Go to **Display > Account Books > Ledger** (or Day Book)
2. Press **Alt+E** to Export → Choose **Excel** or **CSV** format
3. Set date range → Export → Upload the file here

**Works with:**
- Day Book export (all transactions)
- Sales Register / Purchase Register
- Bank statement CSV from any Indian bank
- Any Excel with columns: Date, Amount, Party/Description

**Column names don't need to be exact** — OpsClarity auto-maps common Tally, Vyapar, and bank formats.
        """)
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
        st.session_state.df = df_up
        st.session_state.industry = "restaurant"
        st.session_state.confidence = conf
        st.session_state.mapped_cols = mapped
        st.success(msg)
    else:
        st.error(f"Could not parse: {msg}. Try saving as CSV and re-uploading.")


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df.copy()
    industry = st.session_state.industry

    # ── VIEW MODE TOGGLE ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    vc1, vc2, vc3 = st.columns([1, 1, 4])
    with vc1:
        if st.button("👤  Owner View", use_container_width=True,
                     type="primary" if st.session_state.view_mode=="owner" else "secondary"):
            st.session_state.view_mode = "owner"
    with vc2:
        if st.button("🏛️  CA / Advisor View", use_container_width=True,
                     type="primary" if st.session_state.view_mode=="ca" else "secondary"):
            st.session_state.view_mode = "ca"
    with vc3:
        mode_label = "**Owner View** — plain English, action-oriented" if st.session_state.view_mode=="owner" else "**CA / Advisor View** — detailed, evidence-backed, with risk flags"
        st.markdown(f"<div style='padding-top:.5rem;font-size:13px;color:#5a5a6d;'>{mode_label}</div>", unsafe_allow_html=True)

    is_ca = st.session_state.view_mode == "ca"

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

    # ── KPI CARDS ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green"><div class="metric-label">Revenue</div><div class="metric-value">{fmt_inr(rev)}</div><div class="metric-sub">Total earned</div></div>
        <div class="metric-card red"><div class="metric-label">Expenses</div><div class="metric-value">{fmt_inr(exp)}</div><div class="metric-sub">Total spent</div></div>
        <div class="metric-card {'green' if profit>=0 else 'red'}"><div class="metric-label">Net Profit</div><div class="metric-value">{fmt_inr(abs(profit))}</div><div class="metric-sub">{'Profit' if profit>=0 else 'Loss'} · {abs(margin):.1f}% margin</div></div>
        <div class="metric-card amber"><div class="metric-label">Overdue</div><div class="metric-value">{fmt_inr(overdue_amt)}</div><div class="metric-sub">Cash not yet collected</div></div>
    </div>""", unsafe_allow_html=True)

    # ── MONTH VS MONTH ────────────────────────────────────────────────────────
    mom = month_vs_month(df)
    if mom:
        st.markdown("<div class='section-title'>◈ This month vs last month</div>", unsafe_allow_html=True)
        m1,m2,m3 = st.columns(3)
        def delta_color(pct, higher_better=True): return "#c8ff57" if (pct > 0) == higher_better else "#ff5e5e"
        def delta_arrow(pct): return "▲" if pct > 0 else "▼"
        cur_r, prev_r, pct_r = mom["rev"]
        cur_e, prev_e, pct_e = mom["exp"]
        cur_p, prev_p, pct_p = mom["profit"]
        m1.markdown(f'<div class="metric-card blue"><div class="metric-label">Revenue — {mom["cur_month"]}</div><div class="metric-value">{fmt_inr(cur_r)}</div><div class="metric-sub" style="color:{delta_color(pct_r)}">{delta_arrow(pct_r)} {abs(pct_r):.1f}% vs {mom["prev_month"]} ({fmt_inr(prev_r)})</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card amber"><div class="metric-label">Expenses — {mom["cur_month"]}</div><div class="metric-value">{fmt_inr(cur_e)}</div><div class="metric-sub" style="color:{delta_color(pct_e, higher_better=False)}">{delta_arrow(pct_e)} {abs(pct_e):.1f}% vs {mom["prev_month"]} ({fmt_inr(prev_e)})</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card {"green" if cur_p>=0 else "red"}"><div class="metric-label">Profit — {mom["cur_month"]}</div><div class="metric-value">{fmt_inr(abs(cur_p))}</div><div class="metric-sub" style="color:{delta_color(pct_p)}">{delta_arrow(pct_p)} {abs(pct_p):.1f}% vs {mom["prev_month"]} ({fmt_inr(abs(prev_p))})</div></div>', unsafe_allow_html=True)

    # ── CASH RUNWAY ───────────────────────────────────────────────────────────
    runway = cash_runway_warning(df)
    if runway["stress_level"] == "critical":
        st.error(f"🚨 **Cash flow warning:** Projected loss of **{fmt_inr(abs(runway['net_next_30']))}** next month. Immediate action needed.")
    elif runway["stress_level"] == "warning":
        st.warning(f"⚠️ **Cash flow caution:** Next 30 days look tight — projected net: **{fmt_inr(runway['net_next_30'])}**. You have **{fmt_inr(runway['overdue_risk'])}** in overdue that could ease this.")
    else:
        st.success(f"✅ **Cash flow looks healthy** — projected next month surplus: **{fmt_inr(runway['net_next_30'])}**.")

    # ── HEALTH SCORE ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>◈ Business Health Score</div>", unsafe_allow_html=True)
    overall, color, scores = compute_health_score(df)
    label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs attention" if overall>=45 else "Critical"
    score_html = f'<div class="health-wrap"><div style="display:flex;align-items:baseline;gap:12px;"><div class="health-score" style="color:{color}">{overall}</div><div style="font-size:1.05rem;color:#7f7f92;">/ 100 — <span style="color:{color}">{label}</span></div></div>'
    if is_ca:
        score_html += '<div style="font-size:12px;color:#5a5a6d;margin-top:4px;margin-bottom:8px;">Scored on: profit margin, revenue trend, expense stability, collections health, revenue diversity, cost efficiency.</div>'
    score_html += '<div class="health-grid">'
    for name,(sc,cl) in scores.items():
        score_html += f'<div class="health-item"><div class="health-label">{name}</div><div class="health-bar"><div class="health-fill" style="width:{sc}%;background:{cl};"></div></div><div class="health-score-small">{sc}/100</div></div>'
    score_html += "</div></div>"
    st.markdown(score_html, unsafe_allow_html=True)

    # ── SUMMARY (mode-aware) ──────────────────────────────────────────────────
    if is_ca:
        st.markdown("<div class='section-title'>◈ Advisory Summary</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="ca-summary"><div class="ca-summary-label">CA / Advisor View — Evidence-backed snapshot</div><div class="ca-summary-text">{generate_ca_summary(df,industry)}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='section-title'>◈ Owner Summary</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="owner-summary"><div class="owner-summary-label">Plain-English business snapshot</div><div class="owner-summary-text">{generate_owner_summary(df,industry)}</div></div>', unsafe_allow_html=True)

    # ── TOP 3 PROBLEMS + DRILL-THROUGH ───────────────────────────────────────
    st.markdown("<div class='section-title'>◈ Top 3 problems right now</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Where this business needs attention first.</div>", unsafe_allow_html=True)
    probs = get_top_3_problems(df, industry)
    for i, p in enumerate(probs):
        col_cards = st.columns(3) if i == 0 else None

    # Render all 3 as columns
    prob_cols = st.columns(3)
    for i, p in enumerate(probs):
        with prob_cols[i]:
            st.markdown(f"""<div class="problem-card">
                <div class="problem-tag {p['severity']}">{p['severity'].upper()}</div>
                <div class="problem-title">{p['title']}</div>
                <div class="problem-text">{p['text']}</div>
                <div class="problem-action"><strong>Action:</strong> {p['action']}</div>
            </div>""", unsafe_allow_html=True)
            # ── DRILL-THROUGH ─────────────────────────────────────────────
            drill_df = get_drill_transactions(df, p["drill_type"], p["drill_category"])
            if len(drill_df) > 0:
                with st.expander(f"🔍 Show transactions behind this ({len(drill_df)} rows)"):
                    if is_ca:
                        total = df[
                            (df["Type"]==("Expense" if p["drill_type"] in ["expense_category","margin"] else "Sales")) &
                            (df["Category"]==p["drill_category"] if p["drill_category"] and "Category" in df.columns else True)
                        ]["Amount"].sum()
                        st.caption(f"Total in this category: {fmt_inr(total)}")
                    st.dataframe(drill_df, hide_index=True, use_container_width=True)

    # ── ACTIONS + LEAKS ───────────────────────────────────────────────────────
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

    # ── ANOMALY ALERTS + DRILL ────────────────────────────────────────────────
    alerts = detect_anomalies(df)
    if alerts:
        st.markdown("<div class='section-title'>⚠️ Anomaly Alerts</div>", unsafe_allow_html=True)
        for level, cat_key, text, action in alerts:
            st.markdown(f'<div class="alert-card {level}"><div class="alert-text">{text}</div><div class="alert-action"><strong>Action:</strong> {action}</div></div>', unsafe_allow_html=True)
            if cat_key != "revenue_drop" and is_ca:
                drill = df[(df["Type"]=="Expense") & (df["Category"]==cat_key)].sort_values("Date", ascending=False).head(8)
                if len(drill) > 0:
                    with st.expander(f"🔍 Show {cat_key} transactions"):
                        dcols = [c for c in ["Date","Invoice_No","Party","Amount"] if c in drill.columns]
                        st.dataframe(drill[dcols].assign(Amount=drill["Amount"].apply(fmt_inr)), hide_index=True, use_container_width=True)

    # ── TRUST LAYER ───────────────────────────────────────────────────────────
    conf = st.session_state.confidence
    mapped = st.session_state.mapped_cols
    st.markdown(f'<div class="trust-box"><div class="trust-title">Data confidence</div><div class="trust-text">Parsed with <strong>{conf}%</strong> confidence. Detected fields: <strong>{", ".join(mapped) if mapped else "None"}</strong>. All figures are management estimates. Verify against source books before filing or financial decisions.</div></div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11 = st.tabs([
        "📈 Revenue","💸 Expenses","🏆 Customers",
        "📊 Profit","🏅 Benchmarks","🧾 GST","🔮 Forecast","📋 Collections",
        "🏦 Loan Readiness","Roast Mode","CA Dashboard"])

    with tab1:
        st.markdown("<div class='section-title'>Revenue vs Expenses trend</div>", unsafe_allow_html=True)
        sm = s.groupby("Month")["Amount"].sum(); em = e.groupby("Month")["Amount"].sum()
        st.line_chart(pd.DataFrame({"Revenue":sm,"Expenses":em}).fillna(0).sort_index(), use_container_width=True)
        if is_ca:
            st.markdown("**Monthly Revenue Table**")
            rev_table = sm.reset_index(); rev_table.columns = ["Month","Revenue"]
            rev_table["MoM Change"] = rev_table["Revenue"].pct_change().mul(100).round(1).astype(str) + "%"
            rev_table["Revenue"] = rev_table["Revenue"].apply(fmt_inr)
            st.dataframe(rev_table, hide_index=True, use_container_width=True)

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
        if is_ca:
            st.markdown("**Monthly Expense Trend by Category**")
            if len(e) > 0:
                pivot = e.pivot_table(index="Month", columns="Category", values="Amount", aggfunc="sum").fillna(0)
                st.dataframe(pivot.applymap(lambda x: fmt_inr(x) if x > 0 else "—"), use_container_width=True)

    with tab3:
        st.markdown("<div class='section-title'>Top customers by revenue</div>", unsafe_allow_html=True)
        if len(s)>0:
            st.bar_chart(s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(8), use_container_width=True)
            if is_ca:
                st.markdown("**Customer Concentration Detail**")
                cust_table = s.groupby("Party")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
                cust_table["Share %"] = (cust_table["Amount"]/rev*100).round(1)
                cust_table["Cumulative %"] = cust_table["Share %"].cumsum().round(1)
                cust_table["Amount"] = cust_table["Amount"].apply(fmt_inr)
                st.dataframe(cust_table, hide_index=True, use_container_width=True)

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
                st.markdown(f"""<div class="bench-card">
                    <div class="bench-label">{b['metric']}</div>
                    <div class="bench-row">
                        <div><div class="bench-yours" style="color:{bar_color}">{b['yours']:.1f}%</div></div>
                        <div style="text-align:right"><div class="bench-avg">Industry avg: {b['benchmark']}%</div><div style="font-size:11px;color:{'#c8ff57' if b['good'] else '#ff7c7c'};margin-top:2px;">{'✓ Good' if b['good'] else '⚠ Needs work'}</div></div>
                    </div>
                    <div class="bench-bar-wrap"><div class="bench-bar-fill" style="width:{bar_pct}%;background:{bar_color};"></div></div>
                </div>""", unsafe_allow_html=True)

    with tab6:
        st.markdown("<div class='section-title'>GST Summary</div>", unsafe_allow_html=True)

        # Prominent disclaimer
        st.markdown("""<div class="gst-disclaimer">
            <div class="gst-disclaimer-title">⚠️ Management Estimate — Not for Filing</div>
            <div class="gst-disclaimer-text">
                These figures are <strong>approximations only</strong>, computed from the uploaded data.
                They do <strong>not</strong> replace GSTR-1, GSTR-3B, or GSTR-2A/2B reconciliation.
                Input Tax Credit (ITC) figures must be verified against supplier invoices and GSTR-2A.
                Always have your CA review and file the actual returns. Use this only for management planning.
            </div>
        </div>""", unsafe_allow_html=True)

        gst = gst_summary(df)

        # Data quality warning
        if not gst["has_gst_rates"]:
            st.warning("⚠️ No GST rates found in your data. Output GST is estimated at a flat 5%. Tag transactions with GST rates (0/5/12/18/28%) for accurate figures.")
        elif gst["rate_coverage"] < 0.8:
            st.warning(f"⚠️ Only {gst['rate_coverage']*100:.0f}% of sales transactions have GST rates tagged. Remaining are excluded from GST calculation.")

        if gst["itc_source"] == "estimated":
            st.info("ℹ️ No 'GST Paid' expense category found. ITC is estimated from eligible expenses. Add a 'GST Paid' category for accurate ITC tracking.")

        g1,g2,g3,g4 = st.columns(4)
        g1.metric("Output GST (Est.)", fmt_inr(gst["output_gst"]))
        g2.metric("Input GST / ITC (Est.)", fmt_inr(gst["input_gst"]))
        g3.metric("Net Payable (Est.)", fmt_inr(gst["net_payable"]))
        g4.metric("Taxable Sales", fmt_inr(gst["total_sales"]))
        gc1,gc2 = st.columns(2)
        gc1.metric("CGST (50% of output)", fmt_inr(gst["cgst"]))
        gc2.metric("SGST (50% of output)", fmt_inr(gst["sgst"]))

        # GST Readiness
        st.markdown("<div class='section-title' style='margin-top:1.5rem'>GST Filing Readiness</div>", unsafe_allow_html=True)
        gr = gst_readiness(df)
        gr_color = "#c8ff57" if gr["score"]>=80 else "#ffb557" if gr["score"]>=50 else "#ff5e5e"
        st.markdown(f'<div style="font-family:\'DM Serif Display\',serif;font-size:2.5rem;color:{gr_color};margin-bottom:1rem">{gr["score"]}/100</div>', unsafe_allow_html=True)
        for status, title, desc in gr["checks"]:
            icon = "✅" if status=="pass" else "⚠️" if status=="partial" else "❌"
            bg = "rgba(200,255,87,.05)" if status=="pass" else "rgba(255,181,87,.05)" if status=="partial" else "rgba(255,87,87,.05)"
            border = "rgba(200,255,87,.15)" if status=="pass" else "rgba(255,181,87,.15)" if status=="partial" else "rgba(255,87,87,.15)"
            st.markdown(f'<div style="background:{bg};border:1px solid {border};border-radius:10px;padding:.8rem 1rem;margin-bottom:8px;display:flex;gap:10px;"><span>{icon}</span><div><div style="font-size:14px;font-weight:600;color:#f4f1eb">{title}</div><div style="font-size:13px;color:#8f8fa4;margin-top:2px">{desc}</div></div></div>', unsafe_allow_html=True)

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
                st.markdown(f"""<div class="collection-item">
                    <div><div class="collection-party">{c['party']}</div><div class="collection-days">{c['count']} invoice(s) · {c['days']} days overdue</div></div>
                    <div class="collection-amt">{fmt_inr(c['amount'])}</div>
                </div>""", unsafe_allow_html=True)
                col_wa, col_drill = st.columns([2, 1])
                with col_wa:
                    with st.expander(f"📱 WhatsApp reminder for {c['party']}"):
                        st.text_area("Copy & send:", value=wa_msg, height=100, key=f"wa_{c['party']}", label_visibility="collapsed")
                if is_ca:
                    with col_drill:
                        with st.expander("🔍 View invoices"):
                            party_inv = df[(df["Type"]=="Sales") & (df["Party"]==c["party"]) & (df["Status"]=="Overdue")]
                            dcols = [col for col in ["Date","Invoice_No","Amount","Status"] if col in party_inv.columns]
                            st.dataframe(party_inv[dcols].assign(Amount=party_inv["Amount"].apply(fmt_inr)), hide_index=True, use_container_width=True)
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

    with tab9:
        st.markdown("<div class='section-title'>Bank Loan Readiness</div>", unsafe_allow_html=True)
        loan = bank_loan_readiness(df)
        l1,l2,l3 = st.columns(3)
        sc = loan["score"]
        scol = "#c8ff57" if sc>=70 else "#ffb557" if sc>=45 else "#ff5e5e"
        l1.markdown(f'<div class="metric-card {"green" if sc>=70 else "amber" if sc>=45 else "red"}"><div class="metric-label">Readiness Score</div><div class="metric-value" style="color:{scol}">{sc}/100</div><div class="metric-sub">{"Strong" if sc>=70 else "Borderline" if sc>=45 else "Not ready"}</div></div>', unsafe_allow_html=True)
        l2.markdown(f'<div class="metric-card blue"><div class="metric-label">Loan Eligibility</div><div class="metric-value">{fmt_inr(loan["loan_estimate"])}</div><div class="metric-sub">Estimated (3–6x monthly rev)</div></div>', unsafe_allow_html=True)
        l3.markdown(f'<div class="metric-card green"><div class="metric-label">Monthly Revenue</div><div class="metric-value">{fmt_inr(loan["monthly_rev"])}</div><div class="metric-sub">3-month avg</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
        for status, title, desc in loan["checks"]:
            icon = "✅" if status=="pass" else "⚠️" if status=="partial" else "❌"
            bg = "rgba(200,255,87,.05)" if status=="pass" else "rgba(255,181,87,.05)" if status=="partial" else "rgba(255,87,87,.05)"
            border = "rgba(200,255,87,.15)" if status=="pass" else "rgba(255,181,87,.15)" if status=="partial" else "rgba(255,87,87,.15)"
            st.markdown(f'<div style="background:{bg};border:1px solid {border};border-radius:10px;padding:.8rem 1rem;margin-bottom:8px;display:flex;gap:10px;"><span>{icon}</span><div><div style="font-size:14px;font-weight:600;color:#f4f1eb">{title}</div><div style="font-size:13px;color:#8f8fa4;margin-top:2px">{desc}</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:1.5rem;padding:1rem 1.2rem;background:rgba(37,211,102,.05);border:1px solid rgba(37,211,102,.15);border-radius:12px;display:flex;align-items:center;justify-content:space-between;gap:12px;"><span style="font-size:13px;color:#8f8fa4;">Need help improving loan readiness?</span><a href="https://wa.me/916362319163?text=Hi%2C+I+checked+my+loan+readiness+on+OpsClarity.+Can+we+talk%3F" target="_blank" style="background:#25D366;color:#fff;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;text-decoration:none;white-space:nowrap;">WhatsApp us</a></div>', unsafe_allow_html=True)

    with tab10:
        st.markdown("<div class='section-title'>Roast My Business</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Brutally honest. Surprisingly useful.</div>", unsafe_allow_html=True)
        roasts = get_roast(df, industry)
        for i, roast in enumerate(roasts):
            emoji = "💡" if i==len(roasts)-1 else "🔥"
            bg = "rgba(200,255,87,.05)" if i==len(roasts)-1 else "rgba(255,255,255,.03)"
            border = "rgba(200,255,87,.2)" if i==len(roasts)-1 else "rgba(255,255,255,.07)"
            st.markdown(f'<div style="background:{bg};border:1px solid {border};border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:12px;font-size:15px;color:#f4f1eb;line-height:1.7;">{emoji} {roast}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:1rem;text-align:center;"><a href="https://wa.me/916362319163?text=Hi%2C+I+just+got+my+business+roasted+by+OpsClarity!" target="_blank" style="display:inline-block;background:#25D366;color:#fff;font-size:14px;font-weight:700;padding:12px 28px;border-radius:12px;text-decoration:none;">Share this + talk to founder on WhatsApp</a></div>', unsafe_allow_html=True)

    with tab11:
        st.markdown("<div class='section-title'>CA Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Manage all your clients from one place. Identify who needs urgent attention. Free forever for CAs.</div>", unsafe_allow_html=True)

        clients = get_ca_demo_clients()
        critical = sum(1 for c in clients if c["status"]=="critical")
        warning_c = sum(1 for c in clients if c["status"]=="warning")
        healthy = sum(1 for c in clients if c["status"] in ["good","excellent"])
        total_overdue_ca = sum(c["overdue_raw"] for c in clients)
        ca1,ca2,ca3,ca4,ca5 = st.columns(5)
        ca1.markdown(f'<div class="metric-card blue"><div class="metric-label">Total Clients</div><div class="metric-value">{len(clients)}</div><div class="metric-sub">Demo view</div></div>', unsafe_allow_html=True)
        ca2.markdown(f'<div class="metric-card green"><div class="metric-label">Healthy</div><div class="metric-value">{healthy}</div><div class="metric-sub">Score 65+</div></div>', unsafe_allow_html=True)
        ca3.markdown(f'<div class="metric-card amber"><div class="metric-label">Warning</div><div class="metric-value">{warning_c}</div><div class="metric-sub">Review this week</div></div>', unsafe_allow_html=True)
        ca4.markdown(f'<div class="metric-card red"><div class="metric-label">Critical</div><div class="metric-value">{critical}</div><div class="metric-sub">Act immediately</div></div>', unsafe_allow_html=True)
        ca5.markdown(f'<div class="metric-card amber"><div class="metric-label">Total Overdue</div><div class="metric-value">{fmt_inr(total_overdue_ca)}</div><div class="metric-sub">Across all clients</div></div>', unsafe_allow_html=True)

        # Sort: critical first, then warning, then good
        sort_order = {"critical":0,"warning":1,"good":2,"excellent":3}
        clients_sorted = sorted(clients, key=lambda c: sort_order.get(c["status"],4))

        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown("**Sort by:** Priority (critical first)", unsafe_allow_html=True)
        for c in clients_sorted:
            scol = {"excellent":"#c8ff57","good":"#c8ff57","warning":"#ffb557","critical":"#ff5e5e"}[c["status"]]
            sbg = {"excellent":"rgba(200,255,87,.04)","good":"rgba(200,255,87,.03)","warning":"rgba(255,181,87,.05)","critical":"rgba(255,87,87,.05)"}[c["status"]]
            sborder = {"excellent":"rgba(200,255,87,.18)","good":"rgba(200,255,87,.12)","warning":"rgba(255,181,87,.2)","critical":"rgba(255,87,87,.2)"}[c["status"]]
            alert_html = f'<div style="font-size:12px;color:#ffb557;margin-top:4px;">⚠️ {c["alert"]}</div>' if c["alert"] else ""
            trend_icon = "📈" if c["trend"]=="growing" else "📉" if c["trend"]=="declining" else "➡️"
            margin_color = "#c8ff57" if c["margin_raw"]>=15 else "#ffb557" if c["margin_raw"]>=5 else "#ff5e5e"
            overdue_color = "#ff7c7c" if c["overdue_raw"]>0 else "#c8ff57"
            st.markdown(f"""<div style="background:{sbg};border:1px solid {sborder};border-radius:14px;padding:1.1rem 1.4rem;margin-bottom:8px;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;">
                  <div style="flex:1">
                    <div style="display:flex;align-items:center;gap:10px;">
                      <div style="font-size:14px;font-weight:700;color:#f4f1eb">{c['name']}</div>
                      <div style="font-size:11px;color:#5b5b6f;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);padding:2px 8px;border-radius:6px;">{c['industry'].title()}</div>
                      <div style="font-size:11px;color:#5b5b6f">{trend_icon} {c['trend'].title()}</div>
                    </div>
                    <div style="display:flex;gap:20px;margin-top:6px;flex-wrap:wrap;">
                      <div style="font-size:12px;color:#8f8fa4;">Rev: <strong style="color:#f4f1eb">{c['revenue']}</strong></div>
                      <div style="font-size:12px;color:#8f8fa4;">Margin: <strong style="color:{margin_color}">{c['profit_margin']}</strong></div>
                      <div style="font-size:12px;color:#8f8fa4;">Overdue: <strong style="color:{overdue_color}">{c['overdue']}</strong></div>
                      <div style="font-size:12px;color:#8f8fa4;">{c['months']} months data</div>
                    </div>
                    {alert_html}
                  </div>
                  <div style="text-align:center;min-width:56px">
                    <div style="font-size:1.8rem;font-weight:900;color:{scol};line-height:1">{c['health']}</div>
                    <div style="font-size:10px;color:#5b5b6f">/100</div>
                  </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Priority action list for CA
        urgent = [c for c in clients_sorted if c["status"] in ["critical","warning"]]
        if urgent:
            st.markdown("<div class='section-title' style='margin-top:1.5rem'>Priority Actions This Week</div>", unsafe_allow_html=True)
            for c in urgent:
                if c["status"] == "critical":
                    action = f"🔴 **{c['name']}** — Review immediately. {c['alert'] or 'Critical health score.'} Schedule urgent client call."
                else:
                    action = f"🟡 **{c['name']}** — {c['alert'] or 'Warning signals. Review this week.'}"
                st.markdown(f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.8rem 1rem;margin-bottom:6px;font-size:14px;color:#c8c8d4">{action}</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem;padding:1.2rem 1.4rem;background:rgba(200,255,87,.06);border:1px solid rgba(200,255,87,.2);border-radius:14px;display:flex;align-items:center;justify-content:space-between;gap:16px;"><div><div style="font-size:15px;font-weight:700;color:#f4f1eb">Want this for your actual clients?</div><div style="font-size:13px;color:#8f8fa4;margin-top:3px">Free forever for CAs. White-label available. Upload any client\'s Tally or bank data.</div></div><a href="https://wa.me/916362319163?text=Hi%2C+I+am+a+CA+and+want+to+use+OpsClarity+for+my+clients" target="_blank" style="background:#25D366;color:#fff;font-size:13px;font-weight:700;padding:10px 20px;border-radius:10px;text-decoration:none;white-space:nowrap;">WhatsApp us</a></div>', unsafe_allow_html=True)

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
    ex1,ex2,ex3,ex4,ex5,ex6 = st.columns(6)
    with ex1:
        st.markdown("**📊 CSV Report**")
        st.download_button("⬇ CSV", data=generate_report_csv(df), file_name=f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    with ex2:
        st.markdown("**🏛️ CA Report**")
        st.download_button("⬇ CA HTML", data=generate_ca_report_html(df, industry), file_name=f"OpsClarity_CA_Report_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
    with ex3:
        st.markdown("**🌐 Owner Report**")
        # reuse old html report logic inline
        from io import StringIO as _SIO
        _s = df[df["Type"]=="Sales"]; _e = df[df["Type"]=="Expense"]
        _rev = _s["Amount"].sum(); _exp = _e["Amount"].sum(); _profit = _rev-_exp; _margin = (_profit/_rev*100) if _rev>0 else 0
        _overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
        _overall, _color, _scores = compute_health_score(df)
        _hl = "Excellent" if _overall>=80 else "Good" if _overall>=65 else "Needs Attention" if _overall>=45 else "Critical"
        _probs = get_top_3_problems(df, industry)
        _acts = get_this_week_actions(df, industry)
        _date_str = datetime.now().strftime("%d %B %Y")
        _te = _e.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index() if len(_e)>0 else pd.DataFrame(columns=["Category","Amount"])
        _tc = _s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(5).reset_index() if len(_s)>0 else pd.DataFrame(columns=["Party","Amount"])
        _exp_rows = "".join([f"<tr><td>{row.Category}</td><td style='text-align:right'>{fmt_inr(row.Amount)}</td><td style='text-align:right'>{row.Amount/_exp*100:.1f}%</td></tr>" for _, row in _te.iterrows()]) if len(_te)>0 else ""
        _cust_rows = "".join([f"<tr><td>{row.Party}</td><td style='text-align:right'>{fmt_inr(row.Amount)}</td></tr>" for _, row in _tc.iterrows()]) if len(_tc)>0 else ""
        _prob_html = "".join([f"<div style='margin-bottom:12px;padding:10px 12px;border-left:3px solid {'#2e7d32' if p['severity']=='green' else '#e65100' if p['severity']=='amber' else '#c62828'};background:#f9f9f9;'><strong>{p['title']}</strong><br><span style='font-size:13px;color:#555'>{p['text'].replace('<strong>','').replace('</strong>','')}</span></div>" for p in _probs])
        _act_html = "".join([f"<li style='margin-bottom:6px;font-size:13px'>{a.replace('<strong>','').replace('</strong>','')}</li>" for a in _acts])
        _owner_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family:Arial;color:#1a1a2e;max-width:800px;margin:40px auto;padding:0 24px;}}h2{{color:#1a1a2e;}}table{{width:100%;border-collapse:collapse;font-size:13px;}}th{{background:#f5f5f0;padding:8px;text-align:left;font-size:11px;text-transform:uppercase;color:#888;}}td{{padding:8px;border-bottom:1px solid #f0f0f0;}}.kpi{{display:inline-block;background:#f8f8f6;border-radius:8px;padding:12px 16px;margin:6px;min-width:120px;}}.kpi-v{{font-size:1.5rem;font-weight:800;color:#1a1a2e;}}.kpi-l{{font-size:10px;text-transform:uppercase;color:#888;}}</style></head><body>
        <h2>OpsClarity — Business Report</h2><p style="color:#888;font-size:13px">Generated: {_date_str}</p>
        <div style="margin:20px 0"><div class="kpi"><div class="kpi-l">Revenue</div><div class="kpi-v">{fmt_inr(_rev)}</div></div><div class="kpi"><div class="kpi-l">Expenses</div><div class="kpi-v">{fmt_inr(_exp)}</div></div><div class="kpi"><div class="kpi-l">Profit</div><div class="kpi-v" style="color:{'#2e7d32' if _profit>=0 else '#c62828'}">{fmt_inr(abs(_profit))}</div></div><div class="kpi"><div class="kpi-l">Margin</div><div class="kpi-v">{abs(_margin):.1f}%</div></div></div>
        <h3>Business Summary</h3><p style="line-height:1.8;font-size:14px">{generate_owner_summary(df,industry).replace('<strong>','<b>').replace('</strong>','</b>')}</p>
        <h3>Priority Issues</h3>{_prob_html}
        <h3>Actions This Week</h3><ul>{_act_html}</ul>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:24px"><div><h3>Expenses</h3><table><tr><th>Category</th><th>Amount</th><th>Share</th></tr>{_exp_rows}</table></div><div><h3>Top Customers</h3><table><tr><th>Customer</th><th>Revenue</th></tr>{_cust_rows}</table></div></div>
        <p style="margin-top:40px;color:#bbb;font-size:11px;border-top:1px solid #eee;padding-top:12px">OpsClarity — Management Estimates Only · {_date_str}</p>
        </body></html>"""
        st.download_button("⬇ Owner HTML", data=_owner_html.encode(), file_name=f"OpsClarity_OwnerReport_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
    with ex4:
        st.markdown("**📸 Score Card**")
        st.download_button("⬇ Score Card", data=generate_score_card_html(df, industry), file_name=f"OpsClarity_ScoreCard_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
    with ex5:
        st.markdown("**📱 WhatsApp**")
        st.text_area("Copy & send:", value=generate_whatsapp_summary(df), height=100, label_visibility="collapsed")
    with ex6:
        st.markdown("**📊 Raw Data**")
        st.download_button("⬇ All Data", data=df.to_csv(index=False).encode(), file_name=f"OpsClarity_Data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

    # ── PAYWALL ───────────────────────────────────────────────────────────────
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
                st.success("Payment integration coming soon! WhatsApp us to pay: wa.me/916362319163")

else:
    st.markdown("""
    <div class="divider"></div>
    <div class="problem-grid">
        <div class="problem-card"><div class="problem-tag green">INSTANT</div><div class="problem-title">P&L in 30 seconds</div><div class="problem-text">Upload any messy file. See revenue, expenses, profit, and health score immediately.</div></div>
        <div class="problem-card"><div class="problem-tag amber">SMART</div><div class="problem-title">Not just charts — actions</div><div class="problem-text">OpsClarity tells you what's wrong and exactly what to do about it.</div></div>
        <div class="problem-card"><div class="problem-tag red">REAL</div><div class="problem-title">Built for actual SME pain</div><div class="problem-text">Profit leaks, overdue cash, rising costs, benchmarks, GST — all in one place.</div></div>
    </div>""", unsafe_allow_html=True)
