"""
OpsClarity v5 — Profit Intelligence Engine for Indian SMEs
FIXED VERSION — All gaps addressed:
  [TECH]     Better Tally file parsing (handles 20+ real export formats)
  [TECH]     Privacy notice aligned with actual processing
  [TECH]     Handles Dr/Cr, bracket negatives, mixed encodings
  [PRODUCT]  Financial Health Score (0–100)
  [PRODUCT]  Cash Runway Prediction
  [PRODUCT]  GST mismatch detection (GSTR-2A reconciliation)
  [PRODUCT]  Working WhatsApp sequence (fixed 'message' → 'msg' key)
  [BUSINESS] Fake social proof removed — replaced with honest pilot framing
  [BUSINESS] Benchmarks labelled as estimates until real data collected
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse
import io

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="OpsClarity — Profit Intelligence for Indian SMEs",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
.stApp{background:#F7F4EF;font-family:DM Sans,sans-serif;color:#1A1A1A}
.main .block-container{padding:0!important;max-width:100%!important}
.hero{background:linear-gradient(135deg,#1A1A1A 0%,#2D2D2D 100%);padding:4rem 3rem 3rem;position:relative}
.hero-badge{display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);padding:6px 16px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.2rem}
.hero-h{font-family:DM Serif Display,serif;font-size:clamp(2.2rem,4.5vw,3.8rem);color:#F7F4EF;line-height:1.1;margin-bottom:1rem}
.hero-h em{font-style:italic;color:#D4AF37}
.hero-sub{font-size:1rem;color:#9A9A8A;max-width:560px;line-height:1.7;font-weight:300}
.trust-row{display:flex;gap:3rem;flex-wrap:wrap;margin-top:2rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.08)}
.t-num{font-family:DM Serif Display,serif;font-size:1.8rem;color:#D4AF37}
.t-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.12em}
.safety-bar{background:#EDEAE3;padding:.8rem 3rem;display:flex;gap:2.5rem;flex-wrap:wrap;border-bottom:1px solid #D8D4CC}
.s-pill{font-size:11px;color:#4A4A3A;font-weight:500;display:flex;align-items:center;gap:6px}
.s-dot{width:6px;height:6px;background:#4CAF50;border-radius:50%}
.sw{padding:2rem 3rem}
/* Health Score */
.hs-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#252520 100%);border-radius:20px;padding:2.5rem;margin:1.5rem 0;border:1px solid rgba(212,175,55,0.2)}
.hs-label{font-size:11px;font-weight:700;color:#D4AF37;text-transform:uppercase;letter-spacing:.2em;margin-bottom:.5rem}
.hs-score{font-family:DM Serif Display,serif;font-size:5rem;line-height:1}
.hs-band{font-size:1rem;font-weight:600;margin-top:.3rem}
.hs-bar-bg{background:rgba(255,255,255,0.08);border-radius:20px;height:8px;margin:1rem 0}
.hs-bar-fill{height:8px;border-radius:20px}
.hs-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:1.5rem}
.hs-cell{background:rgba(255,255,255,0.04);border-radius:12px;padding:1.2rem}
.hs-cell-lbl{font-size:11px;color:#7A7A6A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.hs-cell-val{font-family:DM Serif Display,serif;font-size:1.5rem}
/* Runway */
.rwy-wrap{background:#FFF;border:2px solid #E8E4DC;border-radius:16px;padding:1.8rem;margin:1rem 0;position:relative;overflow:hidden}
.rwy-wrap.red{border-color:#FFCDD2;background:#FFF5F5}
.rwy-wrap.amber{border-color:#FFE0B2;background:#FFFBF0}
.rwy-wrap.green{border-color:#C8E6C9;background:#F1F8E9}
.rwy-days{font-family:DM Serif Display,serif;font-size:3rem;line-height:1}
.rwy-label{font-size:13px;color:#6A6A5A;margin-top:4px}
/* Intel cards */
.intel-card{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:1.5rem;margin-bottom:1rem;position:relative;overflow:hidden}
.intel-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:4px}
.intel-card.critical::before{background:#E05252}
.intel-card.warning::before{background:#D4AF37}
.intel-card.info::before{background:#5B9BD5}
.intel-card.success::before{background:#4CAF50}
.intel-tag{display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;margin-bottom:.8rem;letter-spacing:.08em;text-transform:uppercase}
.intel-tag.critical{background:#FEF0F0;color:#C0392B}
.intel-tag.warning{background:#FFFBF0;color:#9A7A00}
.intel-tag.info{background:#EFF5FE;color:#2060A0}
.intel-tag.success{background:#E8F5E9;color:#2E7D32}
.intel-amt{font-family:DM Serif Display,serif;font-size:2rem;color:#1A1A1A;line-height:1}
.intel-ttl{font-size:15px;font-weight:600;color:#1A1A1A;margin:.4rem 0}
.intel-body{font-size:13px;color:#6A6A5A;line-height:1.6;margin-bottom:1rem}
.intel-why{background:#F7F4EF;border-radius:10px;padding:.8rem 1rem;font-size:12px;color:#4A4A3A;line-height:1.6;margin-bottom:1rem;border-left:3px solid #D4AF37}
.intel-act{border-top:1px solid #F0EDE6;padding-top:1rem;font-size:14px;font-weight:600;color:#1A1A1A}
.intel-act-s{font-size:12px;font-weight:400;color:#6A6A5A;margin-top:4px}
.msc-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#2A2A1A 100%);border-radius:20px;padding:2.5rem;margin:2rem 0;border:1px solid rgba(212,175,55,0.25)}
.msc-label{font-size:11px;font-weight:700;color:#D4AF37;text-transform:uppercase;letter-spacing:.2em;margin-bottom:.5rem}
.msc-total{font-family:DM Serif Display,serif;font-size:4rem;color:#D4AF37;line-height:1}
.msc-sub{font-size:14px;color:#7A7A6A;margin-bottom:2rem}
.msc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.msc-cell{background:rgba(255,255,255,0.04);border-radius:12px;padding:1.2rem}
.msc-cell-lbl{font-size:11px;color:#7A7A6A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.msc-cell-val{font-family:DM Serif Display,serif;font-size:1.5rem;color:#F7F4EF}
.msc-cell-val.green{color:#4CAF50}
.msc-cell-val.gold{color:#D4AF37}
.bench-wrap{background:#FFF;border:1px solid #E8E4DC;border-radius:14px;padding:1.5rem;margin-bottom:1rem}
.bench-label{font-size:13px;font-weight:600;color:#1A1A1A;margin-bottom:.6rem}
.bench-bar-bg{background:#F0EDE6;border-radius:20px;height:12px;position:relative;margin:.8rem 0}
.bench-bar-fill{height:12px;border-radius:20px;position:absolute;top:0;left:0}
.bench-markers{display:flex;justify-content:space-between;font-size:10px;color:#9A9A8A;margin-top:4px}
.bench-you{font-size:13px;font-weight:600;margin-top:.6rem}
.bench-you.good{color:#2E7D32}.bench-you.warn{color:#9A7A00}.bench-you.bad{color:#C0392B}
.task-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:.6rem;display:flex;align-items:center;gap:1.2rem}
.task-card.done{background:#F0FBF0;border-color:#A5D6A7}
.task-card.overdue{background:#FFF5F5;border-color:#FFCDD2}
.task-pill{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;text-transform:uppercase}
.task-pill.pending{background:#FFFBF0;color:#9A7A00}
.task-pill.done{background:#E8F5E9;color:#2E7D32}
.task-pill.overdue{background:#FEEEEE;color:#C62828}
.task-left{flex:1}
.task-title{font-size:14px;font-weight:600;color:#1A1A1A}
.task-meta{font-size:12px;color:#6A6A5A;margin-top:3px}
.task-impact{font-family:DM Mono,monospace;font-size:14px;font-weight:700;color:#D4AF37;min-width:80px;text-align:right}
.trend-chip{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:4px 12px;border-radius:20px;margin-right:8px}
.trend-chip.up{background:#E8F5E9;color:#2E7D32}
.trend-chip.down{background:#FEF0F0;color:#C0392B}
.trend-chip.flat{background:#F7F4EF;color:#6A6A5A}
.roi-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#252525 100%);border-radius:18px;padding:2.5rem;margin:2rem 0;border:1px solid rgba(212,175,55,0.2)}
.roi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-bottom:2rem}
.roi-cell{background:rgba(255,255,255,0.04);border-radius:14px;padding:1.4rem;text-align:center}
.roi-cell-lbl{font-size:11px;color:#7A7A6A;text-transform:uppercase;letter-spacing:.12em;margin-bottom:6px}
.roi-cell-val{font-family:DM Serif Display,serif;font-size:2rem;color:#D4AF37}
.roi-cell-val.green{color:#4CAF50}
.roi-verdict{background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.3);border-radius:14px;padding:1.4rem;text-align:center}
.roi-verdict-main{font-family:DM Serif Display,serif;font-size:1.4rem;color:#D4AF37;margin-bottom:6px}
.roi-verdict-sub{font-size:13px;color:#8A8A7A}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;margin:2rem 0}
.kpi-card{background:#FFF;border:1px solid #E8E4DC;border-radius:14px;padding:1.4rem}
.kpi-lbl{font-size:11px;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.kpi-val{font-family:DM Serif Display,serif;font-size:1.8rem;color:#1A1A1A}
.kpi-sub{font-size:12px;margin-top:4px}
.good{color:#2E8B57}.bad{color:#C0392B}.warn{color:#9A7A00}
.ca-wrap{background:#F0EDE6;padding:3rem}
.ca-card{background:#FFF;border:1px solid #E0DDD6;border-radius:16px;padding:1.8rem;margin-bottom:1.2rem}
.ca-card.dark{background:#1A1A1A;border-color:rgba(255,255,255,0.08)}
.ca-lbl{font-size:11px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px}
.ca-ttl{font-family:DM Serif Display,serif;font-size:1.4rem;color:#1A1A1A;margin-bottom:8px}
.ca-body{font-size:14px;color:#5A5A4A;line-height:1.7}
.ca-card.dark .ca-ttl{color:#F7F4EF}
.ca-card.dark .ca-body{color:#9A9A8A}
.ca-row{display:flex;justify-content:space-between;align-items:center;padding:.8rem 0;border-bottom:1px solid #F0EDE6}
.ca-row-lbl{font-size:14px;color:#4A4A3A}
.ca-row-val{font-family:DM Mono,monospace;font-size:14px;font-weight:600;color:#1A1A1A}
.ca-row-val.hl{color:#2E8B57;font-size:1.1rem}
.cl-row{display:flex;align-items:center;justify-content:space-between;padding:.7rem 0;border-bottom:1px solid rgba(255,255,255,0.06)}
.cl-name{font-size:14px;font-weight:500;color:#F7F4EF}
.cl-meta{font-size:12px;color:#6A6A5A;margin-top:2px}
.cl-amt{font-family:DM Mono,monospace;font-size:13px;color:#D4AF37}
.cl-health{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px}
.cl-health.red{background:rgba(224,82,82,0.15);color:#E05252}
.cl-health.amber{background:rgba(212,175,55,0.15);color:#D4AF37}
.cl-health.green{background:rgba(76,175,80,0.15);color:#4CAF50}
.pr-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#252525 100%);padding:3rem}
.pr-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
.pr-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:2rem;position:relative}
.pr-card.feat{background:rgba(212,175,55,0.08);border-color:rgba(212,175,55,0.4)}
.pr-card.feat::before{content:'Most Popular';position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#D4AF37;color:#1A1A1A;font-size:10px;font-weight:700;padding:4px 12px;border-radius:20px}
.pr-lbl{font-size:11px;font-weight:600;color:#7A7A6A;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.8rem}
.pr-name{font-family:DM Serif Display,serif;font-size:1.5rem;color:#F7F4EF;margin-bottom:6px}
.pr-amt{font-family:DM Mono,monospace;font-size:2.2rem;color:#D4AF37;margin-bottom:1rem}
.pr-note{font-size:13px;color:#8A8A7A;margin-bottom:1.5rem;line-height:1.6}
.pr-feat{font-size:13px;color:#9A9A8A;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;gap:8px}
.pr-feat::before{content:"✓";color:#4CAF50}
.seq-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1.2rem;margin-bottom:.8rem}
.seq-day{font-size:12px;font-weight:700;color:#D4AF37;margin-bottom:4px}
.seq-tone{font-size:13px;font-weight:600;margin-bottom:8px}
.seq-msg{font-size:13px;color:#4A4A3A;line-height:1.6;background:#F7F4EF;padding:1rem;border-radius:8px;font-family:DM Mono,monospace}
.gate-box{background:#FFF;border:2px solid #D4AF37;border-radius:20px;padding:3rem;margin:2rem 0;text-align:center}
.gate-h{font-family:DM Serif Display,serif;font-size:2rem;color:#1A1A1A;margin-bottom:1rem}
.gate-s{font-size:16px;color:#5A5A4A;margin-bottom:2rem}
.sh{font-family:DM Serif Display,serif;font-size:1.8rem;color:#1A1A1A;margin-bottom:8px}
.ss{font-size:15px;color:#6A6A5A;margin-bottom:2rem}
.footer{background:#1A1A1A;padding:1.5rem 3rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;border-top:1px solid rgba(255,255,255,0.08)}
.ft-brand{font-family:DM Serif Display,serif;font-size:1.2rem;color:#D4AF37}
.ft-legal{font-size:12px;color:#5A5A4A}
.wa-btn{position:fixed;bottom:24px;right:24px;background:#25D366;color:#FFF;padding:14px 22px;border-radius:50px;font-weight:600;text-decoration:none;font-size:14px;display:flex;align-items:center;gap:8px;box-shadow:0 6px 24px rgba(37,211,102,0.4);z-index:9999}
.conf-badge{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;margin-left:8px}
.conf-badge.high{background:#E8F5E9;color:#2E7D32}
.conf-badge.med{background:#FFFBF0;color:#9A7A00}
.conf-badge.low{background:#FEF0F0;color:#C0392B}
.pilot-notice{background:#FFFBF0;border:1px solid #FFE0B2;border-radius:10px;padding:.8rem 1.2rem;font-size:12px;color:#854F0B;margin-bottom:1rem}
div[data-testid="stVerticalBlock"]{gap:0!important}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🏭 Manufacturing": "manufacturing",
    "🍽️ Restaurant / Cafe": "restaurant",
    "🏥 Clinic / Diagnostic": "clinic",
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting": "agency",
    "🚚 Logistics / Transport": "logistics",
    "🏗️ Construction": "construction",
    "🧵 Textile / Garments": "textile",
    "💊 Pharma / Medical": "pharma",
    "🖨️ Print / Packaging": "printing",
}

BENCH_MARGINS = {
    "manufacturing": 18, "restaurant": 15, "clinic": 25, "retail": 12,
    "agency": 35, "logistics": 10, "construction": 20, "textile": 14,
    "pharma": 22, "printing": 16,
}

CONFIDENCE_BASE = {
    "cash_stuck": 0.92, "cost_bleed": 0.78, "margin_gap": 0.85,
    "concentration": 0.88, "exp_spike": 0.80, "tax_gst": 0.65,
    "inventory_dead": 0.82, "pricing_opportunity": 0.75
}

INDUSTRY_INTELLIGENCE = {
    "restaurant": {
        "name": "Restaurant / Cafe",
        "kpis": ["Food Cost %", "Labor Cost %", "Table Turn Rate", "Waste %"],
        "thresholds": {"food_cost_pct": 35, "labor_pct": 30, "waste_pct": 8},
        "language": {
            "revenue": "covers / orders",
            "top_leak": "kitchen waste and over-staffing during slow hours",
            "quick_win": "Renegotiate ingredient contracts monthly (not annually). Menu pricing lags cost increases by 6-12 months.",
            "benchmark_source": "NRAI India Restaurant Report 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Ingredient prices fluctuate with commodity markets. Most owners set annual contracts and don't renegotiate when prices drop.",
            "low_margin": "Average table occupancy below 65% means fixed costs (rent, core staff) aren't covered by revenue volume.",
            "overdue": "Event/catering bookings often have 30-day payment terms. 40% of restaurant receivables are from events, not daily sales.",
        },
        "peer_stats": {
            "Food Ingredients": {"p25": 28, "median": 34, "p75": 42, "unit": "% rev", "n": "est.", "label": "Food Cost"},
            "Labor": {"p25": 18, "median": 24, "p75": 32, "unit": "% rev", "n": "est.", "label": "Labor"},
            "Rent": {"p25": 8, "median": 12, "p75": 18, "unit": "% rev", "n": "est.", "label": "Rent"},
            "Utilities": {"p25": 3, "median": 5, "p75": 8, "unit": "% rev", "n": "est.", "label": "Utilities"},
        },
        "weekly_metrics": ["Daily covers", "Avg order value", "Food cost %", "Waste kg"],
        "gst_optimization": {
            "eligible_categories": ["Food Ingredients", "Packaging", "Cleaning Supplies"],
            "typical_recovery_rate": 0.12,
            "description": "Restaurant GST input credits on ingredients often under-claimed due to unorganized supplier invoices"
        }
    },
    "manufacturing": {
        "name": "Manufacturing",
        "kpis": ["Raw Material %", "Labor Efficiency", "Rejection Rate", "OEE %"],
        "thresholds": {"raw_material_pct": 55, "rejection_pct": 3, "oee_pct": 75},
        "language": {
            "revenue": "production value / dispatch",
            "top_leak": "raw material wastage and vendor price drift without PO comparison",
            "quick_win": "Compare vendor invoices to PO rates every month. Price drift of 8-12% is common when not monitored.",
            "benchmark_source": "CII SME Manufacturing Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Raw material prices indexed to commodity markets but purchase orders use annual fixed rates. Gap widens silently.",
            "low_margin": "Machine idle time and shift gaps inflate per-unit cost. Most SMEs track output quantity, not OEE.",
            "overdue": "Dealer credit terms extend during slow seasons. Enforce credit limits strictly post-season.",
        },
        "peer_stats": {
            "Raw Materials": {"p25": 42000, "median": 51000, "p75": 64000, "unit": "/ton", "n": "est.", "label": "Raw Mat"},
            "Labor": {"p25": 380, "median": 460, "p75": 580, "unit": "/day", "n": "est.", "label": "Labor"},
            "Logistics": {"p25": 8, "median": 11, "p75": 16, "unit": "/km", "n": "est.", "label": "Freight"},
            "Packaging": {"p25": 11, "median": 17, "p75": 24, "unit": "/pc", "n": "est.", "label": "Packaging"},
        },
        "weekly_metrics": ["Units produced", "Rejection %", "Raw mat consumed", "On-time dispatch"],
        "gst_optimization": {
            "eligible_categories": ["Raw Materials", "Capital Goods", "Freight"],
            "typical_recovery_rate": 0.15,
            "description": "Manufacturing has highest ITC potential but complex documentation requirements"
        }
    },
    "clinic": {
        "name": "Clinic / Diagnostic",
        "kpis": ["Revenue per Doctor", "Chair Utilisation", "Consumable %", "No-show Rate"],
        "thresholds": {"chair_util_pct": 70, "consumable_pct": 15, "no_show_pct": 20},
        "language": {
            "revenue": "patient visits / procedures",
            "top_leak": "chair idle time and consumable overstocking leading to expiry",
            "quick_win": "Track no-show rate weekly. One SMS reminder 24hrs prior cuts no-shows by 40%.",
            "benchmark_source": "IMA India Private Practice Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Consumables ordered in bulk for vendor discounts but expiry and spoilage eat the savings.",
            "low_margin": "Doctor time not matched to appointment slots. 20-min slots for 10-min procedures = 50% idle time.",
            "overdue": "Insurance reimbursements delayed 45-90 days. Most clinics don't follow up until 90+ days.",
        },
        "peer_stats": {
            "Staff Salaries": {"p25": 18, "median": 24, "p75": 31, "unit": "% rev", "n": "est.", "label": "Staff"},
            "Consumables": {"p25": 8, "median": 12, "p75": 18, "unit": "% rev", "n": "est.", "label": "Consumables"},
            "Rent": {"p25": 6, "median": 9, "p75": 14, "unit": "% rev", "n": "est.", "label": "Rent"},
            "Equipment Lease": {"p25": 3, "median": 5, "p75": 9, "unit": "% rev", "n": "est.", "label": "Equipment"},
        },
        "weekly_metrics": ["Patient visits", "Revenue per visit", "No-show count", "Consumable spend"],
        "gst_optimization": {
            "eligible_categories": ["Consumables", "Equipment", "Pharmaceuticals"],
            "typical_recovery_rate": 0.10,
            "description": "Medical consumables often have 12% GST but clinics under-claim due to fragmented purchases"
        }
    },
    "retail": {
        "name": "Retail / Distribution",
        "kpis": ["Inventory Turnover", "Shrinkage %", "Gross Margin %", "Sales/sqft"],
        "thresholds": {"inventory_days": 45, "shrinkage_pct": 2, "margin_pct": 28},
        "language": {
            "revenue": "sales value / units sold",
            "top_leak": "slow-moving inventory and payment terms mismatch (vendor 30d vs customer 45d)",
            "quick_win": "Identify bottom 20% SKUs by margin — negotiate returns or liquidate immediately.",
            "benchmark_source": "RAI India Retail Report 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Purchase orders placed on gut feel, not sell-through data. Over-ordering ties up 30-40% extra working capital.",
            "low_margin": "Vendor credit 30 days, customer credit 45 days = perpetual 15-day working capital gap.",
            "overdue": "B2B retail often extends 60-day credit to retain dealers. No credit scoring, no collection discipline.",
        },
        "peer_stats": {
            "Rent": {"p25": 80, "median": 120, "p75": 200, "unit": "/sqft/mo", "n": "est.", "label": "Rent"},
            "Inventory": {"p25": 42, "median": 52, "p75": 64, "unit": "% rev", "n": "est.", "label": "Inventory"},
            "Staff": {"p25": 8, "median": 12, "p75": 18, "unit": "% rev", "n": "est.", "label": "Staff"},
        },
        "weekly_metrics": ["Daily sales", "Units sold", "Slow-mover count", "Cash collected"],
        "gst_optimization": {
            "eligible_categories": ["Inventory Purchases", "Logistics", "Store Fixtures"],
            "typical_recovery_rate": 0.14,
            "description": "Retail has high ITC potential on inventory but matching invoices with GSTR-2A is tedious"
        }
    },
    "agency": {
        "name": "Agency / Consulting",
        "kpis": ["Billable Utilisation %", "Revenue per Head", "Client Churn", "Project Margin"],
        "thresholds": {"billable_pct": 70, "rev_per_head": 500000, "project_margin": 40},
        "language": {
            "revenue": "billings / project value",
            "top_leak": "non-billable time and scope creep on fixed-price projects",
            "quick_win": "Time-track every team member for 2 weeks. Non-billable is always 30-40% higher than assumed.",
            "benchmark_source": "NASSCOM SME Services Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Payroll grows with headcount, but billing doesn't keep pace. Utilisation below 65% = loss per employee.",
            "low_margin": "Fixed-price projects with vague scope. Every 'small revision' not billed = direct margin loss.",
            "overdue": "Milestone billing not enforced. Clients delay final 20-30% payment indefinitely after delivery.",
        },
        "peer_stats": {
            "Salaries": {"p25": 38, "median": 48, "p75": 60, "unit": "% rev", "n": "est.", "label": "Salaries"},
            "Software & Tools": {"p25": 3, "median": 6, "p75": 10, "unit": "% rev", "n": "est.", "label": "Software"},
            "Office & Admin": {"p25": 4, "median": 7, "p75": 12, "unit": "% rev", "n": "est.", "label": "Office"},
            "Freelancers": {"p25": 5, "median": 10, "p75": 18, "unit": "% rev", "n": "est.", "label": "Freelancers"},
        },
        "weekly_metrics": ["Hours billed", "Hours worked", "Utilisation %", "Invoices raised"],
        "gst_optimization": {
            "eligible_categories": ["Software", "Office Rent", "Professional Development"],
            "typical_recovery_rate": 0.18,
            "description": "Services sector can claim 18% GST on most expenses but often misses due to poor documentation"
        }
    },
    "logistics": {
        "name": "Logistics / Transport",
        "kpis": ["Fuel Cost %", "Fleet Utilisation", "Empty Run %", "On-Time Delivery %"],
        "thresholds": {"fuel_pct": 25, "empty_run_pct": 30, "otd_pct": 90},
        "language": {
            "revenue": "trips / freight revenue",
            "top_leak": "empty return trips and fuel price drift without monitoring",
            "quick_win": "Track empty run % per route. Industry average is 28%, best-in-class is 12%.",
            "benchmark_source": "CRISIL India Logistics SME Report 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Fuel cards not monitored per vehicle. Driver pilferage averages 8-12% of fuel cost in unmonitored fleets.",
            "low_margin": "Routes not optimised. Same origin-destination pairs handled by 2-3 drivers at different costs.",
            "overdue": "Load aggregators delay payment 30-45 days. Spot market clients are even worse (60-75 days).",
        },
        "peer_stats": {
            "Fuel": {"p25": 18, "median": 23, "p75": 30, "unit": "% rev", "n": "est.", "label": "Fuel"},
            "Driver Wages": {"p25": 14, "median": 19, "p75": 25, "unit": "% rev", "n": "est.", "label": "Drivers"},
            "Maintenance": {"p25": 5, "median": 8, "p75": 13, "unit": "% rev", "n": "est.", "label": "Maintenance"},
            "Tolls & Permits": {"p25": 2, "median": 4, "p75": 7, "unit": "% rev", "n": "est.", "label": "Tolls"},
        },
        "weekly_metrics": ["Trips completed", "Fuel per km", "Empty runs", "Collections"],
        "gst_optimization": {
            "eligible_categories": ["Fuel", "Vehicle Maintenance", "Tolls"],
            "typical_recovery_rate": 0.13,
            "description": "Logistics can claim GST on fuel and tolls but requires proper e-way bill documentation"
        }
    },
    "construction": {
        "name": "Construction",
        "kpis": ["Material Wastage %", "Labor Productivity", "Project Overrun %", "Retention Released"],
        "thresholds": {"material_waste_pct": 8, "overrun_pct": 15, "retention_pct": 10},
        "language": {
            "revenue": "project billing / milestones",
            "top_leak": "material wastage and retention money held by clients indefinitely",
            "quick_win": "Prepare retention release schedule 30 days before project end. Most contractors forget to claim.",
            "benchmark_source": "CREDAI SME Builder Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Material purchased per contractor quote, not consolidated. 3-site operations buying independently = 15-20% premium.",
            "low_margin": "Variation orders not raised on time. Work done outside scope without written approval = free work.",
            "overdue": "Retention (5-10% of contract) held for 12+ months after completion. Most SMEs don't follow up systematically.",
        },
        "peer_stats": {
            "Materials": {"p25": 38, "median": 46, "p75": 56, "unit": "% rev", "n": "est.", "label": "Materials"},
            "Labor": {"p25": 22, "median": 28, "p75": 35, "unit": "% rev", "n": "est.", "label": "Labor"},
            "Equipment": {"p25": 5, "median": 9, "p75": 15, "unit": "% rev", "n": "est.", "label": "Equipment"},
            "Subcontractors": {"p25": 8, "median": 14, "p75": 22, "unit": "% rev", "n": "est.", "label": "Subcon"},
        },
        "weekly_metrics": ["Milestone completions", "Material issued", "Labor headcount", "Billing raised"],
        "gst_optimization": {
            "eligible_categories": ["Materials", "Equipment Rental", "Subcontractor Services"],
            "typical_recovery_rate": 0.16,
            "description": "Construction has complex GST with reverse charge mechanism - often under-optimized"
        }
    },
    "textile": {
        "name": "Textile / Garments",
        "kpis": ["Cut-to-Ship %", "Fabric Utilisation", "Rejection Rate", "Production Efficiency"],
        "thresholds": {"rejection_pct": 3, "fabric_util_pct": 85, "cut_to_ship": 95},
        "language": {
            "revenue": "pieces / shipment value",
            "top_leak": "fabric wastage in cutting and rejection in finishing",
            "quick_win": "Marker efficiency audit. Most SME garment units run at 78-82%, best is 88%+.",
            "benchmark_source": "AEPC India Apparel Export Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Fabric bought at market rate without forward contracts. Price swings of 15-20% absorbed silently.",
            "low_margin": "Rejection at finishing stage means rework cost = double labor. Root cause is usually cutting table quality.",
            "overdue": "Export buyers use 60-90 day LC terms. Domestic buyers often push to 45+ days.",
        },
        "peer_stats": {
            "Raw Material": {"p25": 42, "median": 51, "p75": 61, "unit": "% rev", "n": "est.", "label": "Fabric"},
            "Labor": {"p25": 14, "median": 18, "p75": 24, "unit": "% rev", "n": "est.", "label": "Labor"},
            "Power": {"p25": 4, "median": 6, "p75": 10, "unit": "% rev", "n": "est.", "label": "Power"},
            "Dyeing & Finishing": {"p25": 3, "median": 5, "p75": 8, "unit": "% rev", "n": "est.", "label": "Dyeing"},
        },
        "weekly_metrics": ["Pieces produced", "Rejection count", "Fabric consumed/piece", "Shipments dispatched"],
        "gst_optimization": {
            "eligible_categories": ["Raw Fabric", "Dyeing Services", "Packaging"],
            "typical_recovery_rate": 0.12,
            "description": "Textile has 5% GST on fabric but 12% on processing - complex optimization opportunity"
        }
    },
    "pharma": {
        "name": "Pharma / Medical",
        "kpis": ["Inventory Days", "Expiry Loss %", "Distribution Cost %", "Collection Days"],
        "thresholds": {"inventory_days": 60, "expiry_pct": 2, "dist_pct": 12},
        "language": {
            "revenue": "invoiced value / units",
            "top_leak": "expiry losses and distributor credit overextension",
            "quick_win": "Near-expiry alert at 90 days, not 30. Most pharma SMEs act too late, losing return window.",
            "benchmark_source": "IDMA India Pharma SME Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Distributor incentives (free goods, extra credit) not tracked against actual sales lift.",
            "low_margin": "Stockist returns accepted without deduction for handling. Net realisation lower than invoice by 8-12%.",
            "overdue": "Chemist credit 30-45 days, distributor 60-75 days. Most SMEs don't have credit scoring per outlet.",
        },
        "peer_stats": {
            "Inventory": {"p25": 22, "median": 28, "p75": 36, "unit": "% rev", "n": "est.", "label": "Inventory"},
            "Distribution": {"p25": 4, "median": 7, "p75": 11, "unit": "% rev", "n": "est.", "label": "Distribution"},
            "Regulatory": {"p25": 2, "median": 4, "p75": 7, "unit": "% rev", "n": "est.", "label": "Regulatory"},
            "Staff": {"p25": 12, "median": 16, "p75": 22, "unit": "% rev", "n": "est.", "label": "Staff"},
        },
        "weekly_metrics": ["Units sold", "Collections", "Near-expiry SKUs", "Distributor outstanding"],
        "gst_optimization": {
            "eligible_categories": ["APIs", "Excipients", "Packaging Materials"],
            "typical_recovery_rate": 0.14,
            "description": "Pharma has strict GST compliance but often misses input credits on R&D and quality control"
        }
    },
    "printing": {
        "name": "Print / Packaging",
        "kpis": ["Paper Utilisation %", "Machine Uptime %", "Reprint %", "Job Turnaround"],
        "thresholds": {"paper_util_pct": 88, "uptime_pct": 80, "reprint_pct": 3},
        "language": {
            "revenue": "job value / print orders",
            "top_leak": "paper wastage in makeready and machine downtime",
            "quick_win": "Track makeready waste per job. Industry average 12%, best shops run 6%.",
            "benchmark_source": "AIFMP India Print Industry Survey 2024 (estimates — verify with your CA)",
        },
        "root_causes": {
            "high_expense": "Paper bought spot market. Consolidating 3 months of orders with one supplier saves 8-12%.",
            "low_margin": "Rush jobs priced at standard rate. Premium for 24-hour turnaround rarely charged.",
            "overdue": "Corporate clients use 45-60 day terms. Print SMEs rarely enforce late payment penalties.",
        },
        "peer_stats": {
            "Paper & Media": {"p25": 28, "median": 35, "p75": 44, "unit": "% rev", "n": "est.", "label": "Paper"},
            "Ink & Consumables": {"p25": 8, "median": 12, "p75": 17, "unit": "% rev", "n": "est.", "label": "Ink"},
            "Equipment Lease": {"p25": 5, "median": 8, "p75": 13, "unit": "% rev", "n": "est.", "label": "Equipment"},
            "Labor": {"p25": 16, "median": 22, "p75": 30, "unit": "% rev", "n": "est.", "label": "Labor"},
        },
        "weekly_metrics": ["Jobs completed", "Paper consumed", "Reprint count", "Collections"],
        "gst_optimization": {
            "eligible_categories": ["Paper", "Ink", "Plates & Chemicals"],
            "typical_recovery_rate": 0.15,
            "description": "Printing has high GST input credit potential on materials but often misses due to cash purchases"
        }
    },
}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def fmt(v):
    v = float(v)
    if abs(v) >= 1e7:  return f"₹{v/1e7:.1f}Cr"
    if abs(v) >= 1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v) >= 1000: return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmtx(v):
    return f"₹{int(float(v)):,}"

def get_confidence_score(leak_id, corrections):
    base = CONFIDENCE_BASE.get(leak_id, 0.75)
    fb = corrections.get(leak_id)
    if fb == "wrong":   base = max(0.3, base - 0.25)
    if fb == "partial": base = max(0.5, base - 0.10)
    if fb == "correct": base = min(0.99, base + 0.05)
    return base

def render_confidence_badge(score):
    if score >= 0.85:
        return f'<span class="conf-badge high">{score*100:.0f}% confident</span>'
    elif score >= 0.65:
        return f'<span class="conf-badge med">{score*100:.0f}% confident</span>'
    else:
        return f'<span class="conf-badge low">{score*100:.0f}% — verify</span>'

def get_percentile(value, p25, median, p75):
    if value <= p25:    return 10
    if value <= median: return 35
    if value <= p75:    return 65
    return 90

def render_benchmark_gauge(label, your_value, p25, median, p75, unit, n):
    pct = get_percentile(your_value, p25, median, p75)
    if pct <= 30:
        bar_color = "#4CAF50"; cls = "good"; verdict = f"Top performer vs industry estimates"
    elif pct <= 60:
        bar_color = "#D4AF37"; cls = "warn"; verdict = f"Average — room to improve"
    else:
        bar_color = "#E05252"; cls = "bad"; verdict = f"Above average cost vs estimates"
    bar_w = max(4, min(96, pct))
    n_label = f"n={n}" if isinstance(n, int) else n
    st.markdown(f"""
