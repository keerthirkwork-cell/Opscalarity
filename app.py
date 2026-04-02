import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io, random, json, time, os, urllib.parse
from fpdf import FPDF

st.set_page_config(
    page_title="OpsClarity — Profit Recovery System",
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

.nav{display:flex;align-items:center;justify-content:space-between;padding:1rem 0 2rem;}
.nav-logo{font-family:'Playfair Display',serif;font-size:1.4rem;color:#f4f1eb;display:flex;align-items:center;gap:8px;}
.nav-logo .dot{color:#c8ff57;}
.nav-badge{background:rgba(200,255,87,.08);border:1px solid rgba(200,255,87,.2);color:#c8ff57;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.08em;}

.hero{text-align:center;padding:3rem 2rem 2rem;}
.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c8ff57;border:1px solid rgba(200,255,87,.2);padding:6px 16px;border-radius:30px;background:rgba(200,255,87,.04);margin-bottom:1.5rem;}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(2.4rem,5.5vw,4.2rem);line-height:1.08;color:#f4f1eb;letter-spacing:-.02em;margin-bottom:1rem;}
.hero-title em{color:#c8ff57;font-style:italic;}
.hero-sub{max-width:580px;margin:0 auto 2rem;font-size:1.05rem;color:#6b6b80;line-height:1.75;font-weight:300;}

.leak-hero{background:linear-gradient(135deg,rgba(255,80,80,.15),rgba(255,80,80,.05));border:2px solid rgba(255,80,80,.4);border-radius:24px;padding:2rem;margin:1rem 0;}
.leak-hero.green{background:linear-gradient(135deg,rgba(200,255,87,.12),rgba(200,255,87,.04));border-color:rgba(200,255,87,.3);}
.leak-amount{font-family:'Playfair Display',serif;font-size:3.5rem;color:#ff7070;line-height:1;}
.leak-hero.green .leak-amount{color:#c8ff57;}
.leak-title{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#ff7070;margin-bottom:.5rem;}
.leak-hero.green .leak-title{color:#c8ff57;}

.leak-card{background:rgba(255,255,255,.03);border-left:4px solid #ff5e5e;border-radius:0 16px 16px 0;padding:1.2rem;margin-bottom:1rem;}
.leak-card.warning{border-left-color:#ffb557;}
.leak-card.good{border-left-color:#c8ff57;}
.leak-card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;}
.leak-card-title{font-weight:700;color:#f4f1eb;font-size:1.1rem;}
.leak-card-amount{color:#ff7070;font-weight:700;font-size:1.2rem;}
.leak-card.warning .leak-card-amount{color:#ffb557;}
.leak-card.good .leak-card-amount{color:#c8ff57;}
.leak-card-desc{color:#6b6b80;font-size:13px;line-height:1.6;margin-bottom:1rem;}
.leak-card-action{background:rgba(200,255,87,.08);border-radius:8px;padding:.8rem 1rem;font-size:13px;color:#c8ff57;}

.action-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1.2rem;margin-bottom:1rem;}
.action-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem;}
.action-icon-title{display:flex;align-items:center;gap:12px;}
.action-icon{font-size:1.8rem;}
.action-title{font-weight:700;color:#f4f1eb;font-size:1rem;}
.action-day{background:rgba(200,255,87,.1);color:#c8ff57;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;}
.action-task{color:#9090a4;font-size:14px;line-height:1.6;margin-bottom:.8rem;padding-left:2.8rem;}
.action-impact{color:#c8ff57;font-size:12px;font-weight:600;padding-left:2.8rem;}

.kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:1.5rem 0;}
.kpi{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:1.2rem 1.4rem;}
.kpi-label{font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:#4a4a60;font-weight:700;margin-bottom:8px;}
.kpi-val{font-family:'Playfair Display',serif;font-size:2rem;color:#f4f1eb;line-height:1;margin-bottom:4px;}
.kpi-sub{font-size:11px;color:#5a5a70;font-family:'JetBrains Mono',monospace;}

.upload-section{background:rgba(255,255,255,.025);border:1.5px dashed rgba(200,255,87,.25);border-radius:24px;padding:2rem;margin:1.5rem 0;}

.paywall{background:linear-gradient(135deg,rgba(200,255,87,.06),rgba(200,255,87,.01));border:1px solid rgba(200,255,87,.18);border-radius:24px;padding:2.5rem;text-align:center;margin:2rem 0;}
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:1.5rem 0;text-align:left;}
.price-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:1.4rem;}
.price-card.featured{background:rgba(200,255,87,.06);border-color:rgba(200,255,87,.25);}
.price-who{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#5a5a70;font-weight:700;margin-bottom:.5rem;}
.price-amt{font-family:'Playfair Display',serif;font-size:2rem;color:#f4f1eb;line-height:1;margin-bottom:.3rem;}
.price-title{font-weight:700;color:#c8c8d8;margin-bottom:.6rem;}
.price-features{list-style:none;font-size:12px;color:#6b6b80;line-height:2;}
.price-features li::before{content:"✓ ";color:#c8ff57;}

.stButton>button{background:#c8ff57!important;color:#080810!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:.7rem 1.8rem!important;}
.stButton>button:hover{background:#d4ff6e!important;transform:translateY(-1px);}

.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent);margin:2rem 0;}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;color:#f4f1eb;margin:1.5rem 0 .5rem;}
.section-sub{color:#5a5a70;font-size:13px;margin-bottom:1rem;}
.whatsapp-float{position:fixed;bottom:24px;right:24px;background:#25D366;color:white;padding:11px 18px;border-radius:50px;font-weight:700;font-size:13px;text-decoration:none;display:flex;align-items:center;gap:8px;box-shadow:0 4px 20px rgba(37,211,102,.25);z-index:1000;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🍽️ Restaurant / Cafe": "restaurant",
    "🏥 Clinic / Diagnostic Lab": "clinic", 
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting": "agency",
    "🏭 Manufacturing": "manufacturing",
    "🚚 Logistics / Transport": "logistics"
}
INDUSTRY_BENCHMARKS = {"restaurant": 18, "clinic": 25, "retail": 15, "agency": 30, "manufacturing": 20, "logistics": 12}

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def fmt(val):
    val = float(val)
    if abs(val) >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif abs(val) >= 1_00_000:   return f"₹{val/1_00_000:.1f}L"
    elif abs(val) >= 1_000:      return f"₹{val/1000:.1f}k"
    return f"₹{abs(val):.0f}"

def parse_file(file):
    """Parse CSV/Excel with smart column detection"""
    try:
        fname = file.name.lower()
        try:
            df = pd.read_csv(file) if fname.endswith(".csv") else pd.read_excel(file, engine="openpyxl")
        except:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin1") if fname.endswith(".csv") else pd.read_excel(file, engine="openpyxl")
        
        df = df.dropna(how="all").dropna(axis=1, how="all")
        
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher date"]): col_map[col] = "Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit"]): col_map[col] = "Amount"
            elif any(x in cl for x in ["type","txn type","dr/cr","nature"]): col_map[col] = "Type"
            elif any(x in cl for x in ["category","cat","head","narration","ledger","particulars"]): col_map[col] = "Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client","ledger name"]): col_map[col] = "Party"
            elif any(x in cl for x in ["status","paid","cleared","pending"]): col_map[col] = "Status"
            elif any(x in cl for x in ["invoice","bill no","voucher","ref","bill num"]): col_map[col] = "Invoice_No"
        
        df = df.rename(columns=col_map)
        
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
            df = df.dropna(subset=["Date"])
        
        if "Amount" in df.columns:
            df["Amount"] = df["Amount"].astype(str).str.replace(",","").str.replace("(","-").str.replace(")","")
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        
        if "Type" not in df.columns: 
            df["Type"] = "Sales"
        df["Type"] = df["Type"].astype(str).str.strip().str.title()
        df["Type"] = df["Type"].replace({
            "Dr":"Expense","Cr":"Sales","Debit":"Expense","Credit":"Sales",
            "Payment":"Expense","Receipt":"Sales","Purchase":"Expense",
            "Journal":"Expense","Contra":"Expense"
        })
        
        df.loc[~df["Type"].isin(["Sales","Expense"]), "Type"] = df.apply(
            lambda x: "Expense" if any(word in str(x.get("Category","")).lower() for word in ["purchase","expense","payment","salary","rent"]) else "Sales", axis=1
        )
        
        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","—")]:
            if col not in df.columns: df[col] = default
        
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        return df, True, f"Loaded {len(df):,} transactions"
        
    except Exception as ex:
        return None, False, str(ex)

# ─── CORE: PROFIT LEAK DETECTOR ──────────────────────────────────────────────
def detect_profit_leaks(df, industry):
    s = df[df["Type"]=="Sales"]
    e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum()
    exp = e["Amount"].sum()
    profit = rev - exp
    margin = (profit/rev*100) if rev > 0 else 0
    bench = INDUSTRY_BENCHMARKS.get(industry, 15)
    
    leaks = []
    
    # 1. CASH STUCK: Overdue Invoices
    if "Status" in df.columns:
        overdue_df = df[(df["Type"]=="Sales") & (df["Status"].str.lower().isin(["overdue","pending","not paid"]))]
        overdue = overdue_df["Amount"].sum()
        if overdue > 25000:
            annual_cost = overdue * 0.12
            top_debtors = overdue_df.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(3)
            debtor_list = ", ".join([f"{k} (₹{v/1000:.0f}K)" for k,v in top_debtors.items()])
            
            leaks.append({
                "type": "cash_stuck",
                "severity": "critical",
                "title": f"₹{overdue/100000:.1f}L stuck in unpaid invoices",
                "amount": overdue,
                "annual_cost": annual_cost,
                "description": f"Top debtors: {debtor_list}. You are losing working capital monthly.",
                "action": f"Call {top_debtors.index[0]} today. Offer 2% discount for payment within 48 hours.",
                "template": f"Hi, your invoice of ₹{top_debtors.iloc[0]/1000:.0f}K is pending. Pay this week for 2% discount."
            })
    
    # 2. COST BLEED: Vendor Overpayment
    if len(e) > 0:
        for category in e["Category"].unique():
            cat_exp = e[e["Category"]==category]
            if len(cat_exp) >= 3:
                vendor_prices = cat_exp.groupby("Party")["Amount"].agg(['mean','count'])
                vendor_prices = vendor_prices[vendor_prices['count'] >= 2]
                
                if len(vendor_prices) >= 2:
                    cheapest = vendor_prices['mean'].min()
                    expensive = vendor_prices['mean'].max()
                    expensive_vendor = vendor_prices['mean'].idxmax()
                    
                    if expensive > cheapest * 1.20:
                        premium_pct = ((expensive - cheapest) / cheapest) * 100
                        annual_volume = cat_exp[cat_exp["Party"]==expensive_vendor]["Amount"].sum()
                        overspend = (expensive - cheapest) * (annual_volume / expensive)
                        
                        if overspend > 30000:
                            leaks.append({
                                "type": "cost_bleed",
                                "severity": "warning",
                                "title": f"Overpaying {expensive_vendor} by {premium_pct:.0f}%",
                                "amount": overspend,
                                "annual_cost": overspend,
                                "description": f"Same {category} available ₹{cheapest:.0f}/unit vs your ₹{expensive:.0f}. Market rate is lower.",
                                "action": f"Get 3 quotes for {category}. Switch = ₹{overspend/100000:.1f}L/year saved.",
                                "template": f"Requesting quotes for {category}. Current supplier charging premium. Best quote by Friday gets business."
                            })
                            break
    
    # 3. MARGIN GAP
    if margin < bench - 3:
        gap_amount = ((bench - margin) / 100) * rev
        if gap_amount > 50000:
            leaks.append({
                "type": "margin_gap",
                "severity": "critical" if margin < 5 else "warning",
                "title": f"Profit margin {margin:.1f}% vs {bench}% industry avg",
                "amount": gap_amount,
                "annual_cost": gap_amount,
                "description": f"You are earning ₹{gap_amount/100000:.1f}L less per year than peers. Every month of delay = ₹{gap_amount/12/100000:.1f}L lost.",
                "action": f"Audit top 2 expenses. Cut 10% = ₹{gap_amount*0.1/100000:.1f}L immediate boost.",
                "template": "Reviewing expenses this week. Need to reduce costs by 10%. What can you offer?"
            })
    
    # 4. CONCENTRATION RISK
    if len(s) > 0:
        cust_rev = s.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cust_rev) > 0:
            top_pct = (cust_rev.iloc[0] / rev) * 100
            if top_pct > 35:
                risk_value = cust_rev.iloc[0]
                leaks.append({
                    "type": "concentration",
                    "severity": "warning",
                    "title": f"One customer = {top_pct:.0f}% of revenue (DANGER)",
                    "amount": risk_value * 0.15,
                    "annual_cost": risk_value * 0.15,
                    "description": f"{cust_rev.index[0]} can destroy your business if they leave. No negotiation power.",
                    "action": "Sign 2 new customers this month. Diversify or die.",
                    "template": "Looking to expand client base. Currently dependent on one major client. References welcome."
                })
    
    # 5. EXPENSE SPIKE
    if len(e) > 0:
        monthly_exp = e.groupby(e["Date"].dt.to_period("M"))["Amount"].sum()
        if len(monthly_exp) >= 3:
            recent_avg = monthly_exp.iloc[-3:].mean()
            previous_avg = monthly_exp.iloc[:-3].mean() if len(monthly_exp) > 3 else monthly_exp.iloc[0]
            
            if recent_avg > previous_avg * 1.25:
                spike_amount = (recent_avg - previous_avg) * 12
                if spike_amount > 40000:
                    leaks.append({
                        "type": "expense_spike",
                        "severity": "warning",
                        "title": f"Expenses up {((recent_avg/previous_avg-1)*100):.0f}% recently",
                        "amount": spike_amount,
                        "annual_cost": spike_amount,
                        "description": f"Monthly burn increased by ₹{(recent_avg-previous_avg)/1000:.0f}K. At this rate, you will bleed ₹{spike_amount/100000:.1f}L/year.",
                        "action": "Freeze all non-essential spending this week. Audit last 10 payments.",
                        "template": "Implementing cost freeze this week. Reviewing all expenses above ₹10K. Justification required."
                    })
    
    return sorted(leaks, key=lambda x: x['annual_cost'], reverse=True)

# ─── ACTION PLAN GENERATOR ───────────────────────────────────────────────────
def generate_action_plan(df, industry, leaks):
    actions = []
    s = df[df["Type"]=="Sales"]
    e = df[df["Type"]=="Expense"]
    
    # Day 1: Cash recovery
    cash_leaks = [l for l in leaks if l['type']=='cash_stuck']
    if cash_leaks:
        l = cash_leaks[0]
        actions.append({
            "day": "Monday",
            "icon": "🚨",
            "title": "URGENT: Recover stuck cash",
            "task": l['action'],
            "impact": f"₹{l['annual_cost']/100000:.1f}L/year saved",
            "template": l['template']
        })
    else:
        actions.append({
            "day": "Monday",
            "icon": "💰",
            "title": "Optimize collections",
            "task": "Review payment terms. Offer 2% discount for advance payment.",
            "impact": "Improve cash flow by 15%",
            "template": "We now offer 2% discount for payment within 7 days. Interested?"
        })
    
    # Day 2: Cost cutting
    cost_leaks = [l for l in leaks if l['type']=='cost_bleed']
    if cost_leaks:
        l = cost_leaks[0]
        actions.append({
            "day": "Tuesday",
            "icon": "✂️",
            "title": "Cut supplier costs",
            "task": l['action'],
            "impact": f"Save ₹{l['annual_cost']/100000:.1f}L/year",
            "template": l['template']
        })
    else:
        top_exp = e.groupby("Category")["Amount"].sum().idxmax() if len(e) > 0 else "expenses"
        actions.append({
            "day": "Tuesday",
            "icon": "✂️",
            "title": f"Audit {top_exp}",
            "task": f"Review last 10 {top_exp} payments. Flag unusual amounts.",
            "impact": "Find 5-10% waste",
            "template": f"Reviewing {top_exp} costs. Need to reduce by 10%. What options do we have?"
        })
    
    # Day 3: Margin improvement
    margin_leaks = [l for l in leaks if l['type']=='margin_gap']
    if margin_leaks:
        l = margin_leaks[0]
        actions.append({
            "day": "Wednesday",
            "icon": "📈",
            "title": "Fix profit margin",
            "task": l['action'],
            "impact": f"Recover ₹{l['annual_cost']/100000:.1f}L/year",
            "template": l['template']
        })
    else:
        actions.append({
            "day": "Wednesday",
            "icon": "📈",
            "title": "Review pricing",
            "task": "Check if top 5 customers are on old rates. Raise prices 5%.",
            "impact": "5% revenue boost with same costs",
            "template": "Due to rising costs, we are updating our rates by 5% from next month. Value remains unchanged."
        })
    
    # Day 4: Risk management
    risk_leaks = [l for l in leaks if l['type']=='concentration']
    if risk_leaks:
        l = risk_leaks[0]
        actions.append({
            "day": "Thursday",
            "icon": "🛡️",
            "title": "Reduce customer risk",
            "task": l['action'],
            "impact": "Protect business continuity",
            "template": l['template']
        })
    else:
        actions.append({
            "day": "Thursday",
            "icon": "🛡️",
            "title": "Diversify revenue",
            "task": "Identify 2 new customer segments. Start outreach.",
            "impact": "Reduce dependency risk",
            "template": "Exploring new partnerships. Who do you know that needs our services?"
        })
    
    # Day 5: Industry-specific
    industry_actions = {
        "restaurant": {"icon": "🍽️", "title": "Food cost audit", "task": "Check yesterday's wastage. Compare 3 supplier quotes for raw materials.", "impact": "5-10% cost reduction"},
        "clinic": {"icon": "🏥", "title": "Maximize patient value", "task": "Check consultation to lab conversion rate. Are you capturing full visit value?", "impact": "15% revenue per patient"},
        "retail": {"icon": "🛒", "title": "Clear dead stock", "task": "Identify SKUs not sold in 60 days. Run discount sale this weekend.", "impact": "Free up working capital"},
        "agency": {"icon": "💼", "title": "Billable hours check", "task": "Compare team salaries to hours billed. Cut idle capacity.", "impact": "20% margin improvement"},
        "manufacturing": {"icon": "🏭", "title": "Production efficiency", "task": "Check scrap/wastage rates. Benchmark against industry standard.", "impact": "Reduce unit cost by 8%"},
        "logistics": {"icon": "🚚", "title": "Route optimization", "task": "Analyze fuel costs per km. Identify inefficient routes.", "impact": "12% fuel savings"}
    }
    
    ia = industry_actions.get(industry, {"icon": "📊", "title": "Weekly review", "task": "Analyze top 5 customers and expenses. Trend vs last month.", "impact": "Stay on top of numbers"})
    actions.append({
        "day": "Friday",
        "icon": ia["icon"],
        "title": ia["title"],
        "task": ia["task"],
        "impact": ia["impact"],
        "template": "Weekly business review complete. Key focus areas identified for next week."
    })
    
    return actions

# ─── PDF REPORT GENERATOR ────────────────────────────────────────────────────
class LeakReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(200, 255, 87)
        self.cell(0, 10, 'OpsClarity Profit Leak Report', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%d %b %Y")}', 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.set_text_color(200, 200, 200)
        self.multi_cell(0, 5, body)
        self.ln()

def generate_pdf_report(leaks, actions, summary):
    pdf = LeakReportPDF()
    pdf.add_page()
    pdf.set_fill_color(8, 8, 16)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Summary
    pdf.chapter_title('EXECUTIVE SUMMARY')
    total_leak = sum(l['annual_cost'] for l in leaks)
    pdf.chapter_body(f"Total Profit Leaks Detected: ₹{total_leak/100000:.1f}L per year\nRevenue Analyzed: {summary['revenue']}\nProfit Margin: {summary['margin']:.1f}%\nIndustry Benchmark: {summary['benchmark']}%")
    
    # Leaks
    pdf.chapter_title('DETECTED LEAKS')
    for i, leak in enumerate(leaks, 1):
        severity = "CRITICAL" if leak['severity']=='critical' else "WARNING"
        pdf.chapter_body(f"{i}. {leak['title']} [{severity}]\n   Annual Impact: ₹{leak['annual_cost']/100000:.1f}L\n   {leak['description']}\n   ACTION: {leak['action']}")
    
    # Action Plan
    pdf.chapter_title('5-DAY RECOVERY PLAN')
    for act in actions:
        pdf.chapter_body(f"{act['day']}: {act['title']}\nTask: {act['task']}\nExpected Impact: {act['impact']}")
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, 'OpsClarity.in | Built for Indian SMEs | Management estimate, not professional CA advice', 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin1')

# ─── SESSION STATE ────────────────────────────────────────────────────────────
defaults = {"df":None,"industry":"restaurant","leaks":[],"actions":[],"page":"sme","spots":73}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ─── NAVIGATION ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
    <div class="nav-logo">◈<span style="color:#c8ff57;"> OpsClarity</span></div>
    <div style="display:flex;gap:12px;align-items:center;">
        <div class="nav-badge">Profit Recovery System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN APPLICATION ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Trusted by 200+ Indian SMEs</div>
    <h1 class="hero-title">Find where your business<br>is <em>leaking money</em> — instantly</h1>
    <p class="hero-sub">Upload your Tally, Excel, or bank statement. Get specific rupee amounts you are losing and a 5-day action plan to recover them.</p>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
uc1, uc2 = st.columns([2,1])

with uc1:
    uploaded = st.file_uploader(
        "Drop your Tally Day Book, Sales Register, or Excel/CSV",
        type=["csv","xlsx","xls"]
    )
    
    with st.expander("How to export from Tally (3 clicks)"):
        st.markdown("""
**Tally Prime / ERP9:**
1. Go to **Display → Account Books → Day Book** (or Sales Register)
2. Press **Alt+E** → Select **Excel** format
3. Set date range → Export → Upload here

**What we detect:** Overdue invoices, vendor overpayment, margin gaps, customer concentration, expense spikes
        """)

with uc2:
    industry_name = st.selectbox("Your industry", list(INDUSTRY_MAP.keys()))
    ind = INDUSTRY_MAP[industry_name]
    
    if st.button("Try with sample data", use_container_width=True):
        np.random.seed(42)
        months = pd.date_range("2024-01-01", "2024-12-31", freq="ME")
        records = []
        
        cfg = {
            "restaurant": {"customers": ["Ravi Enterprises","Meena Stores","Krishna Traders"], "cats": ["Raw Materials","Staff Salary","Rent","Electricity"]},
            "clinic": {"customers": ["Apollo Health","Sharma Family","City Hospital"], "cats": ["Medicines","Doctor Salaries","Rent","Equipment"]},
            "retail": {"customers": ["Metro Traders","Quick Mart","Raj Superstore"], "cats": ["Inventory","Staff Wages","Rent","Marketing"]},
            "agency": {"customers": ["TechStart","Growfast Brands","FinEdge"], "cats": ["Salaries","Software","Freelancers","Marketing"]}
        }
        c = cfg.get(ind, cfg["retail"])
        
        for month in months:
            for _ in range(20):
                records.append({
                    "Date": month - timedelta(days=np.random.randint(0,28)),
                    "Type": "Sales",
                    "Party": np.random.choice(c["customers"]),
                    "Amount": np.random.uniform(15000, 75000),
                    "Status": np.random.choice(["Paid","Paid","Paid","Overdue"], p=[0.6,0.2,0.1,0.1])
                })
            for cat in c["cats"]:
                records.append({
                    "Date": month - timedelta(days=np.random.randint(0,28)),
                    "Type": "Expense",
                    "Category": cat,
                    "Party": "Vendor",
                    "Amount": np.random.uniform(8000, 45000) * (1.5 if cat in ["Raw Materials","Inventory"] else 1),
                    "Status": "Paid"
                })
        
        df_sample = pd.DataFrame(records)
        df_sample["Date"] = pd.to_datetime(df_sample["Date"])
        df_sample["Month"] = df_sample["Date"].dt.to_period("M").astype(str)
        
        st.session_state.df = df_sample
        st.session_state.industry = ind
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Process Upload
if uploaded:
    df_up, ok, msg = parse_file(uploaded)
    if ok:
        st.session_state.df = df_up
        st.session_state.industry = ind
        st.success(msg)
    else:
        st.error(f"Parse error: {msg}. Try CSV format or contact support.")

# ─── DASHBOARD DISPLAY ────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df
    industry = st.session_state.industry
    
    s = df[df["Type"]=="Sales"]
    e = df[df["Type"]=="Expense"]
    rev = s["Amount"].sum()
    exp = e["Amount"].sum()
    profit = rev - exp
    margin = (profit/rev*100) if rev > 0 else 0
    bench = INDUSTRY_BENCHMARKS.get(industry, 15)
    
    leaks = detect_profit_leaks(df, industry)
    total_leak = sum(l['annual_cost'] for l in leaks)
    actions = generate_action_plan(df, industry, leaks)
    
    # ─── PROFIT LEAK HERO ─────────────────────────────────────────────────────
    if total_leak > 0:
        st.markdown(f"""
        <div class="leak-hero">
            <div class="leak-title">Profit Leaks Detected</div>
            <div class="leak-amount">₹{total_leak/100000:.1f}L/year</div>
            <div style="color:#9090a4;font-size:14px;margin-top:1rem;">
                Found {len(leaks)} critical issues. Fix these = immediate profit recovery.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="leak-hero green">
            <div class="leak-title">No Major Leaks Detected</div>
            <div class="leak-amount">Business Running Tight</div>
            <div style="color:#9090a4;font-size:14px;margin-top:1rem;">
                Margin {margin:.1f}% is healthy. Continue monitoring monthly.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ─── DETAILED LEAKS ───────────────────────────────────────────────────────
    if leaks:
        st.markdown('<div class="section-title">Detailed Leak Analysis</div>', unsafe_allow_html=True)
        
        for leak in leaks[:4]:
            severity_class = leak['severity']
            st.markdown(f"""
            <div class="leak-card {severity_class}">
                <div class="leak-card-header">
                    <span class="leak-card-title">{leak['title']}</span>
                    <span class="leak-card-amount">₹{leak['annual_cost']/100000:.1f}L/year</span>
                </div>
                <div class="leak-card-desc">{leak['description']}</div>
                <div class="leak-card-action">
                    <strong>This week:</strong> {leak['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ─── KPI STRIP ────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    overdue = df[(df["Type"]=="Sales") & (df["Status"].str.lower().isin(["overdue","pending"]))]["Amount"].sum() if "Status" in df.columns else 0
    
    st.markdown(f"""
    <div class="kpi-strip">
        <div class="kpi">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-val">{fmt(rev)}</div>
            <div class="kpi-sub">{len(s)} transactions</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Expenses</div>
            <div class="kpi-val">{fmt(exp)}</div>
            <div class="kpi-sub">{len(e)} transactions</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-val" style="color:{'#c8ff57' if margin>bench else '#ffb557' if margin>5 else '#ff5e5e'};">{margin:.1f}%</div>
            <div class="kpi-sub">vs {bench}% benchmark</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Overdue</div>
            <div class="kpi-val" style="color:{'#ff5e5e' if overdue>rev*0.05 else '#c8ff57'};">{fmt(overdue)}</div>
            <div class="kpi-sub">{(overdue/rev*100 if rev>0 else 0):.1f}% of revenue</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ─── 5-DAY ACTION PLAN ────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your 5-Day Profit Recovery Plan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Specific tasks with templates. Do these = money back in your account.</div>', unsafe_allow_html=True)
    
    for act in actions:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-header">
                <div class="action-icon-title">
                    <span class="action-icon">{act['icon']}</span>
                    <span class="action-title">{act['title']}</span>
                </div>
                <span class="action-day">{act['day']}</span>
            </div>
            <div class="action-task">{act['task']}</div>
            <div class="action-impact">Expected Impact: {act['impact']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ─── DOWNLOAD & SHARE ─────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    summary = {'revenue': fmt(rev), 'margin': margin, 'benchmark': bench}
    pdf_bytes = generate_pdf_report(leaks, actions, summary)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "Download PDF Report",
            pdf_bytes,
            f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            "application/pdf",
            use_container_width=True
        )
    
    with col2:
        share_text = f"""OpsClarity Profit Leak Report

Total Leaks Found: ₹{total_leak/100000:.1f}L/year
Revenue: {fmt(rev)} | Margin: {margin:.1f}%
5-Day Action Plan Generated

opsclarity.streamlit.app"""
        wa_link = f"https://wa.me/?text={urllib.parse.quote(share_text)}"
        st.markdown(f'<a href="{wa_link}" target="_blank" style="display:block;background:#25D366;color:white;padding:11px;border-radius:12px;text-align:center;font-size:14px;font-weight:700;text-decoration:none;">Share on WhatsApp</a>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Copy Summary", use_container_width=True):
            st.code(share_text)
    
    # ─── TRENDS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Monthly Trends", "Expense Breakdown"])
    
    with tab1:
        monthly = df.groupby([df["Date"].dt.to_period("M"), "Type"])["Amount"].sum().unstack(fill_value=0)
        st.line_chart(monthly, use_container_width=True, height=300)
    
    with tab2:
        if len(e) > 0:
            exp_by_cat = e.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            st.bar_chart(exp_by_cat, use_container_width=True, height=300)
    
    # ─── PRICING ──────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    spots = st.session_state.spots
    st.markdown(f"""
    <div class="paywall">
        <div style="background:rgba(255,80,80,0.08);border:1px solid rgba(255,80,80,0.2);border-radius:10px;padding:.8rem;margin-bottom:1.2rem;">
            <div style="color:#ff7070;font-weight:600;font-size:14px;">Only {spots} free full analyses remaining this month</div>
        </div>
        <div class="section-title" style="text-align:center;">Unlock Unlimited Profit Recovery</div>
        
        <div class="pricing-grid">
            <div class="price-card">
                <div class="price-who">Starter</div>
                <div class="price-amt">₹0</div>
                <div class="price-title">Free</div>
                <ul class="price-features">
                    <li>1 leak report/month</li>
                    <li>Basic analysis</li>
                    <li>PDF download</li>
                </ul>
            </div>
            <div class="price-card featured">
                <div class="price-who">For SME Owners</div>
                <div class="price-amt">₹499<span style="font-size:12px;color:#5a5a70;">/mo</span></div>
                <div class="price-title">Pro</div>
                <ul class="price-features">
                    <li>Unlimited reports</li>
                    <li>WhatsApp weekly alerts</li>
                    <li>Vendor benchmarking</li>
                    <li>CA chat support</li>
                </ul>
            </div>
            <div class="price-card">
                <div class="price-who">For CAs & Advisors</div>
                <div class="price-amt">₹1,999<span style="font-size:12px;color:#5a5a70;">/mo</span></div>
                <div class="price-title">CA Partner</div>
                <ul class="price-features">
                    <li>50 client seats</li>
                    <li>White-label reports</li>
                    <li>GST risk scanner</li>
                    <li>Priority support</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("Start Free Trial — 14 Days", use_container_width=True, type="primary"):
            st.session_state.spots = max(0, spots - 1)
            st.balloons()
            st.success("Trial activated! Check WhatsApp for onboarding.")

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<a href="https://wa.me/916362319163?text=Hi%2C+I+need+help+with+OpsClarity" class="whatsapp-float" target="_blank">
    Chat with Us
</a>
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid rgba(255,255,255,.05);margin-top:2rem;">
    <div style="color:#4a4a60;font-size:12px;">OpsClarity · Profit Recovery for Indian SMEs · Built in Bangalore</div>
</div>
""", unsafe_allow_html=True)
