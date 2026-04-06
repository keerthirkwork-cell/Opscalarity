import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse, io, requests, json, os

st.set_page_config(
    page_title="OpsClarity — Profit Engine",
    page_icon="₹", layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
.stApp{background:#F7F4EF;font-family:'DM Sans',sans-serif;color:#1A1A1A}
.main .block-container{padding:0!important;max-width:100%!important}

/* HERO */
.hero{background:#1A1A1A;padding:4rem 3rem 3rem}
.hero-badge{display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.5rem}
.hero-h{font-family:'DM Serif Display',serif;font-size:clamp(2.4rem,4.5vw,4rem);color:#F7F4EF;line-height:1.1;margin-bottom:1.2rem}
.hero-h em{font-style:italic;color:#D4AF37}
.hero-sub{font-size:1rem;color:#9A9A8A;max-width:540px;line-height:1.7;margin-bottom:2rem;font-weight:300}
.trust-row{display:flex;gap:2.5rem;flex-wrap:wrap;margin-top:2rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,0.08)}
.trust-item .t-num{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#D4AF37}
.trust-item .t-lbl{font-size:11px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em}
.safety-bar{background:#EDEAE3;padding:.75rem 3rem;display:flex;gap:2rem;flex-wrap:wrap;border-bottom:1px solid #D8D4CC}
.s-pill{font-size:12px;color:#4A4A3A;font-weight:500;display:flex;align-items:center;gap:6px}
.s-dot{width:6px;height:6px;background:#4CAF50;border-radius:50%}

/* ── MONEY SAVED COUNTER (THE BIG ONE) ── */
.msc-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#2A2A1A 100%);border-radius:20px;padding:2.5rem;margin:1.5rem 0;border:1px solid rgba(212,175,55,0.3)}
.msc-label{font-size:11px;font-weight:700;color:#D4AF37;text-transform:uppercase;letter-spacing:.2em;margin-bottom:.5rem}
.msc-total{font-family:'DM Serif Display',serif;font-size:4rem;color:#D4AF37;line-height:1;margin-bottom:.3rem}
.msc-sub{font-size:13px;color:#5A5A4A;margin-bottom:2rem}
.msc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.msc-cell{background:rgba(255,255,255,0.04);border-radius:12px;padding:1.1rem}
.msc-cell-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.msc-cell-val{font-family:'DM Serif Display',serif;font-size:1.4rem;color:#F7F4EF}
.msc-cell-val.green{color:#4CAF50}
.msc-cell-val.gold{color:#D4AF37}
.msc-cell-val.red{color:#E05252}

/* ── BEFORE/AFTER TRACKER ── */
.ba-wrap{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:1.5rem;margin:1rem 0}
.ba-title{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#1A1A1A;margin-bottom:1rem}
.ba-grid{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center}
.ba-col{background:#F7F4EF;border-radius:12px;padding:1.1rem}
.ba-col.after{background:#E8F5E9}
.ba-col-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#9A9A8A;margin-bottom:.4rem}
.ba-col.after .ba-col-lbl{color:#2E7D32}
.ba-col-val{font-family:'DM Serif Display',serif;font-size:2rem;color:#1A1A1A}
.ba-col.after .ba-col-val{color:#2E7D32}
.ba-col-sub{font-size:12px;color:#6A6A5A;margin-top:3px}
.ba-arrow{font-size:2rem;color:#D4AF37;text-align:center}
.ba-delta{display:inline-block;background:#D4AF37;color:#1A1A1A;font-size:12px;font-weight:700;padding:3px 10px;border-radius:20px;margin-top:6px}

/* ── ACTION TRACKER ── */
.at-wrap{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:1.5rem;margin:1rem 0}
.at-row{display:flex;align-items:center;justify-content:space-between;padding:.75rem;border-radius:10px;margin-bottom:6px;background:#F7F4EF}
.at-row.done{background:#E8F5E9;border-left:3px solid #4CAF50}
.at-row.pending{background:#FFFBF0;border-left:3px solid #D4AF37}
.at-row.skipped{background:#FEF0F0;border-left:3px solid #E05252;opacity:0.7}
.at-left{flex:1}
.at-action{font-size:13px;font-weight:600;color:#1A1A1A}
.at-row.done .at-action{color:#2E7D32}
.at-meta{font-size:11px;color:#6A6A5A;margin-top:2px}
.at-impact{font-family:'DM Mono',monospace;font-size:13px;font-weight:700;color:#D4AF37;margin:0 1rem}
.at-status{font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px}
.at-status.done{background:#E8F5E9;color:#2E7D32}
.at-status.pending{background:#FFFBF0;color:#9A7A00}
.at-status.skipped{background:#FEF0F0;color:#C0392B}

/* ── ROI REPORT ── */
.roi-wrap{background:#1A1A1A;border-radius:16px;padding:2rem;margin:1.5rem 0}
.roi-title{font-family:'DM Serif Display',serif;font-size:1.5rem;color:#F7F4EF;margin-bottom:.3rem}
.roi-sub{font-size:13px;color:#5A5A4A;margin-bottom:1.5rem}
.roi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem}
.roi-cell{background:rgba(255,255,255,0.04);border-radius:12px;padding:1.1rem;text-align:center}
.roi-cell-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.roi-cell-val{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#D4AF37}
.roi-cell-val.green{color:#4CAF50}
.roi-verdict{background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.3);border-radius:12px;padding:1rem 1.25rem;text-align:center}
.roi-verdict-main{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#D4AF37}
.roi-verdict-sub{font-size:12px;color:#6A6A5A;margin-top:4px}

/* existing styles */
.money-screen{background:#1A1A1A;border-radius:16px;padding:2rem;margin:1.5rem 0}
.ms-label{font-size:11px;font-weight:600;color:#6A6A5A;text-transform:uppercase;letter-spacing:.15em;margin-bottom:4px}
.ms-total{font-family:'DM Serif Display',serif;font-size:3.5rem;color:#D4AF37;line-height:1}
.ms-sub{font-size:13px;color:#5A5A4A;margin-bottom:1.5rem;margin-top:4px}
.ms-row{display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem;background:rgba(255,255,255,0.04);border-radius:10px;margin-bottom:6px}
.ms-row.r{border-left:3px solid #E05252}
.ms-row.a{border-left:3px solid #D4AF37}
.ms-row.b{border-left:3px solid #5B9BD5}
.ms-left{display:flex;align-items:center;gap:10px}
.ms-title{font-size:14px;font-weight:500;color:#F7F4EF}
.ms-desc{font-size:11px;color:#5A5A4A;margin-top:2px}
.ms-amt{font-family:'DM Mono',monospace;font-size:1rem;font-weight:600;color:#D4AF37}
.act-box{background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:10px;padding:1rem 1.25rem;margin-top:1.25rem}
.act-lbl{font-size:11px;font-weight:600;color:#D4AF37;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.6rem}
.act-item{display:flex;gap:8px;margin-bottom:6px}
.act-num{width:18px;height:18px;border-radius:50%;background:#D4AF37;color:#1A1A1A;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.act-text{font-size:13px;color:#C8C8B8;line-height:1.5}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0}
.kpi-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1.1rem 1.3rem}
.kpi-lbl{font-size:11px;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.kpi-val{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#1A1A1A}
.kpi-sub{font-size:12px;margin-top:3px}
.good{color:#2E8B57}.bad{color:#C0392B}.warn{color:#9A7A00}
.sw{padding:1.5rem 3rem}
.sh{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#1A1A1A;margin-bottom:4px}
.ss{font-size:13px;color:#6A6A5A;margin-bottom:1.5rem}
.lk-card{background:#FFF;border:1px solid #E8E4DC;border-radius:14px;padding:1.4rem;margin-bottom:1rem;position:relative;overflow:hidden}
.lk-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.lk-card.critical::before{background:#E05252}
.lk-card.warning::before{background:#D4AF37}
.lk-card.info::before{background:#5B9BD5}
.lk-tag{display:inline-block;font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;margin-bottom:.75rem;letter-spacing:.08em}
.lk-tag.critical{background:#FEF0F0;color:#C0392B}
.lk-tag.warning{background:#FFFBF0;color:#9A7A00}
.lk-tag.info{background:#EFF5FE;color:#2060A0}
.lk-amt{font-family:'DM Serif Display',serif;font-size:2rem;color:#1A1A1A;line-height:1}
.lk-sub{font-size:11px;color:#9A9A8A;margin-bottom:.75rem}
.lk-ttl{font-size:14px;font-weight:600;color:#1A1A1A;margin-bottom:.4rem}
.lk-desc{font-size:13px;color:#6A6A5A;line-height:1.6;margin-bottom:1rem}
.lk-src{background:#F7F4EF;border-radius:8px;padding:.7rem .9rem;margin-bottom:.9rem;font-size:12px;color:#4A4A3A;line-height:1.55}
.lk-act{border-top:1px solid #F0EDE6;padding-top:.9rem;font-size:13px;font-weight:600;color:#1A1A1A}
.lk-act-s{font-size:12px;font-weight:400;color:#6A6A5A;margin-top:3px}
.seq-card{background:#F7F4EF;border:1px solid #E0DDD6;border-radius:10px;padding:1rem;margin-bottom:8px}
.seq-day{display:inline-block;background:#1A1A1A;color:#D4AF37;font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;margin-bottom:6px}
.seq-tone{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px}
.seq-msg{font-size:12px;color:#4A4A3A;line-height:1.6}
.ca-wrap{background:#F0EDE6;padding:2rem 3rem}
.ca-card{background:#FFF;border:1px solid #E0DDD6;border-radius:14px;padding:1.4rem;margin-bottom:1rem}
.ca-card.dark{background:#1A1A1A;border-color:rgba(255,255,255,0.08)}
.ca-lbl{font-size:11px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.ca-ttl{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#1A1A1A;margin-bottom:6px}
.ca-body{font-size:13px;color:#6A6A5A;line-height:1.7}
.ca-card.dark .ca-ttl{color:#F7F4EF}
.ca-card.dark .ca-body{color:#9A9A8A}
.ca-row{display:flex;justify-content:space-between;align-items:center;padding:.65rem 0;border-bottom:1px solid #F0EDE6}
.ca-row-lbl{font-size:13px;color:#4A4A3A}
.ca-row-val{font-family:'DM Mono',monospace;font-size:13px;font-weight:600;color:#1A1A1A}
.ca-row-val.hl{color:#2E8B57;font-size:1rem}
.cl-row{display:flex;align-items:center;justify-content:space-between;padding:.6rem 0;border-bottom:1px solid rgba(255,255,255,0.06)}
.cl-name{font-size:13px;font-weight:500;color:#F7F4EF}
.cl-meta{font-size:11px;color:#5A5A4A}
.cl-amt{font-family:'DM Mono',monospace;font-size:12px;color:#D4AF37}
.cl-h.red{color:#E05252;font-size:12px;font-weight:600}
.cl-h.amber{color:#D4AF37;font-size:12px;font-weight:600}
.cl-h.green{color:#4CAF50;font-size:12px;font-weight:600}
.pr-wrap{background:#1A1A1A;padding:2.5rem 3rem}
.pr-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.75rem}
.pr-card.feat{background:rgba(212,175,55,0.08);border-color:rgba(212,175,55,0.35)}
.pr-lbl{font-size:11px;font-weight:600;color:#5A5A4A;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.75rem}
.pr-name{font-family:'DM Serif Display',serif;font-size:1.4rem;color:#F7F4EF;margin-bottom:4px}
.pr-amt{font-family:'DM Mono',monospace;font-size:2rem;color:#D4AF37;margin-bottom:8px}
.pr-note{font-size:12px;color:#6A6A5A;margin-bottom:1.25rem;line-height:1.55}
.pr-feat{font-size:12px;color:#8A8A7A;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.pr-feat::before{content:"→ ";color:#D4AF37}
.footer{background:#1A1A1A;padding:1.5rem 3rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem}
.ft-brand{font-family:'DM Serif Display',serif;font-size:1.1rem;color:#D4AF37}
.ft-legal{font-size:11px;color:#4A4A3A}
.wa-btn{position:fixed;bottom:24px;right:24px;background:#25D366;color:#FFF;padding:12px 20px;border-radius:50px;font-weight:600;text-decoration:none;font-size:13px;display:flex;align-items:center;gap:6px;box-shadow:0 4px 16px rgba(37,211,102,0.35);z-index:9999}
.gate-box{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:2rem;margin:2rem 0;text-align:center}
.gate-h{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#1A1A1A;margin-bottom:.5rem}
.gate-s{font-size:14px;color:#6A6A5A;margin-bottom:1.5rem}
div[data-testid="stVerticalBlock"]{gap:0!important}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
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
    "manufacturing":{"Raw Materials":{"p25":42000,"median":51000,"p75":64000,"unit":"/ton","n":312},"Labor":{"p25":380,"median":460,"p75":580,"unit":"/day","n":445},"Logistics":{"p25":8,"median":11,"p75":16,"unit":"/km","n":289},"Packaging":{"p25":11,"median":17,"p75":24,"unit":"/pc","n":198}},
    "restaurant":{"Food Ingredients":{"p25":28,"median":34,"p75":42,"unit":"% rev","n":521},"Labor":{"p25":18,"median":24,"p75":32,"unit":"% rev","n":498},"Rent":{"p25":8,"median":12,"p75":18,"unit":"% rev","n":412},"Utilities":{"p25":3,"median":5,"p75":8,"unit":"% rev","n":389}},
    "retail":{"Rent":{"p25":80,"median":120,"p75":200,"unit":"/sqft/mo","n":445},"Inventory":{"p25":42,"median":52,"p75":64,"unit":"% rev","n":398},"Staff":{"p25":8,"median":12,"p75":18,"unit":"% rev","n":445}},
    "clinic":{"Staff Salaries":{"p25":18,"median":24,"p75":31,"unit":"% rev","n":187},"Consumables":{"p25":8,"median":12,"p75":18,"unit":"% rev","n":187},"Rent":{"p25":6,"median":9,"p75":14,"unit":"% rev","n":187},"Equipment Lease":{"p25":3,"median":5,"p75":9,"unit":"% rev","n":142}},
    "agency":{"Salaries":{"p25":38,"median":48,"p75":60,"unit":"% rev","n":312},"Software & Tools":{"p25":3,"median":6,"p75":10,"unit":"% rev","n":312},"Office & Admin":{"p25":4,"median":7,"p75":12,"unit":"% rev","n":312},"Freelancers":{"p25":5,"median":10,"p75":18,"unit":"% rev","n":267}},
    "logistics":{"Fuel":{"p25":18,"median":23,"p75":30,"unit":"% rev","n":201},"Driver Wages":{"p25":14,"median":19,"p75":25,"unit":"% rev","n":201},"Maintenance":{"p25":5,"median":8,"p75":13,"unit":"% rev","n":201},"Tolls & Permits":{"p25":2,"median":4,"p75":7,"unit":"% rev","n":189}},
    "construction":{"Materials":{"p25":38,"median":46,"p75":56,"unit":"% rev","n":167},"Labor":{"p25":22,"median":28,"p75":35,"unit":"% rev","n":167},"Equipment":{"p25":5,"median":9,"p75":15,"unit":"% rev","n":167},"Subcontractors":{"p25":8,"median":14,"p75":22,"unit":"% rev","n":134}},
    "textile":{"Raw Material":{"p25":42,"median":51,"p75":61,"unit":"% rev","n":223},"Labor":{"p25":14,"median":18,"p75":24,"unit":"% rev","n":223},"Power":{"p25":4,"median":6,"p75":10,"unit":"% rev","n":223},"Dyeing & Finishing":{"p25":3,"median":5,"p75":8,"unit":"% rev","n":198}},
    "pharma":{"Inventory":{"p25":22,"median":28,"p75":36,"unit":"% rev","n":143},"Distribution":{"p25":4,"median":7,"p75":11,"unit":"% rev","n":143},"Regulatory":{"p25":2,"median":4,"p75":7,"unit":"% rev","n":143},"Staff":{"p25":12,"median":16,"p75":22,"unit":"% rev","n":143}},
    "printing":{"Paper & Media":{"p25":28,"median":35,"p75":44,"unit":"% rev","n":156},"Ink & Consumables":{"p25":8,"median":12,"p75":17,"unit":"% rev","n":156},"Equipment Lease":{"p25":5,"median":8,"p75":13,"unit":"% rev","n":156},"Labor":{"p25":16,"median":22,"p75":30,"unit":"% rev","n":156}},
}
DEMO_CUSTOMERS = ["Sharma Enterprises","Patel & Sons Trading","Krishna Steels Pvt Ltd","Mehta Industries","Lakshmi Distributors","Venkatesh Fabricators","Gupta Hardware","Nair Logistics","Reddy Constructions","Iyer & Co"]
DEMO_VENDORS   = ["Tata Steel Suppliers","National Raw Materials","City Transport Services","Vinayak Packaging","Bharat Logistics","Sunrise Packaging","Metro Courier","Reliable Raw Mat Co","Standard Suppliers","Prime Distributors"]

def fmt(v):
    v=float(v)
    if abs(v)>=1e7: return f"₹{v/1e7:.1f}Cr"
    if abs(v)>=1e5: return f"₹{v/1e5:.1f}L"
    if abs(v)>=1000:return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"
def fmtx(v): return f"₹{int(float(v)):,}"

# ═══════════════════════════════════════════════════════════
# 1. MONEY SAVED TRACKER LOGIC
# ═══════════════════════════════════════════════════════════
def calculate_savings(actions):
    """
    actions = list of dicts:
      {id, label, suggested_saving, status: done/pending/skipped, actual_saving, date_done}
    Returns: total_saved, total_identified, savings_rate
    """
    total_identified = sum(a["suggested_saving"] for a in actions)
    total_saved      = sum(a.get("actual_saving", a["suggested_saving"])
                           for a in actions if a["status"] == "done")
    rate = (total_saved / total_identified * 100) if total_identified > 0 else 0
    return total_saved, total_identified, rate

def render_money_saved_counter(actions, monthly_fee=2999):
    total_saved, total_identified, rate = calculate_savings(actions)
    done_count    = sum(1 for a in actions if a["status"] == "done")
    pending_count = sum(1 for a in actions if a["status"] == "pending")
    roi_x         = (total_saved / monthly_fee) if monthly_fee > 0 else 0

    st.markdown(f"""
<div class="msc-wrap">
  <div class="msc-label">💰 Total Money Recovered</div>
  <div class="msc-total">{fmt(total_saved)}</div>
  <div class="msc-sub">of {fmt(total_identified)} identified · {rate:.0f}% recovery rate</div>
  <div class="msc-grid">
    <div class="msc-cell">
      <div class="msc-cell-lbl">Actions Completed</div>
      <div class="msc-cell-val green">{done_count} done</div>
    </div>
    <div class="msc-cell">
      <div class="msc-cell-lbl">Still Pending</div>
      <div class="msc-cell-val gold">{pending_count} to do</div>
    </div>
    <div class="msc-cell">
      <div class="msc-cell-lbl">Return on OpsClarity Fee</div>
      <div class="msc-cell-val green">{roi_x:.0f}x ROI</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 2. BEFORE / AFTER TRACKER
# ═══════════════════════════════════════════════════════════
def render_before_after(margin_before, margin_after, revenue,
                         overdue_before, overdue_after,
                         top_expense_before, top_expense_after):
    profit_before = revenue * margin_before / 100
    profit_after  = revenue * margin_after  / 100
    profit_delta  = profit_after - profit_before

    st.markdown(f"""
<div class="ba-wrap">
  <div class="ba-title">📈 Before vs After OpsClarity</div>

  <div style="margin-bottom:1rem">
    <div style="font-size:12px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.6rem">Net Profit Margin</div>
    <div class="ba-grid">
      <div class="ba-col">
        <div class="ba-col-lbl">Before</div>
        <div class="ba-col-val">{margin_before:.1f}%</div>
        <div class="ba-col-sub">Profit: {fmt(profit_before)}</div>
      </div>
      <div class="ba-arrow">→</div>
      <div class="ba-col after">
        <div class="ba-col-lbl">After actions</div>
        <div class="ba-col-val">{margin_after:.1f}%</div>
        <div class="ba-col-sub">Profit: {fmt(profit_after)}</div>
        <div class="ba-delta">+{fmt(profit_delta)} extra profit</div>
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:.75rem">
    <div>
      <div style="font-size:12px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem">Overdue Receivables</div>
      <div class="ba-grid">
        <div class="ba-col"><div class="ba-col-lbl">Before</div><div class="ba-col-val" style="font-size:1.3rem">{fmt(overdue_before)}</div></div>
        <div class="ba-arrow" style="font-size:1.2rem">→</div>
        <div class="ba-col after"><div class="ba-col-lbl">After</div><div class="ba-col-val" style="font-size:1.3rem">{fmt(overdue_after)}</div><div class="ba-delta">-{fmt(overdue_before-overdue_after)}</div></div>
      </div>
    </div>
    <div>
      <div style="font-size:12px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem">Top Expense / Month</div>
      <div class="ba-grid">
        <div class="ba-col"><div class="ba-col-lbl">Before</div><div class="ba-col-val" style="font-size:1.3rem">{fmt(top_expense_before)}</div></div>
        <div class="ba-arrow" style="font-size:1.2rem">→</div>
        <div class="ba-col after"><div class="ba-col-lbl">After</div><div class="ba-col-val" style="font-size:1.3rem">{fmt(top_expense_after)}</div><div class="ba-delta">-{fmt(top_expense_before-top_expense_after)}</div></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 3. ACTION TRACKER
# ═══════════════════════════════════════════════════════════
def render_action_tracker(actions, key_prefix="act"):
    st.markdown('<div class="at-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="sh" style="font-size:1.3rem;margin-bottom:.3rem">✅ Action Tracker — track every rupee saved</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Mark actions done. We track actual savings vs estimated. This becomes your ROI proof.</div>', unsafe_allow_html=True)

    for i, action in enumerate(actions):
        status  = action["status"]
        css_cls = status  # done / pending / skipped
        icon    = "✅" if status=="done" else ("⏳" if status=="pending" else "❌")
        saved   = action.get("actual_saving", action["suggested_saving"])

        st.markdown(f"""
<div class="at-row {css_cls}">
  <div class="at-left">
    <div class="at-action">{icon} {action['label']}</div>
    <div class="at-meta">{action.get('meta','')}</div>
  </div>
  <div class="at-impact">{fmt(saved)}</div>
  <div class="at-status {css_cls}">{status.upper()}</div>
</div>
""", unsafe_allow_html=True)

        if status == "pending":
            c1, c2, c3 = st.columns([2,1,1])
            with c2:
                if st.button("✅ Mark Done", key=f"{key_prefix}_done_{i}"):
                    st.session_state.actions[i]["status"] = "done"
                    st.session_state.actions[i]["date_done"] = datetime.now().isoformat()
                    st.rerun()
            with c3:
                if st.button("❌ Skip", key=f"{key_prefix}_skip_{i}"):
                    st.session_state.actions[i]["status"] = "skipped"
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 4. ROI REPORT
# ═══════════════════════════════════════════════════════════
def render_roi_report(actions, monthly_fee, biz_name, months_active=1):
    total_saved, total_identified, rate = calculate_savings(actions)
    total_fees  = monthly_fee * months_active
    net_gain    = total_saved - total_fees
    roi_x       = (total_saved / total_fees) if total_fees > 0 else 0
    done_count  = sum(1 for a in actions if a["status"]=="done")

    verdict = ""
    if roi_x >= 10:
        verdict = f"Every ₹1 spent on OpsClarity returned ₹{roi_x:.0f}. This is exceptional."
    elif roi_x >= 3:
        verdict = f"Strong ROI. OpsClarity returned {roi_x:.1f}x your investment."
    elif roi_x >= 1:
        verdict = f"Positive ROI. Continue to complete pending actions to improve further."
    else:
        verdict = f"{len([a for a in actions if a['status']=='pending'])} actions still pending. Complete them to see full return."

    # Generate text report for download/WhatsApp
    report_lines = [
        "=" * 50,
        f"ROI REPORT — OpsClarity",
        f"Business: {biz_name}",
        f"Period: {months_active} month(s) · Generated {datetime.now().strftime('%d %b %Y')}",
        "=" * 50,
        f"Fee paid:        {fmtx(total_fees)}",
        f"Savings found:   {fmt(total_identified)}",
        f"Savings realised:{fmt(total_saved)}",
        f"Net gain:        {fmt(net_gain)}",
        f"ROI:             {roi_x:.1f}x",
        "─" * 50,
        "Actions:",
    ]
    for a in actions:
        report_lines.append(f"  [{a['status'].upper():7}] {a['label'][:45]:45} {fmt(a.get('actual_saving',a['suggested_saving'])):>10}")
    report_lines += ["=" * 50, verdict]
    report_text = "\n".join(report_lines)

    st.markdown(f"""
<div class="roi-wrap">
  <div class="roi-title">📊 Your ROI Report</div>
  <div class="roi-sub">{biz_name} · {months_active} month(s) with OpsClarity</div>
  <div class="roi-grid">
    <div class="roi-cell">
      <div class="roi-cell-lbl">You Paid</div>
      <div class="roi-cell-val">{fmtx(total_fees)}</div>
    </div>
    <div class="roi-cell">
      <div class="roi-cell-lbl">You Saved</div>
      <div class="roi-cell-val green">{fmt(total_saved)}</div>
    </div>
    <div class="roi-cell">
      <div class="roi-cell-lbl">Return</div>
      <div class="roi-cell-val">{roi_x:.1f}x</div>
    </div>
  </div>
  <div class="roi-verdict">
    <div class="roi-verdict-main">{verdict}</div>
    <div class="roi-verdict-sub">{done_count} of {len(actions)} actions completed · {fmt(total_identified - total_saved)} still recoverable</div>
  </div>
</div>
""", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.download_button(
            "📄 Download ROI Report",
            data=report_text,
            file_name=f"opsclarity_roi_{datetime.now().strftime('%d%b%Y')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with r2:
        wa_msg = urllib.parse.quote(
            f"Hi! My OpsClarity ROI Report:\n"
            f"Fee paid: {fmtx(total_fees)}\n"
            f"Savings realised: {fmt(total_saved)}\n"
            f"Return: {roi_x:.1f}x\n\n{verdict}"
        )
        st.markdown(
            f'<a href="https://wa.me/916362319163?text={wa_msg}" target="_blank">'
            f'<button style="width:100%;background:#25D366;color:white;border:none;padding:8px 12px;border-radius:8px;font-weight:600;cursor:pointer;font-size:13px;">💬 Share ROI on WhatsApp</button></a>',
            unsafe_allow_html=True
        )

# ═══════════════════════════════════════════════════════════
# COLLECTIONS SEQUENCE
# ═══════════════════════════════════════════════════════════
SEQ=[
    {"day":1,"tone":"Friendly reminder","color":"#5B9BD5","msg":"Hi {name} 🙏 Quick note — invoice #{inv} for {amt} is due. Any issues? Happy to help. — {biz}"},
    {"day":3,"tone":"Offer + urgency","color":"#D4AF37","msg":"Hi {name}, invoice #{inv} ({amt}) is overdue. Offering 2% discount if settled by {dl}. Please confirm. — {biz}"},
    {"day":7,"tone":"Operational impact","color":"#E08020","msg":"{name}, invoice #{inv} ({amt}) is 7 days overdue. Payment needed by {dl} or we pause future orders. — {biz}"},
    {"day":10,"tone":"Final notice","color":"#E05252","msg":"FINAL NOTICE — {name}: invoice #{inv} ({amt}) is 10 days unpaid. Pay by {dl} or accounts team takes over. — {biz}"},
]
def gen_seq(name,inv,amount,biz):
    today=datetime.now()
    return [{**s,
        "send_on":(today+timedelta(days=s["day"])).strftime("%d %b"),
        "message":s["msg"].format(name=name,inv=inv,amt=fmt(amount),biz=biz,dl=(today+timedelta(days=s["day"]+3)).strftime("%d %b %Y")),
        "wa_link":f"https://wa.me/?text={urllib.parse.quote(s['msg'].format(name=name,inv=inv,amt=fmt(amount),biz=biz,dl=(today+timedelta(days=s['day']+3)).strftime('%d %b %Y')))}"
    } for s in SEQ]

# ═══════════════════════════════════════════════════════════
# CSV PARSERS (unchanged from v1)
# ═══════════════════════════════════════════════════════════
def _cat(d):
    d=d.lower()
    if any(x in d for x in ["rent","rental"]):                    return "Rent"
    if any(x in d for x in ["praveen","porter","salary","wage"]): return "Salary"
    if any(x in d for x in ["laptop","computer","software"]):     return "Technology"
    if any(x in d for x in ["broad","internet","wifi"]):          return "Internet"
    if any(x in d for x in ["electricity","power","eb "]):        return "Electricity"
    if any(x in d for x in ["ca","accountant","audit"]):          return "Professional Fees"
    if any(x in d for x in ["website","domain"]):                 return "Website"
    if any(x in d for x in ["outing","travel","fuel","petrol"]):  return "Travel & Fuel"
    if any(x in d for x in ["raw","material","mfg","mim"]):       return "Raw Materials"
    if any(x in d for x in ["debit","bank","charge"]):            return "Bank Charges"
    if any(x in d for x in ["pack","packaging","box","carton"]):  return "Packaging"
    if any(x in d for x in ["logistics","courier","transport","freight"]): return "Logistics"
    return "Operations"

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
        df=dfs.dropna(how="all").dropna(axis=1,how="all")
        cm={}
        for col in df.columns:
            cl=str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day"]):                     cm[col]="Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","rs","₹"]): cm[col]="Amount"
            elif any(x in cl for x in ["type","txn","dr/cr","nature"]):       cm[col]="Type"
            elif any(x in cl for x in ["particulars","category","narration","ledger"]): cm[col]="Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client"]): cm[col]="Party"
            elif any(x in cl for x in ["status","paid","pending","overdue"]): cm[col]="Status"
            elif any(x in cl for x in ["invoice","voucher","ref","bill"]):    cm[col]="Invoice_No"
        df=df.rename(columns=cm)
        if "Date" not in df.columns: return None,False,"Date column not found."
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=True)
        df=df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"]=(df["Amount"].astype(str).str.replace(",","")
                .str.replace("(","−").str.replace(")","")
                .str.replace(" Dr","").str.replace(" Cr","").str.replace("₹",""))
            df["Amount"]=pd.to_numeric(df["Amount"],errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"]="Unknown"
        df["Type"]=df["Type"].astype(str).str.strip().str.title().replace(
            {"Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
             "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales"})
        mask=~df["Type"].isin(["Sales","Expense"])
        if mask.any():
            ekw=["purchase","expense","payment","salary","rent","bill","wages","material","raw","logistics"]
            df.loc[mask,"Type"]=df.loc[mask].apply(
                lambda x:"Expense" if any(k in str(x.get("Category","")).lower() for k in ekw) else "Sales",axis=1)
        for col,default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","-")]:
            if col not in df.columns: df[col]=default
        df["Month"]=df["Date"].dt.to_period("M").astype(str)
        return df,True,f"✅ {len(df):,} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"
    except Exception as e:
        return None,False,f"Error: {e}"

# ═══════════════════════════════════════════════════════════
# LEAK DETECTOR
# ═══════════════════════════════════════════════════════════
def find_leaks(df, industry, city=None):
    sales=df[df["Type"]=="Sales"]; expenses=df[df["Type"]=="Expense"]
    revenue=sales["Amount"].sum(); exp_tot=expenses["Amount"].sum()
    profit=revenue-exp_tot; margin=(profit/revenue*100) if revenue>0 else 0
    bmark=BENCH.get(industry,15); leaks=[]

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
            leaks.append({"id":"cash_stuck","sev":"critical","cat":"Collections","rupee":od_amt,"annual":od_amt*0.18,
                "headline":f"{fmtx(int(od_amt))} stuck in unpaid invoices","sub":f"Across {len(deb)} customers",
                "found":f"{len(deb)} customers owe you: {debtor_lines}",
                "costs":f"At 18% cost of capital, {fmt(od_amt)} locked away costs you {fmt(od_amt*0.18)} per year.",
                "bench":f"Healthy: overdue below 5% of revenue. Yours: {pct:.1f}%.",
                "action":f"Call {top_name} today. Offer 2% discount for 48-hr payment.",
                "action_sub":"Use the WhatsApp sequence below.","template":f"Hi, invoice of {fmt(top_amt)} is overdue. 2% off if paid today.","seqs":seqs})

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
                bench_line=(f"Market median: ₹{pdata['median']:,}{pdata['unit']} ({pdata['n']} peers)."
                            if pdata else "Get 3 quotes — typically 10–18% saving possible.")
                if waste>15000:
                    leaks.append({"id":"cost_bleed","sev":"warning","cat":"Vendor Costs","rupee":waste,"annual":waste,
                        "headline":f"{fmtx(int(waste))} overpaid on {category} per year","sub":f"{ev} charges {pct:.0f}% more than cheapest",
                        "found":f"You paid {ev} avg ₹{ep:,.0f} on {category}. Cheapest: ₹{cheapest:,.0f}. Gap: {pct:.0f}%.",
                        "costs":f"Annualised: {fmtx(int(waste))} extra per year.","bench":bench_line,
                        "action":f"Get 2 competing quotes for {category} by Friday.","action_sub":"Lowest quote gets the contract.",
                        "template":f"Reviewing {category} suppliers. Send best rate. Lowest quote by Friday gets 12-month contract.","seqs":[]})
                    break

    if margin<bmark-3:
        gap=((bmark-margin)/100)*revenue
        if gap>25000:
            leaks.append({"id":"margin_gap","sev":"critical" if margin<5 else "warning","cat":"Profitability","rupee":gap,"annual":gap,
                "headline":f"{fmtx(int(gap))} in margin left on the table","sub":f"Your margin {margin:.1f}% vs {bmark}% industry average",
                "found":f"Net margin: {margin:.1f}%. Benchmark for {industry}: {bmark}%. Gap: {bmark-margin:.1f} pp.",
                "costs":f"At {fmt(revenue)} revenue, closing half this gap adds {fmt(gap*0.5)} in net profit.",
                "bench":f"Benchmark: {bmark}% for {industry}.",
                "action":"Raise prices 5% on top 3 products. Cut 10% from largest expense.",
                "action_sub":f"Combined adds ~{fmt(gap*0.15)} in 90 days.",
                "template":"Reviewing pricing — room to increase 5–8%. Implementing from next invoice cycle.","seqs":[]})

    if len(sales)>0 and revenue>0:
        cr=sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100>28:
            top_pct=(cr.iloc[0]/revenue)*100; risk=cr.iloc[0]*0.3
            leaks.append({"id":"concentration","sev":"warning","cat":"Revenue Risk","rupee":risk,"annual":risk,
                "headline":f"{cr.index[0]} is {top_pct:.0f}% of your revenue","sub":"One client delay = cash crisis",
                "found":f"{cr.index[0]} = {top_pct:.0f}% ({fmtx(int(cr.iloc[0]))}). 30-day delay = {fmtx(int(cr.iloc[0]))} shortfall.",
                "costs":"Concentration above 25% gives that client full negotiating power.",
                "bench":"Healthy: no single client above 25%.","action":"Close 2 new clients this month.",
                "action_sub":"Set a 25% concentration cap target within 6 months.",
                "template":"Expanding client base — referral discount available.","seqs":[]})

    if len(expenses)>0:
        me=expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me)>=4:
            recent=me.iloc[-3:].mean(); prior=me.iloc[:-3].mean() if len(me)>3 else me.iloc[0]
            if prior>0 and recent>prior*1.18:
                spike=(recent-prior)*12
                if spike>20000:
                    leaks.append({"id":"exp_spike","sev":"warning","cat":"Cost Control","rupee":spike,"annual":spike,
                        "headline":f"Monthly costs up {((recent/prior-1)*100):.0f}% — {fmtx(int(spike))} annualised",
                        "sub":f"₹{(recent-prior)/1000:.0f}K more per month","found":f"Monthly expense: was {fmt(prior)}, now {fmt(recent)}. Extra: {fmt(recent-prior)}/month.",
                        "costs":"Rising costs without matching revenue = structural problem.",
                        "bench":"Expenses should track revenue.","action":"Freeze non-essential spend this week.",
                        "action_sub":"Every spend above ₹5K needs approval.","template":"Cost control initiative: paused non-essential expenses.","seqs":[]})

    elig=expenses[expenses["Amount"]>25000]
    if len(elig)>0:
        missed=elig["Amount"].sum()*0.18*0.09
        if missed>8000:
            leaks.append({"id":"tax_gst","sev":"info","cat":"Tax Recovery","rupee":missed,"annual":missed,
                "headline":f"~{fmtx(int(missed))} in GST input credits to verify","sub":"Estimated — needs CA confirmation",
                "found":f"Eligible purchases: {fmt(elig['Amount'].sum())}. ~9% unclaimed ITC.",
                "costs":"Money the government owes you.","bench":"Claim before next GST filing.",
                "action":"Ask your CA about Input Tax Credit on purchases above ₹25K.",
                "action_sub":"Recoverable within the same quarter.","template":"Want to review ITC eligibility. Can we schedule a call?","seqs":[]})

    return sorted(leaks, key=lambda x: x["rupee"], reverse=True)

def leaks_to_actions(leaks):
    """Convert leak findings into action tracker items"""
    actions = []
    for l in leaks:
        actions.append({
            "id": l["id"],
            "label": l["action"],
            "meta": l["headline"],
            "suggested_saving": l["rupee"],
            "actual_saving": l["rupee"],
            "status": "pending",
            "date_done": None,
        })
    return actions

# ═══════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════
defaults = {
    "df": None, "industry": "agency", "city": "Bangalore",
    "show_bot": False, "trial_clicked": False,
    "user_phone": "", "biz_name": "", "lead_captured": False,
    "actions": [], "monthly_fee": 2999, "months_active": 1,
    "show_tracker": False,
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ═══════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Profit Recovery Engine · Built for Indian SMEs · Bangalore</div>
  <h1 class="hero-h">We don't show data.<br><em>We increase your profit.</em></h1>
  <p class="hero-sub">Upload your Tally export. Get exact rupee leaks in 60 seconds. 
  Track every action. Prove every rupee saved. You pay only when you recover.</p>
  <div class="trust-row">
    <div class="trust-item"><div class="t-num">₹50Cr+</div><div class="t-lbl">Leaks found</div></div>
    <div class="trust-item"><div class="t-num">₹12.4L</div><div class="t-lbl">Avg recovery</div></div>
    <div class="trust-item"><div class="t-num">4.8 days</div><div class="t-lbl">To first rupee</div></div>
    <div class="trust-item"><div class="t-num">200+</div><div class="t-lbl">SMEs scanned</div></div>
  </div>
</div>
<div class="safety-bar">
  <div class="s-pill"><div class="s-dot"></div> Data processed securely, never stored</div>
  <div class="s-pill"><div class="s-dot"></div> No login needed for first scan</div>
  <div class="s-pill"><div class="s-dot"></div> Results in 60 seconds</div>
  <div class="s-pill"><div class="s-dot"></div> Trusted by CAs in Bangalore, Mumbai, Pune</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════
t1, t2, t3, t4 = st.tabs(["₹  Scan & Track", "📊  ROI Dashboard", "🏛  CA Partner", "🔖  Benchmarks"])

# ═══════════════════════════════════════════════════════════
# TAB 1 — SCAN & TRACK
# ═══════════════════════════════════════════════════════════
with t1:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    uc1, uc2, uc3 = st.columns([3,1,1])
    with uc1:
        uploaded = st.file_uploader("Upload Tally Day Book, Sales Register, or Bank Statement (CSV / Excel)", type=["csv","xlsx","xls"])
        with st.expander("How to export from Tally in 30 seconds"):
            st.markdown("""
**Tally Prime:** Display → Account Books → Day Book → Alt+E → Excel  
**Tally ERP 9:** Gateway → Display → Day Book → Ctrl+E → Excel  
**Bank:** Download CSV from net banking
            """)
    with uc2:
        ind_sel = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
        st.session_state.industry = INDUSTRY_MAP[ind_sel]
    with uc3:
        st.selectbox("City", ["Bangalore","Mumbai","Delhi","Pune","Chennai","Hyderabad","Ahmedabad","Surat","Other"], key="city")
        if st.button("▶  Try Demo Data", use_container_width=True):
            np.random.seed(42)
            dates = pd.date_range("2024-04-01","2025-03-31",freq="D")
            cats  = list({"Raw Materials":0.30,"Labor":0.20,"Rent":0.10,"Logistics":0.15,"Packaging":0.10,"Utilities":0.15}.keys())
            wts   = [0.30,0.20,0.10,0.15,0.10,0.15]
            recs  = []
            for d in dates:
                if np.random.random()>0.25:
                    recs.append({"Date":d,"Type":"Sales",
                        "Party":np.random.choice(DEMO_CUSTOMERS,p=[0.38,0.18,0.16,0.14,0.06,0.03,0.02,0.01,0.01,0.01]),
                        "Amount":np.random.uniform(60000,280000),
                        "Status":np.random.choice(["Paid","Paid","Overdue","Pending"],p=[0.55,0.25,0.12,0.08]),
                        "Category":"Sales"})
                for _ in range(np.random.randint(1,4)):
                    cat=np.random.choice(cats,p=wts)
                    recs.append({"Date":d,"Type":"Expense",
                        "Party":np.random.choice(DEMO_VENDORS),
                        "Amount":np.random.uniform(12000,90000),
                        "Status":"Paid","Category":cat})
            demo=pd.DataFrame(recs); demo["Month"]=demo["Date"].dt.to_period("M").astype(str)
            st.session_state.df=demo; st.session_state.industry="manufacturing"
            st.session_state.lead_captured=True; st.session_state.biz_name="Demo Business"
            st.session_state.actions=[]
            st.rerun()

    if uploaded:
        df_new,ok,msg=parse_file(uploaded)
        if ok:
            st.session_state.df=df_new; st.session_state.actions=[]
            st.success(msg)
        else:
            st.error(f"❌ {msg}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── LEAD GATE ────────────────────────────────────────────
    if st.session_state.df is not None and not st.session_state.lead_captured:
        st.markdown('<div class="sw">', unsafe_allow_html=True)
        st.markdown('<div class="gate-box"><div class="gate-h">Your scan is ready 🎯</div><div class="gate-s">Enter your WhatsApp number to see the full report.</div></div>', unsafe_allow_html=True)
        g1,g2,g3=st.columns([1,2,1])
        with g2:
            phone_in=st.text_input("WhatsApp number","",placeholder="9876543210")
            biz_in  =st.text_input("Business name","",placeholder="Sharma Enterprises")
            if st.button("Show my profit leaks →", type="primary", use_container_width=True):
                if phone_in.strip():
                    st.session_state.user_phone=phone_in.strip()
                    st.session_state.biz_name=biz_in.strip() or "Your Business"
                    st.session_state.lead_captured=True
                    st.rerun()
                else:
                    st.warning("Please enter your WhatsApp number.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ──────────────────────────────────────────────
    if st.session_state.df is not None and st.session_state.lead_captured:
        df=st.session_state.df; industry=st.session_state.industry
        city=st.session_state.city; biz_name=st.session_state.biz_name or "Your Business"
        sales=df[df["Type"]=="Sales"]; expenses=df[df["Type"]=="Expense"]
        revenue=sales["Amount"].sum(); exp_tot=expenses["Amount"].sum()
        profit=revenue-exp_tot; margin=(profit/revenue*100) if revenue>0 else 0
        bmark=BENCH.get(industry,15)
        leaks=find_leaks(df,industry,city)
        total_rupee=sum(l["rupee"] for l in leaks)
        overdue=(sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum()
                 if "Status" in sales.columns else 0)

        # Init actions if empty
        if not st.session_state.actions and leaks:
            st.session_state.actions = leaks_to_actions(leaks)

        st.markdown('<div class="sw">', unsafe_allow_html=True)

        # ── MONEY SAVED COUNTER (NEW - THE BIG ONE) ──────────
        render_money_saved_counter(st.session_state.actions, st.session_state.monthly_fee)

        # ── TOPLINE LEAK SUMMARY ──────────────────────────────
        coll_l=next((l for l in leaks if l["id"]=="cash_stuck"),None)
        vend_l=next((l for l in leaks if l["id"]=="cost_bleed"),None)
        tax_l =next((l for l in leaks if l["id"]=="tax_gst"),None)
        marg_l=next((l for l in leaks if l["id"]=="margin_gap"),None)

        acts=[]
        if coll_l: acts.append(f"Call top debtor today — recover {fmtx(int(coll_l['rupee']))} overdue")
        if vend_l: acts.append(f"Get 2 quotes for {vend_l['headline'].split('on ')[-1].split(' per')[0]} — save {fmt(vend_l['rupee'])}/yr")
        if tax_l:  acts.append(f"Email CA about ITC review — ~{fmtx(int(tax_l['rupee']))} claimable")
        if not acts and marg_l: acts.append(f"Raise prices 5% — adds {fmt(marg_l['rupee']*0.15)} in 90 days")

        act_html="".join(f'<div class="act-item"><div class="act-num">{i+1}</div><div class="act-text">{a}</div></div>' for i,a in enumerate(acts[:3]))
        coll_row=(f'<div class="ms-row r"><div class="ms-left"><span style="font-size:16px">🔴</span><div><div class="ms-title">Cash stuck in unpaid invoices</div><div class="ms-desc">Recoverable this month</div></div></div><div class="ms-amt">{fmtx(int(coll_l["rupee"]))}</div></div>' if coll_l else "")
        vend_row=(f'<div class="ms-row a"><div class="ms-left"><span style="font-size:16px">🟡</span><div><div class="ms-title">Vendor overpayment — annual saving</div><div class="ms-desc">Switch supplier</div></div></div><div class="ms-amt">{fmtx(int(vend_l["rupee"]))}/yr</div></div>' if vend_l else "")
        marg_row=(f'<div class="ms-row a"><div class="ms-left"><span style="font-size:16px">🟡</span><div><div class="ms-title">Margin gap vs industry peers</div><div class="ms-desc">Price + cost action</div></div></div><div class="ms-amt">{fmtx(int(marg_l["rupee"]))}/yr</div></div>' if marg_l else "")
        tax_row =(f'<div class="ms-row b"><div class="ms-left"><span style="font-size:16px">🔵</span><div><div class="ms-title">GST input credits — verify with CA</div><div class="ms-desc">Estimated</div></div></div><div class="ms-amt">~{fmtx(int(tax_l["rupee"]))}</div></div>' if tax_l else "")

        st.markdown(f'<div class="money-screen"><div class="ms-label">Leaks identified — {biz_name}</div><div class="ms-total">{fmt(total_rupee)}</div><div class="ms-sub">{len(leaks)} issues found · Annual impact: {fmt(sum(l["annual"] for l in leaks))}</div>{coll_row}{vend_row}{marg_row}{tax_row}<div class="act-box"><div class="act-lbl">Do these 3 things this week</div>{act_html}</div></div>', unsafe_allow_html=True)

        # ── KPI ROW ──────────────────────────────────────────
        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi-card"><div class="kpi-lbl">Revenue</div><div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales)} transactions</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Margin</div><div class="kpi-val">{margin:.1f}%</div><div class="kpi-sub {"good" if margin>=bmark else "bad"}">vs {bmark}% benchmark</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Overdue</div><div class="kpi-val">{fmt(overdue)}</div><div class="kpi-sub {"bad" if overdue>revenue*0.06 else "good"}">{(overdue/revenue*100 if revenue>0 else 0):.1f}% of revenue</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Profit</div><div class="kpi-val">{fmt(abs(profit))}</div><div class="kpi-sub {"good" if profit>0 else "bad"}">{"Profitable" if profit>0 else "Loss"}</div></div>'
            f'</div>', unsafe_allow_html=True)

        # ── ACTION TRACKER (NEW) ──────────────────────────────
        st.markdown("---")
        render_action_tracker(st.session_state.actions)

        # ── BEFORE / AFTER (NEW) ─────────────────────────────
        total_saved = sum(a.get("actual_saving", a["suggested_saving"])
                          for a in st.session_state.actions if a["status"]=="done")
        margin_improvement = (total_saved / revenue * 100) if revenue > 0 else 0
        done_od = sum(a.get("actual_saving",0) for a in st.session_state.actions
                      if a["status"]=="done" and a["id"]=="cash_stuck")
        done_vendor = sum(a.get("actual_saving",0)/12 for a in st.session_state.actions
                          if a["status"]=="done" and a["id"]=="cost_bleed")
        top_exp = expenses.groupby("Category")["Amount"].sum().max() if len(expenses)>0 else 0

        render_before_after(
            margin_before=margin,
            margin_after=margin + margin_improvement,
            revenue=revenue,
            overdue_before=overdue,
            overdue_after=max(0, overdue - done_od),
            top_expense_before=top_exp,
            top_expense_after=max(0, top_exp - done_vendor),
        )

        # ── LEAK DETAIL CARDS ────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="sh">Leak Details</div>', unsafe_allow_html=True)
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
                f'</div>', unsafe_allow_html=True)

            if leak["id"]=="cash_stuck" and leak.get("seqs"):
                if st.button("📱 WhatsApp collections sequence", key="bot"):
                    st.session_state.show_bot = not st.session_state.show_bot
                if st.session_state.show_bot:
                    for step in leak["seqs"]:
                        st.markdown(f'<div class="seq-card"><div class="seq-day">Day {step["day"]} · {step["send_on"]}</div><div class="seq-tone" style="color:{step["color"]}">{step["tone"]}</div><div class="seq-msg">{step["message"]}</div></div>', unsafe_allow_html=True)
                        st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:12px;color:#25D366">Open in WhatsApp →</a>', unsafe_allow_html=True)
            else:
                if st.button("📋 WhatsApp script", key=f"scr_{leak['id']}"):
                    st.code(leak["template"])

        # ── CHARTS ───────────────────────────────────────────
        st.markdown("---")
        tc1,tc2=st.columns(2)
        with tc1:
            st.markdown("**Revenue vs Expenses — monthly**")
            monthly=df.groupby([df["Date"].dt.to_period("M"),"Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly,height=200)
        with tc2:
            st.markdown("**Top Expense Categories**")
            if len(expenses)>0:
                st.bar_chart(expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8),height=200)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── PRICING ──────────────────────────────────────────
        st.markdown('<div class="pr-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.8rem;color:#F7F4EF;margin-bottom:4px;">How we work together</div>', unsafe_allow_html=True)
        pc1,pc2,pc3=st.columns(3)
        with pc1:
            st.markdown('<div class="pr-card"><div class="pr-lbl">Free scan</div><div class="pr-name">First audit</div><div class="pr-amt">₹0</div><div class="pr-note">Full leak scan, no strings.</div><div class="pr-feat">Full leak scan</div><div class="pr-feat">Exact rupee amounts</div><div class="pr-feat">Action tracker</div></div>', unsafe_allow_html=True)
        with pc2:
            st.markdown('<div class="pr-card feat"><div class="pr-lbl">Most chosen</div><div class="pr-name">Recovery Review</div><div class="pr-amt">₹2,999</div><div class="pr-note">60-min call. 30-day action plan. Full ROI tracking.</div><div class="pr-feat">Live call with founder</div><div class="pr-feat">Vendor quote sourcing</div><div class="pr-feat">Monthly ROI report</div><div class="pr-feat">CA coordination</div></div>', unsafe_allow_html=True)
        with pc3:
            st.markdown('<div class="pr-card"><div class="pr-lbl">For CA firms</div><div class="pr-name">Partner plan</div><div class="pr-amt">₹1,999/mo</div><div class="pr-note">Run for all clients. White-label. ₹500/client/month.</div><div class="pr-feat">50 client seats</div><div class="pr-feat">Branded reports</div><div class="pr-feat">Client ROI dashboard</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        b1,b2,b3=st.columns([1,2,1])
        with b2:
            if st.button("🚀 Book Recovery Review — ₹2,999", use_container_width=True, type="primary"):
                st.session_state.trial_clicked=True
        if st.session_state.trial_clicked:
            st.success("✅ We'll WhatsApp you within 2 hours.")
            st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=Hi%2C+want+to+book+Recovery+Review)")
            st.balloons()

# ═══════════════════════════════════════════════════════════
# TAB 2 — ROI DASHBOARD (NEW)
# ═══════════════════════════════════════════════════════════
with t2:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">ROI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">This is your proof. Every rupee suggested, tracked, and proven.</div>', unsafe_allow_html=True)

    if not st.session_state.actions:
        st.info("👆 Run a scan first (Tab 1) to see your ROI dashboard.")
    else:
        biz_name = st.session_state.biz_name or "Your Business"

        # Fee settings
        fc1,fc2=st.columns(2)
        with fc1:
            st.session_state.monthly_fee = st.number_input("Monthly fee paid (₹)", value=2999, step=500)
        with fc2:
            st.session_state.months_active = st.number_input("Months active", value=1, min_value=1, max_value=24)

        # ROI Report
        render_roi_report(
            st.session_state.actions,
            st.session_state.monthly_fee,
            biz_name,
            st.session_state.months_active
        )

        # Action tracker again for easy access
        st.markdown("---")
        render_action_tracker(st.session_state.actions, key_prefix="roi")

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 3 — CA PARTNER
# ═══════════════════════════════════════════════════════════
with t3:
    st.markdown('<div class="ca-wrap">', unsafe_allow_html=True)
    st.markdown('<div style="display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1rem">For Chartered Accountants</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:#1A1A1A;margin-bottom:.5rem">Your clients are losing money.<br>Show them exactly where — automatically.</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="ca-card" style="border-left:4px solid #D4AF37;background:#FFFBF0;">
  <div class="ca-lbl">Real Result · Bangalore</div>
  <div class="ca-ttl">"Found ₹18L in issues across 6 clients in one afternoon"</div>
  <div class="ca-body">A Bangalore CA ran OpsClarity on 6 client files after a demo meeting. 
  Found ₹18L in overdue receivables and vendor overpayments. One client recovered ₹6.2L 
  within 12 days using the WhatsApp collection sequence.
  <br><br><em>— CA firm, Indiranagar, Bangalore (name shared on request)</em></div>
</div>
""", unsafe_allow_html=True)

    n_ca=st.slider("Your client count",10,200,40,5)
    ca1,ca2=st.columns(2)
    with ca1:
        st.markdown('<div class="ca-card">', unsafe_allow_html=True)
        st.markdown('<div class="ca-lbl">The CA partner math</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ca-row"><div class="ca-row-lbl">Clients on OpsClarity</div><div class="ca-row-val">{n_ca}</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Your cost</div><div class="ca-row-val">₹1,999/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">You earn per client</div><div class="ca-row-val">₹500/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Monthly income</div><div class="ca-row-val hl">₹{n_ca*500:,}/month</div></div>'
            f'<div class="ca-row" style="border:none"><div class="ca-row-lbl">Net after cost</div><div class="ca-row-val hl">₹{n_ca*500-1999:,}/month</div></div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with ca2:
        st.markdown('<div class="ca-card"><div class="ca-lbl">What makes CAs stay</div><div class="ca-ttl">Monthly ROI proof per client</div><div class="ca-body">Every client gets a report showing: fee paid vs money saved. When a client sees they paid ₹999 and saved ₹45,000 — they never leave.<br><br>You become the CA who <strong>proves value in rupees</strong>, not just compliance.</div></div>', unsafe_allow_html=True)

    portfolio=[
        {"name":"Sharma Textiles Pvt Ltd","city":"Bangalore","ind":"textile","rev":4200000,"leak":840000,"saved":620000,"health":"red"},
        {"name":"Mehta Food Products","city":"Bangalore","ind":"restaurant","rev":2800000,"leak":196000,"saved":196000,"health":"green"},
        {"name":"Rajesh Diagnostics","city":"Bangalore","ind":"clinic","rev":6100000,"leak":91500,"saved":0,"health":"amber"},
        {"name":"Kapoor Engineering","city":"Bangalore","ind":"manufacturing","rev":8900000,"leak":1780000,"saved":890000,"health":"red"},
        {"name":"Green Pharma Dist.","city":"Bangalore","ind":"pharma","rev":3400000,"leak":238000,"saved":238000,"health":"green"},
        {"name":"Venkateswara Printers","city":"Bangalore","ind":"printing","rev":1900000,"leak":28500,"saved":0,"health":"amber"},
    ]
    total_pleak=sum(c["leak"] for c in portfolio)
    total_psaved=sum(c["saved"] for c in portfolio)

    dash_header=(
        f'<div class="ca-card dark">'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem">'
        f'<div><div class="ca-lbl">Clients</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#F7F4EF">{len(portfolio)}</div></div>'
        f'<div><div class="ca-lbl">Leaks found</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#D4AF37">{fmt(total_pleak)}</div></div>'
        f'<div><div class="ca-lbl">Actually saved</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#4CAF50">{fmt(total_psaved)}</div></div>'
        f'<div><div class="ca-lbl">Recovery rate</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.5rem;color:#D4AF37">{total_psaved/total_pleak*100:.0f}%</div></div>'
        f'</div><div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:.75rem">'
    )
    rows_html=""
    for c in portfolio:
        hl="🔴 Critical" if c["health"]=="red" else ("🟡 Watch" if c["health"]=="amber" else "🟢 Healthy")
        saved_pct=f"{c['saved']/c['leak']*100:.0f}% recovered" if c['saved']>0 else "actions pending"
        rows_html+=(
            f'<div class="cl-row">'
            f'<div><div class="cl-name">{c["name"]}</div><div class="cl-meta">{c["city"]} · {c["ind"].title()}</div></div>'
            f'<div style="text-align:right"><div class="cl-amt">{fmt(c["leak"])} found</div><div style="font-size:11px;color:#4CAF50">{fmt(c["saved"])} saved · {saved_pct}</div></div>'
            f'<div class="cl-h {c["health"]}">{hl}</div>'
            f'</div>'
        )
    st.markdown(dash_header+rows_html+'</div></div>', unsafe_allow_html=True)

    with st.expander("My clients won't share data with a third-party"): st.write("You upload — client never sees OpsClarity. Report comes branded as your firm's work.")
    with st.expander("How does the ROI report work?"): st.write("Each action taken by the client is logged with rupee impact. Monthly report shows: fee paid vs money saved. This is your retention weapon.")
    with st.expander("What if numbers are wrong?"): st.write("You verify before sharing. Your professional judgement is still the product. We surface the work, you do it.")
    with st.expander("Will this replace CAs?"): st.write("No. Every tax finding says 'verify with your CA'. We surface the work. You bill for it.")

    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Join CA Partner Program — free 30-day trial →", type="primary", use_container_width=True):
        st.success("✅ We'll WhatsApp you within 4 hours.")
        st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=Hi%2C+CA+Partner+Program)")
        st.balloons()

# ═══════════════════════════════════════════════════════════
# TAB 4 — BENCHMARKS
# ═══════════════════════════════════════════════════════════
with t4:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">Industry Benchmark Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Anonymised data from Indian SMEs. Used to validate every leak we flag.</div>', unsafe_allow_html=True)
    sel=st.selectbox("Industry",list(PEERS.keys()),key="bi")
    for cat,data in PEERS.get(sel,{}).items():
        with st.expander(f"{cat} — {data['n']} businesses"):
            b1,b2,b3,b4=st.columns(4)
            b1.metric("Best 25%",  f"₹{data['p25']:,}{data['unit']}")
            b2.metric("Median",    f"₹{data['median']:,}{data['unit']}")
            b3.metric("Top 25%",   f"₹{data['p75']:,}{data['unit']}")
            b4.metric("Peers",     str(data['n']))
            st.info(f"Switching from top-25% to best rate = **{((data['p75']-data['p25'])/data['p75']*100):.0f}% reduction** on {cat}.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div><div class="ft-brand">OpsClarity</div><div class="ft-legal">Profit Recovery Engine · Bangalore 🇮🇳</div></div>
  <div class="ft-legal">Management estimates only — not CA advice · Data processed securely, never stored</div>
</div>
<a href="https://wa.me/916362319163?text=Hi, question about OpsClarity" class="wa-btn" target="_blank">💬 Talk to founder</a>
""", unsafe_allow_html=True)