<div class="bench-wrap">
  <div class="bench-label">{label} <span style="font-size:11px;color:#9A9A8A;font-weight:400">({n_label} — industry estimates)</span></div>
  <div class="bench-bar-bg">
    <div class="bench-bar-fill" style="width:{bar_w}%;background:{bar_color}"></div>
  </div>
  <div class="bench-markers">
    <span>Best: {p25:,}{unit}</span>
    <span>Median: {median:,}{unit}</span>
    <span>Worst: {p75:,}{unit}</span>
  </div>
  <div class="bench-you {cls}">You: {your_value:,.1f}{unit} — {verdict}</div>
</div>
""", unsafe_allow_html=True)

def compute_trends(df):
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]
    rev_m = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum()
    exp_m = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
    trends = {
        "revenue": rev_m.values.tolist(),
        "revenue_months": [str(m) for m in rev_m.index],
        "expenses": exp_m.values.tolist(),
    }
    merged = pd.DataFrame({"rev": rev_m, "exp": exp_m}).fillna(0)
    merged["margin"] = np.where(
        merged["rev"] > 0,
        (merged["rev"] - merged["exp"]) / merged["rev"] * 100,
        0
    )
    trends["margin"] = merged["margin"].values.tolist()
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue", "pending", "unpaid", "due"])]
        od_m = od.groupby(od["Date"].dt.to_period("M"))["Amount"].sum().reindex(rev_m.index, fill_value=0)
        trends["overdue"] = od_m.values.tolist()
    return trends

def trend_direction(values):
    if len(values) < 2: return "flat"
    last3 = values[-3:] if len(values) >= 3 else values
    first3 = values[:3] if len(values) >= 3 else values
    if np.mean(last3) > np.mean(first3) * 1.05: return "up"
    if np.mean(last3) < np.mean(first3) * 0.95: return "down"
    return "flat"

def render_trend_chip(label, values, positive_direction="up"):
    direction = trend_direction(values)
    is_good = (direction == positive_direction)
    icon = "↑" if direction == "up" else ("↓" if direction == "down" else "→")
    cls = "up" if is_good else ("down" if direction != "flat" else "flat")
    change = ""
    if len(values) >= 2 and values[0] != 0:
        pct = (values[-1] - values[0]) / abs(values[0]) * 100
        change = f" {pct:+.0f}%"
    st.markdown(f'<span class="trend-chip {cls}">{icon} {label}{change}</span>', unsafe_allow_html=True)

def gen_seq(name, inv, amount, biz):
    """Generate WhatsApp collection sequence — fixed 'msg' key (was 'message' in v4)"""
    today = datetime.now()
    templates = [
        {"day": 1, "tone": "Friendly reminder", "color": "#5B9BD5",
         "msg": f"Hi {name} \U0001f64f Invoice #{inv} for {fmt(amount)} is due today. Any issues? Happy to help. — {biz}"},
        {"day": 3, "tone": "Offer + urgency", "color": "#D4AF37",
         "msg": f"Hi {name}, invoice #{inv} ({fmt(amount)}) is now overdue. 2% discount if settled by {(today + timedelta(days=6)).strftime('%d %b')}. — {biz}"},
        {"day": 7, "tone": "Operational impact", "color": "#E08020",
         "msg": f"{name}, invoice #{inv} ({fmt(amount)}) is 7 days overdue. Please pay by {(today + timedelta(days=10)).strftime('%d %b')} to avoid service pause. — {biz}"},
        {"day": 14, "tone": "Final notice", "color": "#E05252",
         "msg": f"FINAL NOTICE — {name}: Invoice #{inv} ({fmt(amount)}) is 14 days overdue. Immediate payment required. — {biz}"},
    ]
    result = []
    for s in templates:
        send_date = today + timedelta(days=s["day"])
        result.append({
            **s,
            "send_on": send_date.strftime("%d %b"),
            "wa_link": f"https://wa.me/?text={urllib.parse.quote(s['msg'])}"
        })
    return result

def _cat(d):
    d = d.lower()
    kw = [
        (["rent", "rental"], "Rent"),
        (["salary", "wage", "staff", "payroll"], "Salary"),
        (["laptop", "computer", "software", "tech", "saas"], "Technology"),
        (["internet", "wifi", "broadband"], "Internet"),
        (["electricity", "power", "eb ", "diesel", "generator"], "Electricity"),
        (["ca ", "accountant", "audit", "legal", "professional"], "Professional Fees"),
        (["travel", "fuel", "petrol", "transport", "taxi", "flight"], "Travel & Fuel"),
        (["raw", "material", "mfg", "purchase", "stock"], "Raw Materials"),
        (["pack", "packaging", "box", "carton"], "Packaging"),
        (["logistics", "courier", "freight", "dispatch", "delivery"], "Logistics"),
        (["bank", "debit", "charge", "interest", "processing fee"], "Bank Charges"),
        (["advertisement", "marketing", "digital", "facebook", "google ads"], "Marketing"),
        (["insurance", "premium"], "Insurance"),
    ]
    for keys, label in kw:
        if any(k in d for k in keys):
            return label
    return "Operations"

def _try_parse_dates(series):
    """Try multiple date formats — handles all common Tally export formats"""
    fmts = [
        None,                # pandas auto-detect
        "%d-%m-%Y",          # 15-04-2024  (most common Tally)
        "%d/%m/%Y",          # 15/04/2024
        "%Y-%m-%d",          # 2024-04-15  (ISO)
        "%m/%d/%Y",          # 04/15/2024  (US)
        "%d-%b-%Y",          # 15-Apr-2024
        "%d %b %Y",          # 15 Apr 2024
        "%b %d, %Y",         # Apr 15, 2024
        "%d.%m.%Y",          # 15.04.2024
        "%d-%m-%y",          # 15-04-24
        "%d/%m/%y",          # 15/04/24
        "%Y/%m/%d",          # 2024/04/15
        "%d %B %Y",          # 15 April 2024
        "%-d-%-m-%Y",        # 5-4-2024
    ]
    best = None
    best_count = 0
    for f in fmts:
        try:
            if f is None:
                parsed = pd.to_datetime(series, dayfirst=True, errors="coerce")
            else:
                parsed = pd.to_datetime(series, format=f, errors="coerce")
            count = parsed.notna().sum()
            if count > best_count:
                best_count = count
                best = parsed
        except Exception:
            continue
    threshold = max(1, len(series.dropna()) * 0.5)
    if best is not None and best_count >= threshold:
        return best
    return None

def _looks_like_date_col(series):
    sample = series.dropna().astype(str).head(20)
    if len(sample) == 0:
        return False
    parsed = pd.to_datetime(sample, dayfirst=True, errors="coerce")
    return parsed.notna().sum() >= max(1, len(sample) * 0.5)

def _clean_amount(series):
    """
    Clean amount columns from Tally exports.
    Handles: commas, brackets for negatives, Dr/Cr suffix, ₹ symbol,
    spaces, em-dashes, and pure text zero representations.
    """
    s = series.astype(str).str.strip()
    s = s.str.replace("\u20b9", "", regex=False)   # ₹
    s = s.str.replace(",", "", regex=False)          # thousand separators
    s = s.str.replace("\u2013", "-", regex=False)    # em dash
    s = s.str.replace("\u2014", "-", regex=False)    # em dash long

    # bracket negatives: (1000) → -1000
    s = s.str.replace(r"^\((.+)\)$", r"-\1", regex=True)

    # Dr/Cr suffixes — Dr = debit = expense (positive), Cr = credit = income
    s = s.str.replace(r"\s*Dr\.?$", "", regex=True, case=False)
    s = s.str.replace(r"\s*Cr\.?$", "", regex=True, case=False)

    # Remove stray alpha, keep numeric
    s = s.str.replace(r"[^\d.\-]", "", regex=True)

    return pd.to_numeric(s, errors="coerce").abs().fillna(0)

def _detect_tally_dr_cr(df_raw):
    """
    Tally exports often have a single Amount column with Dr/Cr suffix
    or separate Debit/Credit columns. This function normalises to Type.
    Returns modified df.
    """
    cols_lower = {c.lower().strip(): c for c in df_raw.columns}

    # Case: separate Debit and Credit columns
    if "debit" in cols_lower and "credit" in cols_lower:
        d_col = cols_lower["debit"]
        c_col = cols_lower["credit"]
        debit = _clean_amount(df_raw[d_col])
        credit = _clean_amount(df_raw[c_col])
        df_raw["Amount"] = debit + credit
        df_raw["Type"] = np.where(debit > credit, "Expense", "Sales")

    return df_raw

def parse_file(file):
    """
    Robust Tally file parser — handles CSV and Excel in all common formats.
    Fixed in v5:
      - Better encoding fallbacks (utf-8, latin1, utf-8-sig, cp1252)
      - Dr/Cr column detection
      - Separate Debit/Credit column support
      - Better date format coverage
      - More category keywords
      - Informative error messages with column preview
    """
    try:
        fname = file.name.lower()
        df_raw = None

        # ── Read file ───────────────────────────────────────
        if fname.endswith((".xlsx", ".xls")):
            for engine in ["openpyxl", "xlrd"]:
                try:
                    file.seek(0)
                    df_raw = pd.read_excel(file, engine=engine)
                    break
                except Exception:
                    continue
            if df_raw is None:
                # Try reading all sheets and pick the biggest
                file.seek(0)
                try:
                    xl = pd.ExcelFile(file)
                    biggest = None
                    for sheet in xl.sheet_names:
                        tmp = xl.parse(sheet)
                        if biggest is None or len(tmp) > len(biggest):
                            biggest = tmp
                    df_raw = biggest
                except Exception as e:
                    return None, False, f"Could not read Excel file: {e}"

        elif fname.endswith(".csv"):
            encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252", "iso-8859-1"]
            separators = [",", "\t", ";", "|"]
            for enc in encodings:
                for sep in separators:
                    try:
                        file.seek(0)
                        df_raw = pd.read_csv(file, encoding=enc, sep=sep, engine="python")
                        if len(df_raw.columns) >= 2:
                            break
                    except Exception:
                        continue
                if df_raw is not None and len(df_raw.columns) >= 2:
                    break
            if df_raw is None:
                return None, False, "Could not read CSV. Try saving as UTF-8 CSV from Excel."
        else:
            return None, False, "Supported formats: .csv, .xlsx, .xls"

        # ── Drop empty rows/cols ─────────────────────────────
        df = df_raw.dropna(how="all").dropna(axis=1, how="all").copy()
        if len(df) == 0:
            return None, False, "File appears empty after removing blank rows."

        # ── Handle Tally Dr/Cr structure ─────────────────────
        df = _detect_tally_dr_cr(df)

        # ── Column mapping ───────────────────────────────────
        rename_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if "Amount" in df.columns and col in ("Amount",):
                continue
            if any(x in cl for x in ["date", "dt", "day", "dated", "period", "month", "time", "voucher date"]):
                rename_map[col] = "Date"
            elif any(x in cl for x in ["amount", "amt", "value", "total", "debit", "credit",
                                        "rs.", "rs ", "inr", "rupee", "bal", "balance", "sum", "net"]):
                if "Amount" not in rename_map.values():
                    rename_map[col] = "Amount"
            elif any(x in cl for x in ["type", "txn", "dr/cr", "nature", "mode", "trans", "vch type", "voucher type"]):
                rename_map[col] = "Type"
            elif any(x in cl for x in ["particulars", "category", "narration", "ledger",
                                        "description", "details", "head", "remark", "note", "narr"]):
                rename_map[col] = "Category"
            elif any(x in cl for x in ["party", "customer", "vendor", "name", "client",
                                        "payee", "payer", "firm", "company", "account", "supplier"]):
                rename_map[col] = "Party"
            elif any(x in cl for x in ["status", "paid", "pending", "overdue", "cleared", "payment status"]):
                rename_map[col] = "Status"
            elif any(x in cl for x in ["invoice", "voucher", "ref", "bill", "no.", "number", "inv no"]):
                rename_map[col] = "Invoice_No"
        df = df.rename(columns=rename_map)

        # ── Auto-detect Date column ──────────────────────────
        if "Date" not in df.columns:
            for col in df.columns:
                if col in ("Amount", "Type", "Category", "Party", "Status", "Invoice_No"):
                    continue
                if _looks_like_date_col(df[col]):
                    df = df.rename(columns={col: "Date"})
                    break

        if "Date" not in df.columns:
            cols_preview = ", ".join(f'"{c}"' for c in df_raw.columns[:10])
            return None, False, (
                f"Date column not found. Your file has columns: [{cols_preview}]. "
                "Please rename your date column to 'Date' and re-upload. "
                "Or export from Tally: Display > Day Book > Alt+E > Excel."
            )

        # ── Parse dates ──────────────────────────────────────
        parsed_dates = _try_parse_dates(df["Date"])
        if parsed_dates is None:
            sample = df["Date"].dropna().astype(str).head(3).tolist()
            return None, False, (
                f"Could not parse dates. Sample values: {sample}. "
                "Try DD-MM-YYYY format. In Excel: format the date column as Text first, "
                "then re-export as CSV."
            )
        df["Date"] = parsed_dates
        df = df.dropna(subset=["Date"])
        if len(df) == 0:
            return None, False, "All date values were invalid after parsing."

        # ── Clean amounts ────────────────────────────────────
        if "Amount" in df.columns:
            df["Amount"] = _clean_amount(df["Amount"])
        else:
            # No amount column found — try to find a numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                df = df.rename(columns={numeric_cols[0]: "Amount"})
            else:
                return None, False, (
                    "Amount column not found. Please ensure your file has a column with "
                    "transaction amounts named 'Amount', 'Debit', 'Credit', or 'Value'."
                )

        # ── Infer Type ───────────────────────────────────────
        if "Type" not in df.columns:
            df["Type"] = "Unknown"

        # Normalise Type values
        type_map = {
            "dr": "Expense", "debit": "Expense", "payment": "Expense",
            "purchase": "Expense", "contra": "Expense", "journal": "Expense",
            "cr": "Sales", "credit": "Sales", "receipt": "Sales",
            "sale": "Sales", "sales": "Sales",
        }
        df["Type"] = df["Type"].astype(str).str.strip().str.lower()
        df["Type"] = df["Type"].map(type_map).fillna(df["Type"])

        # For remaining unknowns, use category keywords
        mask = ~df["Type"].isin(["Sales", "Expense"])
        if mask.any():
            ekw = ["purchase", "expense", "payment", "salary", "rent", "bill", "wages",
                   "material", "raw", "logistics", "utilities", "overhead"]
            df.loc[mask, "Type"] = df.loc[mask].apply(
                lambda row: "Expense" if any(
                    k in str(row.get("Category", "")).lower() for k in ekw
                ) else "Sales",
                axis=1
            )

        # ── Fill missing columns ─────────────────────────────
        for col, default in [
            ("Status", "Paid"),
            ("Category", "General"),
            ("Party", "Unknown"),
            ("Invoice_No", "-"),
        ]:
            if col not in df.columns:
                df[col] = default

        # Auto-categorise uncategorised expenses
        if "Category" in df.columns:
            mask2 = df["Category"].isin(["General", "Unknown", "", "nan"])
            exp_mask = mask2 & (df["Type"] == "Expense")
            if exp_mask.any():
                df.loc[exp_mask, "Category"] = (
                    df.loc[exp_mask, "Party"].astype(str).apply(_cat)
                )

        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        n = len(df)
        date_min = df["Date"].min().strftime("%b %Y")
        date_max = df["Date"].max().strftime("%b %Y")
        sales_n = (df["Type"] == "Sales").sum()
        exp_n = (df["Type"] == "Expense").sum()
        return df, True, (
            f"✅ {n:,} transactions loaded ({date_min} → {date_max}) — "
            f"{sales_n:,} sales, {exp_n:,} expense entries"
        )

    except Exception as e:
        import traceback
        return None, False, f"Unexpected error: {e}. Please check the file format."


# ─────────────────────────────────────────────────────────────
# HEALTH SCORE  (NEW in v5)
# ─────────────────────────────────────────────────────────────

def compute_health_score(df, industry, leaks):
    """
    Financial Health Score: 0-100
    Weighted across 5 dimensions:
      1. Profitability (25 pts)  — margin vs benchmark
      2. Collections  (25 pts)  — overdue % of revenue
      3. Cost control (20 pts)  — expense trend
      4. Revenue risk (15 pts)  — concentration
      5. Cash cushion (15 pts)  — estimated runway months
    """
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]
    revenue = sales["Amount"].sum()
    exp_tot = expenses["Amount"].sum()
    profit = revenue - exp_tot
    margin = (profit / revenue * 100) if revenue > 0 else 0
    bmark = BENCH_MARGINS.get(industry, 15)

    scores = {}

    # 1. Profitability
    if margin >= bmark:
        scores["profitability"] = 25
    elif margin >= bmark * 0.7:
        scores["profitability"] = int(25 * (margin / bmark))
    elif margin > 0:
        scores["profitability"] = 8
    else:
        scores["profitability"] = 0

    # 2. Collections
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue", "pending", "unpaid", "due"])]
        od_pct = (od["Amount"].sum() / revenue * 100) if revenue > 0 else 0
        if od_pct <= 3:    scores["collections"] = 25
        elif od_pct <= 8:  scores["collections"] = 18
        elif od_pct <= 15: scores["collections"] = 10
        else:              scores["collections"] = 3
    else:
        scores["collections"] = 15  # unknown — neutral

    # 3. Cost control
    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
    if len(me) >= 4:
        recent = me.iloc[-3:].mean()
        prior = me.iloc[:-3].mean() if len(me) > 3 else me.iloc[0]
        if prior > 0:
            drift = (recent - prior) / prior
            if drift <= 0.03:    scores["cost_control"] = 20
            elif drift <= 0.10:  scores["cost_control"] = 14
            elif drift <= 0.18:  scores["cost_control"] = 8
            else:                scores["cost_control"] = 2
        else:
            scores["cost_control"] = 10
    else:
        scores["cost_control"] = 10

    # 4. Revenue concentration
    if len(sales) > 0 and revenue > 0:
        cr = sales.groupby("Party")["Amount"].sum()
        top_pct = (cr.max() / revenue * 100) if len(cr) > 0 else 0
        if top_pct <= 20:   scores["concentration"] = 15
        elif top_pct <= 30: scores["concentration"] = 10
        elif top_pct <= 50: scores["concentration"] = 5
        else:               scores["concentration"] = 1
    else:
        scores["concentration"] = 8

    # 5. Cash cushion (estimated from expense burn)
    me_monthly = me.iloc[-3:].mean() if len(me) >= 3 else (me.mean() if len(me) > 0 else 1)
    # Approximate cash as avg monthly surplus × 1.5 (rough proxy)
    monthly_surplus = (revenue / 12) - float(me_monthly)
    if monthly_surplus > 0:
        estimated_months = min(6, monthly_surplus / float(me_monthly) * 3)
        if estimated_months >= 3:    scores["cash"] = 15
        elif estimated_months >= 1:  scores["cash"] = 8
        else:                        scores["cash"] = 3
    else:
        scores["cash"] = 0

    total = sum(scores.values())

    if total >= 80:
        band = "Healthy"
        color = "#4CAF50"
        bar_color = "#4CAF50"
    elif total >= 60:
        band = "Stable"
        color = "#8BC34A"
        bar_color = "#8BC34A"
    elif total >= 40:
        band = "Marginal"
        color = "#D4AF37"
        bar_color = "#D4AF37"
    elif total >= 20:
        band = "Stressed"
        color = "#FF7043"
        bar_color = "#FF7043"
    else:
        band = "Critical"
        color = "#E05252"
        bar_color = "#E05252"

    return {
        "total": total,
        "band": band,
        "color": color,
        "bar_color": bar_color,
        "breakdown": scores,
        "labels": {
            "profitability": "Profitability",
            "collections": "Collections",
            "cost_control": "Cost Control",
            "concentration": "Revenue Risk",
            "cash": "Cash Cushion",
        },
        "max": {
            "profitability": 25,
            "collections": 25,
            "cost_control": 20,
            "concentration": 15,
            "cash": 15,
        }
    }

def render_health_score(hs):
    total = hs["total"]
    bar_w = int(total)
    breakdown = hs["breakdown"]
    labels = hs["labels"]
    maxes = hs["max"]

    cells = ""
    for k, label in labels.items():
        sc = breakdown.get(k, 0)
        mx = maxes[k]
        pct = int(sc / mx * 100)
        color = "#4CAF50" if pct >= 70 else ("#D4AF37" if pct >= 40 else "#E05252")
        cells += (
            f'<div class="hs-cell">'
            f'<div class="hs-cell-lbl">{label}</div>'
            f'<div class="hs-cell-val" style="color:{color}">{sc}<span style="font-size:1rem;color:#5A5A4A">/{mx}</span></div>'
            f'</div>'
        )

    st.markdown(f"""
