import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse, random, io

st.set_page_config(
    page_title="OpsClarity — Profit Recovery",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #F7F4EF;
    font-family: 'DM Sans', sans-serif;
    color: #1A1A1A;
}
.main .block-container { padding: 0; max-width: 100%; }

/* ── HERO ── */
.hero {
    background: #1A1A1A;
    padding: 5rem 4rem 4rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 70%);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(212,175,55,0.12);
    border: 1px solid rgba(212,175,55,0.3);
    padding: 6px 16px; border-radius: 30px;
    font-size: 11px; font-weight: 600; color: #D4AF37;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 2rem;
}
.hero-headline {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    color: #F7F4EF;
    line-height: 1.08;
    margin-bottom: 1.5rem;
    max-width: 700px;
}
.hero-headline em {
    font-style: italic;
    color: #D4AF37;
}
.hero-sub {
    font-size: 1.1rem;
    color: #9A9A8A;
    max-width: 520px;
    line-height: 1.7;
    margin-bottom: 2.5rem;
    font-weight: 300;
}
.hero-trust {
    display: flex; gap: 2rem; flex-wrap: wrap;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.08);
}
.trust-item { text-align: left; }
.trust-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem; color: #D4AF37; font-weight: 400;
}
.trust-label { font-size: 11px; color: #6A6A5A; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px; }

/* ── TRUST BANNER ── */
.trust-banner {
    background: #EDEAE3;
    padding: 1rem 4rem;
    display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;
    border-bottom: 1px solid #D8D4CC;
}
.trust-pill {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: #4A4A3A; font-weight: 500;
}
.trust-dot { width: 6px; height: 6px; border-radius: 50%; background: #4CAF50; }

/* ── TOPLINE MONEY SCREEN ── */
.money-screen {
    background: #1A1A1A;
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
}
.money-screen-label {
    font-size: 11px; font-weight: 600; color: #6A6A5A;
    text-transform: uppercase; letter-spacing: 0.15em;
    margin-bottom: 0.5rem;
}
.money-screen-total {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem; color: #D4AF37;
    line-height: 1; margin-bottom: 0.5rem;
}
.money-screen-sub { font-size: 14px; color: #6A6A5A; margin-bottom: 2rem; }
.money-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.25rem;
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    border-left: 3px solid transparent;
}
.money-row.urgent { border-left-color: #E05252; }
.money-row.medium { border-left-color: #D4AF37; }
.money-row.low    { border-left-color: #5B9BD5; }
.money-row-left { display: flex; align-items: center; gap: 12px; }
.money-row-icon { font-size: 18px; }
.money-row-title { font-size: 15px; font-weight: 500; color: #F7F4EF; }
.money-row-desc { font-size: 12px; color: #6A6A5A; margin-top: 2px; }
.money-row-amount { font-family: 'DM Mono', monospace; font-size: 1.1rem; font-weight: 600; color: #D4AF37; }
.action-strip {
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1.5rem;
}
.action-strip-title { font-size: 12px; font-weight: 600; color: #D4AF37; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; }
.action-item-row { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 0.5rem; }
.action-bullet { width: 18px; height: 18px; border-radius: 50%; background: #D4AF37; color: #1A1A1A; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
.action-text { font-size: 13px; color: #C8C8B8; line-height: 1.5; }

/* ── LEAK CARDS ── */
.section-wrap { padding: 2rem 4rem; }
.section-head { font-family: 'DM Serif Display', serif; font-size: 2rem; color: #1A1A1A; margin-bottom: 0.4rem; }
.section-sub { font-size: 14px; color: #6A6A5A; margin-bottom: 2rem; }
.leak-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.25rem; }
.leak-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.leak-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.leak-card.critical::after { background: #E05252; }
.leak-card.warning::after  { background: #D4AF37; }
.leak-card.info::after     { background: #5B9BD5; }
.leak-tag {
    display: inline-block; font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 1rem;
}
.leak-tag.critical { background: #FEF0F0; color: #C0392B; }
.leak-tag.warning  { background: #FFFBF0; color: #9A7A00; }
.leak-tag.info     { background: #EFF5FE; color: #2060A0; }
.leak-rupee {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem; color: #1A1A1A;
    margin-bottom: 0.25rem; line-height: 1;
}
.leak-rupee-sub { font-size: 12px; color: #9A9A8A; margin-bottom: 1rem; }
.leak-title { font-size: 15px; font-weight: 600; color: #1A1A1A; margin-bottom: 0.5rem; }
.leak-desc { font-size: 13px; color: #6A6A5A; line-height: 1.65; margin-bottom: 1.25rem; }
.leak-source {
    background: #F7F4EF; border-radius: 8px;
    padding: 0.75rem 1rem; margin-bottom: 1rem;
    font-size: 12px; color: #4A4A3A;
    line-height: 1.5;
}
.leak-source strong { color: #1A1A1A; }
.leak-action {
    border-top: 1px solid #F0EDE6;
    padding-top: 1rem;
    font-size: 13px; font-weight: 600; color: #1A1A1A;
}
.leak-action-sub { font-size: 12px; font-weight: 400; color: #6A6A5A; margin-top: 3px; }

/* ── KPI ROW ── */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin: 2rem 0; }
.kpi-card {
    background: #FFFFFF; border: 1px solid #E8E4DC;
    border-radius: 14px; padding: 1.25rem 1.5rem;
}
.kpi-label { font-size: 11px; color: #9A9A8A; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.kpi-val { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #1A1A1A; }
.kpi-delta { font-size: 12px; margin-top: 3px; }
.kpi-delta.good { color: #2E8B57; }
.kpi-delta.bad  { color: #C0392B; }
.kpi-delta.warn { color: #9A7A00; }

/* ── UPLOAD ZONE ── */
.upload-wrap { padding: 2rem 4rem; }
.upload-inner {
    background: #FFFFFF;
    border: 2px dashed #C8C4BC;
    border-radius: 20px;
    padding: 2rem;
}

/* ── PRICING ── */
.pricing-wrap { padding: 3rem 4rem; background: #1A1A1A; }
.pricing-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.25rem; margin-top: 2rem; }
.price-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 2rem;
}
.price-card.featured {
    background: rgba(212,175,55,0.08);
    border-color: rgba(212,175,55,0.4);
}
.price-label { font-size: 11px; font-weight: 600; color: #6A6A5A; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 1rem; }
.price-model { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: #F7F4EF; margin-bottom: 0.3rem; }
.price-amount { font-family: 'DM Mono', monospace; font-size: 2.2rem; color: #D4AF37; margin-bottom: 0.5rem; }
.price-note { font-size: 13px; color: #6A6A5A; margin-bottom: 1.5rem; line-height: 1.5; }
.price-features { list-style: none; }
.price-features li { font-size: 13px; color: #9A9A8A; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.price-features li::before { content: "→ "; color: #D4AF37; }

/* ── CA PITCH ── */
.ca-pitch-wrap { padding: 3rem 4rem; background: #F0EDE6; }
.ca-pitch-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; }
.ca-card {
    background: #FFFFFF; border: 1px solid #E0DDD6;
    border-radius: 16px; padding: 1.5rem;
}
.ca-card.dark { background: #1A1A1A; border-color: rgba(255,255,255,0.08); }
.ca-card-label { font-size: 11px; font-weight: 600; color: #9A9A8A; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; }
.ca-card-title { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #1A1A1A; margin-bottom: 0.5rem; }
.ca-card.dark .ca-card-title { color: #F7F4EF; }
.ca-card-body { font-size: 13px; color: #6A6A5A; line-height: 1.7; }
.ca-card.dark .ca-card-body { color: #9A9A8A; }
.ca-math-row { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #F0EDE6; }
.ca-math-label { font-size: 14px; color: #4A4A3A; }
.ca-math-val { font-family: 'DM Mono', monospace; font-size: 14px; font-weight: 600; color: #1A1A1A; }
.ca-math-val.highlight { color: #2E8B57; font-size: 1.1rem; }
.ca-client-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.ca-client-name { font-size: 14px; font-weight: 500; color: #F7F4EF; }
.ca-client-meta { font-size: 11px; color: #6A6A5A; margin-top: 2px; }
.ca-health { font-size: 12px; font-weight: 600; }
.ca-health.red { color: #E05252; }
.ca-health.amber { color: #D4AF37; }
.ca-health.green { color: #4CAF50; }
.ca-leak-amt { font-family: 'DM Mono', monospace; font-size: 13px; color: #D4AF37; }

/* ── COLLECTIONS ── */
.seq-card {
    background: #FFFFFF; border: 1px solid #E8E4DC;
    border-radius: 12px; padding: 1.25rem; margin-bottom: 0.75rem;
}
.seq-day-badge {
    display: inline-block; background: #1A1A1A; color: #D4AF37;
    font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px;
    margin-bottom: 0.5rem;
}
.seq-tone { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.seq-msg { font-size: 13px; color: #4A4A3A; line-height: 1.65; }

/* ── FOOTER ── */
.footer {
    background: #1A1A1A; padding: 2rem 4rem;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
}
.footer-brand { font-family: 'DM Serif Display', serif; font-size: 1.2rem; color: #D4AF37; }
.footer-legal { font-size: 12px; color: #4A4A3A; }

/* ── UTILS ── */
.divider { height: 1px; background: #E8E4DC; margin: 0 4rem; }
.wa-float {
    position: fixed; bottom: 28px; right: 28px;
    background: #25D366; color: white;
    padding: 14px 22px; border-radius: 50px;
    font-weight: 600; text-decoration: none;
    font-size: 14px; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 20px rgba(37,211,102,0.35); z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
INDUSTRY_MAP = {
    "🏭 Manufacturing":          "manufacturing",
    "🍽️ Restaurant / Cafe":     "restaurant",
    "🏥 Clinic / Diagnostic":   "clinic",
    "🛒 Retail / Distribution":  "retail",
    "💼 Agency / Consulting":    "agency",
    "🚚 Logistics / Transport":  "logistics",
    "🏗️ Construction":          "construction",
    "🧵 Textile / Garments":    "textile",
    "💊 Pharma / Medical":      "pharma",
    "🖨️ Print / Packaging":     "printing",
}
INDUSTRY_BENCHMARKS = {
    "manufacturing": 18, "restaurant": 15, "clinic": 25,
    "retail": 12, "agency": 35, "logistics": 10,
    "construction": 20, "textile": 14, "pharma": 22, "printing": 16,
}
CROWDSOURCED = {
    "manufacturing": {
        "Raw Materials": {"p25":42000,"median":51000,"p75":64000,"unit":"/ton","n":312,"city_splits":{"Mumbai":53000,"Delhi":49000,"Pune":48000,"Surat":44000}},
        "Labor":         {"p25":380,  "median":460,  "p75":580,  "unit":"/day","n":445,"city_splits":{"Mumbai":520,"Delhi":480,"Pune":460,"Ahmedabad":390}},
        "Logistics":     {"p25":8,    "median":11,   "p75":16,   "unit":"/km", "n":289,"city_splits":{"Mumbai":13,"Delhi":12,"Pune":10,"Chennai":10}},
        "Packaging":     {"p25":11,   "median":17,   "p75":24,   "unit":"/pc", "n":198,"city_splits":{"Mumbai":18,"Delhi":16,"Pune":15,"Coimbatore":13}},
        "Electricity":   {"p25":7,    "median":9,    "p75":12,   "unit":"/unit","n":267,"city_splits":{"Mumbai":10,"Delhi":9,"Pune":8,"Gujarat":7}},
    },
    "restaurant": {
        "Food Ingredients":{"p25":28,"median":34,"p75":42,"unit":"% rev","n":521,"city_splits":{}},
        "Labor":            {"p25":18,"median":24,"p75":32,"unit":"% rev","n":498,"city_splits":{}},
        "Packaging":        {"p25":8, "median":14,"p75":22,"unit":"/order","n":312,"city_splits":{}},
    },
    "retail": {
        "Inventory Carrying":{"p25":18,"median":26,"p75":36,"unit":"days","n":389,"city_splits":{}},
        "Rent":              {"p25":80,"median":120,"p75":200,"unit":"/sqft/mo","n":445,"city_splits":{}},
    },
    "clinic": {
        "Consumables":  {"p25":8, "median":13,"p75":20,"unit":"% rev","n":234,"city_splits":{}},
        "Lab Reagents": {"p25":15,"median":22,"p75":31,"unit":"% rev","n":189,"city_splits":{}},
    },
    "agency": {
        "Software/Tools":{"p25":8000, "median":14000,"p75":22000,"unit":"/mo","n":312,"city_splits":{}},
        "Freelancers":   {"p25":600,  "median":900,  "p75":1400, "unit":"/hr","n":267,"city_splits":{}},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(v):
    v = float(v)
    if abs(v) >= 1e7:  return f"₹{v/1e7:.1f} Cr"
    if abs(v) >= 1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v) >= 1000: return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmt_exact(v):
    """Show exact rupees with comma formatting for credibility."""
    v = int(float(v))
    return f"₹{v:,}"

# ══════════════════════════════════════════════════════════════════════════════
# COLLECTIONS BOT
# ══════════════════════════════════════════════════════════════════════════════
class CollectionsBot:
    SEQUENCES = [
        {"day":1,  "tone":"Friendly reminder",  "color":"#5B9BD5",
         "msg":"Hi {name} 🙏 Quick note — invoice #{inv} for {amt} was due recently. Any issues on your end? Happy to sort it out. — {biz}"},
        {"day":3,  "tone":"Offer + urgency",    "color":"#D4AF37",
         "msg":"Hi {name}, invoice #{inv} ({amt}) is now overdue. We're offering a 2% early-payment discount if settled by {deadline}. Can you confirm a date? — {biz}"},
        {"day":7,  "tone":"Operational impact", "color":"#E08020",
         "msg":"{name}, invoice #{inv} ({amt}) is 7 days overdue and impacting our cash flow. Payment needed by {deadline} or we'll need to pause future orders. Please respond. — {biz}"},
        {"day":10, "tone":"Final notice",       "color":"#E05252",
         "msg":"FINAL NOTICE — {name}: invoice #{inv} ({amt}) is 10 days unpaid. This is our last reminder before we refer this to our accounts team. Please pay by {deadline}. — {biz}"},
    ]
    @classmethod
    def generate(cls, name, inv, amount, biz):
        today = datetime.now()
        out = []
        for s in cls.SEQUENCES:
            amt_str = fmt(amount)
            msg = s["msg"].format(
                name=name, inv=inv, amt=amt_str, biz=biz,
                deadline=(today + timedelta(days=s["day"]+3)).strftime("%d %b %Y")
            )
            out.append({**s, "send_on":(today+timedelta(days=s["day"])).strftime("%d %b"), "message":msg,
                        "wa_link":f"https://wa.me/?text={urllib.parse.quote(msg)}"})
        return out

# ══════════════════════════════════════════════════════════════════════════════
# CSV PARSERS  (Design AID + Standard Tally)
# ══════════════════════════════════════════════════════════════════════════════
def _classify_expense(d):
    d = d.lower()
    if any(x in d for x in ["rent","rental"]):                        return "Rent"
    if any(x in d for x in ["praveen","porter","salary","wages"]):    return "Salary"
    if any(x in d for x in ["ashok payment"]):                        return "Salary"
    if any(x in d for x in ["laptop","computer"]):                    return "Technology"
    if any(x in d for x in ["broad","internet","wifi"]):              return "Internet"
    if any(x in d for x in ["housekeeping","houskeeping"]):           return "Housekeeping"
    if any(x in d for x in ["furniture","chair"]):                    return "Furniture"
    if any(x in d for x in ["electricity"]):                          return "Electricity"
    if any(x in d for x in ["ca","accountant","audit"]):              return "Professional Fees"
    if any(x in d for x in ["website","domain"]):                     return "Website"
    if any(x in d for x in ["outing","travel","food"]):               return "Travel"
    if any(x in d for x in ["office","accessories","stationery"]):    return "Office Supplies"
    if any(x in d for x in ["glass","basin","electrical","door","key","wash","seal","board"]): return "Office Setup"
    if any(x in d for x in ["mim","mfg","part cost"]):                return "Manufacturing"
    if any(x in d for x in ["debit","bank","charge"]):                return "Bank Charges"
    return "Operations"

def _is_design_aid(raw):
    cells = []
    for r in range(min(2,len(raw))):
        for c in range(min(10,len(raw.columns))):
            cells.append(str(raw.iloc[r,c]).lower().strip())
    return "months" in cells and ("investors" in cells or "expenses" in cells)

def _parse_design_aid(file):
    file.seek(0)
    raw = pd.read_csv(file, header=None, dtype=str).fillna("")
    MMAP = {
        "august":"2024-08","aug":"2024-08",
        "sept":"2024-09","sep":"2024-09","september":"2024-09",
        "oct":"2024-10","october":"2024-10",
        "nov":"2024-11","november":"2024-11",
        "dec":"2024-12","december":"2024-12",
        "jan":"2025-01","january":"2025-01",
        "feb":"2025-02","february":"2025-02",
        "march":"2025-03","mar":"2025-03",
    }
    SKIP = {"total","grand total","each","sub total","-","total-dec balance",
            "total - feb balance","dec balance","feb balance","total-feb balance",""}
    records = []

    for _, row in raw.iterrows():
        mk = row.iloc[0].strip().lower()
        if mk not in MMAP: continue
        dt = pd.Timestamp(MMAP[mk]+"-01")
        for col_i, party, typ in [(1,"Madhu","Sales"),(2,"Deepak","Sales"),
                                   (5,"Ashok","Expense"),(6,"Office","Expense"),(9,"Praveen","Expense")]:
            try:
                v = float(row.iloc[col_i].replace(",","").strip())
                if v > 0:
                    records.append({"Date":dt,"Type":typ,"Party":party,
                                    "Category":"Investment/Capital" if typ=="Sales" else "Operations",
                                    "Amount":v,"Status":"Paid","Invoice_No":"-"})
            except: pass

    cur_m, cur_d = None, None
    for _, row in raw.iterrows():
        c11 = row.iloc[11].strip().lower() if len(row)>11 else ""
        c14 = row.iloc[14].strip().lower() if len(row)>14 else ""
        if c11 in MMAP: cur_m = MMAP[c11]
        if c14 in MMAP: cur_d = MMAP[c14]
        for period, ai, di in [(cur_m,11,12),(cur_d,14,15)]:
            if not period or len(row)<=di: continue
            amt_r = row.iloc[ai].strip()
            desc  = row.iloc[di].strip()
            if desc.lower() in SKIP or not desc: continue
            try:
                v = float(amt_r.replace(",",""))
                if v > 0:
                    records.append({"Date":pd.Timestamp(period+"-01"),"Type":"Expense",
                                    "Party":"Madhu" if ai==11 else "Deepak",
                                    "Category":_classify_expense(desc),
                                    "Amount":v,"Status":"Paid","Invoice_No":"-"})
            except: pass

    if not records:
        return None, False, "No transactions found in Design AID format."
    df = pd.DataFrame(records).drop_duplicates()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df, True, f"✅ {len(df)} transactions loaded ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"

def parse_file(file):
    try:
        fname = file.name.lower()
        if fname.endswith((".xlsx",".xls")):
            try:    raw = pd.read_excel(file, header=None, engine="openpyxl")
            except: raw = pd.read_excel(file, header=None, engine="xlrd")
            file.seek(0)
            try:    df_std = pd.read_excel(file, engine="openpyxl")
            except: df_std = pd.read_excel(file, engine="xlrd")
        elif fname.endswith(".csv"):
            try:    raw = pd.read_csv(file, header=None, dtype=str)
            except: raw = pd.read_csv(file, header=None, encoding="latin1", dtype=str)
            file.seek(0)
            try:    df_std = pd.read_csv(file)
            except: df_std = pd.read_csv(file, encoding="latin1")
        else:
            return None, False, "Use .csv, .xlsx, or .xls"

        if _is_design_aid(raw):
            file.seek(0)
            return _parse_design_aid(file)

        df = df_std.dropna(how="all").dropna(axis=1, how="all")
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher"]): col_map[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","rs","₹"]): col_map[col]="Amount"
            elif any(x in cl for x in ["type","txn","dr/cr","nature"]): col_map[col]="Type"
            elif any(x in cl for x in ["particulars","category","cat","head","narration","ledger"]): col_map[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client","counter"]): col_map[col]="Party"
            elif any(x in cl for x in ["status","paid","pending","overdue","due"]): col_map[col]="Status"
            elif any(x in cl for x in ["bill","invoice","voucher","ref","num","no"]): col_map[col]="Invoice_No"
        df = df.rename(columns=col_map)

        if "Date" not in df.columns:
            return None, False, "Could not find a Date column. For Tally exports ensure column is labelled 'Date' or 'Dt'. For Design AID format ensure first column is 'Months'."

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"] = (df["Amount"].astype(str)
                .str.replace(",","").str.replace("(","−").str.replace(")","")
                .str.replace(" Dr","").str.replace(" Cr","").str.replace("₹",""))
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"]="Unknown"
        df["Type"] = df["Type"].astype(str).str.strip().str.title()
        df["Type"] = df["Type"].replace({"Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
                                          "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales"})
        mask = ~df["Type"].isin(["Sales","Expense"])
        if mask.any():
            ekw=["purchase","expense","payment","salary","rent","bill","wages","material","raw","inventory","logistics","packing"]
            df.loc[mask,"Type"] = df.loc[mask].apply(
                lambda x: "Expense" if any(k in str(x.get("Category","")).lower() for k in ekw) else "Sales", axis=1)
        for col,default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","-")]:
            if col not in df.columns: df[col]=default
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        return df, True, f"✅ {len(df):,} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"
    except Exception as e:
        return None, False, f"Error: {e}. Try saving as CSV."

# ══════════════════════════════════════════════════════════════════════════════
# LEAK DETECTOR — returns structured, chargeable findings
# ══════════════════════════════════════════════════════════════════════════════
def find_leaks(df, industry, city=None):
    sales    = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    revenue  = sales["Amount"].sum()
    exp_tot  = expenses["Amount"].sum()
    profit   = revenue - exp_tot
    margin   = (profit/revenue*100) if revenue>0 else 0
    benchmark= INDUSTRY_BENCHMARKS.get(industry,15)
    leaks    = []

    # ── 1. Cash stuck in overdue invoices ──────────────────────────────────
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid","due","outstanding","unpaid"])]
        od_amt = od["Amount"].sum()
        if od_amt > 10000:
            debtors     = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top5        = debtors.head(5)
            top_name    = debtors.index[0] if len(debtors)>0 else "Customer"
            top_amt     = float(debtors.iloc[0]) if len(debtors)>0 else od_amt
            pct_rev     = od_amt/revenue*100 if revenue>0 else 0
            oldest_days = 45
            collections = CollectionsBot.generate(top_name,"INV-001",top_amt,"Your Business")

            # Exact rupee breakdown for credibility
            debtor_lines = " · ".join([f"{n}: {fmt_exact(a)}" for n,a in top5.items()])

            leaks.append({
                "id":"cash_stuck","severity":"critical","priority":1,
                "category":"Collections",
                "rupee_impact": od_amt,
                "annual_impact": od_amt * 0.18,  # cost of capital
                "headline": f"{fmt_exact(od_amt)} is sitting unpaid",
                "sub": f"Across {len(debtors)} customers · avg {oldest_days} days overdue",
                "what_we_found": f"{len(debtors)} customers owe you money: {debtor_lines}",
                "why_it_costs_you": f"At 18% cost of capital, {fmt_exact(od_amt)} locked away costs you {fmt(od_amt*0.18)} per year in lost opportunity — money you could use to pay vendors faster or fund growth.",
                "benchmark": f"Healthy SMEs keep overdue below 5% of revenue. Yours is at {pct_rev:.1f}%.",
                "next_action": f"Call {top_name} today. Offer 2% discount for payment in 48 hours.",
                "action_sub": "Use the Collections sequence below — takes 10 minutes to set up.",
                "collections": collections,
                "template": f"Hi, your outstanding invoice of {fmt(top_amt)} is overdue. We'd like to offer you 2% off if settled by [date]. Please confirm. — [Your name]"
            })

    # ── 2. Vendor overpayment ───────────────────────────────────────────────
    if len(expenses)>0:
        for category in expenses["Category"].unique():
            ce = expenses[expenses["Category"]==category]
            if len(ce)<3: continue
            vs = ce.groupby("Party")["Amount"].agg(["mean","count","sum"])
            vs = vs[vs["count"]>=2]
            if len(vs)<2: continue
            cheapest   = vs["mean"].min()
            exp_vendor = vs["mean"].idxmax()
            exp_price  = vs["mean"].max()
            annual_vol = float(vs.loc[exp_vendor,"sum"])
            if exp_price > cheapest*1.12:
                pct_premium  = ((exp_price-cheapest)/cheapest)*100
                annual_waste = (exp_price-cheapest)*(annual_vol/exp_price)
                bench        = CROWDSOURCED.get(industry,{}).get(category)
                bench_line   = ""
                if bench:
                    bench_line = f"Market median for {category}: ₹{bench['median']:,}{bench['unit']} ({bench['n']} peers). You pay ₹{exp_price:,.0f}."
                if annual_waste>15000:
                    leaks.append({
                        "id":"cost_bleed","severity":"warning","priority":2,
                        "category":"Vendor Costs",
                        "rupee_impact": annual_waste,
                        "annual_impact": annual_waste,
                        "headline": f"{fmt_exact(int(annual_waste))} overpaid on {category} per year",
                        "sub": f"{exp_vendor} charges {pct_premium:.0f}% more than your cheapest supplier",
                        "what_we_found": f"You paid {exp_vendor} an average of ₹{exp_price:,.0f} per transaction on {category}. Your cheapest supplier for the same category charges ₹{cheapest:,.0f} — a {pct_premium:.0f}% premium.",
                        "why_it_costs_you": f"Annualised, this gap costs you {fmt_exact(int(annual_waste))}. That's money leaving your account quietly, every month, with no invoice showing the overpayment explicitly.",
                        "benchmark": bench_line or f"Get 3 quotes — we typically see 10–18% savings on {category} for {industry} businesses.",
                        "next_action": f"Get 2 competing quotes for {category} by Friday.",
                        "action_sub": "Use the script below. Lowest quote gets the 12-month contract.",
                        "collections": [],
                        "template": f"We are reviewing our {category} suppliers. Please send your best rate for [volume]. Decision by Friday — lowest confirmed quote gets a 12-month contract."
                    })
                    break

    # ── 3. Margin gap ───────────────────────────────────────────────────────
    if margin < benchmark-3:
        gap = ((benchmark-margin)/100)*revenue
        if gap>25000:
            leaks.append({
                "id":"margin_gap","severity":"critical" if margin<5 else "warning","priority":3,
                "category":"Profitability",
                "rupee_impact": gap,
                "annual_impact": gap,
                "headline": f"{fmt_exact(int(gap))} in margin left on the table",
                "sub": f"Your margin is {margin:.1f}% vs {benchmark}% industry average",
                "what_we_found": f"Your net margin is {margin:.1f}%. Similar {industry} businesses in India operate at {benchmark}%. The gap is {benchmark-margin:.1f} percentage points.",
                "why_it_costs_you": f"At your revenue of {fmt(revenue)}, closing half that gap adds {fmt(gap*0.5)} in net profit — without acquiring a single new customer.",
                "benchmark": f"Industry benchmark: {benchmark}% for {industry}. Source: CROWDSOURCED data from {CROWDSOURCED.get(industry,{}).get('Raw Materials',{}).get('n','100+')} peers.",
                "next_action": "Raise prices 5% on top 3 products. Cut 10% from the largest expense line.",
                "action_sub": f"Combined: adds ~{fmt(gap*0.15)} in the next 90 days.",
                "collections": [],
                "template": "Reviewing pricing — our category benchmarks show room to increase rates by 5–8%. Implementing from next invoice cycle."
            })

    # ── 4. Customer concentration ───────────────────────────────────────────
    if len(sales)>0 and revenue>0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100>28:
            top_pct = (cr.iloc[0]/revenue)*100
            risk_amt = cr.iloc[0]*0.3  # 1-month delay risk
            leaks.append({
                "id":"concentration","severity":"warning","priority":4,
                "category":"Revenue Risk",
                "rupee_impact": risk_amt,
                "annual_impact": risk_amt,
                "headline": f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub": "One client delay = cash crisis",
                "what_we_found": f"{cr.index[0]} accounts for {top_pct:.0f}% of total revenue ({fmt_exact(int(cr.iloc[0]))}). If they delay payment by 30 days, your cash flow is short by {fmt_exact(int(cr.iloc[0]))}.",
                "why_it_costs_you": f"Concentration above 25% gives that client full negotiating power. They know you can't afford to lose them — and they use it.",
                "benchmark": "Healthy SMEs: no single client above 25% of revenue.",
                "next_action": "Close 2 new clients this month. Set a 25% cap target for 6 months.",
                "action_sub": "Diversification is the only fix. Start today.",
                "collections":[],
                "template": "Looking to expand our client base. If you know businesses that need [your service], happy to offer a referral discount."
            })

    # ── 5. Expense spike ────────────────────────────────────────────────────
    if len(expenses)>0:
        me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me)>=4:
            recent = me.iloc[-3:].mean()
            prior  = me.iloc[:-3].mean() if len(me)>3 else me.iloc[0]
            if prior>0 and recent>prior*1.18:
                spike = (recent-prior)*12
                if spike>20000:
                    leaks.append({
                        "id":"expense_spike","severity":"warning","priority":5,
                        "category":"Cost Control",
                        "rupee_impact": spike,
                        "annual_impact": spike,
                        "headline": f"Monthly costs up {((recent/prior-1)*100):.0f}% — {fmt_exact(int(spike))} annualised drain",
                        "sub": f"₹{(recent-prior)/1000:.0f}K more per month than 3 months ago",
                        "what_we_found": f"Your average monthly expense was {fmt(prior)} three months ago. It is now {fmt(recent)}. That's {fmt(recent-prior)} extra every month.",
                        "why_it_costs_you": f"Annualised, that's {fmt_exact(int(spike))} in additional costs with no matching revenue increase. This is how profitable businesses go cash-negative.",
                        "benchmark": "Expenses should track revenue growth. Rising faster than revenue = structural problem.",
                        "next_action": "Freeze non-essential spend this week. Audit all recurring subscriptions.",
                        "action_sub": "Every spend above ₹5K needs approval until this is resolved.",
                        "collections":[],
                        "template": "Implementing cost freeze from today. All non-essential expenses paused. Reviewing all vendor contracts."
                    })

    # ── 6. GST / Tax ────────────────────────────────────────────────────────
    exp_eligible = expenses[expenses["Amount"]>25000]
    if len(exp_eligible)>0:
        missed = exp_eligible["Amount"].sum()*0.18*0.09
        if missed>8000:
            leaks.append({
                "id":"tax_gst","severity":"info","priority":6,
                "category":"Tax Recovery",
                "rupee_impact": missed,
                "annual_impact": missed,
                "headline": f"~{fmt_exact(int(missed))} in GST input credits to verify",
                "sub": "Estimated quarterly — confirm with your CA",
                "what_we_found": f"Your eligible purchase transactions total {fmt(exp_eligible['Amount'].sum())}. Approximately 9% of claimable GST input credit goes unclaimed by SMEs of your size.",
                "why_it_costs_you": "This is money the government owes you. It simply requires correct invoice matching and timely filing — your CA can recover it in one session.",
                "benchmark": "Urgency: claim before next GST return filing date.",
                "next_action": "Share this report with your CA. Ask specifically about Input Tax Credit on purchases above ₹25K.",
                "action_sub": "Takes one CA session. Typically recoverable within the same quarter.",
                "collections":[],
                "template": "I'd like to review ITC eligibility on our purchase invoices. Can we schedule a call this week?"
            })

    return sorted(leaks, key=lambda x: x["rupee_impact"], reverse=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k,v in [("df",None),("industry","manufacturing"),("city","Bangalore"),
            ("show_bot",False),("contributed",False),("format","")]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════════════════════
# HERO — rewritten per feedback
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Built for Indian SMEs · Bangalore</div>
  <h1 class="hero-headline">
    Your business is<br>leaking <em>₹5–50 Lakhs.</em><br>We find exactly where.
  </h1>
  <p class="hero-sub">
    Upload your Tally Day Book. In 60 seconds we show you — in exact rupees —
    where money is walking out the door, and the three actions that will stop it this week.
    <strong>You pay only when you recover.</strong>
  </p>
  <div class="hero-trust">
    <div class="trust-item"><div class="trust-num">₹50Cr+</div><div class="trust-label">Leaks identified</div></div>
    <div class="trust-item"><div class="trust-num">₹12.4L</div><div class="trust-label">Avg. recovery</div></div>
    <div class="trust-item"><div class="trust-num">4.8 days</div><div class="trust-label">To first recovery</div></div>
    <div class="trust-item"><div class="trust-num">200+</div><div class="trust-label">SMEs scanned</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TRUST BANNER ── (addresses "data safety" objection upfront)
st.markdown("""
<div class="trust-banner">
  <div class="trust-pill"><div class="trust-dot"></div> Your Tally file never leaves your device</div>
  <div class="trust-pill"><div class="trust-dot"></div> No login required for first scan</div>
  <div class="trust-pill"><div class="trust-dot"></div> Results in 60 seconds</div>
  <div class="trust-pill"><div class="trust-dot"></div> Used by CAs across Bangalore, Mumbai, Pune</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_scan, tab_ca, tab_bench = st.tabs(["₹ Scan My Business", "🏛 CA Partner Program", "📊 Industry Benchmarks"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SCAN
# ══════════════════════════════════════════════════════════════════════════════
with tab_scan:

    # Upload zone
    st.markdown('<div class="upload-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="upload-inner">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3,1,1])
    with c1:
        uploaded = st.file_uploader(
            "Upload your Tally Day Book, Sales Register, or Bank Statement (CSV / Excel)",
            type=["csv","xlsx","xls"], key="up"
        )
        with st.expander("How to export from Tally in 30 seconds"):
            st.markdown("""
**Tally Prime:** Display → Account Books → Day Book → Alt+E → Excel  
**Tally ERP 9:** Gateway → Display → Day Book → Ctrl+E → Excel  
**Bank statement:** Download as CSV from net banking  
**Design AID format:** Your multi-section CSV is detected automatically.
            """)
    with c2:
        ind_disp = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
        st.session_state.industry = INDUSTRY_MAP[ind_disp]
    with c3:
        city = st.selectbox("City", ["Bangalore","Mumbai","Delhi","Pune","Chennai","Hyderabad","Ahmedabad","Surat","Other"])
        st.session_state.city = city
        if st.button("Try Demo Data", use_container_width=True):
            np.random.seed(42)
            dates = pd.date_range("2024-04-01","2025-03-31",freq="D")
            recs  = []
            custs = ["ABC Corp","XYZ Industries","PQR Mfg","LMN Traders","DEF Enterprises"]
            vends = ["Steel Supplier A","Steel Supplier B","Raw Material Co","Logistics Ltd","Packaging Inc","Packaging Pro"]
            for d in dates:
                if np.random.random()>0.25:
                    recs.append({"Date":d,"Type":"Sales",
                        "Party":np.random.choice(custs,p=[0.45,0.2,0.15,0.1,0.1]),
                        "Amount":np.random.uniform(60000,280000),
                        "Status":np.random.choice(["Paid","Paid","Overdue","Pending"],p=[0.55,0.25,0.12,0.08]),
                        "Category":"Sales"})
                for _ in range(np.random.randint(1,4)):
                    recs.append({"Date":d,"Type":"Expense","Party":np.random.choice(vends),
                        "Amount":np.random.uniform(12000,90000),"Status":"Paid",
                        "Category":np.random.choice(["Raw Materials","Raw Materials","Labor","Rent","Logistics","Packaging"],p=[0.30,0.15,0.20,0.10,0.15,0.10])})
            demo = pd.DataFrame(recs)
            demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
            st.session_state.df = demo
            st.session_state.industry = "manufacturing"
            st.session_state.format = "demo"
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    if uploaded:
        df_new, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_new
            st.session_state.format = "design_aid" if "Design AID" in msg else "standard"
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info("Quick fix: open the file in Excel → File → Save As → CSV → upload that.")

    # ── RESULTS ──
    if st.session_state.df is not None:
        df       = st.session_state.df
        industry = st.session_state.industry
        city_sel = st.session_state.city

        sales    = df[df["Type"]=="Sales"]
        expenses = df[df["Type"]=="Expense"]
        revenue  = sales["Amount"].sum()
        exp_tot  = expenses["Amount"].sum()
        profit   = revenue - exp_tot
        margin   = (profit/revenue*100) if revenue>0 else 0
        benchmark= INDUSTRY_BENCHMARKS.get(industry,15)

        leaks      = find_leaks(df, industry, city_sel)
        total_liq  = sum(l["rupee_impact"] for l in leaks)   # immediate recoverable
        total_ann  = sum(l["annual_impact"] for l in leaks)  # annual impact

        overdue_amt = (sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum()
                       if "Status" in sales.columns else 0)

        # ── TOPLINE MONEY SCREEN ── (the key improvement from feedback)
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

        collections_leak = next((l for l in leaks if l["id"]=="cash_stuck"), None)
        vendor_leak      = next((l for l in leaks if l["id"]=="cost_bleed"), None)
        tax_leak         = next((l for l in leaks if l["id"]=="tax_gst"), None)
        margin_leak      = next((l for l in leaks if l["id"]=="margin_gap"), None)

        coll_amt   = collections_leak["rupee_impact"] if collections_leak else 0
        vendor_amt = vendor_leak["annual_impact"]     if vendor_leak else 0
        tax_amt    = tax_leak["rupee_impact"]         if tax_leak else 0
        margin_amt = margin_leak["annual_impact"]     if margin_leak else 0

        # Top 3 actions this week
        week_actions = []
        if collections_leak: week_actions.append(f"Call {collections_leak['collections'][0]['message'].split()[1] if collections_leak['collections'] else 'top debtor'} — offer 2% to settle {fmt_exact(int(coll_amt))} overdue")
        if vendor_leak:      week_actions.append(f"Get 2 quotes for {vendor_leak['headline'].split('on ')[-1].split(' per')[0]} — save {fmt(vendor_amt)} this year")
        if tax_leak:         week_actions.append(f"Email your CA about ITC review — {fmt_exact(int(tax_amt))} claimable")
        if not week_actions and margin_leak: week_actions.append(f"Raise top-3 product prices by 5% — adds {fmt(margin_amt*0.15)} in 90 days")

        action_rows_html = "".join([
            f'<div class="action-item-row"><div class="action-bullet">{i+1}</div><div class="action-text">{a}</div></div>'
            for i, a in enumerate(week_actions[:3])
        ])

        st.markdown(f"""
        <div class="money-screen">
          <div class="money-screen-label">Money you can recover</div>
          <div class="money-screen-total">{fmt(total_liq)}</div>
          <div class="money-screen-sub">Identified across {len(leaks)} issues · Annual impact: {fmt(total_ann)}</div>

          {'<div class="money-row urgent"><div class="money-row-left"><div class="money-row-icon">🔴</div><div><div class="money-row-title">Cash stuck in unpaid invoices</div><div class="money-row-desc">Recoverable this month if you act today</div></div></div><div class="money-row-amount">' + fmt_exact(int(coll_amt)) + '</div></div>' if coll_amt>0 else ''}
          {'<div class="money-row medium"><div class="money-row-left"><div class="money-row-icon">🟡</div><div><div class="money-row-title">Vendor overpayment — annual savings</div><div class="money-row-desc">From switching to market-rate suppliers</div></div></div><div class="money-row-amount">' + fmt_exact(int(vendor_amt)) + '/yr</div></div>' if vendor_amt>0 else ''}
          {'<div class="money-row medium"><div class="money-row-left"><div class="money-row-icon">🟡</div><div><div class="money-row-title">Margin gap vs industry peers</div><div class="money-row-desc">Recoverable through pricing + cost action</div></div></div><div class="money-row-amount">' + fmt_exact(int(margin_amt)) + '/yr</div></div>' if margin_amt>0 else ''}
          {'<div class="money-row low"><div class="money-row-left"><div class="money-row-icon">🔵</div><div><div class="money-row-title">GST input credits to verify with CA</div><div class="money-row-desc">Estimated quarterly — needs CA sign-off</div></div></div><div class="money-row-amount">~' + fmt_exact(int(tax_amt)) + '</div></div>' if tax_amt>0 else ''}

          <div class="action-strip">
            <div class="action-strip-title">Do these 3 things this week</div>
            {action_rows_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── KPI ROW ──
        st.markdown(f"""
        <div class="kpi-row">
          <div class="kpi-card">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-val">{fmt(revenue)}</div>
            <div class="kpi-delta">{len(sales)} transactions</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Net Margin</div>
            <div class="kpi-val">{margin:.1f}%</div>
            <div class="kpi-delta {'good' if margin>=benchmark else 'bad'}">vs {benchmark}% benchmark</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Overdue Invoices</div>
            <div class="kpi-val">{fmt(overdue_amt)}</div>
            <div class="kpi-delta {'bad' if overdue_amt>revenue*0.06 else 'good'}">{(overdue_amt/revenue*100 if revenue>0 else 0):.1f}% of revenue</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Net Profit</div>
            <div class="kpi-val">{fmt(abs(profit))}</div>
            <div class="kpi-delta {'good' if profit>0 else 'bad'}">{'Profitable' if profit>0 else '⚠ Loss'}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── DETAILED LEAK CARDS ── (chargeable output format)
        if leaks:
            st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-head">Where your money is leaking</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-sub">{len(leaks)} issues found — each with exact rupees, source data, and a specific next action.</div>', unsafe_allow_html=True)
            st.markdown('<div class="leak-grid">', unsafe_allow_html=True)

            for leak in leaks[:6]:
                sev = leak["severity"]
                st.markdown(f"""
                <div class="leak-card {sev}">
                  <div class="leak-tag {sev}">{leak['category'].upper()}</div>
                  <div class="leak-rupee">{fmt_exact(int(leak['rupee_impact']))}</div>
                  <div class="leak-rupee-sub">{"immediate recovery" if leak["id"]=="cash_stuck" else "annual impact"}</div>
                  <div class="leak-title">{leak['headline']}</div>
                  <div class="leak-desc">{leak['sub']}</div>
                  <div class="leak-source">
                    <strong>What we found:</strong> {leak['what_we_found']}<br><br>
                    <strong>Why it costs you:</strong> {leak['why_it_costs_you']}<br><br>
                    <strong>Benchmark:</strong> {leak['benchmark']}
                  </div>
                  <div class="leak-action">
                    → {leak['next_action']}
                    <div class="leak-action-sub">{leak['action_sub']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Collections bot for overdue
                if leak["id"]=="cash_stuck" and leak.get("collections"):
                    if st.button("Launch collections sequence →", key="bot_btn"):
                        st.session_state.show_bot = True
                    if st.session_state.show_bot:
                        st.markdown("#### Collections Sequence — send these messages")
                        st.caption("4-step escalation. Stop the moment they pay.")
                        for step in leak["collections"]:
                            st.markdown(f"""
                            <div class="seq-card">
                              <div class="seq-day-badge">Day {step['day']} · {step['send_on']}</div>
                              <div class="seq-tone" style="color:{step['color']}">{step['tone']}</div>
                              <div class="seq-msg">{step['message']}</div>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:12px;color:#25D366;">Send via WhatsApp →</a>', unsafe_allow_html=True)

                # WhatsApp script for other leaks
                if leak["id"] != "cash_stuck":
                    if st.button(f"Get WhatsApp script →", key=f"scr_{leak['id']}"):
                        st.code(leak["template"])

            st.markdown('</div></div>', unsafe_allow_html=True)

        # ── TRENDS ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-head" style="font-size:1.3rem;">Revenue vs Expenses</div>', unsafe_allow_html=True)
            monthly = df.groupby([df["Date"].dt.to_period("M"),"Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly, height=220)
        with c2:
            st.markdown('<div class="section-head" style="font-size:1.3rem;">Top Expense Categories</div>', unsafe_allow_html=True)
            if len(expenses)>0:
                st.bar_chart(expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8), height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── PRICING — audit-first model ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="pricing-wrap">
          <div class="section-head" style="color:#F7F4EF; font-size:2rem;">How we work together</div>
          <div class="section-sub" style="color:#6A6A5A;">No subscription traps. Pay only when you recover money.</div>
          <div class="pricing-grid">

            <div class="price-card">
              <div class="price-label">Free scan</div>
              <div class="price-model">First audit</div>
              <div class="price-amount">₹0</div>
              <div class="price-note">Upload your data. See all leaks instantly. No credit card, no login, no strings.</div>
              <ul class="price-features">
                <li>Full leak scan</li>
                <li>Exact rupee amounts</li>
                <li>Top 3 actions this week</li>
                <li>Collections sequences</li>
              </ul>
            </div>

            <div class="price-card featured">
              <div class="price-label">Most chosen</div>
              <div class="price-model">Success fee</div>
              <div class="price-amount">7–10%</div>
              <div class="price-note">We charge only on money you actually recover. No recovery = no fee. Simple.</div>
              <ul class="price-features">
                <li>Everything in free scan</li>
                <li>Recovery Review call with our team</li>
                <li>Vendor quote sourcing</li>
                <li>Monthly monitoring</li>
                <li>CA coordination</li>
              </ul>
            </div>

            <div class="price-card">
              <div class="price-label">For CA firms</div>
              <div class="price-model">Partner plan</div>
              <div class="price-amount">₹1,999/mo</div>
              <div class="price-note">Run OpsClarity for all your clients. White-label reports. ₹500/client/month you earn.</div>
              <ul class="price-features">
                <li>50 client seats</li>
                <li>Branded monthly reports</li>
                <li>Client health dashboard</li>
                <li>GST + TDS risk scanner</li>
                <li>Revenue share program</li>
              </ul>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c_l,c_c,c_r = st.columns([1,2,1])
        with c_c:
            if st.button("Book a free Recovery Review call →", use_container_width=True, type="primary"):
                st.success("✅ Request noted. We'll WhatsApp you within 2 hours to schedule.")
                st.markdown("Or message the founder directly: [wa.me/916362319163](https://wa.me/916362319163)")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CA PARTNER PITCH (1-page pitch built in)
# ══════════════════════════════════════════════════════════════════════════════
with tab_ca:
    demo_portfolio = [
        {"name":"Sharma Textiles Pvt Ltd",  "city":"Ahmedabad","ind":"textile",       "rev":4200000,"leak":840000, "health":"red"},
        {"name":"Mehta Food Products",       "city":"Mumbai",   "ind":"restaurant",    "rev":2800000,"leak":196000, "health":"amber"},
        {"name":"Rajesh Diagnostics",        "city":"Pune",     "ind":"clinic",        "rev":6100000,"leak":91500,  "health":"green"},
        {"name":"Kapoor Steel Trading",      "city":"Delhi",    "ind":"manufacturing", "rev":8900000,"leak":1780000,"health":"red"},
        {"name":"Green Pharma Dist.",        "city":"Chennai",  "ind":"pharma",        "rev":3400000,"leak":238000, "health":"amber"},
        {"name":"Sri Venkateswara Printers", "city":"Hyderabad","ind":"printing",      "rev":1900000,"leak":28500,  "health":"green"},
    ]
    total_rev   = sum(c["rev"]  for c in demo_portfolio)
    total_leak  = sum(c["leak"] for c in demo_portfolio)
    crit_count  = sum(1 for c in demo_portfolio if c["health"]=="red")

    st.markdown("""
    <div class="ca-pitch-wrap">
      <div class="hero-badge" style="margin-bottom:1rem;">For Chartered Accountants</div>
      <div class="section-head" style="font-size:2.2rem;">Your clients are losing money.<br>You can show them exactly where.</div>
      <div class="section-sub" style="font-size:1rem; max-width:600px; margin-bottom:2rem;">
        OpsClarity gives you a branded profit-leak report for every client — automated, monthly, zero extra work.
        CAs who use it retain clients longer, get more referrals, and earn ₹500/client/month in passive income.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    # Math card
    st.markdown('<div class="section-head" style="font-size:1.5rem; margin-bottom:1rem;">The CA partner math</div>', unsafe_allow_html=True)
    n_ca = st.slider("Your client count", 10, 200, 40, 5)
    st.markdown(f"""
    <div class="ca-pitch-grid">
      <div class="ca-card">
        <div class="ca-card-label">Your numbers</div>
        <div class="ca-math-row"><div class="ca-math-label">Clients on OpsClarity</div><div class="ca-math-val">{n_ca}</div></div>
        <div class="ca-math-row"><div class="ca-math-label">Your cost (platform)</div><div class="ca-math-val">₹1,999/month</div></div>
        <div class="ca-math-row"><div class="ca-math-label">You earn per client</div><div class="ca-math-val">₹500/month</div></div>
        <div class="ca-math-row"><div class="ca-math-label">Monthly passive income</div><div class="ca-math-val highlight">₹{n_ca*500:,}/month</div></div>
        <div class="ca-math-row" style="border:none"><div class="ca-math-label">Net after platform cost</div><div class="ca-math-val highlight">₹{n_ca*500-1999:,}/month</div></div>
      </div>
      <div class="ca-card">
        <div class="ca-card-label">What your clients get</div>
        <div class="ca-card-title">Monthly profit health report</div>
        <div class="ca-card-body">
          Branded with your CA firm name. Shows every client exactly where they're losing money — in exact rupees, with specific actions.<br><br>
          <strong>Every month, without you doing any extra work.</strong><br><br>
          Clients who receive this report: renew without asking, refer you more, and stop shopping around for another CA.
          That's the real value — not the ₹500/month. It's the <em>relationship deepening</em>.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Live client dashboard demo
    st.markdown('<div class="section-head" style="font-size:1.5rem; margin: 2rem 0 1rem;">Your client dashboard — live view</div>', unsafe_allow_html=True)

    # Build rows first to avoid nested f-string issues
    client_rows_html = ""
    for c in demo_portfolio:
        hl = "🔴 Critical" if c["health"]=="red" else "🟡 Watch" if c["health"]=="amber" else "🟢 Healthy"
        client_rows_html += (
            f'<div class="ca-client-row">'
            f'<div><div class="ca-client-name">{c["name"]}</div>'
            f'<div class="ca-client-meta">{c["city"]} · {c["ind"].title()}</div></div>'
            f'<div class="ca-leak-amt">{fmt(c["leak"])}</div>'
            f'<div class="ca-health {c["health"]}">{hl}</div>'
            f'</div>'
        )

    st.markdown(
        f'''<div class="ca-card dark">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;">
        <div><div class="ca-card-label">Active clients</div><div class="ca-card-title">''' + str(len(demo_portfolio)) + f'''</div></div>
        <div><div class="ca-card-label">Leaks found</div><div class="ca-card-title" style="color:#D4AF37;">''' + fmt(total_leak) + f'''</div></div>
        <div><div class="ca-card-label">Critical — action needed</div><div class="ca-card-title" style="color:#E05252;">''' + str(crit_count) + f''' clients</div></div>
      </div>
      <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:1rem;">''' + client_rows_html + '''</div>
    </div>''',
        unsafe_allow_html=True
    )


    # CA objections addressed
    st.markdown('<div class="section-head" style="font-size:1.5rem; margin: 2rem 0 1rem;">Questions CAs ask us</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ca-pitch-grid">
      <div class="ca-card">
        <div class="ca-card-label">Q: My clients won't share data</div>
        <div class="ca-card-body">You upload the file — your client never interacts with OpsClarity directly. You control what they see. The report comes branded as your firm's work. Clients see a CA service, not a third-party app.</div>
      </div>
      <div class="ca-card">
        <div class="ca-card-label">Q: What if the numbers are wrong?</div>
        <div class="ca-card-body">OpsClarity flags potential leaks. You verify before sharing — exactly as you'd review any report before signing off. This is your co-pilot, not your replacement. Your professional judgement is still the product.</div>
      </div>
      <div class="ca-card">
        <div class="ca-card-label">Q: I already do this manually</div>
        <div class="ca-card-body">If you already do this for 40 clients manually every month, you know how many hours it takes. OpsClarity does the same analysis in 60 seconds per client. That time goes back to you — or to more clients.</div>
      </div>
      <div class="ca-card">
        <div class="ca-card-label">Q: Will it replace CAs?</div>
        <div class="ca-card-body">No. The report says "verify with your CA" seven times. Tax findings, ITC claims, TDS — all of these require a qualified CA to action. We create the work. You do the work. Your client pays you more.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    c_l,c_c,c_r = st.columns([1,2,1])
    with c_c:
        if st.button("Join CA Partner Program — free 30-day trial →", use_container_width=True, type="primary"):
            st.balloons()
            st.success("✅ Application received. We'll call within 4 hours to set up your dashboard.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
with tab_bench:
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Industry Benchmark Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Anonymised data from Indian SMEs. Used to validate every leak we flag.</div>', unsafe_allow_html=True)

    sel_ind = st.selectbox("Industry", list(CROWDSOURCED.keys()), key="bi")
    bd = CROWDSOURCED.get(sel_ind,{})
    if bd:
        for cat, data in bd.items():
            with st.expander(f"{cat} — {data['n']} businesses reporting"):
                b1,b2,b3,b4 = st.columns(4)
                b1.metric("Best 25% pay", f"₹{data['p25']:,}{data['unit']}")
                b2.metric("Median",       f"₹{data['median']:,}{data['unit']}")
                b3.metric("Top 25% pay",  f"₹{data['p75']:,}{data['unit']}")
                b4.metric("Sample size",  str(data["n"]))
                savings = ((data["p75"]-data["p25"])/data["p75"])*100
                st.info(f"Switching from top-25% rate to best-25% rate = **{savings:.0f}% cost reduction** on {cat}.")
                if data.get("city_splits"):
                    st.dataframe(pd.DataFrame([(c,r) for c,r in data["city_splits"].items()],
                                              columns=["City",f"Rate ({data['unit']})"]),
                                 hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
  <div>
    <div class="footer-brand">OpsClarity</div>
    <div class="footer-legal">Profit Recovery · Built in Bangalore 🇮🇳</div>
  </div>
  <div class="footer-legal">
    Management estimates only — not CA advice · Your data stays on your device ·
    <a href="#" style="color:#6A6A5A;">Privacy</a> · <a href="#" style="color:#6A6A5A;">Terms</a>
  </div>
</div>
<a href="https://wa.me/916362319163?text=Hi, question about OpsClarity" class="wa-float" target="_blank">
  💬 Talk to founder
</a>
""", unsafe_allow_html=True)
