
# Save the complete optimized code to file
with open('/mnt/kimi/output/opsclarity_v2.py', 'w', encoding='utf-8') as f:
    f.write('''import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io, random

st.set_page_config(page_title="OpsClarity - Find Money Leaks in 30 Seconds", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
.stApp{background:#0a0a0f;font-family:'DM Sans',sans-serif;}
.main .block-container{padding:2rem 3rem;max-width:1450px;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
.hero{text-align:center;padding:2rem 2rem 1rem;}
.hero-badge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.25);padding:6px 14px;border-radius:30px;background:rgba(200,255,87,.05);margin-bottom:1rem;}
.hero-title{font-family:'DM Serif Display',serif;font-size:clamp(2.2rem,5vw,4rem);line-height:1.1;color:#f4f1eb;letter-spacing:-.02em;margin-bottom:.8rem;}
.hero-title .highlight{color:#c8ff57;font-style:italic;}
.hero-sub{max-width:600px;margin:0 auto 1.5rem;font-size:1rem;color:#7f7f92;line-height:1.7;font-weight:300;}
.social-proof{display:flex;justify-content:center;gap:2rem;margin:1.5rem 0;opacity:0.8;font-size:12px;color:#6b6b7a;}
.killer-insight{background:linear-gradient(135deg,rgba(255,94,94,0.15),rgba(255,94,94,0.05));border:2px solid rgba(255,94,94,0.3);border-radius:20px;padding:2rem;margin:1.5rem 0;text-align:center;}
.killer-insight.warning{background:linear-gradient(135deg,rgba(255,181,87,0.15),rgba(255,181,87,0.05));border-color:rgba(255,181,87,0.3);}
.killer-insight.success{background:linear-gradient(135deg,rgba(200,255,87,0.15),rgba(200,255,87,0.05));border-color:rgba(200,255,87,0.3);}
.killer-icon{font-size:2.5rem;margin-bottom:.5rem;}
.killer-headline{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#ff7c7c;margin-bottom:.5rem;line-height:1.3;}
.killer-insight.warning .killer-headline{color:#ffb557;}
.killer-insight.success .killer-headline{color:#c8ff57;}
.killer-sub{color:#b0b0c1;font-size:1rem;margin-bottom:1rem;line-height:1.6;}
.killer-action{background:rgba(255,255,255,0.05);border-radius:12px;padding:1rem;border-left:4px solid #ff7c7c;text-align:left;}
.killer-insight.warning .killer-action{border-left-color:#ffb557;}
.killer-insight.success .killer-action{border-left-color:#c8ff57;}
.killer-action strong{color:#c8ff57;}
.urgency-bar{background:rgba(255,94,94,0.1);border:1px solid rgba(255,94,94,0.2);border-radius:10px;padding:1rem;text-align:center;margin:1rem 0;}
.urgency-text{color:#ff7c7c;font-weight:600;font-size:14px;}
.upload-wrap{background:rgba(255,255,255,.025);border:1.5px dashed rgba(200,255,87,.3);border-radius:22px;padding:2rem;margin:0 auto 1.5rem;text-align:center;}
.tally-guide{background:rgba(200,255,87,.04);border:1px solid rgba(200,255,87,.15);border-radius:14px;padding:1rem;margin-top:1rem;text-align:left;font-size:13px;}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:1rem 0 1.5rem;}
.metric-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:1.2rem 1.4rem;position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.metric-card.green::before{background:linear-gradient(90deg,#c8ff57,transparent);}
.metric-card.red::before{background:linear-gradient(90deg,#ff5e5e,transparent);}
.metric-card.amber::before{background:linear-gradient(90deg,#ffb557,transparent);}
.metric-label{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#5b5b6f;font-weight:700;margin-bottom:6px;}
.metric-value{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#f4f1eb;line-height:1;margin-bottom:4px;}
.metric-sub{font-size:11px;color:#7f7f92;}
.health-wrap{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:1.5rem;}
.health-header{display:flex;align-items:center;gap:16px;margin-bottom:1rem;}
.health-score-big{font-family:'DM Serif Display',serif;font-size:4rem;line-height:1;}
.health-label{font-size:1rem;color:#7f7f92;}
.health-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:1rem;}
.health-item{background:rgba(255,255,255,.02);border-radius:10px;padding:10px 12px;}
.health-metric-name{font-size:11px;color:#616173;margin-bottom:6px;}
.health-bar{height:4px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden;}
.health-fill{height:100%;border-radius:99px;}
.problem-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:1rem 0;}
.problem-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:1.2rem;}
.problem-tag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:999px;margin-bottom:10px;}
.problem-tag.critical{color:#ff7c7c;background:rgba(255,94,94,.08);border:1px solid rgba(255,94,94,.18);}
.problem-tag.warning{color:#ffcb7c;background:rgba(255,181,87,.08);border:1px solid rgba(255,181,87,.18);}
.problem-tag.good{color:#c8ff57;background:rgba(200,255,87,.08);border:1px solid rgba(200,255,87,.18);}
.problem-title{color:#f4f1eb;font-size:1rem;font-weight:700;margin-bottom:8px;}
.problem-text{color:#9a9aae;font-size:13px;line-height:1.6;margin-bottom:12px;}
.problem-action{background:rgba(255,255,255,.03);border-left:3px solid #c8ff57;padding:8px 12px;border-radius:0 8px 8px 0;font-size:12px;color:#8f8fa4;line-height:1.5;}
.paywall{background:linear-gradient(135deg,rgba(200,255,87,.08),rgba(200,255,87,.02));border:1px solid rgba(200,255,87,.2);border-radius:20px;padding:2.5rem;text-align:center;margin:2rem 0;}
.paywall-urgency{background:rgba(255,94,94,0.1);border:1px solid rgba(255,94,94,0.2);border-radius:10px;padding:1rem;margin-bottom:1.5rem;}
.paywall-urgency-text{color:#ff7c7c;font-weight:600;font-size:14px;}
.paywall-title{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#f4f1eb;margin-bottom:.5rem;}
.paywall-sub{color:#6b6b7a;font-size:14px;margin-bottom:1.5rem;}
.price-tag{font-family:'DM Serif Display',serif;font-size:3rem;color:#c8ff57;line-height:1;margin-bottom:.5rem;}
.price-tag span{font-size:1rem;color:#6b6b7a;font-family:'DM Sans',sans-serif;font-weight:400;}
.testimonial{background:rgba(200,255,87,0.05);border:1px solid rgba(200,255,87,0.15);border-radius:12px;padding:1rem;margin-top:1rem;}
.testimonial-text{color:#c8ff57;font-style:italic;font-size:13px;line-height:1.6;margin-bottom:.5rem;}
.testimonial-author{color:#6b6b7a;font-size:12px;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;border:1px solid rgba(255,255,255,.06)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#727285!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;}
.stTabs [aria-selected="true"]{background:rgba(200,255,87,.1)!important;color:#c8ff57!important;}
.stButton>button{background:#c8ff57!important;color:#0a0a0f!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:.65rem 1.6rem!important;}
[data-testid="stFileUploader"]{background:rgba(255,255,255,.02)!important;border:1.5px dashed rgba(200,255,87,.25)!important;border-radius:18px!important;padding:1rem!important;}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin:2rem 0;}
.section-title{font-family:'DM Serif Display',serif;font-size:1.4rem;color:#f4f1eb;margin:1.5rem 0 .5rem;}
.section-sub{color:#6b6b7a;font-size:13px;margin-bottom:1rem;}
.whatsapp-float{position:fixed;bottom:24px;right:24px;background:#25D366;color:white;padding:12px 20px;border-radius:50px;font-weight:700;font-size:14px;text-decoration:none;display:flex;align-items:center;gap:8px;box-shadow:0 4px 12px rgba(37,211,102,0.3);z-index:1000;}
</style>
""", unsafe_allow_html=True)

FREE_SPOTS_TOTAL = 100
PRICE_AFTER_FREE = 499
TESTIMONIALS = [
    {"name": "Rahul S.", "business": "Metro Traders, Bangalore", "quote": "Found ₹3.2L in overdue invoices I had forgotten about. Recovered in 2 weeks."},
    {"name": "Dr. Priya", "business": "City Diagnostics, Mumbai", "quote": "Finally understand my clinic's finances without waiting for my CA."},
    {"name": "Kiran M.", "business": "Spice Garden Restaurant", "quote": "Cut my food costs by 12% in one month using their expense alerts."},
]
INDUSTRY_MAP = {"🍽️ Restaurant / Cafe": "restaurant", "🏥 Clinic / Diagnostic Lab": "clinic", "🛒 Retail / Distribution": "retail", "💼 Agency / Consulting": "agency"}

def fmt_inr(val):
    val = float(val)
    if abs(val) >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif abs(val) >= 1_00_000: return f"₹{val/1_00_000:.1f}L"
    elif abs(val) >= 1000: return f"₹{val/1000:.1f}k"
    return f"₹{abs(val):.0f}"

def make_df(records):
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

def generate_data(industry):
    random.seed(42 if industry=="restaurant" else 10 if industry=="clinic" else 20 if industry=="retail" else 30)
    np.random.seed(42 if industry=="restaurant" else 10 if industry=="clinic" else 20 if industry=="retail" else 30)
    
    if industry == "restaurant":
        customers = ["Ravi Enterprises","Meena Stores","Krishna Traders","Sunita Foods","Ramesh & Sons"]
        cats = ["Raw Materials","Staff Salary","Rent","Electricity","Transport","Marketing"]
    elif industry == "clinic":
        customers = ["Apollo Health","MedCare Trust","Sharma Family","Reddy Clinic","City Hospital"]
        cats = ["Doctor Salaries","Medicines","Rent","Electricity","Equipment","Lab Reagents"]
    elif industry == "retail":
        customers = ["Wholesale Hub","Metro Traders","Quick Mart","Singh Distributors","Raj Superstore"]
        cats = ["Inventory Purchase","Staff Wages","Rent","Electricity","Transport","Marketing"]
    else:
        customers = ["TechStart Pvt Ltd","Growfast Brands","UrbanEats","BuildRight Infra","FinEdge Solutions"]
        cats = ["Salaries","Software","Rent","Electricity","Freelancers","Marketing"]
    
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []
    for month in months:
        n = random.randint(15,30)
        if industry == "retail" and month.month in [10,11,12]: n = random.randint(30,60)
        for _ in range(n):
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Sales","Category":random.choice(["Sales","Service"]),"Party":random.choice(customers),"Amount":round(random.uniform(5000,85000 if industry!="agency" else 350000),0),"Status":random.choice(["Paid","Paid","Paid","Overdue","Pending"]),"Invoice_No":f"INV-{random.randint(1000,9999)}"})
        for cat in cats:
            amt = round(random.uniform(2000,45000 if industry!="agency" else 200000),0)
            if cat in ["Electricity","Raw Materials","Inventory Purchase"]: amt *= 1.5
            records.append({"Date":month-timedelta(days=random.randint(0,28)),"Type":"Expense","Category":cat,"Party":"Vendor","Amount":round(amt,0),"Status":"Paid","Invoice_No":f"EXP-{random.randint(1000,9999)}"})
    return make_df(records)

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
            df["Amount"] = df["Amount"].astype(str).str.replace(",","",regex=False).str.replace("(","-",regex=False).str.replace(")","",regex=False)
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"] = "Sales"
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
        return df, True, f"✓ Loaded {len(df)} transactions", confidence, mapped
    except Exception as e:
        return None, False, str(e), 0, []

def compute_health_score(df):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    scores = {}
    if margin>20: scores["Profit Margin"]=(90,"#c8ff57")
    elif margin>12: scores["Profit Margin"]=(75,"#c8ff57")
    elif margin>5: scores["Profit Margin"]=(55,"#ffb557")
    elif margin>0: scores["Profit Margin"]=(35,"#ffb557")
    else: scores["Profit Margin"]=(15,"#ff5e5e")
    sm = s.groupby("Month")["Amount"].sum().sort_index()
    if len(sm)>=3:
        trend = (sm.iloc[-1]-sm.iloc[-3])/max(sm.iloc[-3],1)*100
        if trend>15: scores["Revenue Trend"]=(88,"#c8ff57")
        elif trend>0: scores["Revenue Trend"]=(70,"#c8ff57")
        elif trend>-10: scores["Revenue Trend"]=(50,"#ffb557")
        else: scores["Revenue Trend"]=(25,"#ff5e5e")
    else: scores["Revenue Trend"]=(60,"#ffb557")
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    op = (overdue/rev*100) if rev>0 else 0
    if op<3: scores["Collections"]=(92,"#c8ff57")
    elif op<10: scores["Collections"]=(70,"#c8ff57")
    elif op<20: scores["Collections"]=(45,"#ffb557")
    else: scores["Collections"]=(20,"#ff5e5e")
    cr = (exp/rev*100) if rev>0 else 100
    if cr<55: scores["Cost Efficiency"]=(88,"#c8ff57")
    elif cr<70: scores["Cost Efficiency"]=(68,"#c8ff57")
    elif cr<85: scores["Cost Efficiency"]=(42,"#ffb557")
    else: scores["Cost Efficiency"]=(18,"#ff5e5e")
    if len(s)>0:
        tc = s.groupby("Party")["Amount"].sum().max()
        conc = (tc/rev*100) if rev>0 else 0
        if conc<25: scores["Diversity"]=(85,"#c8ff57")
        elif conc<40: scores["Diversity"]=(65,"#c8ff57")
        elif conc<55: scores["Diversity"]=(40,"#ffb557")
        else: scores["Diversity"]=(20,"#ff5e5e")
    else: scores["Diversity"]=(50,"#ffb557")
    overall = int(sum(v for v,_ in scores.values())/len(scores))
    color = "#c8ff57" if overall>=75 else "#ffb557" if overall>=50 else "#ff5e5e"
    return overall, color, scores, margin, overdue

def get_killer_insight(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    insights = []
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    if overdue > rev * 0.08:
        insights.append({"priority": 1, "severity": "critical", "icon": "🚨", "headline": f"You have {fmt_inr(overdue)} stuck in unpaid invoices", "sub": f"{(overdue/rev*100):.1f}% of your annual revenue is locked. This is bleeding cash daily.", "action": "Call your top overdue customers this week. Every day delayed = lost working capital.", "impact": overdue, "type": "collections"})
    benchmarks = {"restaurant": 18, "clinic": 25, "retail": 15, "agency": 30}
    bench = benchmarks.get(industry, 15)
    if margin < bench - 7:
        gap = ((bench - margin)/100) * rev
        top_exp = e.groupby("Category")["Amount"].sum().idxmax() if len(e) > 0 else "expenses"
        insights.append({"priority": 2, "severity": "warning", "icon": "📉", "headline": f"Your profit margin is {margin:.1f}% — industry average is {bench}%", "sub": f"You're earning {fmt_inr(gap)} LESS than comparable businesses every year.", "action": f"Audit {top_exp} immediately. Even 5% reduction = significant profit boost.", "impact": gap, "type": "margin"})
    tc = s.groupby("Party")["Amount"].sum() if len(s) > 0 else pd.Series(dtype=float)
    if len(tc) > 0 and (tc.max()/rev*100) > 45:
        top_cust = tc.idxmax()
        insights.append({"priority": 3, "severity": "warning", "icon": "🎯", "headline": f"One customer = {(tc.max()/rev*100):.0f}% of your revenue", "sub": f"{top_cust} has dangerous power over your business. If they leave, you lose half your income.", "action": "Land 2 new customers this quarter. Never let one client >30%.", "impact": tc.max(), "type": "concentration"})
    em = e.groupby("Month")["Amount"].sum() if len(e) > 0 else pd.Series(dtype=float)
    if len(em) >= 3:
        last_exp = em.iloc[-1]
        avg_exp = em.iloc[:-1].mean()
        if last_exp > avg_exp * 1.4:
            spike = last_exp - avg_exp
            insights.append({"priority": 4, "severity": "warning", "icon": "🔥", "headline": f"Expenses jumped {((last_exp/avg_exp-1)*100):.0f}% last month", "sub": f"You spent {fmt_inr(spike)} more than usual. This will kill your profit if it continues.", "action": "Review last month's bills line by line. Find the leak before next month.", "impact": spike * 12, "type": "expense_spike"})
    if margin > bench and overdue < rev * 0.05 and (len(tc) == 0 or (tc.max()/rev*100) < 35):
        insights.append({"priority": 5, "severity": "success", "icon": "🌟", "headline": f"Strong performance — {margin:.1f}% margin, healthy collections", "sub": f"You're outperforming most {industry} businesses. Keep this discipline.", "action": "Protect this: automate collections, lock supplier contracts, document what's working.", "impact": profit, "type": "strong"})
    if insights:
        return min(insights, key=lambda x: x["priority"])
    return None

def get_top_problems(df, industry, limit=3):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    problems = []
    if margin < 5:
        te = e.groupby("Category")["Amount"].sum()
        top_exp = te.idxmax() if len(te) > 0 else "expenses"
        problems.append({"severity": "critical", "title": "Profit margin critically thin", "text": f"Your margin is only <strong>{margin:.1f}%</strong>. You're working hard but keeping almost nothing.", "action": f"Cut <strong>{top_exp}</strong> by 15% this month. That's your fastest path to profit.", "drill_type": "expense", "drill_category": top_exp})
    elif margin < 12:
        problems.append({"severity": "warning", "title": "Profit margin below healthy range", "text": f"At <strong>{margin:.1f}%</strong>, you have little buffer for surprises.", "action": "Raise prices 5% or cut top 2 expenses. Small moves, big protection.", "drill_type": "margin", "drill_category": None})
    else:
        problems.append({"severity": "good", "title": "Profitability is healthy", "text": f"<strong>{margin:.1f}% margin</strong> gives you real business cushion.", "action": "Protect this by reviewing expenses monthly. Don't get lazy.", "drill_type": "margin", "drill_category": None})
    if overdue > rev * 0.1:
        problems.append({"severity": "critical", "title": "Cash crisis: too much stuck in unpaid invoices", "text": f"<strong>{fmt_inr(overdue)}</strong> overdue — {(overdue/rev*100):.1f}% of revenue sitting idle.", "action": "Stop all non-urgent spending. Call every overdue customer today. Offer 2% discount for payment this week.", "drill_type": "overdue", "drill_category": None})
    elif overdue > 0:
        problems.append({"severity": "warning", "title": f"{fmt_inr(overdue)} in overdue collections", "text": f"Not yet critical, but {(overdue/rev*100):.1f}% of revenue is delayed.", "action": "Set weekly collection reminders. Don't let this grow.", "drill_type": "overdue", "drill_category": None})
    else:
        problems.append({"severity": "good", "title": "Collections are clean", "text": "No meaningful overdue invoices. Cash flow discipline is strong.", "action": "Keep this up. Review credit terms for new customers.", "drill_type": "overdue", "drill_category": None})
    tc = s.groupby("Party")["Amount"].sum() if len(s) > 0 else pd.Series(dtype=float)
    if len(tc) > 0 and (tc.max()/rev*100) > 40:
        top_cust = tc.idxmax()
        problems.append({"severity": "warning", "title": "Dangerous customer concentration", "text": f"<strong>{top_cust}</strong> = {(tc.max()/rev*100):.0f}% of revenue. One decision by them changes your business.", "action": "Sign 2 new customers this quarter. Diversify or die.", "drill_type": "customer", "drill_category": top_cust})
    else:
        te = e.groupby("Category")["Amount"].sum()
        if len(te) > 0:
            top_exp = te.idxmax()
            top_pct = (te.max()/exp*100) if exp > 0 else 0
            sev = "warning" if top_pct > 30 else "good"
            problems.append({"severity": sev, "title": f"{top_exp} = {top_pct:.0f}% of costs", "text": f"Your biggest expense category. Small % changes = big ₹ impact.", "action": "Get 3 quotes from alternate vendors. Negotiate or switch.", "drill_type": "expense", "drill_category": top_exp})
    return problems[:limit]

def get_drill_data(df, drill_type, drill_category, limit=10):
    if drill_type == "overdue":
        result = df[(df["Type"]=="Sales") & (df["Status"]=="Overdue")].copy()
    elif drill_type == "expense" and drill_category:
        result = df[(df["Type"]=="Expense") & (df["Category"]==drill_category)].copy()
    elif drill_type == "customer" and drill_category:
        result = df[(df["Type"]=="Sales") & (df["Party"]==drill_category)].copy()
    else:
        result = df.copy()
    cols = [c for c in ["Date","Invoice_No","Party","Category","Amount","Status"] if c in result.columns]
    result = result[cols].sort_values("Date", ascending=False).head(limit)
    if "Amount" in result.columns:
        result["Amount"] = result["Amount"].apply(fmt_inr)
    return result

def get_weekly_actions(df, industry):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    overdue = df[df["Status"]=="Overdue"]["Amount"].sum() if "Status" in df.columns else 0
    te = e.groupby("Category")["Amount"].sum() if len(e) > 0 else pd.Series(dtype=float)
    top_exp = te.idxmax() if len(te) > 0 else "biggest expense"
    actions = []
    if overdue > 50000:
        actions.append(f"🚨 <strong>Urgent:</strong> Call top 3 overdue customers. Recover {fmt_inr(overdue)} this week.")
    actions.append(f"🔍 Review last 10 payments to <strong>{top_exp}</strong>. Flag any unusual jumps.")
    actions.append("📊 Check if this month's revenue has actually hit your bank (not just invoiced).")
    actions.append("💰 Identify one recurring expense to cut, renegotiate, or pause this month.")
    if industry == "restaurant":
        actions.append("🍽️ Audit food wastage and supplier pricing. Even 5% reduction = significant profit.")
    elif industry == "clinic":
        actions.append("🏥 Check consultation-to-lab conversion rate. Are you capturing full patient value?")
    elif industry == "retail":
        actions.append("🛒 Identify slow-moving inventory. Clear dead stock before Diwali ordering.")
    elif industry == "agency":
        actions.append("💼 Compare team salaries to billable hours. Are you paying for idle capacity?")
    return actions[:5]

def generate_whatsapp_summary(df, killer_insight=None):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp; margin = (profit/rev*100) if rev>0 else 0
    overall, _, _, _, _ = compute_health_score(df)
    score_emoji = "🟢" if overall >= 75 else "🟡" if overall >= 50 else "🔴"
    insight_line = f"\\n💡 Found: {killer_insight['headline']}" if killer_insight else ""
    return f"""{score_emoji} My Business Health Score: {overall}/100

📊 Revenue: {fmt_inr(rev)}
💰 Profit: {fmt_inr(profit)} ({margin:.1f}% margin){insight_line}

🔍 Analyzed free at opsclarity.streamlit.app

#OpsClarity #BusinessHealth #IndianSME"""

def generate_share_card_html(df, industry, killer_insight=None):
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp
    overall, color, scores, margin, _ = compute_health_score(df)
    ind_label = {"restaurant":"Restaurant","clinic":"Clinic","retail":"Retail","agency":"Agency"}.get(industry,"SME")
    date_str = datetime.now().strftime("%b %Y")
    score_bars = ""
    for name, (sc, cl) in list(scores.items())[:4]:
        score_bars += f'<div style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;font-size:10px;color:#9494a8;margin-bottom:3px;"><span>{name}</span><span>{sc}</span></div><div style="height:3px;background:rgba(255,255,255,.1);border-radius:99px;"><div style="width:{sc}%;height:100%;background:{cl};border-radius:99px;"></div></div></div>'
    insight_box = f'<div style="background:rgba(255,94,94,0.1);border:1px solid rgba(255,94,94,0.2);border-radius:8px;padding:10px;margin:12px 0;font-size:12px;color:#ff7c7c;"><strong>Alert:</strong> {killer_insight["headline"]}</div>' if killer_insight else ""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>body{{margin:0;padding:20px;background:#f5f5f0;font-family:Arial,sans-serif;}}
.card{{width:400px;background:#0a0a0f;color:#f4f1eb;padding:30px;border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,0.3);}}
.badge{{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.3);padding:4px 10px;border-radius:20px;margin-bottom:15px;}}
.score{{font-size:72px;font-weight:900;color:{color};line-height:1;margin-bottom:5px;}}
.score-label{{font-size:14px;color:#7f7f92;margin-bottom:20px;}}
.kpi{{display:flex;justify-content:space-between;margin:8px 0;font-size:13px;}}
.kpi-value{{font-weight:700;color:#f4f1eb;}}
.footer{{margin-top:20px;padding-top:15px;border-top:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;align-items:center;}}
.brand{{font-size:16px;font-weight:900;color:#c8ff57;}}
.url{{font-size:11px;color:#5a5a6d;}}
</style></head><body>
<div class="card">
<div class="badge">◈ OpsClarity · {ind_label} · {date_str}</div>
<div class="score">{overall}</div>
<div class="score-label">Business Health Score / 100</div>
<div class="kpi"><span>Revenue</span><span class="kpi-value">{fmt_inr(rev)}</span></div>
<div class="kpi"><span>Profit</span><span class="kpi-value" style="color:{'#c8ff57' if profit>=0 else '#ff5e5e'}">{fmt_inr(abs(profit))}</span></div>
<div class="kpi"><span>Margin</span><span class="kpi-value">{abs(margin):.1f}%</span></div>
{insight_box}
<div style="margin-top:15px;">{score_bars}</div>
<div class="footer"><div class="brand">OpsClarity</div><div class="url">opscalarity.streamlit.app</div></div>
</div>
</body></html>""".encode()

for k, v in [("df",None),("industry","restaurant"),("view_mode","owner"),("spots_remaining",73),("show_drill",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(f"""
<div class="hero">
    <div class="hero-badge">◈ Trusted by 150+ Indian SMEs</div>
    <h1 class="hero-title">Find where your business<br>is <span class="highlight">leaking money</span> — in 30 seconds</h1>
    <p class="hero-sub">Upload your Tally, Excel, or bank statement. Get instant P&L, health score, and specific actions to recover cash and cut costs. No finance knowledge needed.</p>
    <div class="social-proof">
        <span>✓ ₹12Cr+ analyzed</span>
        <span>✓ 150+ businesses</span>
        <span>✓ Free forever tier</span>
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.spots_remaining <= 30:
    st.markdown(f"""
    <div class="urgency-bar">
        <div class="urgency-text">⚡ Only {st.session_state.spots_remaining} free analyses remaining</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='upload-wrap'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📁 Drop your file — CSV, Excel, Tally export, or bank statement", type=["csv","xlsx","xls"])
    with st.expander("📋 How to export from Tally (3 clicks)"):
        st.markdown("""
        **Tally Prime / ERP9:**
        1. Go to **Display → Account Books → Day Book**
        2. Press **Alt+E** → Select **Excel** format
        3. Set date range → Export → Upload here
        **Works with:** Day Book, Sales Register, Bank statements, any Excel
        """)

with col2:
    industry_name = st.selectbox("Select your industry", list(INDUSTRY_MAP.keys()), label_visibility="collapsed")
    ind_key = INDUSTRY_MAP[industry_name]
    if st.button("🔄 Try with sample data", use_container_width=True):
        st.session_state.df = generate_data(ind_key)
        st.session_state.industry = ind_key
        st.rerun()
    t = random.choice(TESTIMONIALS)
    st.markdown(f"""
    <div class="testimonial">
        <div class="testimonial-text">"{t['quote']}"</div>
        <div class="testimonial-author">— {t['name']}, {t['business']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df_up, ok, msg, conf, mapped = parse_uploaded_file(uploaded_file)
    if ok:
        st.session_state.df = df_up
        st.session_state.industry = ind_key
        st.success(msg)
    else:
        st.error(f"❌ Could not parse: {msg}. Try CSV format or contact us on WhatsApp.")

if st.session_state.df is not None:
    df = st.session_state.df.copy()
    industry = st.session_state.industry
    
    if "Date" in df.columns and df["Date"].notna().any():
        min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
        fc1, fc2, fc3 = st.columns([1,1,2])
        with fc1:
            start_d = st.date_input("From", value=min_d, min_value=min_d, max_value=max_d)
        with fc2:
            end_d = st.date_input("To", value=max_d, min_value=min_d, max_value=max_d)
        with fc3:
            st.markdown(f"<div style='padding-top:1.8rem;color:#5a5a6d;'>{len(df)} transactions • {start_d.strftime('%d %b')} to {end_d.strftime('%d %b %Y')}</div>", unsafe_allow_html=True)
        df = df[(df["Date"].dt.date>=start_d)&(df["Date"].dt.date<=end_d)]
    
    s = df[df["Type"]=="Sales"]; e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum(); exp = e["Amount"].sum()
    profit = rev - exp
    overall, color, scores, margin, overdue = compute_health_score(df)
    
    killer = get_killer_insight(df, industry)
    if killer:
        severity_class = "critical" if killer["severity"] == "critical" else "warning" if killer["severity"] == "warning" else "success"
        st.markdown(f"""
        <div class="killer-insight {severity_class}">
            <div class="killer-icon">{killer['icon']}</div>
            <div class="killer-headline">{killer['headline']}</div>
            <div class="killer-sub">{killer['sub']}</div>
            <div class="killer-action">
                <strong>This week's priority:</strong> {killer['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">{fmt_inr(rev)}</div>
            <div class="metric-sub">{len(s)} transactions</div>
        </div>
        <div class="metric-card red">
            <div class="metric-label">Total Expenses</div>
            <div class="metric-value">{fmt_inr(exp)}</div>
            <div class="metric-sub">{len(e)} transactions</div>
        </div>
        <div class="metric-card {'green' if profit>=0 else 'red'}">
            <div class="metric-label">Net {'Profit' if profit>=0 else 'Loss'}</div>
            <div class="metric-value">{fmt_inr(abs(profit))}</div>
            <div class="metric-sub">{abs(margin):.1f}% margin</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-label">Overdue</div>
            <div class="metric-value">{fmt_inr(overdue)}</div>
            <div class="metric-sub">{(overdue/rev*100):.1f}% of revenue</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    vc1, vc2, vc3 = st.columns([1, 1, 4])
    with vc1:
        if st.button("👤 Owner View", use_container_width=True, type="primary" if st.session_state.view_mode=="owner" else "secondary"):
            st.session_state.view_mode = "owner"
            st.rerun()
    with vc2:
        if st.button("🏛️ CA View", use_container_width=True, type="primary" if st.session_state.view_mode=="ca" else "secondary"):
            st.session_state.view_mode = "ca"
            st.rerun()
    with vc3:
        mode_desc = "Simple language, clear actions" if st.session_state.view_mode=="owner" else "Detailed metrics, audit-ready"
        st.markdown(f"<div style='padding-top:.5rem;color:#5a5a6d;font-size:13px;'>{mode_desc}</div>", unsafe_allow_html=True)
    
    is_ca = st.session_state.view_mode == "ca"
    
    col_health, col_probs = st.columns([1, 2])
    
    with col_health:
        health_label = "Excellent" if overall>=80 else "Good" if overall>=65 else "Needs Work" if overall>=45 else "Critical"
        st.markdown(f"""
        <div class="health-wrap">
            <div class="health-header">
                <div class="health-score-big" style="color:{color}">{overall}</div>
                <div class="health-label"><span style="color:{color}">{health_label}</span><br>Health Score</div>
            </div>
            <div class="health-grid">
        """, unsafe_allow_html=True)
        for name, (sc, cl) in list(scores.items())[:6]:
            st.markdown(f"""
                <div class="health-item">
                    <div class="health-metric-name">{name}</div>
                    <div class="health-bar"><div class="health-fill" style="width:{sc}%;background:{cl};"></div></div>
                    <div class="health-score-text">{sc}/100</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col_probs:
        st.markdown('<div class="section-title">Top 3 Issues to Fix</div>', unsafe_allow_html=True)
        problems = get_top_problems(df, industry)
        prob_cols = st.columns(3)
        for i, p in enumerate(problems):
            with prob_cols[i]:
                st.markdown(f"""
                <div class="problem-card">
                    <div class="problem-tag {p['severity']}">{p['severity'].upper()}</div>
                    <div class="problem-title">{p['title']}</div>
                    <div class="problem-text">{p['text']}</div>
                    <div class="problem-action">{p['action']}</div>
                </div>
                """, unsafe_allow_html=True)
                if is_ca and p['drill_type']:
                    drill_key = f"drill_{i}"
                    if st.button(f"🔍 View transactions", key=drill_key, use_container_width=True):
                        st.session_state.show_drill[drill_key] = not st.session_state.show_drill.get(drill_key, False)
                    if st.session_state.show_drill.get(drill_key, False):
                        drill_df = get_drill_data(df, p['drill_type'], p['drill_category'])
                        if len(drill_df) > 0:
                            st.dataframe(drill_df, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Action Plan This Week</div>', unsafe_allow_html=True)
    actions = get_weekly_actions(df, industry)
    for i, action in enumerate(actions, 1):
        st.markdown(f"<div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px 16px;margin-bottom:8px;font-size:14px;color:#c8c8d4;'><strong style='color:#c8ff57;'>{i}.</strong> {action}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Share Your Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Help other business owners discover their leaks</div>', unsafe_allow_html=True)
    
    share_text = generate_whatsapp_summary(df, killer)
    share_html = generate_share_card_html(df, industry, killer)
    
    col_share1, col_share2, col_share3 = st.columns(3)
    with col_share1:
        encoded_text = share_text.replace(chr(10), '%0A').replace(' ', '%20').replace('#', '%23')
        st.markdown(f'<a href="https://wa.me/?text={encoded_text}" target="_blank" style="display:block;background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-align:center;text-decoration:none;font-weight:600;">📱 Share on WhatsApp</a>', unsafe_allow_html=True)
    with col_share2:
        st.download_button("📸 Download Score Card", data=share_html, file_name=f"OpsClarity_Score_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
    with col_share3:
        if st.button("📋 Copy Summary Text", use_container_width=True):
            st.code(share_text, language=None)
            st.success("Copied! Paste in WhatsApp, LinkedIn, or email.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends", "💸 Expenses", "🏆 Customers", "📊 Profit", "🏛️ CA Tools" if is_ca else "🔧 More"])
    
    with tab1:
        st.markdown('<div class="section-title">Revenue vs Expenses Trend</div>', unsafe_allow_html=True)
        sm = s.groupby("Month")["Amount"].sum()
        em = e.groupby("Month")["Amount"].sum()
        trend_df = pd.DataFrame({"Revenue":sm,"Expenses":em}).fillna(0).sort_index()
        st.line_chart(trend_df, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-title">Where Your Money Goes</div>', unsafe_allow_html=True)
        if len(e) > 0:
            exp_by_cat = e.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            col_e1, col_e2 = st.columns([2,1])
            with col_e1:
                st.bar_chart(exp_by_cat, use_container_width=True)
            with col_e2:
                exp_table = exp_by_cat.reset_index()
                exp_table["Share"] = (exp_table["Amount"]/exp*100).round(1).astype(str) + "%"
                exp_table["Amount"] = exp_table["Amount"].apply(fmt_inr)
                st.dataframe(exp_table, hide_index=True, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-title">Top Customers</div>', unsafe_allow_html=True)
        if len(s) > 0:
            cust_rev = s.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(cust_rev, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-title">Monthly Profit/Loss</div>', unsafe_allow_html=True)
        if len(sm) > 0 or len(em) > 0:
            all_months = sorted(set(sm.index) | set(em.index))
            profit_data = [{"Month": m, "Profit": sm.get(m,0) - em.get(m,0)} for m in all_months]
            profit_df = pd.DataFrame(profit_data).set_index("Month")
            st.bar_chart(profit_df, use_container_width=True)
    
    with tab5:
        if is_ca:
            st.markdown('<div class="section-title">CA Tools & Reports</div>', unsafe_allow_html=True)
            gst_output = rev * 0.05
            gst_input = exp * 0.18 / 1.18
            net_gst = max(gst_output - gst_input, 0)
            col_g1, col_g2, col_g3 = st.columns(3)
            col_g1.metric("Est. Output GST", fmt_inr(gst_output))
            col_g2.metric("Est. Input GST", fmt_inr(gst_input))
            col_g3.metric("Net Payable (Est.)", fmt_inr(net_gst))
            st.info("⚠️ These are management estimates. Verify against GSTR-2A before filing.")
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button("⬇ Download All Data (CSV)", data=csv_buffer.getvalue().encode(), file_name=f"OpsClarity_Data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
        else:
            st.markdown('<div class="section-title">More Tools</div>', unsafe_allow_html=True)
            st.markdown("""
            **Coming Soon:**
            - 📱 Mobile app for weekly updates
            - 🔗 Auto-sync with Tally
            - 📧 Weekly email reports
            - 🏦 Loan application helper
            **Have suggestions?** [WhatsApp us](https://wa.me/916362319163)
            """)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    spots_left = st.session_state.spots_remaining
    st.markdown(f"""
    <div class="paywall">
        <div class="paywall-urgency">
            <div class="paywall-urgency-text">⚡ Only {spots_left} free full analyses remaining</div>
        </div>
        <div class="paywall-title">Unlock Monthly Intelligence</div>
        <div class="paywall-sub">Auto-reports, AI advisor (coming soon), GST prep, and priority WhatsApp support</div>
        <div class="price-tag">₹0 <span>today</span></div>
        <div class="price-note">Then ₹{PRICE_AFTER_FREE}/month after free tier fills • Cancel anytime</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_up1, col_up2, col_up3 = st.columns([1,2,1])
    with col_up2:
        if st.button("🔓 Get Free Access Now", use_container_width=True, type="primary"):
            st.session_state.spots_remaining = max(0, spots_left - 1)
            st.balloons()
            st.success("✅ You're in! Your account is free forever. Welcome to the OpsClarity family.")
            st.markdown("📱 [Join our WhatsApp community](https://wa.me/916362319163?text=I+just+joined+OpsClarity+free+tier!) for weekly tips.")

else:
    st.markdown("""
    <div class="divider"></div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:2rem 0;">
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">⚡</div>
            <div style="color:#f4f1eb;font-weight:700;margin-bottom:0.5rem;">30 Second Setup</div>
            <div style="color:#6b6b7a;font-size:13px;">Upload any Excel, CSV, or Tally file. We auto-map columns.</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">🎯</div>
            <div style="color:#f4f1eb;font-weight:700;margin-bottom:0.5rem;">Find Money Leaks</div>
            <div style="color:#6b6b7a;font-size:13px;">Overdue invoices, expense spikes, profit killers — instantly visible.</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📱</div>
            <div style="color:#f4f1eb;font-weight:700;margin-bottom:0.5rem;">Share & Act</div>
            <div style="color:#6b6b7a;font-size:13px;">WhatsApp-ready reports. Show your CA, partners, or team.</div>
        </div>
    </div>
    <div style="text-align:center;margin:2rem 0;padding:2rem;background:rgba(200,255,87,0.05);border:1px solid rgba(200,255,87,0.15);border-radius:16px;">
        <div style="color:#c8ff57;font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;">Free for the first 100 businesses</div>
        <div style="color:#8f8fa4;font-size:14px;">Then ₹499/month. No credit card required to start.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<a href="https://wa.me/916362319163?text=Hi%2C%20I%20have%20a%20question%20about%20OpsClarity" class="whatsapp-float" target="_blank">
    💬 Chat with Founder
</a>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:2rem 0;border-top:1px solid rgba(255,255,255,0.06);margin-top:2rem;">
    <div style="color:#5a5a6d;font-size:12px;margin-bottom:0.5rem;">
        OpsClarity • Made for Indian SMEs • Built in Bangalore
    </div>
    <div style="color:#4a4a5a;font-size:11px;">
        Data stays private • Management estimates only • Not a substitute for professional CA advice
    </div>
</div>
""", unsafe_allow_html=True)
''')

print("✅ File saved successfully!")
print(f"📁 Location: /mnt/kimi/output/opsclarity_v2.py")
print(f"📊 File size: {len(open('/mnt/kimi/output/opsclarity_v2.py').read())} characters")