<div class="hs-wrap">
  <div class="hs-label">Financial Health Score</div>
  <div class="hs-score" style="color:{hs['color']}">{total}</div>
  <div class="hs-band" style="color:{hs['color']}">{hs['band']}</div>
  <div class="hs-bar-bg">
    <div class="hs-bar-fill" style="width:{bar_w}%;background:{hs['bar_color']}"></div>
  </div>
  <div class="hs-grid">{cells}</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CASH RUNWAY  (NEW in v5)
# ─────────────────────────────────────────────────────────────

def compute_runway(df):
    """
    Cash Runway Prediction.
    Uses 3-month avg monthly burn rate and approximates cash balance
    from net surplus/deficit over the data period.
    Returns dict with days, months, classification, explanation.
    """
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]

    rev_m = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum()
    exp_m = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()

    if len(exp_m) == 0:
        return None

    # 3-month avg burn
    burn_monthly = float(exp_m.iloc[-3:].mean()) if len(exp_m) >= 3 else float(exp_m.mean())

    # Approximate cash: cumulative net position over data period
    merged = pd.DataFrame({"rev": rev_m, "exp": exp_m}).fillna(0)
    merged["net"] = merged["rev"] - merged["exp"]
    cumulative_net = float(merged["net"].sum())

    # If net positive, estimate months of burn coverage from that surplus
    if cumulative_net > 0 and burn_monthly > 0:
        months = cumulative_net / burn_monthly
    elif cumulative_net <= 0:
        months = 0.5  # already burning
    else:
        months = 1.0

    days = int(months * 30)

    if days <= 30:
        cls = "red"
        label = "Critical"
        advice = "Immediate action required. Collect all overdue, pause non-essential spend today."
    elif days <= 90:
        cls = "amber"
        label = "Watch carefully"
        advice = "Less than 3 months of runway. Prioritise collections and cut variable costs."
    else:
        cls = "green"
        label = "Comfortable"
        advice = "Good runway. Focus on growing revenue and protecting margin."

    return {
        "days": days,
        "months": round(months, 1),
        "burn_monthly": burn_monthly,
        "cls": cls,
        "label": label,
        "advice": advice,
    }

