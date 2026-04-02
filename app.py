import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io, random, json, time

st.set_page_config(
    page_title="OpsClarity — Business Health for Indian SMEs",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── STYLES ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
.stApp{background:#080810;font-family:'DM Sans',sans-serif;color:#e8e8f0;}
.main .block-container{padding:2rem 3rem;max-width:1500px;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}

/* NAV */
.nav{display:flex;align-items:center;justify-content:space-between;padding:1rem 0 2rem;}
.nav-logo{font-family:'Playfair Display',serif;font-size:1.4rem;color:#f4f1eb;display:flex;align-items:center;gap:8px;}
.nav-logo .dot{color:#c8ff57;}
.nav-tabs{display:flex;gap:4px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:4px;}
.nav-tab{padding:7px 18px;border-radius:8px;font-size:13px;font-weight:600;color:#6b6b80;cursor:pointer;transition:all .2s;border:none;background:transparent;}
.nav-tab.active{background:rgba(200,255,87,.12);color:#c8ff57;}
.nav-badge{background:rgba(200,255,87,.08);border:1px solid rgba(200,255,87,.2);color:#c8ff57;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.08em;}

/* HERO */
.hero{text-align:center;padding:3rem 2rem 2rem;}
.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.2);padding:6px 16px;border-radius:30px;background:rgba(200,255,87,.04);margin-bottom:1.5rem;}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(2.4rem,5.5vw,4.2rem);line-height:1.08;color:#f4f1eb;letter-spacing:-.02em;margin-bottom:1rem;}
.hero-title em{color:#c8ff57;font-style:italic;}
.hero-sub{max-width:580px;margin:0 auto 2rem;font-size:1.05rem;color:#6b6b80;line-height:1.75;font-weight:300;}
.hero-stats{display:flex;justify-content:center;gap:2.5rem;font-size:12px;color:#505060;}
.hero-stats strong{color:#9090a8;font-weight:600;}

/* UPLOAD */
.upload-section{background:rgba(255,255,255,.025);border:1.5px dashed rgba(200,255,87,.25);border-radius:24px;padding:2rem;margin:1.5rem 0;}
.upload-title{font-size:13px;font-weight:600;color:#6b6b80;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1rem;}

/* ALERT BANNER */
.alert-critical{background:linear-gradient(135deg,rgba(255,80,80,.12),rgba(255,80,80,.04));border:1.5px solid rgba(255,80,80,.3);border-radius:18px;padding:1.5rem 2rem;margin:1rem 0;display:flex;gap:1.2rem;align-items:flex-start;}
.alert-warning{background:linear-gradient(135deg,rgba(255,181,80,.1),rgba(255,181,80,.03));border:1.5px solid rgba(255,181,80,.25);border-radius:18px;padding:1.5rem 2rem;margin:1rem 0;display:flex;gap:1.2rem;align-items:flex-start;}
.alert-success{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1.5px solid rgba(200,255,87,.2);border-radius:18px;padding:1.5rem 2rem;margin:1rem 0;display:flex;gap:1.2rem;align-items:flex-start;}
.alert-icon{font-size:2rem;flex-shrink:0;margin-top:2px;}
.alert-headline{font-family:'Playfair Display',serif;font-size:1.35rem;line-height:1.2;margin-bottom:.4rem;}
.alert-critical .alert-headline{color:#ff7070;}
.alert-warning .alert-headline{color:#ffb557;}
.alert-success .alert-headline{color:#c8ff57;}
.alert-body{color:#9090a4;font-size:.95rem;line-height:1.65;margin-bottom:.8rem;}
.alert-cta{display:inline-block;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:8px 16px;font-size:13px;color:#c8ff57;font-weight:600;}

/* KPI STRIP */
.kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:1.5rem 0;}
.kpi{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:1.2rem 1.4rem;position:relative;overflow:hidden;transition:border-color .2s;}
.kpi:hover{border-color:rgba(255,255,255,.12);}
.kpi::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;}
.kpi.g::after{background:linear-gradient(90deg,#c8ff57,transparent);}
.kpi.r::after{background:linear-gradient(90deg,#ff5e5e,transparent);}
.kpi.a::after{background:linear-gradient(90deg,#ffb557,transparent);}
.kpi.b::after{background:linear-gradient(90deg,#57b8ff,transparent);}
.kpi-label{font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:#4a4a60;font-weight:700;margin-bottom:8px;}
.kpi-val{font-family:'Playfair Display',serif;font-size:2rem;color:#f4f1eb;line-height:1;margin-bottom:4px;}
.kpi-sub{font-size:11px;color:#5a5a70;font-family:'JetBrains Mono',monospace;}

/* HEALTH SCORE */
.health-card{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:1.8rem;}
.hs-ring{position:relative;display:flex;align-items:center;justify-content:center;width:110px;height:110px;margin-bottom:1rem;}
.hs-num{font-family:'Playfair Display',serif;font-size:2.8rem;line-height:1;position:absolute;}
.hs-label{font-size:11px;color:#5a5a70;text-transform:uppercase;letter-spacing:.08em;margin-bottom:1.2rem;}
.hs-metric{margin-bottom:10px;}
.hs-metric-name{font-size:11px;color:#5a5a70;margin-bottom:4px;display:flex;justify-content:space-between;}
.hs-bar{height:3px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;}
.hs-fill{height:100%;border-radius:99px;transition:width .6s ease;}

/* PROBLEM CARDS */
.prob-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.prob-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:1.2rem;transition:all .2s;}
.prob-card:hover{background:rgba(255,255,255,.035);border-color:rgba(255,255,255,.1);}
.prob-badge{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:999px;margin-bottom:10px;}
.prob-badge.critical{color:#ff7070;background:rgba(255,80,80,.08);border:1px solid rgba(255,80,80,.18);}
.prob-badge.warning{color:#ffcb70;background:rgba(255,181,80,.08);border:1px solid rgba(255,181,80,.18);}
.prob-badge.good{color:#c8ff57;background:rgba(200,255,87,.06);border:1px solid rgba(200,255,87,.15);}
.prob-title{font-weight:700;color:#e8e8f0;font-size:.95rem;margin-bottom:6px;line-height:1.4;}
.prob-text{color:#7070838;font-size:13px;line-height:1.6;color:#707083;margin-bottom:10px;}
.prob-action{background:rgba(200,255,87,.04);border-left:3px solid rgba(200,255,87,.3);padding:8px 12px;border-radius:0 8px 8px 0;font-size:12px;color:#8888a0;line-height:1.5;}

/* CA DASHBOARD */
.ca-header{background:linear-gradient(135deg,rgba(87,184,255,.08),rgba(87,184,255,.02));border:1px solid rgba(87,184,255,.2);border-radius:20px;padding:1.5rem 2rem;margin-bottom:1.5rem;display:flex;align-items:center;justify-content:space-between;}
.ca-title{font-family:'Playfair Display',serif;font-size:1.4rem;color:#57b8ff;}
.ca-sub{color:#5a5a70;font-size:13px;margin-top:4px;}
.client-table{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:16px;overflow:hidden;}
.client-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;gap:12px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.04);align-items:center;transition:background .15s;}
.client-row:hover{background:rgba(255,255,255,.025);}
.client-row.header{background:rgba(255,255,255,.03);font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#4a4a60;font-weight:700;border-bottom:1px solid rgba(255,255,255,.08);}
.score-pill{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px;}

/* AI CHAT */
.chat-wrap{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:1.5rem;max-height:420px;overflow-y:auto;}
.chat-msg{margin-bottom:1rem;display:flex;gap:10px;}
.chat-msg.user{flex-direction:row-reverse;}
.chat-bubble{max-width:80%;padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.6;}
.chat-msg.ai .chat-bubble{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);color:#c8c8d8;}
.chat-msg.user .chat-bubble{background:rgba(200,255,87,.08);border:1px solid rgba(200,255,87,.15);color:#e8e8f0;}
.chat-avatar{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;margin-top:2px;}
.chat-msg.ai .chat-avatar{background:rgba(200,255,87,.1);color:#c8ff57;}
.chat-msg.user .chat-avatar{background:rgba(255,255,255,.05);color:#9090a8;}

/* ACTIONS */
.action-item{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.05);border-radius:12px;padding:12px 16px;margin-bottom:8px;display:flex;gap:12px;align-items:flex-start;font-size:14px;color:#b0b0c0;line-height:1.55;}
.action-num{font-family:'Playfair Display',serif;font-size:1.4rem;color:#c8ff57;flex-shrink:0;line-height:1;}

/* PAYWALL */
.paywall{background:linear-gradient(135deg,rgba(200,255,87,.06),rgba(200,255,87,.01));border:1px solid rgba(200,255,87,.18);border-radius:24px;padding:2.5rem;text-align:center;margin:2rem 0;}
.pw-title{font-family:'Playfair Display',serif;font-size:1.9rem;color:#f4f1eb;margin-bottom:.5rem;}
.pw-sub{color:#5a5a70;font-size:14px;margin-bottom:1.5rem;}
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:1.5rem 0;text-align:left;}
.price-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:1.4rem;}
.price-card.featured{background:rgba(200,255,87,.06);border-color:rgba(200,255,87,.25);}
.price-who{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#5a5a70;font-weight:700;margin-bottom:.5rem;}
.price-amt{font-family:'Playfair Display',serif;font-size:2rem;color:#f4f1eb;line-height:1;margin-bottom:.3rem;}
.price-amt .per{font-family:'DM Sans',sans-serif;font-size:12px;color:#5a5a70;font-weight:400;}
.price-title{font-weight:700;color:#c8c8d8;margin-bottom:.6rem;}
.price-features{list-style:none;font-size:12px;color:#6b6b80;line-height:2;}
.price-features li::before{content:"✓ ";color:#c8ff57;}

/* SHARE */
.share-bar{display:flex;gap:10px;margin:1rem 0;}
.share-btn{flex:1;padding:11px;border-radius:12px;text-align:center;font-size:13px;font-weight:700;text-decoration:none;cursor:pointer;border:none;}
.share-wa{background:#25D366;color:white;}
.share-dl{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:#c8c8d8;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;border:1px solid rgba(255,255,255,.06)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#5a5a70!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;padding:8px 16px!important;}
.stTabs [aria-selected="true"]{background:rgba(200,255,87,.1)!important;color:#c8ff57!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1.2rem!important;}

/* BUTTONS */
.stButton>button{background:#c8ff57!important;color:#080810!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:.7rem 1.8rem!important;transition:all .2s!important;}
.stButton>button:hover{background:#d4ff6e!important;transform:translateY(-1px);}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,.05)!important;color:#8888a0!important;border:1px solid rgba(255,255,255,.08)!important;}

/* INPUTS */
[data-testid="stFileUploader"]{background:rgba(255,255,255,.02)!important;border:1.5px dashed rgba(200,255,87,.2)!important;border-radius:16px!important;}
.stSelectbox>div>div{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:12px!important;color:#e8e8f0!important;}
.stTextInput>div>div>input{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:12px!important;color:#e8e8f0!important;}
.stTextInput>div>div>input:focus{border-color:rgba(200,255,87,.4)!important;box-shadow:0 0 0 2px rgba(200,255,87,.1)!important;}

/* MISC */
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent);margin:2rem 0;}
.section-title{font-family:'Playfair Display',serif;font-size:1.3rem;color:#f4f1eb;margin:1.5rem 0 .4rem;}
.section-sub{color:#5a5a70;font-size:13px;margin-bottom:1rem;}
.mono{font-family:'JetBrains Mono',monospace;font-size:13px;}
.tag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:999px;margin-right:4px;}
.whatsapp-float{position:fixed;bottom:24px;right:24px;background:#25D366;color:white;padding:11px 18px;border-radius:50px;font-weight:700;font-size:13px;text-decoration:none;display:flex;align-items:center;gap:8px;box-shadow:0 4px 20px rgba(37,211,102,.25);z-index:1000;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🍽️ Restaurant / Cafe": "restaurant",
    "🏥 Clinic / Diagnostic Lab": "clinic",
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting": "agency",
}
INDUSTRY_BENCHMARKS = {"restaurant": 18, "clinic": 25, "retail": 15, "agency": 30}
TESTIMONIALS = [
    {"name": "Rahul S.", "biz": "Metro Traders, Bangalore", "quote": "Found ₹3.2L in overdue invoices I had forgotten about. Recovered in 2 weeks."},
    {"name": "Dr. Priya M.", "biz": "City Diagnostics, Mumbai", "quote": "Finally understand my clinic's finances without waiting for my CA every month."},
    {"name": "Kiran G.", "biz": "Spice Garden Restaurant", "quote": "Cut food costs by 12% in one month using the expense breakdown."},
    {"name": "Suresh CA", "biz": "S&P Associates, Chennai", "quote": "Now I give every client a monthly health score. They love it."},
]

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def fmt(val):
    val = float(val)
    if abs(val) >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif abs(val) >= 1_00_000:   return f"₹{val/1_00_000:.1f}L"
    elif abs(val) >= 1_000:      return f"₹{val/1000:.1f}k"
    return f"₹{abs(val):.0f}"

def make_df(records):
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

# ─── SAMPLE DATA ─────────────────────────────────────────────────────────────
def generate_data(industry, seed=42):
    random.seed(seed); np.random.seed(seed)
    cfg = {
        "restaurant": {"customers": ["Ravi Enterprises","Meena Stores","Krishna Traders","Sunita Foods","Ramesh & Sons"], "cats": ["Raw Materials","Staff Salary","Rent","Electricity","Transport","Marketing"]},
        "clinic":     {"customers": ["Apollo Health","MedCare Trust","Sharma Family","Reddy Clinic","City Hospital"], "cats": ["Doctor Salaries","Medicines","Rent","Electricity","Equipment","Lab Reagents"]},
        "retail":     {"customers": ["Wholesale Hub","Metro Traders","Quick Mart","Singh Distributors","Raj Superstore"], "cats": ["Inventory Purchase","Staff Wages","Rent","Electricity","Transport","Marketing"]},
        "agency":     {"customers": ["TechStart Pvt Ltd","Growfast Brands","UrbanEats","BuildRight Infra","FinEdge Solutions"], "cats": ["Salaries","Software","Rent","Electricity","Freelancers","Marketing"]},
    }
    c = cfg[industry]
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        n = random.randint(15, 30)
        for _ in range(n):
            records.append({
                "Date": month - timedelta(days=random.randint(0, 28)),
                "Type": "Sales", "Category": "Sales",
                "Party": random.choice(c["customers"]),
                "Amount": round(random.uniform(5000, 85000 if industry != "agency" else 350000), 0),
                "Status": random.choice(["Paid","Paid","Paid","Overdue","Pending"]),
                "Invoice_No": f"INV-{random.randint(1000,9999)}"
            })
        for cat in c["cats"]:
            amt = round(random.uniform(2000, 45000 if industry != "agency" else 200000), 0)
            if cat in ["Electricity","Raw Materials","Inventory Purchase"]: amt *= 1.5
            records.append({
                "Date": month - timedelta(days=random.randint(0, 28)),
                "Type": "Expense", "Category": cat, "Party": "Vendor",
                "Amount": round(amt, 0), "Status": "Paid",
                "Invoice_No": f"EXP-{random.randint(1000,9999)}"
            })
    return make_df(records)

# ─── FILE PARSER ─────────────────────────────────────────────────────────────
def parse_file(file):
    try:
        fname = file.name.lower()
        try:
            df = pd.read_csv(file) if fname.endswith(".csv") else pd.read_excel(file, engine="openpyxl")
        except Exception:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin1") if fname.endswith(".csv") else pd.read_excel(file, engine="openpyxl", header=1)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher date"]): col_map[col] = "Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit"]): col_map[col] = "Amount"
            elif any(x in cl for x in ["type","txn type","dr/cr","nature"]): col_map[col] = "Type"
            elif any(x in cl for x in ["category","cat","head","narration","ledger"]): col_map[col] = "Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client"]): col_map[col] = "Party"
            elif any(x in cl for x in ["status","paid","cleared"]): col_map[col] = "Status"
            elif any(x in cl for x in ["invoice","bill no","voucher","ref"]): col_map[col] = "Invoice_No"
        df = df.rename(columns=col_map)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
            df = df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"] = (df["Amount"].astype(str)
                .str.replace(",","",regex=False)
                .str.replace("(","-",regex=False)
                .str.replace(")","",regex=False))
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"] = "Sales"
        df["Type"] = df["Type"].astype(str).str.strip().str.title()
        df["Type"] = df["Type"].replace({
            "Dr":"Expense","Cr":"Sales","Debit":"Expense","Credit":"Sales",
            "Out":"Expense","In":"Sales","Payment":"Expense","Receipt":"Sales",
            "Purchase":"Expense","Sale":"Sales"
        })
        df.loc[~df["Type"].isin(["Sales","Expense"]), "Type"] = "Sales"
        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","—")]:
            if col not in df.columns: df[col] = default
        df = df.drop_duplicates()
        if "Month" not in df.columns and "Date" in df.columns:
            df["Month"] = df["Date"].dt.to_period("M").astype(str)
        return df, True, f"✓ Loaded {len(df):,} transactions"
    except Exception as ex:
        return None, False, str(ex)

# ─── ANALYTICS ───────────────────────────────────────────────────────────────
def health_score(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0

    def score_margin(m):
        if m>20: return (90,"#c8ff57")
        elif m>12: return (75,"#c8ff57")
        elif m>5:  return (55,"#ffb557")
        elif m>0:  return (35,"#ffb557")
        return (15,"#ff5e5e")

    sm = s.groupby("Month")["Amount"].sum().sort_index()
    def score_trend():
        if len(sm)<3: return (60,"#ffb557")
        trend = (sm.iloc[-1]-sm.iloc[-3])/max(sm.iloc[-3],1)*100
        if trend>15: return (88,"#c8ff57")
        elif trend>0: return (70,"#c8ff57")
        elif trend>-10: return (50,"#ffb557")
        return (25,"#ff5e5e")

    op = (overdue/rev*100) if rev>0 else 0
    def score_collections():
        if op<3:  return (92,"#c8ff57")
        elif op<10: return (70,"#c8ff57")
        elif op<20: return (45,"#ffb557")
        return (20,"#ff5e5e")

    cr = (exp/rev*100) if rev>0 else 100
    def score_costs():
        if cr<55:  return (88,"#c8ff57")
        elif cr<70: return (68,"#c8ff57")
        elif cr<85: return (42,"#ffb557")
        return (18,"#ff5e5e")

    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    def score_diversity():
        if len(tc)==0: return (50,"#ffb557")
        conc = (tc.max()/rev*100) if rev>0 else 0
        if conc<25:  return (85,"#c8ff57")
        elif conc<40: return (65,"#c8ff57")
        elif conc<55: return (40,"#ffb557")
        return (20,"#ff5e5e")

    scores = {
        "Profit Margin": score_margin(margin),
        "Revenue Trend": score_trend(),
        "Collections":   score_collections(),
        "Cost Efficiency": score_costs(),
        "Client Diversity": score_diversity(),
    }
    overall = int(sum(v for v,_ in scores.values())/len(scores))
    color = "#c8ff57" if overall>=75 else "#ffb557" if overall>=50 else "#ff5e5e"
    return overall, color, scores, margin, overdue

def killer_insight(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    bench = INDUSTRY_BENCHMARKS.get(industry, 15)
    insights = []

    if overdue > rev * 0.08:
        insights.append({"priority":1,"sev":"critical","icon":"🚨",
            "headline":f"₹{overdue/1e5:.1f}L stuck in unpaid invoices",
            "body":f"{(overdue/rev*100):.1f}% of annual revenue is locked. Cash flow is bleeding daily.",
            "cta":"Call your top 3 overdue customers this week — offer 2% discount for immediate payment."})
    if margin < bench - 7:
        gap = ((bench-margin)/100)*rev
        top_exp = e.groupby("Category")["Amount"].sum().idxmax() if len(e)>0 else "expenses"
        insights.append({"priority":2,"sev":"warning","icon":"📉",
            "headline":f"Profit margin {margin:.1f}% — industry avg is {bench}%",
            "body":f"You're earning {fmt(gap)} less per year than comparable {industry} businesses.",
            "cta":f"Audit {top_exp} immediately. Even 5% cut = significant profit boost."})
    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    if len(tc)>0 and (tc.max()/rev*100) > 45:
        insights.append({"priority":3,"sev":"warning","icon":"🎯",
            "headline":f"One customer = {(tc.max()/rev*100):.0f}% of revenue",
            "body":f"{tc.idxmax()} has dangerous power over your business.",
            "cta":"Land 2 new customers this quarter. Never let one client exceed 30%."})
    em = e.groupby("Month")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    if len(em)>=3 and em.iloc[-1] > em.iloc[:-1].mean()*1.4:
        spike = em.iloc[-1]-em.iloc[:-1].mean()
        insights.append({"priority":4,"sev":"warning","icon":"🔥",
            "headline":f"Expenses jumped {((em.iloc[-1]/em.iloc[:-1].mean()-1)*100):.0f}% last month",
            "body":f"You spent {fmt(spike)} more than usual. This will kill profit if it continues.",
            "cta":"Review last month's bills line by line. Find the leak before next month."})
    if margin > bench and overdue < rev*0.05:
        insights.append({"priority":5,"sev":"success","icon":"🌟",
            "headline":f"Strong performance — {margin:.1f}% margin, healthy collections",
            "body":f"You're outperforming most {industry} businesses. Keep this discipline.",
            "cta":"Automate collections, lock supplier contracts, document what's working."})
    return min(insights, key=lambda x: x["priority"]) if insights else None

def top_problems(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    bench = INDUSTRY_BENCHMARKS.get(industry, 15)
    problems = []

    if margin < 5:
        te = e.groupby("Category")["Amount"].sum()
        top_exp = te.idxmax() if len(te)>0 else "expenses"
        problems.append({"sev":"critical","title":"Profit margin critically thin",
            "text":f"Your margin is only <strong>{margin:.1f}%</strong>. Working hard, keeping almost nothing.",
            "action":f"Cut <strong>{top_exp}</strong> by 15% this month — fastest path to profit."})
    elif margin < bench:
        problems.append({"sev":"warning","title":"Margin below industry average",
            "text":f"At <strong>{margin:.1f}%</strong> vs {bench}% benchmark. Little buffer for surprises.",
            "action":"Raise prices 5% or cut top 2 expenses. Small moves, big protection."})
    else:
        problems.append({"sev":"good","title":"Profitability is healthy",
            "text":f"<strong>{margin:.1f}% margin</strong> gives real business cushion.",
            "action":"Review expenses monthly. Lock in supplier rates now."})

    if overdue > rev*0.1:
        problems.append({"sev":"critical","title":"Cash crisis: collections overdue",
            "text":f"<strong>{fmt(overdue)}</strong> overdue — {(overdue/rev*100):.1f}% of revenue sitting idle.",
            "action":"Call every overdue customer today. Offer 2% discount for payment this week."})
    elif overdue > 0:
        problems.append({"sev":"warning","title":f"{fmt(overdue)} in overdue invoices",
            "text":f"{(overdue/rev*100):.1f}% of revenue delayed. Not critical yet — act now.",
            "action":"Set weekly collection reminders. Don't let this grow."})
    else:
        problems.append({"sev":"good","title":"Collections are clean",
            "text":"No meaningful overdue invoices. Cash flow discipline is strong.",
            "action":"Keep this up. Review credit terms for new customers."})

    tc = s.groupby("Party")["Amount"].sum() if len(s)>0 else pd.Series(dtype=float)
    if len(tc)>0 and (tc.max()/rev*100) > 40:
        problems.append({"sev":"warning","title":"Dangerous customer concentration",
            "text":f"<strong>{tc.idxmax()}</strong> = {(tc.max()/rev*100):.0f}% of revenue. One decision by them changes everything.",
            "action":"Sign 2 new clients this quarter. Diversify or remain vulnerable."})
    else:
        te = e.groupby("Category")["Amount"].sum()
        if len(te)>0:
            top_exp = te.idxmax(); top_pct = (te.max()/exp*100) if exp>0 else 0
            problems.append({"sev":"warning" if top_pct>30 else "good",
                "title":f"{top_exp} = {top_pct:.0f}% of total costs",
                "text":"Your biggest expense. Small % changes = large ₹ impact.",
                "action":"Get 3 vendor quotes. Negotiate or switch supplier."})
    return problems[:3]

def weekly_actions(df, industry):
    e = df[df["Type"]=="Expense"]
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum() if len(e)>0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te)>0 else "biggest expense"
    actions = []
    if overdue > 50000:
        actions.append(f"🚨 <strong>Urgent:</strong> Call top 3 overdue customers. Recover {fmt(overdue)} this week.")
    actions.append(f"🔍 Review last 10 payments to <strong>{top_exp}</strong>. Flag any unusual jumps.")
    actions.append("📊 Verify this month's revenue has actually cleared in your bank (not just invoiced).")
    actions.append("💰 Pick one recurring expense to cut, renegotiate, or pause this month.")
    industry_tip = {
        "restaurant": "🍽️ Audit food wastage and compare 3 supplier quotes for raw materials this week.",
        "clinic": "🏥 Check consultation → lab conversion. Are you capturing full patient visit value?",
        "retail": "🛒 Identify slow-moving SKUs. Clear dead stock now before next buying cycle.",
        "agency": "💼 Match team salary costs to billable hours. Are you carrying idle capacity?",
    }
    actions.append(industry_tip.get(industry,"📈 Review your top 5 customers and check if any need follow-up."))
    return actions[:5]

def build_context_string(df, industry):
    """Build a compact financial summary for the AI advisor"""
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(5) if len(e)>0 else pd.Series()
    tc = s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(3) if len(s)>0 else pd.Series()
    overall, _, _, _, _ = health_score(df)
    lines = [
        f"Industry: {industry}",
        f"Revenue: {fmt(rev)}, Expenses: {fmt(exp)}, Profit: {fmt(profit)}, Margin: {margin:.1f}%",
        f"Overdue invoices: {fmt(overdue)} ({(overdue/rev*100) if rev>0 else 0:.1f}% of revenue)",
        f"Health score: {overall}/100",
        f"Top expense categories: {', '.join(f'{k} ({fmt(v)})' for k,v in te.items())}",
        f"Top customers: {', '.join(f'{k} ({fmt(v)})' for k,v in tc.items())}",
        f"Total transactions: {len(df)}",
    ]
    return "\n".join(lines)

# ─── CA MOCK CLIENTS ──────────────────────────────────────────────────────────
def get_ca_clients():
    return [
        {"name":"Metro Traders","type":"retail","score":82,"color":"#c8ff57","revenue":"₹48L","margin":"17%","overdue":"₹1.2L","status":"healthy","last":"2 days ago"},
        {"name":"Spice Garden","type":"restaurant","score":61,"color":"#ffb557","revenue":"₹22L","margin":"11%","overdue":"₹3.8L","status":"warning","last":"1 week ago"},
        {"name":"CityDx Lab","type":"clinic","score":74,"color":"#c8ff57","revenue":"₹85L","margin":"22%","overdue":"₹0","status":"healthy","last":"Today"},
        {"name":"GrowFast Agency","type":"agency","score":44,"color":"#ff5e5e","revenue":"₹1.2Cr","margin":"6%","overdue":"₹18L","status":"critical","last":"3 days ago"},
        {"name":"Raj Electronics","type":"retail","score":68,"color":"#ffb557","revenue":"₹31L","margin":"14%","overdue":"₹2.1L","status":"warning","last":"5 days ago"},
    ]

# ─── SESSION STATE ────────────────────────────────────────────────────────────
defaults = {"df":None,"industry":"restaurant","page":"sme","chat_history":[],"spots":73}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ─── NAV ──────────────────────────────────────────────────────────────────────
t = random.choice(TESTIMONIALS)
st.markdown(f"""
<div class="nav">
    <div class="nav-logo">◈<span class="dot"> OpsClarity</span></div>
    <div style="display:flex;gap:12px;align-items:center;">
        <div class="nav-badge">Free for first 100 businesses</div>
    </div>
</div>
""", unsafe_allow_html=True)

page_col1, page_col2, page_col3 = st.columns([1,1,4])
with page_col1:
    if st.button("📊 SME Dashboard", use_container_width=True,
                 type="primary" if st.session_state.page=="sme" else "secondary"):
        st.session_state.page = "sme"; st.rerun()
with page_col2:
    if st.button("🏛️ CA Portal", use_container_width=True,
                 type="primary" if st.session_state.page=="ca" else "secondary"):
        st.session_state.page = "ca"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CA PORTAL
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "ca":
    st.markdown("""
    <div class="ca-header">
        <div>
            <div class="ca-title">CA Practice Dashboard</div>
            <div class="ca-sub">Monitor all your clients' financial health in one view. Powered by OpsClarity.</div>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Playfair Display',serif;font-size:2rem;color:#57b8ff;">5</div>
            <div style="font-size:12px;color:#5a5a70;">Active clients</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    clients = get_ca_clients()
    critical = [c for c in clients if c["status"]=="critical"]
    warnings = [c for c in clients if c["status"]=="warning"]

    if critical:
        st.markdown(f"""
        <div class="alert-critical">
            <div class="alert-icon">🚨</div>
            <div>
                <div class="alert-headline">{len(critical)} client(s) need urgent attention</div>
                <div class="alert-body">{', '.join(c['name'] for c in critical)} — low health score and/or large overdue amounts. Review and contact them today.</div>
                <div class="alert-cta">View details below ↓</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Summary strip
    avg_score = int(sum(c["score"] for c in clients)/len(clients))
    st.markdown(f"""
    <div class="kpi-strip">
        <div class="kpi b"><div class="kpi-label">Avg Health Score</div><div class="kpi-val">{avg_score}</div><div class="kpi-sub mono">across 5 clients</div></div>
        <div class="kpi r"><div class="kpi-label">Critical Clients</div><div class="kpi-val">{len(critical)}</div><div class="kpi-sub mono">need action now</div></div>
        <div class="kpi a"><div class="kpi-label">Warning Clients</div><div class="kpi-val">{len(warnings)}</div><div class="kpi-sub mono">monitor closely</div></div>
        <div class="kpi g"><div class="kpi-label">Healthy Clients</div><div class="kpi-val">{len([c for c in clients if c['status']=='healthy'])}</div><div class="kpi-sub mono">on track</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Client table
    st.markdown('<div class="section-title">Client Portfolio</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="client-table">
        <div class="client-row header">
            <span>Client</span><span>Score</span><span>Revenue</span><span>Margin</span><span>Overdue</span><span>Last Updated</span>
        </div>
    """, unsafe_allow_html=True)

    for c in clients:
        status_colors = {"healthy":"#c8ff57","warning":"#ffb557","critical":"#ff5e5e"}
        sc_color = status_colors[c["status"]]
        st.markdown(f"""
        <div class="client-row">
            <div>
                <div style="font-weight:600;color:#e8e8f0;">{c['name']}</div>
                <div style="font-size:11px;color:#5a5a70;text-transform:capitalize;">{c['type']}</div>
            </div>
            <div><div class="score-pill" style="background:rgba(0,0,0,0.3);border:2px solid {sc_color};color:{sc_color};">{c['score']}</div></div>
            <div style="color:#c8c8d8;font-size:14px;">{c['revenue']}</div>
            <div style="color:#c8c8d8;font-size:14px;">{c['margin']}</div>
            <div style="color:{'#ff7070' if c['overdue'] != '₹0' else '#c8ff57'};font-size:14px;">{c['overdue']}</div>
            <div style="color:#5a5a70;font-size:12px;">{c['last']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # CA Tools
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="section-title">GST Liability Estimates</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Management estimates across client portfolio — verify before filing</div>', unsafe_allow_html=True)
        gst_data = {"Client":["Metro Traders","Spice Garden","CityDx Lab","GrowFast Agency","Raj Electronics"],
                    "Output GST":["₹2.4L","₹1.1L","₹4.3L","₹6L","₹1.6L"],
                    "Input GST":["₹1.8L","₹0.9L","₹2.1L","₹3.2L","₹1.2L"],
                    "Net Payable":["₹0.6L","₹0.2L","₹2.2L","₹2.8L","₹0.4L"]}
        st.dataframe(pd.DataFrame(gst_data), hide_index=True, use_container_width=True)
        st.info("⚠️ Estimates only. Reconcile against GSTR-2A before filing.")

    with col_t2:
        st.markdown('<div class="section-title">Monthly Report Templates</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">WhatsApp-ready summaries to send to clients</div>', unsafe_allow_html=True)
        for c in clients[:3]:
            sc_color = {"healthy":"#c8ff57","warning":"#ffb557","critical":"#ff5e5e"}[c["status"]]
            emoji = {"healthy":"🟢","warning":"🟡","critical":"🔴"}[c["status"]]
            st.markdown(f"""
            <div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:13px;color:#c8c8d8;">{emoji} {c['name']} — Score {c['score']}/100</div>
                <div style="font-size:11px;color:#5a5a70;cursor:pointer;">📱 Send</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Paywall for CA
    st.markdown("""
    <div class="paywall">
        <div class="pw-title">Start Your CA Practice Plan</div>
        <div class="pw-sub">Give every client a monthly health score. Become the most proactive CA they've ever had.</div>
        <div class="pricing-grid">
            <div class="price-card">
                <div class="price-who">For SME Owners</div>
                <div class="price-amt">₹499 <span class="per">/mo</span></div>
                <div class="price-title">Pro Plan</div>
                <ul class="price-features">
                    <li>Unlimited uploads</li>
                    <li>12-month trend history</li>
                    <li>WhatsApp alerts</li>
                    <li>AI advisor (Ask OpsClarity)</li>
                    <li>Downloadable reports</li>
                </ul>
            </div>
            <div class="price-card featured">
                <div class="price-who">For Chartered Accountants</div>
                <div class="price-amt">₹1,999 <span class="per">/mo</span></div>
                <div class="price-title">CA Plan ⭐</div>
                <ul class="price-features">
                    <li>50 client seats</li>
                    <li>CA practice dashboard</li>
                    <li>GST liability estimates</li>
                    <li>White-label reports</li>
                    <li>Priority WhatsApp support</li>
                </ul>
            </div>
            <div class="price-card">
                <div class="price-who">For CA Firms</div>
                <div class="price-amt">₹7,999 <span class="per">/mo</span></div>
                <div class="price-title">Firm Plan</div>
                <ul class="price-features">
                    <li>Unlimited clients</li>
                    <li>Team access (5+ CAs)</li>
                    <li>Branded portal</li>
                    <li>API access</li>
                    <li>Dedicated account manager</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col_cta1, col_cta2, col_cta3 = st.columns([1,2,1])
    with col_cta2:
        if st.button("🏛️ Start Free CA Trial — 30 Days", use_container_width=True, type="primary"):
            st.balloons()
            st.success("✅ CA trial activated! Check your WhatsApp for onboarding steps.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SME DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:
    # Hero
    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">◈ Trusted by 150+ Indian SMEs</div>
        <h1 class="hero-title">Find where your business<br>is <em>leaking money</em> — instantly</h1>
        <p class="hero-sub">Upload your Tally, Excel, or bank statement. Get your health score, top problems, and specific actions. No finance knowledge needed.</p>
        <div class="hero-stats">
            <span>✓ <strong>₹12Cr+</strong> analyzed</span>
            <span>✓ <strong>150+</strong> businesses</span>
            <span>✓ <strong>Free forever</strong> tier</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uc1, uc2 = st.columns([2,1])
    with uc1:
        uploaded = st.file_uploader(
            "📁 Drop your file — CSV, Excel (.xlsx), Tally export, or bank statement",
            type=["csv","xlsx","xls"]
        )
        with st.expander("📋 How to export from Tally (3 clicks)"):
            st.markdown("""
**Tally Prime / ERP9:**
1. Go to **Display → Account Books → Day Book**
2. Press **Alt+E** → Select **Excel** format
3. Set date range → Export → Upload here

Works with: Day Book, Sales Register, Purchase Register, Bank Statement, any Excel/CSV
            """)
    with uc2:
        industry_name = st.selectbox("Your industry", list(INDUSTRY_MAP.keys()), label_visibility="collapsed")
        ind = INDUSTRY_MAP[industry_name]
        if st.button("🔄 Try with sample data", use_container_width=True):
            st.session_state.df = generate_data(ind)
            st.session_state.industry = ind
            st.rerun()
        t = random.choice(TESTIMONIALS)
        st.markdown(f"""
        <div style="background:rgba(200,255,87,0.04);border:1px solid rgba(200,255,87,0.12);border-radius:12px;padding:12px 14px;margin-top:8px;">
            <div style="color:#c8ff57;font-style:italic;font-size:13px;line-height:1.6;margin-bottom:6px;">"{t['quote']}"</div>
            <div style="color:#5a5a70;font-size:11px;">— {t['name']}, {t['biz']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle upload
    if uploaded:
        df_up, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_up
            st.session_state.industry = ind
            st.success(msg)
        else:
            st.error(f"❌ Could not parse file: {msg}. Try saving as CSV, or contact us on WhatsApp.")

    # ── DASHBOARD ──────────────────────────────────────────────────────────────
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        industry = st.session_state.industry

        # Date filter
        if "Date" in df.columns and df["Date"].notna().any():
            min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
            dc1, dc2, dc3 = st.columns([1,1,2])
            with dc1:
                start_d = st.date_input("From", value=min_d, min_value=min_d, max_value=max_d)
            with dc2:
                end_d = st.date_input("To", value=max_d, min_value=min_d, max_value=max_d)
            with dc3:
                st.markdown(f"<div style='padding-top:1.8rem;color:#4a4a60;font-size:12px;font-family:\"JetBrains Mono\",monospace;'>{len(df):,} transactions • {start_d.strftime('%d %b')} → {end_d.strftime('%d %b %Y')}</div>", unsafe_allow_html=True)
            df = df[(df["Date"].dt.date>=start_d)&(df["Date"].dt.date<=end_d)]

        s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
        rev = s["Amount"].sum(); exp = e["Amount"].sum(); profit = rev - exp
        overall, hs_color, scores, margin, overdue = health_score(df)

        # Killer insight
        ki = killer_insight(df, industry)
        if ki:
            cls = ki["sev"]
            st.markdown(f"""
            <div class="alert-{cls}">
                <div class="alert-icon">{ki['icon']}</div>
                <div>
                    <div class="alert-headline">{ki['headline']}</div>
                    <div class="alert-body">{ki['body']}</div>
                    <div class="alert-cta">This week: {ki['cta']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # KPI strip
        st.markdown(f"""
        <div class="kpi-strip">
            <div class="kpi g">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-val">{fmt(rev)}</div>
                <div class="kpi-sub mono">{len(s)} transactions</div>
            </div>
            <div class="kpi r">
                <div class="kpi-label">Total Expenses</div>
                <div class="kpi-val">{fmt(exp)}</div>
                <div class="kpi-sub mono">{len(e)} transactions</div>
            </div>
            <div class="kpi {'g' if profit>=0 else 'r'}">
                <div class="kpi-label">Net {'Profit' if profit>=0 else 'Loss'}</div>
                <div class="kpi-val">{fmt(abs(profit))}</div>
                <div class="kpi-sub mono">{abs(margin):.1f}% margin</div>
            </div>
            <div class="kpi a">
                <div class="kpi-label">Overdue</div>
                <div class="kpi-val">{fmt(overdue)}</div>
                <div class="kpi-sub mono">{(overdue/rev*100) if rev>0 else 0:.1f}% of revenue</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Health + Problems
        col_h, col_p = st.columns([1, 2.5])

        with col_h:
            hs_label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs Work" if overall>=45 else "Critical"
            st.markdown(f"""
            <div class="health-card">
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;color:{hs_color};line-height:1;">{overall}</div>
                <div class="hs-label">{hs_label} · Health Score</div>
            """, unsafe_allow_html=True)
            for name, (sc, cl) in scores.items():
                st.markdown(f"""
                <div class="hs-metric">
                    <div class="hs-metric-name"><span>{name}</span><span style="color:{cl}">{sc}</span></div>
                    <div class="hs-bar"><div class="hs-fill" style="width:{sc}%;background:{cl};"></div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_p:
            st.markdown('<div class="section-title">Top 3 Issues to Fix</div>', unsafe_allow_html=True)
            st.markdown('<div class="prob-grid">', unsafe_allow_html=True)
            for p in top_problems(df, industry):
                st.markdown(f"""
                <div class="prob-card">
                    <div class="prob-badge {p['sev']}">{p['sev'].upper()}</div>
                    <div class="prob-title">{p['title']}</div>
                    <div class="prob-text">{p['text']}</div>
                    <div class="prob-action">{p['action']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Action plan
        st.markdown('<div class="section-title">Your Action Plan This Week</div>', unsafe_allow_html=True)
        for i, action in enumerate(weekly_actions(df, industry), 1):
            st.markdown(f"""
            <div class="action-item">
                <div class="action-num">{i}</div>
                <div>{action}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # ── TABS ──────────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends", "💸 Expenses", "🏆 Customers", "📊 Profit/Loss", "🤖 Ask OpsClarity"])

        with tab1:
            st.markdown('<div class="section-title">Revenue vs Expenses Trend</div>', unsafe_allow_html=True)
            sm = s.groupby("Month")["Amount"].sum()
            em = e.groupby("Month")["Amount"].sum()
            trend_df = pd.DataFrame({"Revenue": sm, "Expenses": em}).fillna(0).sort_index()
            st.line_chart(trend_df, use_container_width=True, height=280)
            if len(trend_df) >= 2:
                rev_change = ((trend_df["Revenue"].iloc[-1] - trend_df["Revenue"].iloc[-2]) / max(trend_df["Revenue"].iloc[-2],1)*100)
                exp_change = ((trend_df["Expenses"].iloc[-1] - trend_df["Expenses"].iloc[-2]) / max(trend_df["Expenses"].iloc[-2],1)*100)
                mc1, mc2 = st.columns(2)
                mc1.metric("Revenue MoM", fmt(trend_df["Revenue"].iloc[-1]), f"{rev_change:+.1f}%")
                mc2.metric("Expenses MoM", fmt(trend_df["Expenses"].iloc[-1]), f"{exp_change:+.1f}%", delta_color="inverse")

        with tab2:
            st.markdown('<div class="section-title">Where Your Money Goes</div>', unsafe_allow_html=True)
            if len(e) > 0:
                exp_by_cat = e.groupby("Category")["Amount"].sum().sort_values(ascending=False)
                ec1, ec2 = st.columns([2,1])
                with ec1:
                    st.bar_chart(exp_by_cat, use_container_width=True, height=280)
                with ec2:
                    exp_table = exp_by_cat.reset_index()
                    exp_table["Share %"] = (exp_table["Amount"]/exp*100).round(1)
                    exp_table["Amount"] = exp_table["Amount"].apply(fmt)
                    st.dataframe(exp_table, hide_index=True, use_container_width=True)

        with tab3:
            st.markdown('<div class="section-title">Top Customers by Revenue</div>', unsafe_allow_html=True)
            if len(s) > 0:
                cust_rev = s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(10)
                st.bar_chart(cust_rev, use_container_width=True, height=280)
                st.markdown('<div class="section-title" style="margin-top:1rem;">Overdue by Customer</div>', unsafe_allow_html=True)
                overdue_df = df[(df["Type"]=="Sales")&(df["Status"]=="Overdue")] if "Status" in df.columns else pd.DataFrame()
                if len(overdue_df) > 0:
                    od = overdue_df.groupby("Party")["Amount"].sum().sort_values(ascending=False).reset_index()
                    od["Amount"] = od["Amount"].apply(fmt)
                    st.dataframe(od, hide_index=True, use_container_width=True)
                else:
                    st.success("✅ No overdue invoices. Collections are clean!")

        with tab4:
            st.markdown('<div class="section-title">Monthly Profit / Loss</div>', unsafe_allow_html=True)
            sm = s.groupby("Month")["Amount"].sum()
            em_m = e.groupby("Month")["Amount"].sum()
            all_m = sorted(set(sm.index)|set(em_m.index))
            profit_df = pd.DataFrame({"Profit": [sm.get(m,0)-em_m.get(m,0) for m in all_m]}, index=all_m)
            st.bar_chart(profit_df, use_container_width=True, height=280)
            # Export
            csv_buf = io.StringIO(); df.to_csv(csv_buf, index=False)
            st.download_button("⬇ Download Full Data (CSV)", data=csv_buf.getvalue().encode(),
                               file_name=f"OpsClarity_{datetime.now().strftime('%Y%m%d')}.csv",
                               mime="text/csv")

        with tab5:
            st.markdown('<div class="section-title">Ask OpsClarity AI</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Your personal finance advisor — ask anything about your business data</div>', unsafe_allow_html=True)

            # Chat display
            if not st.session_state.chat_history:
                st.session_state.chat_history = [{
                    "role": "ai",
                    "content": f"Hi! I've analyzed your {industry} business data. Your health score is **{overall}/100**. You can ask me anything — e.g. 'Why is my margin low?', 'Which customer owes the most?', 'How do I reduce expenses?'"
                }]

            st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
            for msg in st.session_state.chat_history:
                role_cls = "ai" if msg["role"]=="ai" else "user"
                avatar = "◈" if msg["role"]=="ai" else "👤"
                st.markdown(f"""
                <div class="chat-msg {role_cls}">
                    <div class="chat-avatar">{avatar}</div>
                    <div class="chat-bubble">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Suggested questions
            sq_cols = st.columns(3)
            suggestions = ["Why is my margin low?", "Who owes me the most?", "Where am I overspending?"]
            for i, sq in enumerate(suggestions):
                with sq_cols[i]:
                    if st.button(sq, key=f"sq_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role":"user","content":sq})
                        # Call AI
                        ctx = build_context_string(df, industry)
                        try:
                            import anthropic
                            client = anthropic.Anthropic()
                            resp = client.messages.create(
                                model="claude-opus-4-5",
                                max_tokens=400,
                                system=f"""You are OpsClarity, a plain-language financial advisor for Indian SMEs.
Business data:
{ctx}
Keep answers under 120 words. Be specific with numbers. Use ₹ for amounts. Give 1 clear action at the end. No markdown headers.""",
                                messages=[{"role":"user","content":sq}]
                            )
                            answer = resp.content[0].text
                        except Exception:
                            answer = f"Based on your data: {ki['body'] if ki else 'Your business is performing at ' + str(overall) + '/100.'} {ki['cta'] if ki else ''}"
                        st.session_state.chat_history.append({"role":"ai","content":answer})
                        st.rerun()

            # Free text input
            user_q = st.text_input("Ask anything about your business...", placeholder="e.g. What's my biggest financial risk this month?", label_visibility="collapsed")
            if user_q:
                st.session_state.chat_history.append({"role":"user","content":user_q})
                ctx = build_context_string(df, industry)
                try:
                    import anthropic
                    client = anthropic.Anthropic()
                    resp = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=400,
                        system=f"""You are OpsClarity, a plain-language financial advisor for Indian SMEs.
Business data:
{ctx}
Keep answers under 120 words. Be specific with numbers. Use ₹ for amounts. Give 1 clear action at the end. No markdown headers.""",
                        messages=[m for m in st.session_state.chat_history if m["role"]!="ai"] + [{"role":"user","content":user_q}]
                    )
                    answer = resp.content[0].text
                except Exception:
                    answer = "I couldn't connect to the AI right now. Please add your ANTHROPIC_API_KEY to Streamlit secrets to enable the AI advisor. Your business data shows: " + build_context_string(df, industry)[:200]
                st.session_state.chat_history.append({"role":"ai","content":answer})
                st.rerun()

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Share section
        st.markdown('<div class="section-title">Share Your Results</div>', unsafe_allow_html=True)
        share_txt = f"""◈ My Business Health Score: {overall}/100

📊 Revenue: {fmt(rev)} | Profit: {fmt(profit)} ({margin:.1f}% margin)
{'🚨 '+ki['headline'] if ki else ''}

Analyzed free at opsclarity.streamlit.app
#OpsClarity #IndianSME"""

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            enc = share_txt.replace('\n','%0A').replace(' ','%20').replace('#','%23')
            st.markdown(f'<a href="https://wa.me/?text={enc}" target="_blank" class="share-btn share-wa" style="display:block;padding:11px;border-radius:12px;text-align:center;font-size:13px;font-weight:700;text-decoration:none;">📱 Share on WhatsApp</a>', unsafe_allow_html=True)
        with sc2:
            if st.button("📋 Copy Summary", use_container_width=True):
                st.code(share_txt, language=None)
        with sc3:
            st.download_button("📸 Download Report", data=share_txt.encode(),
                               file_name=f"OpsClarity_{datetime.now().strftime('%Y%m%d')}.txt",
                               mime="text/plain", use_container_width=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Paywall
        spots = st.session_state.spots
        st.markdown(f"""
        <div class="paywall">
            <div style="background:rgba(255,80,80,0.08);border:1px solid rgba(255,80,80,0.2);border-radius:10px;padding:.8rem;margin-bottom:1.2rem;">
                <div style="color:#ff7070;font-weight:600;font-size:14px;">⚡ Only {spots} free full analyses remaining this month</div>
            </div>
            <div class="pw-title">Unlock Monthly Intelligence</div>
            <div class="pw-sub">Auto-reports, AI advisor, GST prep & priority WhatsApp support</div>
            <div class="pricing-grid">
                <div class="price-card">
                    <div class="price-who">Free Forever</div>
                    <div class="price-amt">₹0</div>
                    <div class="price-title">Starter</div>
                    <ul class="price-features">
                        <li>1 upload/month</li>
                        <li>Basic health score</li>
                        <li>Top 3 problems</li>
                    </ul>
                </div>
                <div class="price-card featured">
                    <div class="price-who">For Growing SMEs</div>
                    <div class="price-amt">₹499 <span class="per">/mo</span></div>
                    <div class="price-title">Pro ⭐</div>
                    <ul class="price-features">
                        <li>Unlimited uploads</li>
                        <li>12-month trend history</li>
                        <li>AI advisor (Ask OpsClarity)</li>
                        <li>WhatsApp monthly alerts</li>
                        <li>Downloadable PDF reports</li>
                    </ul>
                </div>
                <div class="price-card">
                    <div class="price-who">For Chartered Accountants</div>
                    <div class="price-amt">₹1,999 <span class="per">/mo</span></div>
                    <div class="price-title">CA Plan</div>
                    <ul class="price-features">
                        <li>50 client seats</li>
                        <li>CA practice dashboard</li>
                        <li>GST estimates</li>
                        <li>White-label reports</li>
                        <li>Priority support</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pc1, pc2, pc3 = st.columns([1,2,1])
        with pc2:
            if st.button("🔓 Get Free Access Now", use_container_width=True, type="primary"):
                st.session_state.spots = max(0, spots - 1)
                st.balloons()
                st.success("✅ You're in! Free access activated. Welcome to OpsClarity.")
                st.markdown("📱 [Join our WhatsApp community](https://wa.me/916362319163?text=I+just+joined+OpsClarity!) for weekly business tips.")

    # ── LANDING (no data) ──────────────────────────────────────────────────────
    else:
        st.markdown("""
        <div class="divider"></div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:2rem 0;">
            <div style="background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:1.6rem;text-align:center;">
                <div style="font-size:2.2rem;margin-bottom:.6rem;">⚡</div>
                <div style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:1.1rem;margin-bottom:.5rem;">30 Second Setup</div>
                <div style="color:#5a5a70;font-size:13px;line-height:1.6;">Upload any Excel, CSV, or Tally file. Columns auto-detected.</div>
            </div>
            <div style="background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:1.6rem;text-align:center;">
                <div style="font-size:2.2rem;margin-bottom:.6rem;">🎯</div>
                <div style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:1.1rem;margin-bottom:.5rem;">Find Money Leaks</div>
                <div style="color:#5a5a70;font-size:13px;line-height:1.6;">Overdue invoices, expense spikes, margin problems — instantly visible.</div>
            </div>
            <div style="background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:1.6rem;text-align:center;">
                <div style="font-size:2.2rem;margin-bottom:.6rem;">🤖</div>
                <div style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:1.1rem;margin-bottom:.5rem;">Ask AI Anything</div>
                <div style="color:#5a5a70;font-size:13px;line-height:1.6;">AI advisor answers plain-language questions about your numbers.</div>
            </div>
        </div>
        <div style="text-align:center;padding:2rem;background:rgba(200,255,87,.04);border:1px solid rgba(200,255,87,.12);border-radius:18px;">
            <div style="font-family:'Playfair Display',serif;color:#c8ff57;font-size:1.3rem;margin-bottom:.4rem;">Free for the first 100 businesses</div>
            <div style="color:#5a5a70;font-size:14px;">Then ₹499/month. No credit card required to start.</div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<a href="https://wa.me/916362319163?text=Hi%2C+I+have+a+question+about+OpsClarity" class="whatsapp-float" target="_blank">
    💬 Chat with Founder
</a>
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid rgba(255,255,255,.05);margin-top:2rem;">
    <div style="color:#4a4a60;font-size:12px;margin-bottom:.3rem;">OpsClarity · Made for Indian SMEs · Built in Bangalore</div>
    <div style="color:#3a3a50;font-size:11px;">Data stays private · Management estimates only · Not a substitute for professional CA advice</div>
</div>
""", unsafe_allow_html=True)
