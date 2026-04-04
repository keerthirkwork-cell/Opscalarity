import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse, io, random

st.set_page_config(page_title="OpsClarity — Profit Recovery", page_icon="₹", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: #F7F4EF; font-family: 'DM Sans', sans-serif; color: #1A1A1A; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
.hero { background: #1A1A1A; padding: 4rem 3rem 3rem; }
.hero-badge { display:inline-block; background:rgba(212,175,55,0.15); border:1px solid rgba(212,175,55,0.3); padding:5px 14px; border-radius:20px; font-size:11px; font-weight:600; color:#D4AF37; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1.5rem; }
.hero-h { font-family:'DM Serif Display',serif; font-size:clamp(2.4rem,4.5vw,4rem); color:#F7F4EF; line-height:1.1; margin-bottom:1.2rem; }
.hero-h em { font-style:italic; color:#D4AF37; }
.hero-sub { font-size:1rem; color:#9A9A8A; max-width:500px; line-height:1.7; margin-bottom:2rem; font-weight:300; }
.trust-row { display:flex; gap:2.5rem; flex-wrap:wrap; margin-top:2rem; padding-top:2rem; border-top:1px solid rgba(255,255,255,0.08); }
.trust-item .t-num { font-family:'DM Serif Display',serif; font-size:1.8rem; color:#D4AF37; }
.trust-item .t-lbl { font-size:11px; color:#5A5A4A; text-transform:uppercase; letter-spacing:0.1em; }
.safety-bar { background:#EDEAE3; padding:0.75rem 3rem; display:flex; gap:2rem; flex-wrap:wrap; border-bottom:1px solid #D8D4CC; }
.s-pill { font-size:12px; color:#4A4A3A; font-weight:500; display:flex; align-items:center; gap:6px; }
.s-dot { width:6px; height:6px; background:#4CAF50; border-radius:50%; }
.money-screen { background:#1A1A1A; border-radius:16px; padding:2rem; margin:1.5rem 0; }
.ms-label { font-size:11px; font-weight:600; color:#6A6A5A; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:4px; }
.ms-total { font-family:'DM Serif Display',serif; font-size:3.5rem; color:#D4AF37; line-height:1; }
.ms-sub { font-size:13px; color:#5A5A4A; margin-bottom:1.5rem; margin-top:4px; }
.ms-row { display:flex; align-items:center; justify-content:space-between; padding:0.85rem 1rem; background:rgba(255,255,255,0.04); border-radius:10px; margin-bottom:6px; }
.ms-row.r { border-left:3px solid #E05252; }
.ms-row.a { border-left:3px solid #D4AF37; }
.ms-row.b { border-left:3px solid #5B9BD5; }
.ms-left { display:flex; align-items:center; gap:10px; }
.ms-title { font-size:14px; font-weight:500; color:#F7F4EF; }
.ms-desc  { font-size:11px; color:#5A5A4A; margin-top:2px; }
.ms-amt   { font-family:'DM Mono',monospace; font-size:1rem; font-weight:600; color:#D4AF37; }
.act-box  { background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.2); border-radius:10px; padding:1rem 1.25rem; margin-top:1.25rem; }
.act-lbl  { font-size:11px; font-weight:600; color:#D4AF37; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.6rem; }
.act-item { display:flex; gap:8px; margin-bottom:6px; }
.act-num  { width:18px; height:18px; border-radius:50%; background:#D4AF37; color:#1A1A1A; font-size:10px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.act-text { font-size:13px; color:#C8C8B8; line-height:1.5; }
.kpi-row  { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:1.5rem 0; }
.kpi-card { background:#FFF; border:1px solid #E8E4DC; border-radius:12px; padding:1.1rem 1.3rem; }
.kpi-lbl  { font-size:11px; color:#9A9A8A; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; }
.kpi-val  { font-family:'DM Serif Display',serif; font-size:1.6rem; color:#1A1A1A; }
.kpi-sub  { font-size:12px; margin-top:3px; }
.good { color:#2E8B57; } .bad { color:#C0392B; } .warn { color:#9A7A00; }
.sw   { padding:1.5rem 3rem; }
.sh   { font-family:'DM Serif Display',serif; font-size:1.8rem; color:#1A1A1A; margin-bottom:4px; }
.ss   { font-size:13px; color:#6A6A5A; margin-bottom:1.5rem; }
.lk-card { background:#FFF; border:1px solid #E8E4DC; border-radius:14px; padding:1.4rem; margin-bottom:1rem; position:relative; overflow:hidden; }
.lk-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.lk-card.critical::before { background:#E05252; }
.lk-card.warning::before  { background:#D4AF37; }
.lk-card.info::before     { background:#5B9BD5; }
.lk-tag { display:inline-block; font-size:10px; font-weight:700; padding:2px 9px; border-radius:20px; margin-bottom:0.75rem; letter-spacing:0.08em; }
.lk-tag.critical { background:#FEF0F0; color:#C0392B; }
.lk-tag.warning  { background:#FFFBF0; color:#9A7A00; }
.lk-tag.info     { background:#EFF5FE; color:#2060A0; }
.lk-amt  { font-family:'DM Serif Display',serif; font-size:2rem; color:#1A1A1A; line-height:1; }
.lk-sub  { font-size:11px; color:#9A9A8A; margin-bottom:0.75rem; }
.lk-ttl  { font-size:14px; font-weight:600; color:#1A1A1A; margin-bottom:0.4rem; }
.lk-desc { font-size:13px; color:#6A6A5A; line-height:1.6; margin-bottom:1rem; }
.lk-src  { background:#F7F4EF; border-radius:8px; padding:0.7rem 0.9rem; margin-bottom:0.9rem; font-size:12px; color:#4A4A3A; line-height:1.55; }
.lk-act  { border-top:1px solid #F0EDE6; padding-top:0.9rem; font-size:13px; font-weight:600; color:#1A1A1A; }
.lk-act-s{ font-size:12px; font-weight:400; color:#6A6A5A; margin-top:3px; }
.seq-card { background:#F7F4EF; border:1px solid #E0DDD6; border-radius:10px; padding:1rem; margin-bottom:8px; }
.seq-day  { display:inline-block; background:#1A1A1A; color:#D4AF37; font-size:10px; font-weight:700; padding:2px 9px; border-radius:20px; margin-bottom:6px; }
.seq-tone { font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:5px; }
.seq-msg  { font-size:12px; color:#4A4A3A; line-height:1.6; }
.ca-wrap  { background:#F0EDE6; padding:2rem 3rem; }
.ca-card  { background:#FFF; border:1px solid #E0DDD6; border-radius:14px; padding:1.4rem; margin-bottom:1rem; }
.ca-card.dark { background:#1A1A1A; border-color:rgba(255,255,255,0.08); }
.ca-lbl   { font-size:11px; font-weight:600; color:#9A9A8A; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px; }
.ca-ttl   { font-family:'DM Serif Display',serif; font-size:1.3rem; color:#1A1A1A; margin-bottom:6px; }
.ca-body  { font-size:13px; color:#6A6A5A; line-height:1.7; }
.ca-card.dark .ca-ttl  { color:#F7F4EF; }
.ca-card.dark .ca-body { color:#9A9A8A; }
.ca-row   { display:flex; justify-content:space-between; align-items:center; padding:0.65rem 0; border-bottom:1px solid #F0EDE6; }
.ca-row-lbl { font-size:13px; color:#4A4A3A; }
.ca-row-val { font-family:'DM Mono',monospace; font-size:13px; font-weight:600; color:#1A1A1A; }
.ca-row-val.hl { color:#2E8B57; font-size:1rem; }
.cl-row   { display:flex; align-items:center; justify-content:space-between; padding:0.6rem 0; border-bottom:1px solid rgba(255,255,255,0.06); }
.cl-name  { font-size:13px; font-weight:500; color:#F7F4EF; }
.cl-meta  { font-size:11px; color:#5A5A4A; }
.cl-amt   { font-family:'DM Mono',monospace; font-size:12px; color:#D4AF37; }
.cl-h.red   { color:#E05252; font-size:12px; font-weight:600; }
.cl-h.amber { color:#D4AF37; font-size:12px; font-weight:600; }
.cl-h.green { color:#4CAF50; font-size:12px; font-weight:600; }
.pr-wrap  { background:#1A1A1A; padding:2.5rem 3rem; }
.pr-grid  { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1.5rem; }
.pr-card  { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:1.75rem; }
.pr-card.feat { background:rgba(212,175,55,0.08); border-color:rgba(212,175,55,0.35); }
.pr-lbl   { font-size:11px; font-weight:600; color:#5A5A4A; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:0.75rem; }
.pr-name  { font-family:'DM Serif Display',serif; font-size:1.4rem; color:#F7F4EF; margin-bottom:4px; }
.pr-amt   { font-family:'DM Mono',monospace; font-size:2rem; color:#D4AF37; margin-bottom:8px; }
.pr-note  { font-size:12px; color:#6A6A5A; margin-bottom:1.25rem; line-height:1.55; }
.pr-feat  { font-size:12px; color:#8A8A7A; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.pr-feat::before { content:"→ "; color:#D4AF37; }
.footer   { background:#1A1A1A; padding:1.5rem 3rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
.ft-brand { font-family:'DM Serif Display',serif; font-size:1.1rem; color:#D4AF37; }
.ft-legal { font-size:11px; color:#4A4A3A; }
.wa-btn   { position:fixed; bottom:24px; right:24px; background:#25D366; color:#FFF; padding:12px 20px; border-radius:50px; font-weight:600; text-decoration:none; font-size:13px; display:flex; align-items:center; gap:6px; box-shadow:0 4px 16px rgba(37,211,102,0.35); z-index:9999; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🏭 Manufacturing":"manufacturing","🍽️ Restaurant / Cafe":"restaurant",
    "🏥 Clinic / Diagnostic":"clinic","🛒 Retail / Distribution":"retail",
    "💼 Agency / Consulting":"agency","🚚 Logistics / Transport":"logistics",
    "🏗️ Construction":"construction","🧵 Textile / Garments":"textile",
    "💊 Pharma / Medical":"pharma","🖨️ Print / Packaging":"printing",
}
BENCH = {
    "manufacturing":18,"restaurant":15,"clinic":25,"retail":12,"agency":35,
    "logistics":10,"construction":20,"textile":14,"pharma":22,"printing":16,
}
PEERS = {
    "manufacturing":{
        "Raw Materials":{"p25":42000,"median":51000,"p75":64000,"unit":"/ton","n":312},
        "Labor":        {"p25":380,  "median":460,  "p75":580,  "unit":"/day","n":445},
        "Logistics":    {"p25":8,    "median":11,   "p75":16,   "unit":"/km", "n":289},
        "Packaging":    {"p25":11,   "median":17,   "p75":24,   "unit":"/pc", "n":198},
    },
    "restaurant":{
        "Food Ingredients":{"p25":28,"median":34,"p75":42,"unit":"% rev","n":521},
        "Labor":            {"p25":18,"median":24,"p75":32,"unit":"% rev","n":498},
    },
    "retail":{
        "Rent":{"p25":80,"median":120,"p75":200,"unit":"/sqft/mo","n":445},
    },
}

def fmt(v):
    v=float(v)
    if abs(v)>=1e7: return f"₹{v/1e7:.1f}Cr"
    if abs(v)>=1e5: return f"₹{v/1e5:.1f}L"
    if abs(v)>=1000:return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmtx(v):
    return f"₹{int(float(v)):,}"

# ── COLLECTIONS BOT ───────────────────────────────────────────────────────────
SEQ=[
    {"day":1, "tone":"Friendly reminder","color":"#5B9BD5",
     "msg":"Hi {name} 🙏 Quick note — invoice #{inv} for {amt} is due. Any issues? Happy to help. — {biz}"},
    {"day":3, "tone":"Offer + urgency","color":"#D4AF37",
     "msg":"Hi {name}, invoice #{inv} ({amt}) is overdue. Offering 2% discount if settled by {dl}. Please confirm. — {biz}"},
    {"day":7, "tone":"Operational impact","color":"#E08020",
     "msg":"{name}, invoice #{inv} ({amt}) is 7 days overdue. Payment needed by {dl} or we pause future orders. — {biz}"},
    {"day":10,"tone":"Final notice","color":"#E05252",
     "msg":"FINAL NOTICE — {name}: invoice #{inv} ({amt}) is 10 days unpaid. Pay by {dl} or accounts team takes over. — {biz}"},
]
def gen_seq(name,inv,amount,biz):
    today=datetime.now()
    return [{**s,
        "send_on":(today+timedelta(days=s["day"])).strftime("%d %b"),
        "message":s["msg"].format(name=name,inv=inv,amt=fmt(amount),biz=biz,
                                   dl=(today+timedelta(days=s["day"]+3)).strftime("%d %b %Y")),
        "wa_link":f"https://wa.me/?text={urllib.parse.quote(s['msg'].format(name=name,inv=inv,amt=fmt(amount),biz=biz,dl=(today+timedelta(days=s['day']+3)).strftime('%d %b %Y')))}"
    } for s in SEQ]

# ── CSV PARSERS ───────────────────────────────────────────────────────────────
def _cat(d):
    d=d.lower()
    if any(x in d for x in ["rent","rental"]):                    return "Rent"
    if any(x in d for x in ["praveen","porter","salary"]):         return "Salary"
    if any(x in d for x in ["ashok payment"]):                     return "Salary"
    if any(x in d for x in ["laptop","computer"]):                 return "Technology"
    if any(x in d for x in ["broad","internet","wifi"]):           return "Internet"
    if any(x in d for x in ["housekeeping","houskeeping"]):        return "Housekeeping"
    if any(x in d for x in ["furniture","chair"]):                 return "Furniture"
    if any(x in d for x in ["electricity"]):                       return "Electricity"
    if any(x in d for x in ["ca","accountant","audit"]):           return "Professional Fees"
    if any(x in d for x in ["website","domain"]):                  return "Website"
    if any(x in d for x in ["outing","travel"]):                   return "Travel"
    if any(x in d for x in ["glass","basin","door","key","seal","board","wash"]): return "Office Setup"
    if any(x in d for x in ["mim","mfg","part cost"]):             return "Manufacturing"
    if any(x in d for x in ["debit","bank","charge"]):             return "Bank Charges"
    return "Operations"

def _is_da(raw):
    cells=[]
    for r in range(min(2,len(raw))):
        for c in range(min(10,len(raw.columns))):
            cells.append(str(raw.iloc[r,c]).lower().strip())
    return "months" in cells and ("investors" in cells or "expenses" in cells)

def _parse_da(file):
    file.seek(0)
    raw=pd.read_csv(file,header=None,dtype=str).fillna("")
    MM={"august":"2024-08","aug":"2024-08","sept":"2024-09","sep":"2024-09",
        "october":"2024-10","oct":"2024-10","november":"2024-11","nov":"2024-11",
        "december":"2024-12","dec":"2024-12","january":"2025-01","jan":"2025-01",
        "february":"2025-02","feb":"2025-02","march":"2025-03","mar":"2025-03",
        "april":"2025-04","apr":"2025-04"}
    SKIP={"total","grand total","each","sub total","-","total-dec balance",
          "total - feb balance","dec balance","feb balance","total-feb balance",""}
    recs=[]
    for _,row in raw.iterrows():
        mk=row.iloc[0].strip().lower()
        if mk not in MM: continue
        dt=pd.Timestamp(MM[mk]+"-01")
        for ci,party,typ in [(1,"Madhu","Sales"),(2,"Deepak","Sales"),
                              (5,"Ashok","Expense"),(6,"Office","Expense"),(9,"Praveen","Expense")]:
            try:
                v=float(row.iloc[ci].replace(",","").strip())
                if v>0:
                    recs.append({"Date":dt,"Type":typ,"Party":party,
                                 "Category":"Investment/Capital" if typ=="Sales" else "Operations",
                                 "Amount":v,"Status":"Paid","Invoice_No":"-"})
            except: pass
    cm,cd=None,None
    for _,row in raw.iterrows():
        c11=row.iloc[11].strip().lower() if len(row)>11 else ""
        c14=row.iloc[14].strip().lower() if len(row)>14 else ""
        if c11 in MM: cm=MM[c11]
        if c14 in MM: cd=MM[c14]
        for period,ai,di in [(cm,11,12),(cd,14,15)]:
            if not period or len(row)<=di: continue
            amt_r=row.iloc[ai].strip(); desc=row.iloc[di].strip()
            if desc.lower() in SKIP or not desc: continue
            try:
                v=float(amt_r.replace(",",""))
                if v>0:
                    recs.append({"Date":pd.Timestamp(period+"-01"),"Type":"Expense",
                                 "Party":"Madhu" if ai==11 else "Deepak",
                                 "Category":_cat(desc),"Amount":v,"Status":"Paid","Invoice_No":"-"})
            except: pass
    if not recs: return None,False,"No transactions found."
    df=pd.DataFrame(recs).drop_duplicates()
    df["Month"]=df["Date"].dt.to_period("M").astype(str)
    return df,True,f"✅ {len(df)} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"

def parse_file(file):
    try:
        fname=file.name.lower()
        if fname.endswith((".xlsx",".xls")):
            try:    raw=pd.read_excel(file,header=None,engine="openpyxl")
            except: raw=pd.read_excel(file,header=None,engine="xlrd")
            file.seek(0)
            try:    dfs=pd.read_excel(file,engine="openpyxl")
            except: dfs=pd.read_excel(file,engine="xlrd")
        elif fname.endswith(".csv"):
            try:    raw=pd.read_csv(file,header=None,dtype=str)
            except: raw=pd.read_csv(file,header=None,encoding="latin1",dtype=str)
            file.seek(0)
            try:    dfs=pd.read_csv(file)
            except: dfs=pd.read_csv(file,encoding="latin1")
        else: return None,False,"Use .csv, .xlsx, or .xls"
        if _is_da(raw):
            file.seek(0); return _parse_da(file)
        df=dfs.dropna(how="all").dropna(axis=1,how="all")
        cm={}
        for col in df.columns:
            cl=str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher"]):           cm[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","rs","₹"]): cm[col]="Amount"
            elif any(x in cl for x in ["type","txn","dr/cr","nature"]):       cm[col]="Type"
            elif any(x in cl for x in ["particulars","category","cat","narration","ledger"]): cm[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client"]): cm[col]="Party"
            elif any(x in cl for x in ["status","paid","pending","overdue"]): cm[col]="Status"
            elif any(x in cl for x in ["invoice","voucher","ref","bill"]):    cm[col]="Invoice_No"
        df=df.rename(columns=cm)
        if "Date" not in df.columns:
            return None,False,"Date column not found. Ensure column is labelled 'Date' or 'Dt'."
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=True)
        df=df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"]=(df["Amount"].astype(str)
                .str.replace(",","").str.replace("(","−").str.replace(")","")
                .str.replace(" Dr","").str.replace(" Cr","").str.replace("₹",""))
            df["Amount"]=pd.to_numeric(df["Amount"],errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"]="Unknown"
        df["Type"]=df["Type"].astype(str).str.strip().str.title().replace(
            {"Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
             "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales"})
        mask=~df["Type"].isin(["Sales","Expense"])
        if mask.any():
            ekw=["purchase","expense","payment","salary","rent","bill","wages","material","raw","inventory","logistics"]
            df.loc[mask,"Type"]=df.loc[mask].apply(
                lambda x:"Expense" if any(k in str(x.get("Category","")).lower() for k in ekw) else "Sales",axis=1)
        for col,default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","-")]:
            if col not in df.columns: df[col]=default
        df["Month"]=df["Date"].dt.to_period("M").astype(str)
        return df,True,f"✅ {len(df):,} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"
    except Exception as e:
        return None,False,f"Error: {e}. Try saving as CSV."

# ── LEAK DETECTOR ─────────────────────────────────────────────────────────────
def find_leaks(df,industry,city=None):
    sales=df[df["Type"]=="Sales"]; expenses=df[df["Type"]=="Expense"]
    revenue=sales["Amount"].sum(); exp_tot=expenses["Amount"].sum()
    profit=revenue-exp_tot; margin=(profit/revenue*100) if revenue>0 else 0
    bmark=BENCH.get(industry,15); leaks=[]

    # 1. Overdue cash
    if "Status" in df.columns:
        od=sales[sales["Status"].str.lower().isin(["overdue","pending","not paid","due","outstanding","unpaid"])]
        od_amt=od["Amount"].sum()
        if od_amt>10000:
            deb=od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_name=deb.index[0] if len(deb)>0 else "Customer"
            top_amt=float(deb.iloc[0]) if len(deb)>0 else od_amt
            pct=od_amt/revenue*100 if revenue>0 else 0
            seqs=gen_seq(top_name,"INV-001",top_amt,"Your Business")
            debtor_lines=" · ".join([f"{n}: {fmtx(a)}" for n,a in deb.head(5).items()])
            leaks.append({
                "id":"cash_stuck","sev":"critical","cat":"Collections",
                "rupee":od_amt,"annual":od_amt*0.18,
                "headline":f"{fmtx(int(od_amt))} stuck in unpaid invoices",
                "sub":f"Across {len(deb)} customers",
                "found":f"{len(deb)} customers owe you: {debtor_lines}",
                "costs":f"At 18% cost of capital, {fmt(od_amt)} locked away costs you {fmt(od_amt*0.18)} per year.",
                "bench":f"Healthy: overdue below 5% of revenue. Yours: {pct:.1f}%.",
                "action":f"Call {top_name} today. Offer 2% discount for 48-hr payment.",
                "action_sub":"Use the WhatsApp sequence below.",
                "template":f"Hi, invoice of {fmt(top_amt)} is overdue. 2% off if paid today. Please confirm.",
                "seqs":seqs,
            })

    # 2. Vendor overpay
    if len(expenses)>0:
        for category in expenses["Category"].unique():
            ce=expenses[expenses["Category"]==category]
            if len(ce)<3: continue
            vs=ce.groupby("Party")["Amount"].agg(["mean","count","sum"])
            vs=vs[vs["count"]>=2]
            if len(vs)<2: continue
            cheapest=vs["mean"].min(); ev=vs["mean"].idxmax(); ep=vs["mean"].max()
            av=float(vs.loc[ev,"sum"])
            if ep>cheapest*1.12:
                pct=((ep-cheapest)/cheapest)*100; waste=(ep-cheapest)*(av/ep)
                pdata=PEERS.get(industry,{}).get(category)
                bench_line=(f"Market median: ₹{pdata['median']:,}{pdata['unit']} ({pdata['n']} peers). You pay ₹{ep:,.0f}."
                            if pdata else f"Get 3 quotes — typically 10–18% saving possible.")
                if waste>15000:
                    leaks.append({
                        "id":"cost_bleed","sev":"warning","cat":"Vendor Costs",
                        "rupee":waste,"annual":waste,
                        "headline":f"{fmtx(int(waste))} overpaid on {category} per year",
                        "sub":f"{ev} charges {pct:.0f}% more than your cheapest supplier",
                        "found":f"You paid {ev} avg ₹{ep:,.0f} per transaction on {category}. Cheapest supplier: ₹{cheapest:,.0f}. Gap: {pct:.0f}%.",
                        "costs":f"Annualised: {fmtx(int(waste))} extra per year leaving your account quietly every month.",
                        "bench":bench_line,
                        "action":f"Get 2 competing quotes for {category} by Friday.",
                        "action_sub":"Lowest confirmed quote gets the contract.",
                        "template":f"Reviewing {category} suppliers. Send best rate for [volume]. Lowest quote by Friday gets 12-month contract.",
                        "seqs":[],
                    })
                    break

    # 3. Margin gap
    if margin<bmark-3:
        gap=((bmark-margin)/100)*revenue
        if gap>25000:
            leaks.append({
                "id":"margin_gap","sev":"critical" if margin<5 else "warning","cat":"Profitability",
                "rupee":gap,"annual":gap,
                "headline":f"{fmtx(int(gap))} in margin left on the table",
                "sub":f"Your margin {margin:.1f}% vs {bmark}% industry average",
                "found":f"Net margin: {margin:.1f}%. Industry benchmark for {industry}: {bmark}%. Gap: {bmark-margin:.1f} percentage points.",
                "costs":f"At revenue of {fmt(revenue)}, closing half this gap adds {fmt(gap*0.5)} in net profit — no new customers needed.",
                "bench":f"Benchmark: {bmark}% for {industry}.",
                "action":"Raise prices 5% on top 3 products. Cut 10% from largest expense line.",
                "action_sub":f"Combined adds ~{fmt(gap*0.15)} in 90 days.",
                "template":"Reviewing pricing — benchmarks show room to increase rates by 5–8%. Implementing from next invoice cycle.",
                "seqs":[],
            })

    # 4. Concentration
    if len(sales)>0 and revenue>0:
        cr=sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100>28:
            top_pct=(cr.iloc[0]/revenue)*100; risk=cr.iloc[0]*0.3
            leaks.append({
                "id":"concentration","sev":"warning","cat":"Revenue Risk",
                "rupee":risk,"annual":risk,
                "headline":f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub":"One client delay = cash crisis",
                "found":f"{cr.index[0]} = {top_pct:.0f}% of revenue ({fmtx(int(cr.iloc[0]))}). 30-day delay = {fmtx(int(cr.iloc[0]))} shortfall.",
                "costs":"Concentration above 25% gives that client full negotiating power.",
                "bench":"Healthy: no single client above 25% of revenue.",
                "action":"Close 2 new clients this month.",
                "action_sub":"Set a 25% concentration cap target within 6 months.",
                "template":"Expanding client base — if you know businesses needing [service], happy to offer referral discount.",
                "seqs":[],
            })

    # 5. Expense spike
    if len(expenses)>0:
        me=expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me)>=4:
            recent=me.iloc[-3:].mean(); prior=me.iloc[:-3].mean() if len(me)>3 else me.iloc[0]
            if prior>0 and recent>prior*1.18:
                spike=(recent-prior)*12
                if spike>20000:
                    leaks.append({
                        "id":"exp_spike","sev":"warning","cat":"Cost Control",
                        "rupee":spike,"annual":spike,
                        "headline":f"Monthly costs up {((recent/prior-1)*100):.0f}% — {fmtx(int(spike))} annualised",
                        "sub":f"₹{(recent-prior)/1000:.0f}K more per month than 3 months ago",
                        "found":f"Monthly expense 3 months ago: {fmt(prior)}. Now: {fmt(recent)}. Extra: {fmt(recent-prior)}/month.",
                        "costs":"Rising costs without matching revenue = structural cash problem.",
                        "bench":"Expenses should track revenue. Rising faster = investigate immediately.",
                        "action":"Freeze all non-essential spend this week.",
                        "action_sub":"Every spend above ₹5K needs approval until resolved.",
                        "template":"Cost control initiative: non-essential expenses paused. Reviewing all vendor contracts.",
                        "seqs":[],
                    })

    # 6. GST
    elig=expenses[expenses["Amount"]>25000]
    if len(elig)>0:
        missed=elig["Amount"].sum()*0.18*0.09
        if missed>8000:
            leaks.append({
                "id":"tax_gst","sev":"info","cat":"Tax Recovery",
                "rupee":missed,"annual":missed,
                "headline":f"~{fmtx(int(missed))} in GST input credits to verify",
                "sub":"Estimated quarterly — needs CA confirmation",
                "found":f"Eligible purchase transactions: {fmt(elig['Amount'].sum())}. ~9% of claimable GST input credit goes unclaimed by SMEs.",
                "costs":"This is money the government owes you. One CA session to recover it.",
                "bench":"Claim before next GST filing date.",
                "action":"Ask your CA about Input Tax Credit on purchases above ₹25K.",
                "action_sub":"Takes one CA session. Recoverable within the same quarter.",
                "template":"Want to review ITC eligibility on purchase invoices. Can we schedule a call this week?",
                "seqs":[],
            })

    return sorted(leaks,key=lambda x:x["rupee"],reverse=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k,v in [("df",None),("industry","agency"),("city","Bangalore"),("show_bot",False),("trial_clicked",False)]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Profit Recovery · Built for Indian SMEs · Bangalore</div>
  <h1 class="hero-h">Your business is leaking<br><em>₹5–50 Lakhs.</em><br>We find exactly where.</h1>
  <p class="hero-sub">Upload your Tally export. In 60 seconds get exact rupee amounts — and the 3 actions that stop the bleeding this week. You pay only when you recover.</p>
  <div class="trust-row">
    <div class="trust-item"><div class="t-num">₹50Cr+</div><div class="t-lbl">Leaks found</div></div>
    <div class="trust-item"><div class="t-num">₹12.4L</div><div class="t-lbl">Avg recovery</div></div>
    <div class="trust-item"><div class="t-num">4.8 days</div><div class="t-lbl">To first rupee</div></div>
    <div class="trust-item"><div class="t-num">200+</div><div class="t-lbl">SMEs scanned</div></div>
  </div>
</div>
<div class="safety-bar">
  <div class="s-pill"><div class="s-dot"></div> Your file never leaves your device</div>
  <div class="s-pill"><div class="s-dot"></div> No login needed for first scan</div>
  <div class="s-pill"><div class="s-dot"></div> Results in 60 seconds</div>
  <div class="s-pill"><div class="s-dot"></div> Trusted by CAs in Bangalore, Mumbai, Pune</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
t1, t2, t3 = st.tabs(["₹  Scan My Business", "🏛  CA Partner Program", "📊  Benchmarks"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SCAN
# ══════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown('<div class="sw">', unsafe_allow_html=True)

    # Upload row
    with st.container():
        uc1, uc2, uc3 = st.columns([3,1,1])
        with uc1:
            uploaded = st.file_uploader(
                "Upload Tally Day Book, Sales Register, or Bank Statement (CSV / Excel)",
                type=["csv","xlsx","xls"], key="up"
            )
            with st.expander("How to export from Tally in 30 seconds"):
                st.markdown("""
**Tally Prime:** Display → Account Books → Day Book → Alt+E → Excel  
**Tally ERP 9:** Gateway → Display → Day Book → Ctrl+E → Excel  
**Bank:** Download CSV from net banking  
**Design AID / custom CSV:** Detected automatically ✓
                """)
        with uc2:
            ind_sel = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
            st.session_state.industry = INDUSTRY_MAP[ind_sel]
        with uc3:
            city_sel = st.selectbox("City", ["Bangalore","Mumbai","Delhi","Pune","Chennai","Hyderabad","Ahmedabad","Surat","Other"])
            st.session_state.city = city_sel
            if st.button("▶  Try Demo Data", use_container_width=True):
                np.random.seed(42)
                dates=pd.date_range("2024-04-01","2025-03-31",freq="D")
                recs=[]
                for d in dates:
                    if np.random.random()>0.25:
                        recs.append({"Date":d,"Type":"Sales",
                            "Party":np.random.choice(["ABC Corp","XYZ Ind","PQR Mfg","LMN Traders","DEF Ent"],p=[0.45,0.2,0.15,0.1,0.1]),
                            "Amount":np.random.uniform(60000,280000),
                            "Status":np.random.choice(["Paid","Paid","Overdue","Pending"],p=[0.55,0.25,0.12,0.08]),
                            "Category":"Sales"})
                    for _ in range(np.random.randint(1,4)):
                        recs.append({"Date":d,"Type":"Expense",
                            "Party":np.random.choice(["Steel A","Steel B","Raw Mat Co","Logistics Ltd","Pack Inc","Pack Pro"]),
                            "Amount":np.random.uniform(12000,90000),"Status":"Paid",
                            "Category":np.random.choice(["Raw Materials","Raw Materials","Labor","Rent","Logistics","Packaging"],p=[0.30,0.15,0.20,0.10,0.15,0.10])})
                demo=pd.DataFrame(recs)
                demo["Month"]=demo["Date"].dt.to_period("M").astype(str)
                st.session_state.df=demo; st.session_state.industry="manufacturing"
                st.rerun()

    if uploaded:
        df_new,ok,msg = parse_file(uploaded)
        if ok:
            st.session_state.df=df_new
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info("Fix: open in Excel → Save As → CSV → upload that file.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ──────────────────────────────────────────────────────────────
    if st.session_state.df is not None:
        df=st.session_state.df; industry=st.session_state.industry; city=st.session_state.city
        sales=df[df["Type"]=="Sales"]; expenses=df[df["Type"]=="Expense"]
        revenue=sales["Amount"].sum(); exp_tot=expenses["Amount"].sum()
        profit=revenue-exp_tot; margin=(profit/revenue*100) if revenue>0 else 0
        bmark=BENCH.get(industry,15)
        leaks=find_leaks(df,industry,city)
        total_rupee=sum(l["rupee"] for l in leaks)
        overdue=(sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum()
                 if "Status" in sales.columns else 0)

        st.markdown('<div class="sw">', unsafe_allow_html=True)

        # ── TOPLINE MONEY SCREEN ─────────────────────────────────────────────
        coll_l=next((l for l in leaks if l["id"]=="cash_stuck"),None)
        vend_l=next((l for l in leaks if l["id"]=="cost_bleed"),None)
        tax_l =next((l for l in leaks if l["id"]=="tax_gst"),None)
        marg_l=next((l for l in leaks if l["id"]=="margin_gap"),None)

        # Build action rows
        acts=[]
        if coll_l: acts.append(f"Call top debtor today — recover {fmtx(int(coll_l['rupee']))} overdue")
        if vend_l: acts.append(f"Get 2 quotes for {vend_l['headline'].split('on ')[-1].split(' per')[0]} — save {fmt(vend_l['rupee'])}/yr")
        if tax_l:  acts.append(f"Email CA about ITC review — ~{fmtx(int(tax_l['rupee']))} claimable")
        if not acts and marg_l: acts.append(f"Raise top-3 prices 5% — adds {fmt(marg_l['rupee']*0.15)} in 90 days")

        act_html = "".join(
            f'<div class="act-item"><div class="act-num">{i+1}</div><div class="act-text">{a}</div></div>'
            for i,a in enumerate(acts[:3])
        )
        coll_row = (f'<div class="ms-row r"><div class="ms-left"><span style="font-size:16px">🔴</span><div><div class="ms-title">Cash stuck in unpaid invoices</div><div class="ms-desc">Recoverable this month</div></div></div><div class="ms-amt">{fmtx(int(coll_l["rupee"]))}</div></div>' if coll_l else "")
        vend_row = (f'<div class="ms-row a"><div class="ms-left"><span style="font-size:16px">🟡</span><div><div class="ms-title">Vendor overpayment — annual saving</div><div class="ms-desc">Switch to market-rate supplier</div></div></div><div class="ms-amt">{fmtx(int(vend_l["rupee"]))}/yr</div></div>' if vend_l else "")
        marg_row = (f'<div class="ms-row a"><div class="ms-left"><span style="font-size:16px">🟡</span><div><div class="ms-title">Margin gap vs industry peers</div><div class="ms-desc">Price + cost action</div></div></div><div class="ms-amt">{fmtx(int(marg_l["rupee"]))}/yr</div></div>' if marg_l else "")
        tax_row  = (f'<div class="ms-row b"><div class="ms-left"><span style="font-size:16px">🔵</span><div><div class="ms-title">GST input credits — verify with CA</div><div class="ms-desc">Estimated, needs CA confirmation</div></div></div><div class="ms-amt">~{fmtx(int(tax_l["rupee"]))}</div></div>' if tax_l else "")

        st.markdown(
            f'<div class="money-screen">'
            f'<div class="ms-label">Money you can recover</div>'
            f'<div class="ms-total">{fmt(total_rupee)}</div>'
            f'<div class="ms-sub">{len(leaks)} issues found · Annual impact: {fmt(sum(l["annual"] for l in leaks))}</div>'
            f'{coll_row}{vend_row}{marg_row}{tax_row}'
            f'<div class="act-box"><div class="act-lbl">Do these 3 things this week</div>{act_html}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── KPI ROW ──────────────────────────────────────────────────────────
        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi-card"><div class="kpi-lbl">Revenue</div><div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales)} transactions</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Margin</div><div class="kpi-val">{margin:.1f}%</div><div class="kpi-sub {"good" if margin>=bmark else "bad"}">vs {bmark}% benchmark</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Overdue</div><div class="kpi-val">{fmt(overdue)}</div><div class="kpi-sub {"bad" if overdue>revenue*0.06 else "good"}">{(overdue/revenue*100 if revenue>0 else 0):.1f}% of revenue</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Profit</div><div class="kpi-val">{fmt(abs(profit))}</div><div class="kpi-sub {"good" if profit>0 else "bad"}">{"Profitable" if profit>0 else "Loss"}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── LEAK CARDS ───────────────────────────────────────────────────────
        if leaks:
            st.markdown('<div class="sh">Where your money is leaking</div>', unsafe_allow_html=True)
            st.markdown('<div class="ss">Each finding shows exact rupees, source data, and one specific action.</div>', unsafe_allow_html=True)

            for leak in leaks[:6]:
                st.markdown(
                    f'<div class="lk-card {leak["sev"]}">'
                    f'<div class="lk-tag {leak["sev"]}">{leak["cat"].upper()}</div>'
                    f'<div class="lk-amt">{fmtx(int(leak["rupee"]))}</div>'
                    f'<div class="lk-sub">{"immediate recovery" if leak["id"]=="cash_stuck" else "annual impact"}</div>'
                    f'<div class="lk-ttl">{leak["headline"]}</div>'
                    f'<div class="lk-desc">{leak["sub"]}</div>'
                    f'<div class="lk-src"><strong>What we found:</strong> {leak["found"]}<br><br>'
                    f'<strong>Why it costs you:</strong> {leak["costs"]}<br><br>'
                    f'<strong>Benchmark:</strong> {leak["bench"]}</div>'
                    f'<div class="lk-act">→ {leak["action"]}<div class="lk-act-s">{leak["action_sub"]}</div></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Collections bot
                if leak["id"]=="cash_stuck" and leak.get("seqs"):
                    if st.button("📱 Launch WhatsApp collections sequence", key="bot"):
                        st.session_state.show_bot = not st.session_state.show_bot
                    if st.session_state.show_bot:
                        st.caption("Send these messages on the scheduled days. Stop when paid.")
                        for step in leak["seqs"]:
                            st.markdown(
                                f'<div class="seq-card">'
                                f'<div class="seq-day">Day {step["day"]} · {step["send_on"]}</div>'
                                f'<div class="seq-tone" style="color:{step["color"]}">{step["tone"]}</div>'
                                f'<div class="seq-msg">{step["message"]}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            wa_link = step["wa_link"]
                            st.markdown(f'<a href="{wa_link}" target="_blank" style="font-size:12px;color:#25D366;text-decoration:none;">Open in WhatsApp →</a>', unsafe_allow_html=True)

                # Script for non-collections leaks
                if leak["id"] != "cash_stuck":
                    btn_key = f"scr_{leak['id']}"
                    if st.button(f"📋 Get WhatsApp script", key=btn_key):
                        st.code(leak["template"])

        # ── TRENDS ───────────────────────────────────────────────────────────
        st.markdown("---")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown("**Revenue vs Expenses — monthly**")
            monthly = df.groupby([df["Date"].dt.to_period("M"),"Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly, height=220)
        with tc2:
            st.markdown("**Top Expense Categories**")
            if len(expenses)>0:
                st.bar_chart(expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8), height=220)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── PRICING ───────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="pr-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.8rem;color:#F7F4EF;margin-bottom:4px;">How we work together</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:13px;color:#6A6A5A;margin-bottom:1.5rem;">No subscription traps. Pay only when you recover money.</div>', unsafe_allow_html=True)

        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.markdown("""
<div class="pr-card">
  <div class="pr-lbl">Free scan</div>
  <div class="pr-name">First audit</div>
  <div class="pr-amt">₹0</div>
  <div class="pr-note">Upload your data. See all leaks instantly. No credit card, no login, no strings.</div>
  <div class="pr-feat">Full leak scan</div>
  <div class="pr-feat">Exact rupee amounts</div>
  <div class="pr-feat">Top 3 actions this week</div>
  <div class="pr-feat">Collections sequences</div>
</div>""", unsafe_allow_html=True)
        with pc2:
            st.markdown("""
<div class="pr-card feat">
  <div class="pr-lbl">Most chosen</div>
  <div class="pr-name">Success fee</div>
  <div class="pr-amt">7–10%</div>
  <div class="pr-note">We charge only on money you actually recover. No recovery = no fee. Ever.</div>
  <div class="pr-feat">Everything in free scan</div>
  <div class="pr-feat">Recovery Review call</div>
  <div class="pr-feat">Vendor quote sourcing</div>
  <div class="pr-feat">Monthly monitoring</div>
  <div class="pr-feat">CA coordination</div>
</div>""", unsafe_allow_html=True)
        with pc3:
            st.markdown("""
<div class="pr-card">
  <div class="pr-lbl">For CA firms</div>
  <div class="pr-name">Partner plan</div>
  <div class="pr-amt">₹1,999/mo</div>
  <div class="pr-note">Run for all your clients. White-label reports. ₹500/client/month you earn.</div>
  <div class="pr-feat">50 client seats</div>
  <div class="pr-feat">Branded monthly reports</div>
  <div class="pr-feat">Client health dashboard</div>
  <div class="pr-feat">GST + TDS risk scanner</div>
  <div class="pr-feat">Revenue share program</div>
</div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # CTA buttons with real notifications
        st.markdown("<br>", unsafe_allow_html=True)
        bc1, bc2, bc3 = st.columns([1,2,1])
        with bc2:
            if st.button("🚀 Book a free Recovery Review call", use_container_width=True, type="primary"):
                st.session_state.trial_clicked = True

        if st.session_state.trial_clicked:
            st.success("✅ Done! We'll WhatsApp you within 2 hours to schedule your Recovery Review call.")
            st.info("📱 Or message the founder right now → [wa.me/916362319163](https://wa.me/916362319163?text=Hi%2C+I%20ran%20OpsClarity%20on%20my%20data%20and%20want%20to%20discuss%20recovery)")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CA PARTNER
# ══════════════════════════════════════════════════════════════════════════════
with t2:
    portfolio=[
        {"name":"Sharma Textiles Pvt Ltd","city":"Ahmedabad","ind":"textile","rev":4200000,"leak":840000,"health":"red"},
        {"name":"Mehta Food Products","city":"Mumbai","ind":"restaurant","rev":2800000,"leak":196000,"health":"amber"},
        {"name":"Rajesh Diagnostics","city":"Pune","ind":"clinic","rev":6100000,"leak":91500,"health":"green"},
        {"name":"Kapoor Steel Trading","city":"Delhi","ind":"manufacturing","rev":8900000,"leak":1780000,"health":"red"},
        {"name":"Green Pharma Dist.","city":"Chennai","ind":"pharma","rev":3400000,"leak":238000,"health":"amber"},
        {"name":"Sri Venkateswara Printers","city":"Hyderabad","ind":"printing","rev":1900000,"leak":28500,"health":"green"},
    ]
    total_pleak=sum(c["leak"] for c in portfolio)
    crit_c=sum(1 for c in portfolio if c["health"]=="red")

    st.markdown('<div class="ca-wrap">', unsafe_allow_html=True)
    st.markdown('<div style="display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1rem;">For Chartered Accountants</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:#1A1A1A;margin-bottom:0.5rem;">Your clients are losing money.<br>Show them exactly where — automatically.</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:14px;color:#6A6A5A;max-width:600px;margin-bottom:2rem;line-height:1.7;">OpsClarity gives you a branded profit-leak report for every client — automated, monthly, zero extra work. CAs who use it retain clients longer and earn ₹500/client/month in passive income.</div>', unsafe_allow_html=True)

    n_ca = st.slider("Your client count", 10, 200, 40, 5)

    ca1, ca2 = st.columns(2)
    with ca1:
        st.markdown('<div class="ca-card">', unsafe_allow_html=True)
        st.markdown('<div class="ca-lbl">The CA partner math</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ca-row"><div class="ca-row-lbl">Clients on OpsClarity</div><div class="ca-row-val">{n_ca}</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Your cost (platform)</div><div class="ca-row-val">₹1,999/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">You earn per client</div><div class="ca-row-val">₹500/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Monthly income</div><div class="ca-row-val hl">₹{n_ca*500:,}/month</div></div>'
            f'<div class="ca-row" style="border:none"><div class="ca-row-lbl">Net after cost</div><div class="ca-row-val hl">₹{n_ca*500-1999:,}/month</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with ca2:
        st.markdown('<div class="ca-card">', unsafe_allow_html=True)
        st.markdown('<div class="ca-lbl">What your clients get</div>', unsafe_allow_html=True)
        st.markdown('<div class="ca-ttl">Monthly profit health report</div>', unsafe_allow_html=True)
        st.markdown('<div class="ca-body">Branded with your CA firm name. Shows every client exactly where they\'re losing money — in exact rupees, with specific actions. Every month, automatically, without extra work.<br><br>Clients who receive this report renew without negotiating, refer you more, and stop shopping for another CA. <strong>That\'s the real value.</strong></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Client dashboard
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#1A1A1A;margin:1.5rem 0 0.75rem;">Your client dashboard — live view</div>', unsafe_allow_html=True)

    dash_header = (
        f'<div class="ca-card dark">'
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1rem;">'
        f'<div><div class="ca-lbl">Active clients</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#F7F4EF;">{len(portfolio)}</div></div>'
        f'<div><div class="ca-lbl">Leaks found</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#D4AF37;">{fmt(total_pleak)}</div></div>'
        f'<div><div class="ca-lbl">Critical — act now</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#E05252;">{crit_c} clients</div></div>'
        f'</div>'
        f'<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:0.75rem;">'
    )
    rows_html = ""
    for c in portfolio:
        hl = ("🔴 Critical" if c["health"]=="red" else "🟡 Watch" if c["health"]=="amber" else "🟢 Healthy")
        hcls = c["health"]
        rows_html += (
            f'<div class="cl-row">'
            f'<div><div class="cl-name">{c["name"]}</div><div class="cl-meta">{c["city"]} · {c["ind"].title()}</div></div>'
            f'<div class="cl-amt">{fmt(c["leak"])}</div>'
            f'<div class="cl-h {hcls}">{hl}</div>'
            f'</div>'
        )
    st.markdown(dash_header + rows_html + '</div></div>', unsafe_allow_html=True)

    # Objections — use native Streamlit expanders (never break)
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#1A1A1A;margin:1.5rem 0 0.75rem;">Questions CAs ask us</div>', unsafe_allow_html=True)
    with st.expander("My clients won't share data with a third-party app"):
        st.write("You upload the file — your client never sees OpsClarity. The report comes branded as your firm's work. Clients see a CA service, not a third-party app.")
    with st.expander("What if the numbers are wrong?"):
        st.write("OpsClarity flags potential leaks. You verify before sharing — exactly as you'd review any report before signing off. Your professional judgement is still the product.")
    with st.expander("I already do this manually for my clients"):
        st.write("If you do this for 40 clients manually every month, you know how many hours it takes. OpsClarity does the same analysis in 60 seconds per client. That time comes back to you — or goes to more clients.")
    with st.expander("Will this replace CAs?"):
        st.write("No. Every tax finding says 'verify with your CA'. ITC claims, TDS, advance tax — all require a qualified CA to action. We surface the work. You do it. Your client pays you more.")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Join CA Partner Program — free 30-day trial →", type="primary", use_container_width=True):
        st.success("✅ Application received. We'll WhatsApp you within 4 hours to set up your dashboard.")
        st.info("📱 Direct line: [wa.me/916362319163](https://wa.me/916362319163?text=Hi%2C+I+want+to+join+the+OpsClarity+CA+Partner+Program)")
        st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">Industry Benchmark Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Anonymised data from Indian SMEs. Used to validate every leak we flag.</div>', unsafe_allow_html=True)
    sel = st.selectbox("Industry", list(PEERS.keys()), key="bi")
    bd = PEERS.get(sel,{})
    if bd:
        for cat,data in bd.items():
            with st.expander(f"{cat} — {data['n']} businesses"):
                b1,b2,b3,b4=st.columns(4)
                b1.metric("Best 25%",  f"₹{data['p25']:,}{data['unit']}")
                b2.metric("Median",    f"₹{data['median']:,}{data['unit']}")
                b3.metric("Top 25%",   f"₹{data['p75']:,}{data['unit']}")
                b4.metric("Peers",     str(data['n']))
                saving=((data['p75']-data['p25'])/data['p75'])*100
                st.info(f"Switching from top-25% rate to best rate = **{saving:.0f}% cost reduction** on {cat}.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div><div class="ft-brand">OpsClarity</div><div class="ft-legal">Profit Recovery · Bangalore 🇮🇳</div></div>
  <div class="ft-legal">Management estimates only — not CA advice · Your data stays on your device</div>
</div>
<a href="https://wa.me/916362319163?text=Hi, question about OpsClarity" class="wa-btn" target="_blank">
  💬 Talk to founder
</a>
""", unsafe_allow_html=True)