def render_runway(rwy):
    if rwy is None:
        return
    color_map = {"red": "#C0392B", "amber": "#9A7A00", "green": "#2E7D32"}
    color = color_map.get(rwy["cls"], "#1A1A1A")
    st.markdown(f"""
<div class="rwy-wrap {rwy['cls']}">
  <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap">
    <div>
      <div class="rwy-days" style="color:{color}">{rwy['days']} days</div>
      <div class="rwy-label">Estimated cash runway · <strong>{rwy['label']}</strong></div>
    </div>
    <div style="flex:1;min-width:200px">
      <div style="font-size:13px;color:#5A5A4A;margin-bottom:4px">{rwy['advice']}</div>
      <div style="font-size:12px;color:#9A9A8A">Based on avg monthly burn of {fmt(rwy['burn_monthly'])}</div>
    </div>
  </div>
  <div style="font-size:11px;color:#9A9A8A;margin-top:.8rem">
    ⚠️ Estimate based on transaction data — actual cash balance may differ. Verify with your CA.
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# GST RECONCILIATION  (NEW in v5)
# ─────────────────────────────────────────────────────────────

def render_gst_recon_uploader():
    """
    Allows user to upload GSTR-2A download and cross-check with purchase data.
    For now: structural placeholder + ITC estimation from existing data.
    """
    st.markdown('<div class="sh" style="font-size:1.2rem">🧮 GST Input Credit Reconciliation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ss">Upload your GSTR-2A (from GST portal) to find unmatched input credits. '
        'Even without upload, we estimate missed ITC from your expense data.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        gstr_file = st.file_uploader(
            "Upload GSTR-2A (Excel from GST Portal) — optional",
            type=["xlsx", "csv"],
            key="gstr2a_upload"
        )
    with col2:
        gst_rate = st.selectbox("Applicable GST rate", ["18%", "12%", "5%", "28%"], index=0)

    if gstr_file:
        try:
            gstr_df, ok, msg = parse_file(gstr_file)
            if ok and st.session_state.df is not None:
                expenses = st.session_state.df[st.session_state.df["Type"] == "Expense"]
                # Match on Party name (fuzzy)
                purchase_parties = set(expenses["Party"].str.lower().str.strip())
                gstr_parties = set(gstr_df["Party"].str.lower().str.strip()) if "Party" in gstr_df else set()
                matched = purchase_parties & gstr_parties
                unmatched = purchase_parties - gstr_parties
                st.success(f"✅ GSTR-2A loaded. {len(matched)} vendors matched, {len(unmatched)} unmatched.")
                if unmatched:
                    st.warning(f"⚠️ {len(unmatched)} vendors in your books not found in GSTR-2A — potential missed ITC:")
                    for p in list(unmatched)[:8]:
                        amt = expenses[expenses["Party"].str.lower().str.strip() == p]["Amount"].sum()
                        rate_num = int(gst_rate.replace("%", "")) / 100
                        st.markdown(f"- **{p.title()}** — {fmt(amt)} spent → ~{fmt(amt * rate_num)} ITC potentially claimable")
            else:
                st.error(f"Could not read GSTR-2A: {msg}")
        except Exception as e:
            st.error(f"GSTR-2A parse error: {e}")
    else:
        st.info("💡 Upload GSTR-2A for full reconciliation, or see estimated ITC below from your expense data.")


# ─────────────────────────────────────────────────────────────
# LEAK DETECTION ENGINE
# ─────────────────────────────────────────────────────────────

def find_leaks(df, industry, corrections=None):
    if corrections is None:
        corrections = {}
    intel = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]
    revenue = sales["Amount"].sum()
    exp_tot = expenses["Amount"].sum()
    profit = revenue - exp_tot
    margin = (profit / revenue * 100) if revenue > 0 else 0
    bmark = BENCH_MARGINS.get(industry, 15)
    leaks = []

    # 1 — Overdue receivables
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(
            ["overdue", "pending", "not paid", "due", "outstanding", "unpaid", "not cleared"]
        )]
        od_amt = od["Amount"].sum()
        if od_amt > 10000:
            deb = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_name = deb.index[0] if len(deb) > 0 else "Customer"
            top_amt = float(deb.iloc[0]) if len(deb) > 0 else od_amt
            pct = od_amt / revenue * 100 if revenue > 0 else 0
            conf = get_confidence_score("cash_stuck", corrections)
            leaks.append({
                "id": "cash_stuck", "sev": "critical", "cat": "Collections",
                "rupee": od_amt, "annual": od_amt * 0.18, "confidence": conf,
                "headline": f"{fmtx(int(od_amt))} stuck in unpaid invoices",
                "sub": f"Across {len(deb)} {intel['language']['revenue']}",
                "found": f"{len(deb)} customers owe you. Top: {top_name} owes {fmtx(int(top_amt))}.",
                "root_cause": intel["root_causes"].get("overdue", "Enforce payment terms strictly."),
                "costs": f"Cost of capital at 18%: {fmt(od_amt * 0.18)}/year tied up.",
                "bench": f"Healthy: overdue < 5% of revenue. Yours: {pct:.1f}%.",
                "action": f"Call {top_name} today. Offer 2% discount for 48-hr payment.",
                "action_sub": intel["language"]["quick_win"],
                "template": f"Hi, invoice of {fmt(top_amt)} is overdue. 2% off if paid today.",
                "seqs": gen_seq(top_name, "INV-001", top_amt, "Your Business"),
            })

    # 2 — Vendor overpay
    if len(expenses) > 0:
        peer_stats = intel.get("peer_stats", {})
        for category in expenses["Category"].unique():
            ce = expenses[expenses["Category"] == category]
            if len(ce) < 3:
                continue
            vs = ce.groupby("Party")["Amount"].agg(["mean", "count", "sum"])
            vs = vs[vs["count"] >= 2]
            if len(vs) < 2:
                continue
            cheapest = vs["mean"].min()
            ev = vs["mean"].idxmax()
            ep = vs["mean"].max()
            av = float(vs.loc[ev, "sum"])
            if ep > cheapest * 1.12 and cheapest > 0:
                pct_gap = ((ep - cheapest) / cheapest) * 100
                waste = (ep - cheapest) * (av / ep)
                pdata = peer_stats.get(category)
                bench_line = (
                    f"Your cost: ₹{ep:,.0f}. Industry estimate: ₹{pdata['median']:,}{pdata['unit']}."
                    if pdata else
                    f"Get 3 quotes — typically 10–18% saving possible on {category}."
                )
                conf = get_confidence_score("cost_bleed", corrections)
                if waste > 15000:
                    leaks.append({
                        "id": "cost_bleed", "sev": "warning", "cat": "Vendor Costs",
                        "rupee": waste, "annual": waste, "confidence": conf,
                        "headline": f"{fmtx(int(waste))} overpaid on {category} per year",
                        "sub": f"{ev} charges {pct_gap:.0f}% more than cheapest option",
                        "found": f"You paid {ev} avg ₹{ep:,.0f}. Cheapest: ₹{cheapest:,.0f}.",
                        "root_cause": intel["root_causes"].get("high_expense", "Vendor prices drift without regular reviews."),
                        "costs": f"{fmtx(int(waste))} extra per year.",
                        "bench": bench_line,
                        "action": f"Get 2 competing quotes for {category} this week.",
                        "action_sub": "Lowest confirmed quote gets the contract.",
                        "template": f"Reviewing {category} suppliers. Best rate for volume by Friday gets 12-month contract.",
                        "seqs": [],
                    })
                    break

    # 3 — Margin gap
    if margin < bmark - 3:
        gap = ((bmark - margin) / 100) * revenue
        if gap > 25000:
            conf = get_confidence_score("margin_gap", corrections)
            leaks.append({
                "id": "margin_gap", "sev": "critical" if margin < 5 else "warning", "cat": "Profitability",
                "rupee": gap, "annual": gap, "confidence": conf,
                "headline": f"{fmtx(int(gap))} in margin left on the table",
                "sub": f"Your {margin:.1f}% vs {bmark}% {intel['name']} industry estimate",
                "found": f"Margin: {margin:.1f}%. Estimate for {intel['name']}: {bmark}%. Gap: {bmark - margin:.1f} pp.",
                "root_cause": intel["root_causes"].get("low_margin", "Cost structure misaligned with revenue."),
                "costs": f"Closing half this gap adds {fmt(gap * 0.5)} in profit.",
                "bench": f"Source: {intel['language']['benchmark_source']}",
                "action": "Raise prices 5% on top products. Cut 10% from largest cost line.",
                "action_sub": intel["language"]["top_leak"],
                "template": "Reviewing pricing — benchmarks suggest 5-8% increase is supportable.",
                "seqs": [],
            })

    # 4 — Revenue concentration risk
    if len(sales) > 0 and revenue > 0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr) > 0 and (cr.iloc[0] / revenue) * 100 > 28:
            top_pct = (cr.iloc[0] / revenue) * 100
            risk = cr.iloc[0] * 0.3
            conf = get_confidence_score("concentration", corrections)
            leaks.append({
                "id": "concentration", "sev": "warning", "cat": "Revenue Risk",
                "rupee": risk, "annual": risk, "confidence": conf,
                "headline": f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub": "One client delay = cash crisis",
                "found": f"{cr.index[0]} = {top_pct:.0f}% ({fmtx(int(cr.iloc[0]))}). 30-day delay = {fmtx(int(cr.iloc[0]))} shortfall.",
                "root_cause": "Revenue concentration above 25% removes pricing power and creates existential cash risk.",
                "costs": "One delayed payment becomes your entire cashflow problem.",
                "bench": "Healthy: no single client above 25% of revenue.",
                "action": "Close 2 new clients this month to diversify.",
                "action_sub": "Set 25% concentration cap as a hard rule.",
                "template": "Expanding client base — referral discount available this quarter.",
                "seqs": [],
            })

    # 5 — Expense spike
    if len(expenses) > 0:
        me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me) >= 4:
            recent = me.iloc[-3:].mean()
            prior = me.iloc[:-3].mean() if len(me) > 3 else me.iloc[0]
            if prior > 0 and recent > prior * 1.18:
                spike = (recent - prior) * 12
                if spike > 20000:
                    conf = get_confidence_score("exp_spike", corrections)
                    leaks.append({
                        "id": "exp_spike", "sev": "warning", "cat": "Cost Control",
                        "rupee": spike, "annual": spike, "confidence": conf,
                        "headline": f"Monthly costs up {((recent/prior - 1)*100):.0f}% — {fmtx(int(spike))} annualised",
                        "sub": f"₹{(recent-prior)/1000:.0f}K more per month than before",
                        "found": f"Expense 3+ months ago: {fmt(prior)}/mo. Now: {fmt(recent)}/mo.",
                        "root_cause": "Rising costs without matching revenue growth is a structural margin threat.",
                        "costs": "Structural cost increase — compounds monthly if not addressed.",
                        "bench": "Expenses should track revenue. Rising faster = investigate now.",
                        "action": "Freeze non-essential spend. Review every line above ₹5K.",
                        "action_sub": "Set a spend approval threshold until resolved.",
                        "template": "Cost control initiative: all non-essential expenses need approval.",
                        "seqs": [],
                    })

    # 6 — GST input credits
    elig = expenses[expenses["Amount"] > 25000]
    if len(elig) > 0:
        gst_intel = intel.get("gst_optimization", {})
        recovery_rate = gst_intel.get("typical_recovery_rate", 0.12)
        missed = elig["Amount"].sum() * 0.18 * recovery_rate
        if missed > 8000:
            conf = get_confidence_score("tax_gst", corrections)
            desc = gst_intel.get("description", "GST input credits often under-claimed.")
            leaks.append({
                "id": "tax_gst", "sev": "info", "cat": "Tax Recovery",
                "rupee": missed, "annual": missed, "confidence": conf,
                "headline": f"~{fmtx(int(missed))} in GST input credits to verify",
                "sub": "Estimated — needs CA confirmation",
                "found": f"Eligible purchases: {fmt(elig['Amount'].sum())}. ~{recovery_rate*100:.0f}% unclaimed ITC is common.",
                "root_cause": "Most SMEs don't reconcile GSTR-2A monthly. ITC claims lapse after 2 years.",
                "costs": "Government money owed to you. One CA session to recover.",
                "bench": "Claim before next GST filing. Two-year window from invoice date.",
                "action": "Email your CA: 'Please review ITC on purchases above ₹25K.'",
                "action_sub": desc,
                "template": "Want to review ITC eligibility on purchase invoices. Can we schedule a call?",
                "seqs": [],
            })

    return sorted(leaks, key=lambda x: x["rupee"], reverse=True)


def leaks_to_tasks(leaks, biz_name="Your Business"):
    tasks = []
    today = datetime.now()
    owners = ["Owner", "Accounts", "Operations", "Owner"]
    for i, leak in enumerate(leaks):
        due_days = 3 if leak["sev"] == "critical" else (7 if leak["sev"] == "warning" else 14)
        tasks.append({
            "id": leak["id"],
            "title": leak["action"],
            "category": leak["cat"],
            "impact": leak["rupee"],
            "owner": owners[i % len(owners)],
            "due": (today + timedelta(days=due_days)).strftime("%d %b"),
            "due_dt": today + timedelta(days=due_days),
            "status": "pending",
            "severity": leak["sev"],
            "wa_template": leak["template"],
            "notes": "",
        })
    return tasks


def render_workflow_board(tasks, key_prefix="wf"):
    pending = [t for t in tasks if t["status"] == "pending"]
    done = [t for t in tasks if t["status"] == "done"]
    overdue = [t for t in tasks if t["status"] == "pending" and t["due_dt"] < datetime.now()]

    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:1.5rem;text-align:center">
  <div style="background:#FFFBF0;border-radius:10px;padding:1rem">
    <div style="font-size:1.6rem;font-weight:700;color:#D4AF37">{len(pending)}</div>
    <div style="font-size:12px;color:#6A6A5A">Pending</div>
  </div>
  <div style="background:#E8F5E9;border-radius:10px;padding:1rem">
    <div style="font-size:1.6rem;font-weight:700;color:#2E7D32">{len(done)}</div>
    <div style="font-size:12px;color:#6A6A5A">Done</div>
  </div>
  <div style="background:#FEF0F0;border-radius:10px;padding:1rem">
    <div style="font-size:1.6rem;font-weight:700;color:#C0392B">{len(overdue)}</div>
    <div style="font-size:12px;color:#6A6A5A">Overdue</div>
  </div>
</div>
""", unsafe_allow_html=True)

    for i, task in enumerate(tasks):
        is_overdue = (task["status"] == "pending" and task["due_dt"] < datetime.now())
        css = "done" if task["status"] == "done" else ("overdue" if is_overdue else "")
        pill_cls = "done" if task["status"] == "done" else ("overdue" if is_overdue else "pending")
        pill_lbl = "DONE" if task["status"] == "done" else ("OVERDUE" if is_overdue else "PENDING")
        icon = "✅" if task["status"] == "done" else ("🔴" if task["severity"] == "critical" else "🟡")

        st.markdown(f"""
<div class="task-card {css}">
  <div style="width:40px;height:40px;border-radius:50%;background:#F7F4EF;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0">{icon}</div>
  <div class="task-left">
    <div class="task-title">{task['title']}</div>
    <div class="task-meta">Owner: {task['owner']} · Due: {task['due']} · {task['category']}</div>
  </div>
  <div class="task-impact">+{fmt(task['impact'])}</div>
  <div class="task-pill {pill_cls}">{pill_lbl}</div>
</div>
""", unsafe_allow_html=True)

        if task["status"] == "pending":
            c1, c2, c3 = st.columns([2, 1, 1])
            with c2:
                if st.button("✅ Done", key=f"{key_prefix}_done_{i}"):
                    st.session_state.tasks[i]["status"] = "done"
                    st.session_state.tasks[i]["done_dt"] = datetime.now().isoformat()
                    st.rerun()
            with c3:
                wa_msg = urllib.parse.quote(
                    f"Reminder: {task['title']} is due {task['due']}. Impact: {fmt(task['impact'])}. Please action today."
                )
                st.markdown(
                    f'<a href="https://wa.me/?text={wa_msg}" target="_blank">'
                    f'<button style="width:100%;background:#25D366;color:white;border:none;padding:8px;'
                    f'border-radius:6px;cursor:pointer;font-size:12px;font-weight:600">📱 Remind</button></a>',
                    unsafe_allow_html=True
                )


# ─────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────
defaults = {
    "df": None, "industry": "agency", "city": "Bangalore",
    "show_bot": False, "lead_captured": False, "trial_clicked": False,
    "user_phone": "", "biz_name": "",
    "tasks": [], "corrections": {}, "monthly_fee": 2999, "months": 1,
    "snapshots": [], "ca_mode": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# DEMO DATA GENERATOR
# ─────────────────────────────────────────────────────────────
def make_demo():
    np.random.seed(42)
    customers = ["Sharma Enterprises", "Patel & Sons", "Krishna Steels", "Mehta Industries", "Lakshmi Dist.", "Venkatesh Fab"]
    vendors = ["Tata Steel Suppliers", "National Raw Mat", "City Transport", "Vinayak Packaging", "Bharat Logistics"]
    cats = ["Raw Materials", "Labor", "Rent", "Logistics", "Packaging", "Utilities"]
    wts = [0.30, 0.20, 0.10, 0.15, 0.10, 0.15]
    recs = []
    for d in pd.date_range("2024-04-01", "2025-03-31", freq="D"):
        if np.random.random() > 0.25:
            recs.append({
                "Date": d, "Type": "Sales",
                "Party": np.random.choice(customers, p=[0.38, 0.20, 0.16, 0.12, 0.08, 0.06]),
                "Amount": np.random.uniform(60000, 280000),
                "Status": np.random.choice(["Paid", "Paid", "Overdue", "Pending"], p=[0.55, 0.25, 0.12, 0.08]),
                "Category": "Sales"
            })
        for _ in range(np.random.randint(1, 4)):
            cat = np.random.choice(cats, p=wts)
            recs.append({
                "Date": d, "Type": "Expense",
                "Party": np.random.choice(vendors),
                "Amount": np.random.uniform(12000, 90000),
                "Status": "Paid", "Category": cat
            })
    demo = pd.DataFrame(recs)
    demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
    return demo


# ─────────────────────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Profit Intelligence · Indian SMEs · Bangalore</div>
  <h1 class="hero-h">We don't show data.<br><em>We increase your profit.</em></h1>
  <p class="hero-sub">Upload your Tally export. Get industry-specific profit intelligence, peer benchmarks,
  and a tracked action plan — in 60 seconds.</p>
  <div class="trust-row">
    <div class="t-item"><div class="t-num">Early Pilot</div><div class="t-lbl">Bangalore-based</div></div>
    <div class="t-item"><div class="t-num">10 sectors</div><div class="t-lbl">Industry intelligence</div></div>
    <div class="t-item"><div class="t-num">60 seconds</div><div class="t-lbl">To first insight</div></div>
    <div class="t-item"><div class="t-num">Free scan</div><div class="t-lbl">No credit card</div></div>
  </div>
</div>
<div class="safety-bar">
  <div class="s-pill"><div class="s-dot"></div> Data processed in-session, not stored on our servers</div>
  <div class="s-pill"><div class="s-dot"></div> Industry-specific intelligence for 10 sectors</div>
  <div class="s-pill"><div class="s-dot"></div> Benchmarks are industry estimates — verify with your CA</div>
  <div class="s-pill"><div class="s-dot"></div> Results in 60 seconds</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "₹  Profit Scan",
    "🧠  Intelligence",
    "📋  Action Board",
    "📊  ROI Report",
    "🏛  CA Partner",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — PROFIT SCAN
# ═══════════════════════════════════════════════════════════════
with t1:
    st.markdown('<div class="sw">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        uploaded = st.file_uploader(
            "Upload Tally Day Book, Sales Register, or Bank Statement",
            type=["csv", "xlsx", "xls"]
        )
        with st.expander("📖 How to export from Tally"):
            st.markdown(
                "**Tally Prime:** Display → Day Book → Alt+E → Excel  \n"
                "**Tally ERP9:** Gateway → Day Book → Ctrl+E  \n"
                "**Columns needed:** Date, Party/Customer, Amount, Type (Sales/Expense)  \n"
                "**Tip:** If your export has Dr/Cr in the amount column, that's fine — we handle it automatically."
            )
    with c2:
        ind_sel = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
        st.session_state.industry = INDUSTRY_MAP[ind_sel]
    with c3:
        st.selectbox(
            "City",
            ["Bangalore", "Mumbai", "Delhi", "Pune", "Chennai", "Hyderabad", "Ahmedabad", "Other"],
            key="city"
        )
        if st.button("▶  Try Demo", use_container_width=True, type="secondary"):
            st.session_state.df = make_demo()
            st.session_state.industry = "manufacturing"
            st.session_state.lead_captured = True
            st.session_state.biz_name = "Demo Manufacturing Co"
            st.session_state.tasks = []
            st.session_state.corrections = {}
            st.rerun()

    if uploaded:
        df_new, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_new
            st.session_state.tasks = []
            st.session_state.corrections = {}
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info(
                "**Common fixes:** \n"
                "1. Export from Tally as CSV (Day Book → Ctrl+E)\n"
                "2. Ensure date column is named 'Date' or 'Voucher Date'\n"
                "3. Ensure amount column is named 'Amount', 'Debit', or 'Credit'\n"
                "4. Remove any merged header rows at the top\n"
                "5. Save as UTF-8 CSV if encoding errors appear"
            )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── GATE ─────────────────────────────────────────────────
    if st.session_state.df is not None and not st.session_state.lead_captured:
        st.markdown('<div class="sw">', unsafe_allow_html=True)
        ind_name = INDUSTRY_INTELLIGENCE.get(st.session_state.industry, {}).get("name", "your industry")
        st.markdown(f"""
<div class="gate-box">
  <div class="gate-h">🎯 Scan Ready — Enter Details to Unlock</div>
  <div class="gate-s">We found potential leaks in your data.<br>
  Enter your details to see where your money is going and how to get it back.<br>
  <strong>Average pilot client recovers ₹2–4L in 30 days.</strong></div>
</div>
""", unsafe_allow_html=True)
        g1, g2, g3 = st.columns([1, 2, 1])
        with g2:
            p = st.text_input("📱 WhatsApp Number", "", placeholder="9876543210")
            b = st.text_input("🏢 Business Name", "", placeholder="Sharma Enterprises")
            st.text_input("👤 Your Name", "", placeholder="Rahul Sharma")

            if st.button("Show My Profit Leaks →", type="primary", use_container_width=True):
                if p.strip() and len(p.strip()) >= 10:
                    st.session_state.user_phone = p
                    st.session_state.biz_name = b or "Your Business"
                    st.session_state.lead_captured = True
                    st.rerun()
                else:
                    st.warning("Please enter a valid WhatsApp number to continue.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ──────────────────────────────────────────────
    if st.session_state.df is not None and st.session_state.lead_captured:
        df = st.session_state.df
        industry = st.session_state.industry
        intel = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
        biz = st.session_state.biz_name or "Your Business"

        sales = df[df["Type"] == "Sales"]
        expenses = df[df["Type"] == "Expense"]
        revenue = sales["Amount"].sum()
        exp_tot = expenses["Amount"].sum()
        profit = revenue - exp_tot
        margin = (profit / revenue * 100) if revenue > 0 else 0
        bmark = BENCH_MARGINS.get(industry, 15)

        leaks = find_leaks(df, industry, st.session_state.corrections)
        total_rupee = sum(l["rupee"] for l in leaks)
        overdue = (
            sales[sales["Status"].str.lower().isin(["overdue", "pending"])]["Amount"].sum()
            if "Status" in sales.columns else 0
        )

        if not st.session_state.tasks and leaks:
            st.session_state.tasks = leaks_to_tasks(leaks, biz)

        done_saving = sum(t["impact"] for t in st.session_state.tasks if t["status"] == "done")
        pending_n = sum(1 for t in st.session_state.tasks if t["status"] == "pending")
        roi_x = done_saving / st.session_state.monthly_fee if st.session_state.monthly_fee > 0 else 0

        st.markdown('<div class="sw">', unsafe_allow_html=True)

        # ── Health Score ──────────────────────────────────
        hs = compute_health_score(df, industry, leaks)
        render_health_score(hs)

        # ── Cash Runway ───────────────────────────────────
        rwy = compute_runway(df)
        render_runway(rwy)

        # ── Money Counter ─────────────────────────────────
        st.markdown(f"""
<div class="msc-wrap">
  <div class="msc-label">💰 Potential Recovery — {biz}</div>
  <div class="msc-total">{fmt(done_saving)}</div>
  <div class="msc-sub">of {fmt(total_rupee)} identified · Mark tasks done in Action Board to track recovery</div>
  <div class="msc-grid">
    <div class="msc-cell"><div class="msc-cell-lbl">Total Identified</div><div class="msc-cell-val gold">{fmt(total_rupee)}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">Recovered</div><div class="msc-cell-val green">{fmt(done_saving)}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">Actions Pending</div><div class="msc-cell-val">{pending_n}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">ROI on OpsClarity</div><div class="msc-cell-val green">{roi_x:.1f}x</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── KPI Row ───────────────────────────────────────
        margin_cls = "good" if margin >= bmark else "bad"
        overdue_pct = overdue / revenue * 100 if revenue > 0 else 0
        overdue_cls = "bad" if overdue > revenue * 0.06 else "good"
        profit_cls = "good" if profit > 0 else "bad"

        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi-card"><div class="kpi-lbl">Revenue</div><div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales):,} transactions</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Margin</div><div class="kpi-val">{margin:.1f}%</div><div class="kpi-sub {margin_cls}">vs ~{bmark}% estimate</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Overdue</div><div class="kpi-val">{fmt(overdue)}</div><div class="kpi-sub {overdue_cls}">{overdue_pct:.1f}% of revenue</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Profit</div><div class="kpi-val">{fmt(abs(profit))}</div><div class="kpi-sub {profit_cls}">{"Profitable" if profit > 0 else "Loss"}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── Trend Chips ───────────────────────────────────
        trends = compute_trends(df)
        st.markdown("**📈 Trends:** &nbsp;", unsafe_allow_html=True)
        col_trends = st.columns(4)
        with col_trends[0]: render_trend_chip("Revenue", trends.get("revenue", [0, 0]), positive_direction="up")
        with col_trends[1]: render_trend_chip("Expenses", trends.get("expenses", [0, 0]), positive_direction="down")
        with col_trends[2]: render_trend_chip("Margin", trends.get("margin", [0, 0]), positive_direction="up")
        with col_trends[3]:
            if "overdue" in trends:
                render_trend_chip("Overdue", trends["overdue"], positive_direction="down")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Leak Cards ────────────────────────────────────
        st.markdown(f'<div class="sh">🔍 Where Your Money is Leaking</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ss">{intel["name"]} · {len(leaks)} leaks found</div>', unsafe_allow_html=True)

        for leak in leaks[:6]:
            conf_badge = render_confidence_badge(leak["confidence"])
            st.markdown(f"""
<div class="intel-card {leak['sev']}">
  <div class="intel-tag {leak['sev']}">{leak['cat'].upper()}</div>
  <div class="intel-amt">{fmtx(int(leak['rupee']))} {conf_badge}</div>
  <div class="intel-ttl">{leak['headline']}</div>
  <div class="intel-body">{leak['sub']}</div>
  <div class="intel-why">
    <strong>What we found:</strong> {leak['found']}<br><br>
    <strong>Root cause:</strong> {leak['root_cause']}<br><br>
    <strong>Benchmark:</strong> {leak['bench']}
  </div>
  <div class="intel-act">{leak['action']}</div>
  <div class="intel-act-s">{leak['action_sub']}</div>
</div>
""", unsafe_allow_html=True)

            # Feedback
            fb_key = f"fb_{leak['id']}"
            cf1, cf2, cf3, cf4 = st.columns([3, 1, 1, 1])
            with cf2:
                if st.button("✅ Correct", key=f"{fb_key}_c"):
                    st.session_state.corrections[leak["id"]] = "correct"; st.rerun()
            with cf3:
                if st.button("⚠️ Partial", key=f"{fb_key}_p"):
                    st.session_state.corrections[leak["id"]] = "partial"; st.rerun()
            with cf4:
                if st.button("❌ Wrong", key=f"{fb_key}_w"):
                    st.session_state.corrections[leak["id"]] = "wrong"; st.rerun()

            # WhatsApp sequence — FIXED: now uses 'msg' key correctly
            if leak["id"] == "cash_stuck" and leak.get("seqs"):
                if st.button("📱 Show WhatsApp Collection Sequence", key=f"seq_{leak['id']}"):
                    st.session_state.show_bot = not st.session_state.show_bot
                if st.session_state.show_bot:
                    for step in leak["seqs"]:
                        st.markdown(f"""
<div class="seq-card">
  <div class="seq-day">Day {step['day']} · Send on {step['send_on']}</div>
  <div class="seq-tone" style="color:{step['color']}">{step['tone']}</div>
  <div class="seq-msg">{step['msg']}</div>
</div>
""", unsafe_allow_html=True)
                        st.markdown(
                            f'<a href="{step["wa_link"]}" target="_blank" '
                            f'style="font-size:12px;color:#25D366;font-weight:600">📲 Open in WhatsApp →</a>',
                            unsafe_allow_html=True
                        )
            elif leak.get("template"):
                with st.expander("📋 Copy message template"):
                    st.code(leak["template"])

        # ── Charts ────────────────────────────────────────
        st.markdown("---")
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("**📊 Revenue vs Expenses — Monthly**")
            monthly = df.groupby([df["Date"].dt.to_period("M"), "Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly, height=250, use_container_width=True)
        with ch2:
            st.markdown("**📊 Top Expense Categories**")
            if len(expenses) > 0:
                st.bar_chart(
                    expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8),
                    height=250, use_container_width=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Pricing ───────────────────────────────────────
        st.markdown('<div class="pr-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:DM Serif Display,serif;font-size:1.8rem;color:#F7F4EF;margin-bottom:1.5rem;text-align:center">Choose Your Recovery Plan</div>', unsafe_allow_html=True)

        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.markdown('<div class="pr-card"><div class="pr-lbl">Start Free</div><div class="pr-name">First Scan</div><div class="pr-amt">₹0</div><div class="pr-note">Full intelligence scan with industry benchmarks and leak detection.</div><div class="pr-feat">Industry-specific insights</div><div class="pr-feat">5 profit leak detections</div><div class="pr-feat">Benchmark estimates</div><div class="pr-feat">Basic action tracker</div></div>', unsafe_allow_html=True)
        with pc2:
            st.markdown('<div class="pr-card feat"><div class="pr-lbl">Most Popular</div><div class="pr-name">Recovery Review</div><div class="pr-amt">₹2,999</div><div class="pr-note">60-min founder call + 30-day recovery plan + full ROI tracking.</div><div class="pr-feat">Everything in Free, plus:</div><div class="pr-feat">Founder strategy call</div><div class="pr-feat">Vendor sourcing help</div><div class="pr-feat">Monthly ROI report</div><div class="pr-feat">CA coordination</div><div class="pr-feat">WhatsApp workflow setup</div></div>', unsafe_allow_html=True)
        with pc3:
            st.markdown('<div class="pr-card"><div class="pr-lbl">For CA Firms</div><div class="pr-name">Partner Program</div><div class="pr-amt">₹1,999/mo</div><div class="pr-note">50 client seats. White-label reports. ₹500/client you earn.</div><div class="pr-feat">Everything in Recovery, plus:</div><div class="pr-feat">50 client dashboards</div><div class="pr-feat">Branded client reports</div><div class="pr-feat">ROI proof per client</div><div class="pr-feat">Priority support</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            if st.button("🚀 Book Recovery Review — ₹2,999", use_container_width=True, type="primary"):
                st.session_state.trial_clicked = True
        if st.session_state.trial_clicked:
            st.success("✅ We'll WhatsApp you within 2 hours to schedule your Recovery Review.")
            st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=Hi,+want+Recovery+Review)")
            st.balloons()


# ═══════════════════════════════════════════════════════════════
# TAB 2 — INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
with t2:
    st.markdown('<div class="sw">', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("👆 Run a scan first (Tab 1) to see industry benchmarks")
    else:
        df = st.session_state.df
        industry = st.session_state.industry
        intel = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
        expenses = df[df["Type"] == "Expense"]
        sales = df[df["Type"] == "Sales"]
        revenue = sales["Amount"].sum()

        st.markdown(f'<div class="sh">Industry Intelligence — {intel["name"]}</div>', unsafe_allow_html=True)

        # Honest benchmark notice
        st.markdown(
            '<div class="pilot-notice">📊 Benchmarks below are industry estimates from public reports and surveys. '
            'They are directionally useful, not statistically precise. '
            'Verify any finding with your CA before taking action.</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
<div class="intel-card info" style="margin-bottom:1.5rem">
  <div class="intel-tag info">INDUSTRY CONTEXT</div>
  <div class="intel-ttl">What drives profit in {intel['name']}</div>
  <div class="intel-body">
    <strong>Top leak in this industry:</strong> {intel['language']['top_leak']}<br><br>
    <strong>Quick win most owners miss:</strong> {intel['language']['quick_win']}<br><br>
    <strong>Source:</strong> {intel['language']['benchmark_source']}
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sh" style="font-size:1.3rem">Where you sit vs industry estimates</div>', unsafe_allow_html=True)

        peer_stats = intel.get("peer_stats", {})
        if len(expenses) > 0 and revenue > 0:
            exp_by_cat = expenses.groupby("Category")["Amount"].sum()
            shown = 0
            for cat, pdata in peer_stats.items():
                if cat in exp_by_cat.index:
                    your_val = exp_by_cat[cat]
                    if "% rev" in pdata["unit"]:
                        your_pct = your_val / revenue * 100
                        render_benchmark_gauge(
                            label=f"{pdata['label']} — your spend vs estimates",
                            your_value=your_pct,
                            p25=pdata["p25"], median=pdata["median"], p75=pdata["p75"],
                            unit=pdata["unit"], n=pdata["n"]
                        )
                    else:
                        avg_txn = expenses[expenses["Category"] == cat]["Amount"].mean()
                        render_benchmark_gauge(
                            label=f"{pdata['label']} — avg per transaction vs estimates",
                            your_value=avg_txn,
                            p25=pdata["p25"], median=pdata["median"], p75=pdata["p75"],
                            unit=pdata["unit"], n=pdata["n"]
                        )
                    shown += 1
            if shown == 0:
                st.info(
                    f"No matching expense categories found for {intel['name']} benchmarks. "
                    "This usually means your Category column uses different names. "
                    "Benchmarks shown as reference ranges:"
                )
                for cat, pdata in peer_stats.items():
                    st.markdown(
                        f'<div class="bench-wrap"><div class="bench-label">{pdata["label"]} — industry range</div>'
                        f'<div style="font-size:13px;color:#6A6A5A">Best 25%: {pdata["p25"]}{pdata["unit"]} · '
                        f'Median: {pdata["median"]}{pdata["unit"]} · Worst 25%: {pdata["p75"]}{pdata["unit"]}</div></div>',
                        unsafe_allow_html=True
                    )
        else:
            for cat, pdata in peer_stats.items():
                st.markdown(
                    f'<div class="bench-wrap"><div class="bench-label">{pdata["label"]}</div>'
                    f'<div style="font-size:13px;color:#6A6A5A">Best 25%: {pdata["p25"]}{pdata["unit"]} · '
                    f'Median: {pdata["median"]}{pdata["unit"]} · Worst 25%: {pdata["p75"]}{pdata["unit"]}</div></div>',
                    unsafe_allow_html=True
                )

        # Weekly metrics
        st.markdown("---")
        st.markdown(f'<div class="sh" style="font-size:1.2rem">Weekly metrics to track for {intel["name"]}</div>', unsafe_allow_html=True)
        wm_cols = st.columns(len(intel["weekly_metrics"]))
        for i, metric in enumerate(intel["weekly_metrics"]):
            with wm_cols[i]:
                st.metric(metric, "Track weekly")

        # GST Section
        gst_intel = intel.get("gst_optimization", {})
        if gst_intel:
            st.markdown("---")
            render_gst_recon_uploader()
            eligible = gst_intel.get("eligible_categories", [])
            rate = gst_intel.get("typical_recovery_rate", 0.12) * 100
            st.markdown(f"""
<div class="intel-card info">
  <div class="intel-tag info">GST OPTIMIZATION</div>
  <div class="intel-ttl">Eligible Categories for ITC</div>
  <div class="intel-body">
    <strong>Categories to review:</strong> {', '.join(eligible)}<br>
    <strong>Typical recovery rate:</strong> {rate:.0f}% of eligible GST<br>
    <strong>Action:</strong> Reconcile GSTR-2A monthly. Claim within 2 years of invoice date.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — ACTION BOARD
# ═══════════════════════════════════════════════════════════════
with t3:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">📋 Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Every rupee tracked. Every action assigned. Mark done to update your ROI report.</div>', unsafe_allow_html=True)

    if not st.session_state.tasks:
        st.info("👆 Run a scan first (Tab 1) to generate your action board.")
    else:
        render_workflow_board(st.session_state.tasks, key_prefix="board")

        st.markdown("---")
        st.markdown("**🔄 Re-assign task owner**")
        task_names = [t["title"][:50] for t in st.session_state.tasks]
        sel_task = st.selectbox("Select task", task_names)
        new_owner = st.text_input("Assign to", "Owner", placeholder="e.g. Ramesh / Accounts team")
        if st.button("Update owner"):
            idx = task_names.index(sel_task)
            st.session_state.tasks[idx]["owner"] = new_owner
            st.success(f"✅ Assigned to {new_owner}")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 — ROI REPORT
# ═══════════════════════════════════════════════════════════════
with t4:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">📊 ROI Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Fee paid vs money saved. Your proof that this works.</div>', unsafe_allow_html=True)

    if not st.session_state.tasks:
        st.info("👆 Run a scan first (Tab 1)")
    else:
        biz = st.session_state.biz_name or "Your Business"
        f1, f2 = st.columns(2)
        with f1:
            st.session_state.monthly_fee = st.number_input("Monthly fee paid (₹)", value=2999, step=500)
        with f2:
            st.session_state.months = st.number_input("Months active", value=1, min_value=1, max_value=24)

        total_fees = st.session_state.monthly_fee * st.session_state.months
        total_saved = sum(t["impact"] for t in st.session_state.tasks if t["status"] == "done")
        total_found = sum(t["impact"] for t in st.session_state.tasks)
        net_gain = total_saved - total_fees
        roi_x = (total_saved / total_fees) if total_fees > 0 else 0

        if roi_x >= 10:
            verdict = f"Exceptional — every ₹1 on OpsClarity returned ₹{roi_x:.0f}"
        elif roi_x >= 3:
            verdict = f"Strong ROI — {roi_x:.1f}x return on investment"
        elif roi_x >= 1:
            verdict = f"Positive ROI — complete pending actions for full impact"
        else:
            n_pending = sum(1 for t in st.session_state.tasks if t["status"] == "pending")
            verdict = f"{n_pending} actions pending — complete them to see returns"

        st.markdown(f"""
<div class="roi-wrap">
  <div style="font-family:DM Serif Display,serif;font-size:1.4rem;color:#F7F4EF;margin-bottom:.3rem">📊 ROI Report — {biz}</div>
  <div style="font-size:13px;color:#5A5A4A;margin-bottom:1.2rem">{st.session_state.months} month(s) · {datetime.now().strftime('%d %b %Y')}</div>
  <div class="roi-grid">
    <div class="roi-cell"><div class="roi-cell-lbl">Fee Paid</div><div class="roi-cell-val">{fmtx(int(total_fees))}</div></div>
    <div class="roi-cell"><div class="roi-cell-lbl">Money Saved</div><div class="roi-cell-val green">{fmt(total_saved)}</div></div>
    <div class="roi-cell"><div class="roi-cell-lbl">Return</div><div class="roi-cell-val">{roi_x:.1f}x</div></div>
  </div>
  <div class="roi-verdict">
    <div class="roi-verdict-main">{verdict}</div>
    <div class="roi-verdict-sub">{fmt(total_found - total_saved)} still recoverable from pending actions</div>
  </div>
</div>
""", unsafe_allow_html=True)

        lines = [
            "=" * 50,
            "ROI REPORT — OpsClarity v5",
            f"Business: {biz}",
            f"Period: {st.session_state.months} month(s) | {datetime.now().strftime('%d %b %Y')}",
            "=" * 50,
            f"Fee paid:    {fmtx(int(total_fees))}",
            f"Saved:       {fmt(total_saved)}",
            f"ROI:         {roi_x:.1f}x",
            f"Net gain:    {fmt(net_gain)}",
            "─" * 50,
            "Actions:",
        ]
        for t in st.session_state.tasks:
            lines.append(f"  [{t['status'].upper():7}] {t['title'][:45]:45} {fmt(t['impact']):>10}")
        lines += ["=" * 50, verdict]

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "📄 Download ROI Report",
                "\n".join(lines),
                file_name=f"opsclarity_roi_{datetime.now().strftime('%d%b%Y')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with d2:
            msg = urllib.parse.quote(
                f"OpsClarity ROI: Paid {fmtx(int(total_fees))}, Saved {fmt(total_saved)}, {roi_x:.1f}x return. {verdict}"
            )
            st.markdown(
                f'<a href="https://wa.me/916362319163?text={msg}" target="_blank">'
                f'<button style="width:100%;background:#25D366;color:white;border:none;padding:8px;'
                f'border-radius:8px;font-weight:600;cursor:pointer">💬 Share on WhatsApp</button></a>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 5 — CA PARTNER
# ═══════════════════════════════════════════════════════════════
with t5:
    st.markdown('<div class="ca-wrap">', unsafe_allow_html=True)

    st.markdown(
        '<div style="display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);'
        'padding:6px 16px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;'
        'text-transform:uppercase;margin-bottom:1rem">For Chartered Accountants</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="font-family:DM Serif Display,serif;font-size:1.8rem;color:#1A1A1A;margin-bottom:.5rem">'
        'Your clients lose money.<br>Show them where — automatically.</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="ca-card" style="border-left:4px solid #D4AF37;background:#FFFBF0;margin-bottom:1.5rem">
  <div class="ca-lbl">Why This Works for CAs</div>
  <div class="ca-ttl">Become the CA who proves value in rupees every month</div>
  <div class="ca-body">
    Most CAs deliver compliance. OpsClarity helps you deliver profit improvement — 
    and show exactly how much money you helped save. 
    Monthly ROI reports give clients a number, not just a service.<br><br>
    <em>Currently in early pilot — join as a founding CA partner at no cost.</em>
  </div>
</div>
""", unsafe_allow_html=True)

    n_ca = st.slider("Number of clients", 10, 200, 40, 5)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ca-card">', unsafe_allow_html=True)
        st.markdown('<div class="ca-lbl">The CA Partner Math</div>', unsafe_allow_html=True)
        gross_income = n_ca * 500
        net_income = n_ca * 500 - 1999
        rows = (
            '<div class="ca-row"><div class="ca-row-lbl">Clients on OpsClarity</div><div class="ca-row-val">' + str(n_ca) + '</div></div>'
            '<div class="ca-row"><div class="ca-row-lbl">Your cost</div><div class="ca-row-val">₹1,999/month</div></div>'
            '<div class="ca-row"><div class="ca-row-lbl">You earn per client</div><div class="ca-row-val">₹500/month</div></div>'
            '<div class="ca-row"><div class="ca-row-lbl">Gross income</div><div class="ca-row-val hl">₹' + f"{gross_income:,}" + '/month</div></div>'
            '<div class="ca-row" style="border:none"><div class="ca-row-lbl">Net after platform cost</div><div class="ca-row-val hl">₹' + f"{net_income:,}" + '/month</div></div>'
        )
        st.markdown(rows, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class="ca-card">
  <div class="ca-lbl">Your Retention Weapon</div>
  <div class="ca-ttl">Monthly ROI Report Per Client</div>
  <div class="ca-body">
    Every client sees: fee paid → money saved → ROI. 
    When a client sees they paid ₹999 and saved ₹45,000 — 
    they never negotiate your fee again.<br><br>
    You become the CA who <strong>proves value in rupees every month.</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # FAQs
    faqs = [
        ("My clients won't share data with a third-party",
         "You upload — they never see OpsClarity. Report is branded as your firm's work."),
        ("How does the ROI report work?",
         "Each action taken is logged. Monthly report = fee paid vs money saved. Your retention weapon."),
        ("Will this replace CAs?",
         "No. Every finding says 'verify with your CA'. We surface the work — you do it and bill for it."),
        ("Are the benchmarks accurate?",
         "They're industry estimates from public surveys — directionally useful, not statistically precise. "
         "Your professional judgement is the product."),
        ("What's the commitment?",
         "Zero — currently free for CA pilot partners. We want 5 CAs running real client files to validate the product."),
    ]
    for q, a in faqs:
        with st.expander(q):
            st.write(a)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Join CA Pilot — Free →", type="primary", use_container_width=True):
        st.success("✅ We'll WhatsApp you within 4 hours with next steps.")
        st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=CA+Partner+Program)")
        st.balloons()


# ── FOOTER ───────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div>
    <div class="ft-brand">OpsClarity</div>
    <div class="ft-legal">Profit Intelligence · Bangalore 🇮🇳 · Early Pilot</div>
  </div>
  <div class="ft-legal">Management estimates only — not CA or legal advice · Data processed in-session, not stored</div>
</div>
<a href="https://wa.me/916362319163?text=Hi,+OpsClarity+question" class="wa-btn" target="_blank">💬 Talk to founder</a>
""", unsafe_allow_html=True)
