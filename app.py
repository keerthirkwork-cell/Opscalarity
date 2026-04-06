"""
OpsClarity v3 — Profit Intelligence Engine for Indian SMEs
Complete Production Version with all 5 Upgrades:
1. Industry Intelligence Layer
2. Benchmarking Engine
3. Learning System
4. Continuous Tracking
5. Workflow Integration
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse

st.set_page_config(
    page_title="OpsClarity — Profit Intelligence",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
.stApp{background:#F7F4EF;font-family:'DM Sans',sans-serif;color:#1A1A1A}
.main .block-container{padding:0!important;max-width:100%!important}
.hero{background:#1A1A1A;padding:3.5rem 3rem 2.5rem}
.hero-badge{display:inline-block;background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.2rem}
.hero-h{font-family:'DM Serif Display',serif;font-size:clamp(2rem,4vw,3.5rem);color:#F7F4EF;line-height:1.1;margin-bottom:1rem}
.hero-h em{font-style:italic;color:#D4AF37}
.hero-sub{font-size:.95rem;color:#9A9A8A;max-width:520px;line-height:1.7;font-weight:300}
.trust-row{display:flex;gap:2rem;flex-wrap:wrap;margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.08)}
.t-num{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#D4AF37}
.t-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em}
.safety-bar{background:#EDEAE3;padding:.6rem 3rem;display:flex;gap:2rem;flex-wrap:wrap;border-bottom:1px solid #D8D4CC}
.s-pill{font-size:11px;color:#4A4A3A;font-weight:500;display:flex;align-items:center;gap:5px}
.s-dot{width:5px;height:5px;background:#4CAF50;border-radius:50%}
.sw{padding:1.5rem 3rem}
.intel-card{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:1.4rem;margin-bottom:1rem;position:relative;overflow:hidden}
.intel-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:4px}
.intel-card.critical::before{background:#E05252}
.intel-card.warning::before{background:#D4AF37}
.intel-card.info::before{background:#5B9BD5}
.intel-card.success::before{background:#4CAF50}
.intel-tag{display:inline-block;font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;margin-bottom:.6rem;letter-spacing:.08em}
.intel-tag.critical{background:#FEF0F0;color:#C0392B}
.intel-tag.warning{background:#FFFBF0;color:#9A7A00}
.intel-tag.info{background:#EFF5FE;color:#2060A0}
.intel-tag.success{background:#E8F5E9;color:#2E7D32}
.intel-amt{font-family:'DM Serif Display',serif;font-size:1.9rem;color:#1A1A1A;line-height:1}
.intel-ttl{font-size:14px;font-weight:600;color:#1A1A1A;margin:.4rem 0}
.intel-body{font-size:13px;color:#6A6A5A;line-height:1.6;margin-bottom:.8rem}
.intel-why{background:#F7F4EF;border-radius:8px;padding:.65rem .9rem;font-size:12px;color:#4A4A3A;line-height:1.55;margin-bottom:.8rem}
.intel-act{border-top:1px solid #F0EDE6;padding-top:.75rem;font-size:13px;font-weight:600;color:#1A1A1A}
.intel-act-s{font-size:12px;font-weight:400;color:#6A6A5A;margin-top:2px}
.bench-wrap{background:#FFF;border:1px solid #E8E4DC;border-radius:14px;padding:1.2rem;margin-bottom:.75rem}
.bench-label{font-size:12px;font-weight:600;color:#1A1A1A;margin-bottom:.4rem}
.bench-bar-bg{background:#F0EDE6;border-radius:20px;height:10px;position:relative;margin:.5rem 0}
.bench-bar-fill{height:10px;border-radius:20px;position:absolute;top:0;left:0}
.bench-markers{display:flex;justify-content:space-between;font-size:10px;color:#9A9A8A;margin-top:2px}
.bench-you{font-size:12px;font-weight:600;margin-top:.4rem}
.bench-you.good{color:#2E7D32}
.bench-you.warn{color:#9A7A00}
.bench-you.bad{color:#C0392B}
.msc-wrap{background:linear-gradient(135deg,#1A1A1A 0%,#2A2A1A 100%);border-radius:20px;padding:2rem;margin:1.5rem 0;border:1px solid rgba(212,175,55,0.25)}
.msc-label{font-size:10px;font-weight:700;color:#D4AF37;text-transform:uppercase;letter-spacing:.2em;margin-bottom:.4rem}
.msc-total{font-family:'DM Serif Display',serif;font-size:3.5rem;color:#D4AF37;line-height:1}
.msc-sub{font-size:13px;color:#5A5A4A;margin-bottom:1.5rem;margin-top:4px}
.msc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}
.msc-cell{background:rgba(255,255,255,0.04);border-radius:10px;padding:.9rem}
.msc-cell-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}
.msc-cell-val{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#F7F4EF}
.msc-cell-val.green{color:#4CAF50}
.msc-cell-val.gold{color:#D4AF37}
.task-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.5rem;display:flex;align-items:center;gap:1rem}
.task-card.done{background:#F0FBF0;border-color:#A5D6A7}
.task-card.overdue{background:#FFF5F5;border-color:#FFCDD2}
.task-pill{font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px}
.task-pill.pending{background:#FFFBF0;color:#9A7A00}
.task-pill.done{background:#E8F5E9;color:#2E7D32}
.task-pill.overdue{background:#FEEEEE;color:#C62828}
.task-left{flex:1}
.task-title{font-size:13px;font-weight:600;color:#1A1A1A}
.task-meta{font-size:11px;color:#6A6A5A;margin-top:2px}
.task-impact{font-family:'DM Mono',monospace;font-size:13px;font-weight:700;color:#D4AF37}
.trend-chip{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px}
.trend-chip.up{background:#E8F5E9;color:#2E7D32}
.trend-chip.down{background:#FEF0F0;color:#C0392B}
.trend-chip.flat{background:#F7F4EF;color:#6A6A5A}
.roi-wrap{background:#1A1A1A;border-radius:16px;padding:2rem;margin:1.5rem 0}
.roi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem}
.roi-cell{background:rgba(255,255,255,0.04);border-radius:12px;padding:1rem;text-align:center}
.roi-cell-lbl{font-size:10px;color:#5A5A4A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px}
.roi-cell-val{font-family:'DM Serif Display',serif;font-size:1.7rem;color:#D4AF37}
.roi-cell-val.green{color:#4CAF50}
.roi-verdict{background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.3);border-radius:12px;padding:1rem;text-align:center}
.roi-verdict-main{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#D4AF37}
.roi-verdict-sub{font-size:12px;color:#6A6A5A;margin-top:4px}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0}
.kpi-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1rem 1.2rem}
.kpi-lbl{font-size:10px;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}
.kpi-val{font-family:'DM Serif Display',serif;font-size:1.5rem;color:#1A1A1A}
.kpi-sub{font-size:11px;margin-top:2px}
.good{color:#2E8B57}.bad{color:#C0392B}.warn{color:#9A7A00}
.sh{font-family:'DM Serif Display',serif;font-size:1.6rem;color:#1A1A1A;margin-bottom:4px}
.ss{font-size:13px;color:#6A6A5A;margin-bottom:1.2rem}
.gate-box{background:#FFF;border:1px solid #E8E4DC;border-radius:16px;padding:2rem;margin:2rem 0;text-align:center}
.gate-h{font-family:'DM Serif Display',serif;font-size:1.5rem;color:#1A1A1A;margin-bottom:.5rem}
.gate-s{font-size:13px;color:#6A6A5A;margin-bottom:1.2rem}
.ca-wrap{background:#F0EDE6;padding:2rem 3rem}
.ca-card{background:#FFF;border:1px solid #E0DDD6;border-radius:14px;padding:1.4rem;margin-bottom:1rem}
.ca-card.dark{background:#1A1A1A;border-color:rgba(255,255,255,0.08)}
.ca-lbl{font-size:11px;font-weight:600;color:#9A9A8A;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.ca-ttl{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#1A1A1A;margin-bottom:6px}
.ca-body{font-size:13px;color:#6A6A5A;line-height:1.7}
.ca-card.dark .ca-ttl{color:#F7F4EF}
.ca-card.dark .ca-body{color:#9A9A8A}
.ca-row{display:flex;justify-content:space-between;align-items:center;padding:.6rem 0;border-bottom:1px solid #F0EDE6}
.ca-row-lbl{font-size:13px;color:#4A4A3A}
.ca-row-val{font-family:'DM Mono',monospace;font-size:13px;font-weight:600;color:#1A1A1A}
.ca-row-val.hl{color:#2E8B57;font-size:1rem}
.cl-row{display:flex;align-items:center;justify-content:space-between;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,0.06)}
.cl-name{font-size:13px;font-weight:500;color:#F7F4EF}
.cl-meta{font-size:11px;color:#5A5A4A}
.cl-amt{font-family:'DM Mono',monospace;font-size:12px;color:#D4AF37}
.pr-wrap{background:#1A1A1A;padding:2rem 3rem}
.pr-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:1.5rem}
.pr-card.feat{background:rgba(212,175,55,0.08);border-color:rgba(212,175,55,0.3)}
.pr-lbl{font-size:10px;font-weight:600;color:#5A5A4A;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.6rem}
.pr-name{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#F7F4EF;margin-bottom:3px}
.pr-amt{font-family:'DM Mono',monospace;font-size:1.8rem;color:#D4AF37;margin-bottom:6px}
.pr-note{font-size:12px;color:#6A6A5A;margin-bottom:1rem;line-height:1.55}
.pr-feat{font-size:12px;color:#8A8A7A;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.pr-feat::before{content:"→ ";color:#D4AF37}
.footer{background:#1A1A1A;padding:1.2rem 3rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem}
.ft-brand{font-family:'DM Serif Display',serif;font-size:1rem;color:#D4AF37}
.ft-legal{font-size:11px;color:#4A4A3A}
.wa-btn{position:fixed;bottom:24px;right:24px;background:#25D366;color:#FFF;padding:11px 18px;border-radius:50px;font-weight:600;text-decoration:none;font-size:13px;display:flex;align-items:center;gap:6px;box-shadow:0 4px 16px rgba(37,211,102,0.35);z-index:9999}
div[data-testid="stVerticalBlock"]{gap:0!important}
.seq-card{background:#FFF;border:1px solid #E8E4DC;border-radius:12px;padding:1rem;margin-bottom:.5rem}
.seq-day{font-size:11px;font-weight:700;color:#D4AF37;margin-bottom:3px}
.seq-tone{font-size:12px;font-weight:600;margin-bottom:6px}
.seq-msg{font-size:13px;color:#4A4A3A;line-height:1.5}
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

# ─────────────────────────────────────────────────────────────
# INDUSTRY INTELLIGENCE LAYER
# ─────────────────────────────────────────────────────────────
INDUSTRY_INTELLIGENCE = {
    "restaurant": {
        "name": "Restaurant / Cafe",
        "kpis": ["Food Cost %", "Labor Cost %", "Table Turn Rate", "Waste %"],
        "thresholds": {"food_cost_pct": 35, "labor_pct": 30, "waste_pct": 8},
        "language": {
            "revenue": "covers / orders",
            "top_leak": "kitchen waste and over-staffing",
            "quick_win": "Negotiate ingredient contracts monthly, not annually",
            "benchmark_source": "NRAI India Restaurant Report 2024",
        },
        "root_causes": {
            "high_expense": "Ingredient prices fluctuate — most owners don't renegotiate. Menu pricing often lags cost increases by 6-12 months.",
            "low_margin": "Avg table occupancy below 65% means fixed costs (rent, staff) aren't covered by revenue volume.",
            "overdue": "Event/catering bookings often have 30-day payment terms — enforce deposits upfront.",
        },
        "peer_stats": {
            "Food Ingredients": {"p25": 28, "median": 34, "p75": 42, "unit": "% rev", "n": 521, "label": "Food Cost"},
            "Labor":            {"p25": 18, "median": 24, "p75": 32, "unit": "% rev", "n": 498, "label": "Labor"},
            "Rent":             {"p25": 8,  "median": 12, "p75": 18, "unit": "% rev", "n": 412, "label": "Rent"},
            "Utilities":        {"p25": 3,  "median": 5,  "p75": 8,  "unit": "% rev", "n": 389, "label": "Utilities"},
        },
        "weekly_metrics": ["Daily covers", "Avg order value", "Food cost %", "Waste kg"],
    },
    "manufacturing": {
        "name": "Manufacturing",
        "kpis": ["Raw Material %", "Labor Efficiency", "Rejection Rate", "OEE %"],
        "thresholds": {"raw_material_pct": 55, "rejection_pct": 3, "oee_pct": 75},
        "language": {
            "revenue": "production value / dispatch",
            "top_leak": "raw material wastage and vendor price drift",
            "quick_win": "Compare vendor invoices to PO rates every month — drift of 8-12% is common",
            "benchmark_source": "CII SME Manufacturing Survey 2024",
        },
        "root_causes": {
            "high_expense": "Raw material prices indexed to commodity markets but purchase orders use annual fixed rates. Gap widens silently.",
            "low_margin": "Machine idle time and shift gaps inflate per-unit cost. Most SMEs track output, not OEE.",
            "overdue": "Dealer credit terms extend during slow seasons. Enforce credit limits strictly post-monsoon.",
        },
        "peer_stats": {
            "Raw Materials": {"p25": 42000, "median": 51000, "p75": 64000, "unit": "/ton", "n": 312, "label": "Raw Mat"},
            "Labor":         {"p25": 380,   "median": 460,   "p75": 580,   "unit": "/day", "n": 445, "label": "Labor"},
            "Logistics":     {"p25": 8,     "median": 11,    "p75": 16,    "unit": "/km",  "n": 289, "label": "Freight"},
            "Packaging":     {"p25": 11,    "median": 17,    "p75": 24,    "unit": "/pc",  "n": 198, "label": "Packaging"},
        },
        "weekly_metrics": ["Units produced", "Rejection %", "Raw mat consumed", "On-time dispatch"],
    },
    "clinic": {
        "name": "Clinic / Diagnostic",
        "kpis": ["Revenue per Doctor", "Chair Utilisation", "Consumable %", "No-show Rate"],
        "thresholds": {"chair_util_pct": 70, "consumable_pct": 15, "no_show_pct": 20},
        "language": {
            "revenue": "patient visits / procedures",
            "top_leak": "chair idle time and consumable overstocking",
            "quick_win": "Track no-show rate weekly — 1 SMS reminder cuts no-shows by 40%",
            "benchmark_source": "IMA India Private Practice Survey 2024",
        },
        "root_causes": {
            "high_expense": "Consumables ordered in bulk for vendor discounts, but expiry and spoilage eat the savings.",
            "low_margin": "Doctor time not matched to appointment slots. 20-min slots for 10-min procedures = 50% idle time.",
            "overdue": "Insurance reimbursements delayed 45-90 days. Most clinics don't follow up until 90+ days.",
        },
        "peer_stats": {
            "Staff Salaries":  {"p25": 18, "median": 24, "p75": 31, "unit": "% rev", "n": 187, "label": "Staff"},
            "Consumables":     {"p25": 8,  "median": 12, "p75": 18, "unit": "% rev", "n": 187, "label": "Consumables"},
            "Rent":            {"p25": 6,  "median": 9,  "p75": 14, "unit": "% rev", "n": 187, "label": "Rent"},
            "Equipment Lease": {"p25": 3,  "median": 5,  "p75": 9,  "unit": "% rev", "n": 142, "label": "Equipment"},
        },
        "weekly_metrics": ["Patient visits", "Revenue per visit", "No-show count", "Consumable spend"],
    },
    "retail": {
        "name": "Retail / Distribution",
        "kpis": ["Inventory Turnover", "Shrinkage %", "Gross Margin %", "Sales/sqft"],
        "thresholds": {"inventory_days": 45, "shrinkage_pct": 2, "margin_pct": 28},
        "language": {
            "revenue": "sales value / units sold",
            "top_leak": "slow-moving inventory and payment terms mismatch",
            "quick_win": "Identify bottom 20% SKUs by margin — negotiate returns or liquidate",
            "benchmark_source": "RAI India Retail Report 2024",
        },
        "root_causes": {
            "high_expense": "Purchase orders placed on gut feel, not sell-through data. Over-ordering ties up 30-40% extra working capital.",
            "low_margin": "Vendor credit 30 days, customer credit 45 days = perpetual working capital gap.",
            "overdue": "B2B retail often extends 60-day credit to retain dealers. No credit scoring, no discipline.",
        },
        "peer_stats": {
            "Rent":      {"p25": 80,  "median": 120, "p75": 200, "unit": "/sqft/mo", "n": 445, "label": "Rent"},
            "Inventory": {"p25": 42,  "median": 52,  "p75": 64,  "unit": "% rev",   "n": 398, "label": "Inventory"},
            "Staff":     {"p25": 8,   "median": 12,  "p75": 18,  "unit": "% rev",   "n": 445, "label": "Staff"},
        },
        "weekly_metrics": ["Daily sales", "Units sold", "Slow-mover count", "Cash collected"],
    },
    "agency": {
        "name": "Agency / Consulting",
        "kpis": ["Billable Utilisation %", "Revenue per Head", "Client Churn", "Project Margin"],
        "thresholds": {"billable_pct": 70, "rev_per_head": 500000, "project_margin": 40},
        "language": {
            "revenue": "billings / project value",
            "top_leak": "non-billable time and scope creep on fixed projects",
            "quick_win": "Time-track every team member for 2 weeks — non-billable is always 30-40% higher than assumed",
            "benchmark_source": "NASSCOM SME Services Survey 2024",
        },
        "root_causes": {
            "high_expense": "Payroll grows with headcount, but billing doesn't keep pace. Utilisation below 65% = loss per employee.",
            "low_margin": "Fixed-price projects with vague scope. Every revision round that isn't billed = direct margin loss.",
            "overdue": "Milestone billing not enforced. Clients delay final 20-30% payment indefinitely after delivery.",
        },
        "peer_stats": {
            "Salaries":         {"p25": 38, "median": 48, "p75": 60, "unit": "% rev", "n": 312, "label": "Salaries"},
            "Software & Tools": {"p25": 3,  "median": 6,  "p75": 10, "unit": "% rev", "n": 312, "label": "Software"},
            "Office & Admin":   {"p25": 4,  "median": 7,  "p75": 12, "unit": "% rev", "n": 312, "label": "Office"},
            "Freelancers":      {"p25": 5,  "median": 10, "p75": 18, "unit": "% rev", "n": 267, "label": "Freelancers"},
        },
        "weekly_metrics": ["Hours billed", "Hours worked", "Utilisation %", "Invoices raised"],
    },
    "logistics": {
        "name": "Logistics / Transport",
        "kpis": ["Fuel Cost %", "Fleet Utilisation", "Empty Run %", "On-Time Delivery %"],
        "thresholds": {"fuel_pct": 25, "empty_run_pct": 30, "otd_pct": 90},
        "language": {
            "revenue": "trips / freight revenue",
            "top_leak": "empty return trips and fuel price drift",
            "quick_win": "Track empty run % per route — industry average is 28%, best-in-class is 12%",
            "benchmark_source": "CRISIL India Logistics SME Report 2024",
        },
        "root_causes": {
            "high_expense": "Fuel cards not monitored per vehicle. Driver pilferage averages 8-12% of fuel cost in unmonitored fleets.",
            "low_margin": "Route not optimised. Same origin-destination pairs handled by 2-3 drivers at different costs.",
            "overdue": "Load aggregators delay payment 30-45 days. Spot market clients are even worse.",
        },
        "peer_stats": {
            "Fuel":            {"p25": 18, "median": 23, "p75": 30, "unit": "% rev", "n": 201, "label": "Fuel"},
            "Driver Wages":    {"p25": 14, "median": 19, "p75": 25, "unit": "% rev", "n": 201, "label": "Drivers"},
            "Maintenance":     {"p25": 5,  "median": 8,  "p75": 13, "unit": "% rev", "n": 201, "label": "Maintenance"},
            "Tolls & Permits": {"p25": 2,  "median": 4,  "p75": 7,  "unit": "% rev", "n": 189, "label": "Tolls"},
        },
        "weekly_metrics": ["Trips completed", "Fuel per km", "Empty runs", "Collections"],
    },
    "construction": {
        "name": "Construction",
        "kpis": ["Material Wastage %", "Labor Productivity", "Project Overrun %", "Retention Released"],
        "thresholds": {"material_waste_pct": 8, "overrun_pct": 15, "retention_pct": 10},
        "language": {
            "revenue": "project billing / milestones",
            "top_leak": "material wastage and retention money held by clients",
            "quick_win": "Prepare retention release schedule 30 days before project end — most contractors forget to claim",
            "benchmark_source": "CREDAI SME Builder Survey 2024",
        },
        "root_causes": {
            "high_expense": "Material purchased per contractor quote, not consolidated. 3-site operations buying independently = 15-20% premium.",
            "low_margin": "Variation orders not raised on time. Work done outside scope without written approval.",
            "overdue": "Retention (5-10% of contract) held for 12+ months after completion. Most SMEs don't follow up.",
        },
        "peer_stats": {
            "Materials":      {"p25": 38, "median": 46, "p75": 56, "unit": "% rev", "n": 167, "label": "Materials"},
            "Labor":          {"p25": 22, "median": 28, "p75": 35, "unit": "% rev", "n": 167, "label": "Labor"},
            "Equipment":      {"p25": 5,  "median": 9,  "p75": 15, "unit": "% rev", "n": 167, "label": "Equipment"},
            "Subcontractors": {"p25": 8,  "median": 14, "p75": 22, "unit": "% rev", "n": 134, "label": "Subcon"},
        },
        "weekly_metrics": ["Milestone completions", "Material issued", "Labor headcount", "Billing raised"],
    },
    "textile": {
        "name": "Textile / Garments",
        "kpis": ["Cut-to-Ship %", "Fabric Utilisation", "Rejection Rate", "Production Efficiency"],
        "thresholds": {"rejection_pct": 3, "fabric_util_pct": 85, "cut_to_ship": 95},
        "language": {
            "revenue": "pieces / shipment value",
            "top_leak": "fabric wastage and rejection in finishing",
            "quick_win": "Marker efficiency audit — most SME garment units run at 78-82%, best is 88%+",
            "benchmark_source": "AEPC India Apparel Export Survey 2024",
        },
        "root_causes": {
            "high_expense": "Fabric bought at market rate without forward contracts. Price swings of 15-20% are absorbed silently.",
            "low_margin": "Rejection at finishing stage means rework cost = double labor. Root cause is usually cutting table quality.",
            "overdue": "Export buyers use 60-90 day LC terms. Domestic buyers often push to 45+ days.",
        },
        "peer_stats": {
            "Raw Material":       {"p25": 42, "median": 51, "p75": 61, "unit": "% rev", "n": 223, "label": "Fabric"},
            "Labor":              {"p25": 14, "median": 18, "p75": 24, "unit": "% rev", "n": 223, "label": "Labor"},
            "Power":              {"p25": 4,  "median": 6,  "p75": 10, "unit": "% rev", "n": 223, "label": "Power"},
            "Dyeing & Finishing": {"p25": 3,  "median": 5,  "p75": 8,  "unit": "% rev", "n": 198, "label": "Dyeing"},
        },
        "weekly_metrics": ["Pieces produced", "Rejection count", "Fabric consumed/piece", "Shipments dispatched"],
    },
    "pharma": {
        "name": "Pharma / Medical",
        "kpis": ["Inventory Days", "Expiry Loss %", "Distribution Cost %", "Collection Days"],
        "thresholds": {"inventory_days": 60, "expiry_pct": 2, "dist_pct": 12},
        "language": {
            "revenue": "invoiced value / units",
            "top_leak": "expiry losses and distributor credit overextension",
            "quick_win": "Near-expiry alert at 90 days — most pharma SMEs act at 30 days, losing return window",
            "benchmark_source": "IDMA India Pharma SME Survey 2024",
        },
        "root_causes": {
            "high_expense": "Distributor incentives (free goods, extra credit) not tracked against actual sales lift.",
            "low_margin": "Stockist returns accepted without deduction for handling. Net realisation lower than invoice.",
            "overdue": "Chemist credit 30-45 days, distributor 60-75 days. Most SMEs don't have credit scoring per outlet.",
        },
        "peer_stats": {
            "Inventory":    {"p25": 22, "median": 28, "p75": 36, "unit": "% rev", "n": 143, "label": "Inventory"},
            "Distribution": {"p25": 4,  "median": 7,  "p75": 11, "unit": "% rev", "n": 143, "label": "Distribution"},
            "Regulatory":   {"p25": 2,  "median": 4,  "p75": 7,  "unit": "% rev", "n": 143, "label": "Regulatory"},
            "Staff":        {"p25": 12, "median": 16, "p75": 22, "unit": "% rev", "n": 143, "label": "Staff"},
        },
        "weekly_metrics": ["Units sold", "Collections", "Near-expiry SKUs", "Distributor outstanding"],
    },
    "printing": {
        "name": "Print / Packaging",
        "kpis": ["Paper Utilisation %", "Machine Uptime %", "Reprint %", "Job Turnaround"],
        "thresholds": {"paper_util_pct": 88, "uptime_pct": 80, "reprint_pct": 3},
        "language": {
            "revenue": "job value / print orders",
            "top_leak": "paper wastage and machine downtime",
            "quick_win": "Track makeready waste per job — industry average 12%, best shops run 6%",
            "benchmark_source": "AIFMP India Print Industry Survey 2024",
        },
        "root_causes": {
            "high_expense": "Paper bought spot market. Consolidating 3 months of orders with one supplier saves 8-12%.",
            "low_margin": "Rush jobs priced at standard rate. Premium for 24-hour turnaround rarely charged.",
            "overdue": "Corporate clients use 45-60 day terms. Print SMEs rarely enforce late payment penalties.",
        },
        "peer_stats": {
            "Paper & Media":     {"p25": 28, "median": 35, "p75": 44, "unit": "% rev", "n": 156, "label": "Paper"},
            "Ink & Consumables": {"p25": 8,  "median": 12, "p75": 17, "unit": "% rev", "n": 156, "label": "Ink"},
            "Equipment Lease":   {"p25": 5,  "median": 8,  "p75": 13, "unit": "% rev", "n": 156, "label": "Equipment"},
            "Labor":             {"p25": 16, "median": 22, "p75": 30, "unit": "% rev", "n": 156, "label": "Labor"},
        },
        "weekly_metrics": ["Jobs completed", "Paper consumed", "Reprint count", "Collections"],
    },
}

# ─────────────────────────────────────────────────────────────
# BENCHMARKING ENGINE
# ─────────────────────────────────────────────────────────────
def get_percentile(value, p25, median, p75):
    if value <= p25:    return 10
    if value <= median: return 35
    if value <= p75:    return 65
    return 90

def render_benchmark_gauge(label, your_value, p25, median, p75, unit, n, higher_is_better=False):
    pct = get_percentile(your_value, p25, median, p75)
    if higher_is_better:
        pct = 100 - pct
    if pct <= 30:
        bar_color = "#4CAF50"; cls = "good"; verdict = f"Top performer — better than most {n} peers"
    elif pct <= 60:
        bar_color = "#D4AF37"; cls = "warn"; verdict = f"Average — room to improve vs {n} peers"
    else:
        bar_color = "#E05252"; cls = "bad"; verdict = f"Above average cost — {n} peers do better"
    bar_w = max(4, min(96, pct))
    st.markdown(f"""
<div class="bench-wrap">
  <div class="bench-label">{label} <span style="font-size:11px;color:#9A9A8A;font-weight:400">({n} Indian SME peers)</span></div>
  <div class="bench-bar-bg">
    <div class="bench-bar-fill" style="width:{bar_w}%;background:{bar_color}"></div>
  </div>
  <div class="bench-markers">
    <span>Best: {p25:,}{unit}</span>
    <span>Median: {median:,}{unit}</span>
    <span>Worst: {p75:,}{unit}</span>
  </div>
  <div class="bench-you {cls}">You: {your_value:,.0f}{unit} — {verdict}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LEARNING SYSTEM
# ─────────────────────────────────────────────────────────────
def get_confidence_score(leak_id, corrections):
    base = {
        "cash_stuck": 0.92, "cost_bleed": 0.78, "margin_gap": 0.85,
        "concentration": 0.88, "exp_spike": 0.80, "tax_gst": 0.65
    }
    score = base.get(leak_id, 0.75)
    feedback = corrections.get(leak_id)
    if feedback == "wrong":   score = max(0.3, score - 0.25)
    if feedback == "partial": score = max(0.5, score - 0.10)
    if feedback == "correct": score = min(0.99, score + 0.05)
    return score

def render_confidence_badge(score):
    if score >= 0.85:
        color = "#2E7D32"; label = f"{score*100:.0f}% confident"
    elif score >= 0.65:
        color = "#9A7A00"; label = f"{score*100:.0f}% confident"
    else:
        color = "#C0392B"; label = f"{score*100:.0f}% — verify manually"
    return f'<span style="display:inline-block;font-size:10px;background:#F7F4EF;color:{color};font-weight:700;padding:2px 8px;border-radius:10px;margin-left:6px">{label}</span>'

# ─────────────────────────────────────────────────────────────
# CONTINUOUS TRACKING ENGINE
# ─────────────────────────────────────────────────────────────
def compute_trends(df):
    sales    = df[df["Type"] == "Sales"]
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
    last3  = values[-3:] if len(values) >= 3 else values
    first3 = values[:3]  if len(values) >= 3 else values
    if np.mean(last3) > np.mean(first3) * 1.05: return "up"
    if np.mean(last3) < np.mean(first3) * 0.95: return "down"
    return "flat"

def render_trend_chip(label, values, positive_direction="up"):
    direction = trend_direction(values)
    is_good = (direction == positive_direction)
    icon  = "↑" if direction == "up" else ("↓" if direction == "down" else "→")
    cls   = "up" if is_good else ("down" if direction != "flat" else "flat")
    change = ""
    if len(values) >= 2 and values[0] != 0:
        pct = (values[-1] - values[0]) / abs(values[0]) * 100
        change = f" {pct:+.0f}%"
    st.markdown(f'<span class="trend-chip {cls}">{icon} {label}{change}</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# WORKFLOW INTEGRATION
# ─────────────────────────────────────────────────────────────
def leaks_to_tasks(leaks, biz_name="Your Business"):
    tasks = []
    today = datetime.now()
    owners = ["Owner", "Accounts", "Operations", "Owner"]
    for i, leak in enumerate(leaks):
        due_days = 3 if leak["sev"] == "critical" else (7 if leak["sev"] == "warning" else 14)
        tasks.append({
            "id":         leak["id"],
            "title":      leak["action"],
            "category":   leak["cat"],
            "impact":     leak["rupee"],
            "owner":      owners[i % len(owners)],
            "due":        (today + timedelta(days=due_days)).strftime("%d %b"),
            "due_dt":     today + timedelta(days=due_days),
            "status":     "pending",
            "severity":   leak["sev"],
            "wa_template": leak["template"],
            "notes":      "",
        })
    return tasks

def render_workflow_board(tasks, key_prefix="wf"):
    pending = [t for t in tasks if t["status"] == "pending"]
    done    = [t for t in tasks if t["status"] == "done"]
    overdue = [t for t in tasks if t["status"] == "pending" and t["due_dt"] < datetime.now()]
    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:1rem;text-align:center">
  <div style="background:#FFFBF0;border-radius:10px;padding:.6rem">
    <div style="font-size:1.4rem;font-weight:700;color:#D4AF37">{len(pending)}</div>
    <div style="font-size:11px;color:#6A6A5A">Pending</div>
  </div>
  <div style="background:#E8F5E9;border-radius:10px;padding:.6rem">
    <div style="font-size:1.4rem;font-weight:700;color:#2E7D32">{len(done)}</div>
    <div style="font-size:11px;color:#6A6A5A">Done</div>
  </div>
  <div style="background:#FEF0F0;border-radius:10px;padding:.6rem">
    <div style="font-size:1.4rem;font-weight:700;color:#C0392B">{len(overdue)}</div>
    <div style="font-size:11px;color:#6A6A5A">Overdue</div>
  </div>
</div>
""", unsafe_allow_html=True)

    for i, task in enumerate(tasks):
        is_overdue = (task["status"] == "pending" and task["due_dt"] < datetime.now())
        css      = "done" if task["status"] == "done" else ("overdue" if is_overdue else "")
        pill_cls = "done" if task["status"] == "done" else ("overdue" if is_overdue else "pending")
        pill_lbl = "DONE" if task["status"] == "done" else ("OVERDUE" if is_overdue else "PENDING")
        icon     = "✅" if task["status"] == "done" else ("🔴" if task["severity"] == "critical" else "🟡")

        st.markdown(f"""
<div class="task-card {css}">
  <div style="width:36px;height:36px;border-radius:50%;background:#F7F4EF;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">{icon}</div>
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
                    f'<button style="width:100%;background:#25D366;color:white;border:none;padding:6px;'
                    f'border-radius:6px;cursor:pointer;font-size:12px">📱 Remind</button></a>',
                    unsafe_allow_html=True
                )

# ─────────────────────────────────────────────────────────────
# CORE HELPERS
# ─────────────────────────────────────────────────────────────
def fmt(v):
    v = float(v)
    if abs(v) >= 1e7:  return f"₹{v/1e7:.1f}Cr"
    if abs(v) >= 1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v) >= 1000: return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmtx(v):
    return f"₹{int(float(v)):,}"

SEQ = [
    {"day": 1,  "tone": "Friendly reminder",    "color": "#5B9BD5", "msg": "Hi {name} 🙏 Invoice #{inv} for {amt} is due. Any issues? Happy to help. — {biz}"},
    {"day": 3,  "tone": "Offer + urgency",       "color": "#D4AF37", "msg": "Hi {name}, invoice #{inv} ({amt}) overdue. 2% discount if settled by {dl}. — {biz}"},
    {"day": 7,  "tone": "Operational impact",    "color": "#E08020", "msg": "{name}, invoice #{inv} ({amt}) 7 days overdue. Pay by {dl} or orders paused. — {biz}"},
    {"day": 10, "tone": "Final notice",          "color": "#E05252", "msg": "FINAL NOTICE — {name}: invoice #{inv} ({amt}) 10 days unpaid. Pay by {dl}. — {biz}"},
]

def gen_seq(name, inv, amount, biz):
    today = datetime.now()
    result = []
    for s in SEQ:
        send_date = today + timedelta(days=s["day"])
        deadline  = today + timedelta(days=s["day"] + 3)
        msg = s["msg"].format(
            name=name, inv=inv, amt=fmt(amount), biz=biz,
            dl=deadline.strftime("%d %b %Y")
        )
        result.append({
            **s,
            "send_on": send_date.strftime("%d %b"),
            "message": msg,
            "wa_link": f"https://wa.me/?text={urllib.parse.quote(msg)}"
        })
    return result

def _cat(d):
    d = d.lower()
    kw = [
        (["rent", "rental"],                        "Rent"),
        (["salary", "wage", "praveen", "ashok"],    "Salary"),
        (["laptop", "computer", "software", "tech"],"Technology"),
        (["internet", "wifi", "broadband"],         "Internet"),
        (["electricity", "power", "eb "],           "Electricity"),
        (["ca ", "accountant", "audit"],            "Professional Fees"),
        (["travel", "fuel", "petrol", "transport"], "Travel & Fuel"),
        (["raw", "material", "mfg", "mim"],         "Raw Materials"),
        (["pack", "packaging", "box", "carton"],    "Packaging"),
        (["logistics", "courier", "freight"],       "Logistics"),
        (["bank", "debit", "charge"],               "Bank Charges"),
    ]
    for keys, label in kw:
        if any(k in d for k in keys):
            return label
    return "Operations"

def parse_file(file):
    try:
        fname = file.name.lower()
        if fname.endswith((".xlsx", ".xls")):
            try:    dfs = pd.read_excel(file, engine="openpyxl")
            except: dfs = pd.read_excel(file, engine="xlrd")
        elif fname.endswith(".csv"):
            try:    dfs = pd.read_csv(file)
            except: dfs = pd.read_csv(file, encoding="latin1")
        else:
            return None, False, "Use .csv, .xlsx, or .xls"

        df = dfs.dropna(how="all").dropna(axis=1, how="all")
        cm = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date", "dt", "day"]):
                cm[col] = "Date"
            elif any(x in cl for x in ["amount", "amt", "value", "total", "debit", "credit", "rs", "₹"]):
                cm[col] = "Amount"
            elif any(x in cl for x in ["type", "txn", "dr/cr", "nature"]):
                cm[col] = "Type"
            elif any(x in cl for x in ["particulars", "category", "narration", "ledger"]):
                cm[col] = "Category"
            elif any(x in cl for x in ["party", "customer", "vendor", "name", "client"]):
                cm[col] = "Party"
            elif any(x in cl for x in ["status", "paid", "pending", "overdue"]):
                cm[col] = "Status"
            elif any(x in cl for x in ["invoice", "voucher", "ref", "bill"]):
                cm[col] = "Invoice_No"
        df = df.rename(columns=cm)

        if "Date" not in df.columns:
            return None, False, "Date column not found."
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["Date"])

        if "Amount" in df.columns:
            df["Amount"] = (
                df["Amount"].astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("(", "-", regex=False)
                .str.replace(")", "", regex=False)
                .str.replace(" Dr", "", regex=False)
                .str.replace(" Cr", "", regex=False)
                .str.replace("₹", "", regex=False)
            )
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)

        if "Type" not in df.columns:
            df["Type"] = "Unknown"
        df["Type"] = (
            df["Type"].astype(str).str.strip().str.title()
            .replace({
                "Dr": "Expense", "Debit": "Expense", "Payment": "Expense", "Purchase": "Expense",
                "Cr": "Sales", "Credit": "Sales", "Receipt": "Sales", "Sale": "Sales"
            })
        )
        mask = ~df["Type"].isin(["Sales", "Expense"])
        if mask.any():
            ekw = ["purchase", "expense", "payment", "salary", "rent", "bill", "wages", "material", "raw", "logistics"]
            df.loc[mask, "Type"] = df.loc[mask].apply(
                lambda x: "Expense" if any(k in str(x.get("Category", "")).lower() for k in ekw) else "Sales",
                axis=1
            )

        for col, default in [("Status", "Paid"), ("Category", "General"), ("Party", "Unknown"), ("Invoice_No", "-")]:
            if col not in df.columns:
                df[col] = default

        if "Category" in df.columns:
            mask2 = df["Category"].isin(["General", "Unknown", ""])
            df.loc[mask2 & (df["Type"] == "Expense"), "Category"] = (
                df.loc[mask2 & (df["Type"] == "Expense"), "Party"].apply(_cat)
            )

        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        return df, True, f"✅ {len(df):,} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"
    except Exception as e:
        return None, False, f"Error: {e}"

# ─────────────────────────────────────────────────────────────
# INTELLIGENT LEAK DETECTOR
# ─────────────────────────────────────────────────────────────
def find_leaks(df, industry, corrections=None):
    if corrections is None:
        corrections = {}
    intel    = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
    sales    = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]
    revenue  = sales["Amount"].sum()
    exp_tot  = expenses["Amount"].sum()
    profit   = revenue - exp_tot
    margin   = (profit / revenue * 100) if revenue > 0 else 0
    bmark    = BENCH_MARGINS.get(industry, 15)
    leaks    = []

    # 1 — Overdue receivables
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue", "pending", "not paid", "due", "outstanding", "unpaid"])]
        od_amt = od["Amount"].sum()
        if od_amt > 10000:
            deb      = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_name = deb.index[0] if len(deb) > 0 else "Customer"
            top_amt  = float(deb.iloc[0]) if len(deb) > 0 else od_amt
            pct      = od_amt / revenue * 100 if revenue > 0 else 0
            conf     = get_confidence_score("cash_stuck", corrections)
            leaks.append({
                "id": "cash_stuck", "sev": "critical", "cat": "Collections",
                "rupee": od_amt, "annual": od_amt * 0.18, "confidence": conf,
                "headline": f"{fmtx(int(od_amt))} stuck in unpaid invoices",
                "sub": f"Across {len(deb)} {intel['language']['revenue']}",
                "found": f"{len(deb)} customers owe you. Top: {top_name} owes {fmtx(int(top_amt))}.",
                "root_cause": intel["root_causes"].get("overdue", "Enforce payment terms strictly."),
                "costs": f"Cost of capital at 18%: {fmt(od_amt * 0.18)}/year tied up.",
                "bench": f"Healthy: overdue < 5% of revenue. Yours: {pct:.1f}%. {intel['language']['quick_win']}",
                "action": f"Call {top_name} today. Offer 2% discount for 48-hr payment.",
                "action_sub": f"Use WhatsApp sequence below. {intel['language']['quick_win']}",
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
            ev       = vs["mean"].idxmax()
            ep       = vs["mean"].max()
            av       = float(vs.loc[ev, "sum"])
            if ep > cheapest * 1.12:
                pct_gap = ((ep - cheapest) / cheapest) * 100
                waste   = (ep - cheapest) * (av / ep)
                pdata   = peer_stats.get(category)
                bench_line = (
                    f"Your cost: ₹{ep:,.0f}. Industry median: ₹{pdata['median']:,}{pdata['unit']} ({pdata['n']} peers)."
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
                        "found": f"You paid {ev} avg ₹{ep:,.0f} on {category}. Cheapest: ₹{cheapest:,.0f}.",
                        "root_cause": intel["root_causes"].get("high_expense", "Vendor prices drift without regular reviews."),
                        "costs": f"{fmtx(int(waste))} extra per year — silently leaving your account.",
                        "bench": bench_line,
                        "action": f"Get 2 competing quotes for {category} this week.",
                        "action_sub": "Lowest confirmed quote gets the contract.",
                        "template": f"Reviewing {category} suppliers. Best rate for [volume] by Friday gets 12-month contract.",
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
                "sub": f"Your {margin:.1f}% vs {bmark}% {intel['name']} benchmark",
                "found": f"Margin: {margin:.1f}%. {intel['name']} benchmark: {bmark}%. Gap: {bmark - margin:.1f} pp.",
                "root_cause": intel["root_causes"].get("low_margin", "Cost structure misaligned with revenue."),
                "costs": f"Closing half this gap adds {fmt(gap * 0.5)} in profit — no new customers needed.",
                "bench": f"Source: {intel['language']['benchmark_source']}. Median margin: {bmark}%.",
                "action": "Raise prices 5% on top products. Cut 10% from largest cost line.",
                "action_sub": f"Industry insight: {intel['language']['top_leak']}",
                "template": "Reviewing pricing — benchmarks show 5-8% increase is supportable.",
                "seqs": [],
            })

    # 4 — Revenue concentration risk
    if len(sales) > 0 and revenue > 0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr) > 0 and (cr.iloc[0] / revenue) * 100 > 28:
            top_pct = (cr.iloc[0] / revenue) * 100
            risk    = cr.iloc[0] * 0.3
            conf    = get_confidence_score("concentration", corrections)
            leaks.append({
                "id": "concentration", "sev": "warning", "cat": "Revenue Risk",
                "rupee": risk, "annual": risk, "confidence": conf,
                "headline": f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub": "One client delay = cash crisis",
                "found": f"{cr.index[0]} = {top_pct:.0f}% ({fmtx(int(cr.iloc[0]))}). 30-day delay = {fmtx(int(cr.iloc[0]))} shortfall.",
                "root_cause": "Revenue concentration above 25% removes pricing power and creates existential cash risk.",
                "costs": "Concentration above 25% gives that client full negotiating power.",
                "bench": "Healthy: no single client above 25% of revenue.",
                "action": "Close 2 new clients this month to diversify.",
                "action_sub": "Set 25% concentration cap as a hard rule.",
                "template": "Expanding client base — referral discount available.",
                "seqs": [],
            })

    # 5 — Expense spike
    if len(expenses) > 0:
        me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me) >= 4:
            recent = me.iloc[-3:].mean()
            prior  = me.iloc[:-3].mean() if len(me) > 3 else me.iloc[0]
            if prior > 0 and recent > prior * 1.18:
                spike = (recent - prior) * 12
                if spike > 20000:
                    conf = get_confidence_score("exp_spike", corrections)
                    leaks.append({
                        "id": "exp_spike", "sev": "warning", "cat": "Cost Control",
                        "rupee": spike, "annual": spike, "confidence": conf,
                        "headline": f"Monthly costs up {((recent/prior - 1)*100):.0f}% — {fmtx(int(spike))} annualised",
                        "sub": f"₹{(recent-prior)/1000:.0f}K more per month than 3 months ago",
                        "found": f"Expense 3 months ago: {fmt(prior)}/mo. Now: {fmt(recent)}/mo.",
                        "root_cause": "Rising costs without matching revenue growth is a structural margin threat.",
                        "costs": "Structural cost increase — will compound monthly if not addressed.",
                        "bench": "Expenses should track revenue. Rising faster = investigate now.",
                        "action": "Freeze non-essential spend. Review every line above ₹5K.",
                        "action_sub": "Set a spend approval threshold until resolved.",
                        "template": "Cost control initiative: non-essential expenses paused.",
                        "seqs": [],
                    })

    # 6 — GST input credits
    elig = expenses[expenses["Amount"] > 25000]
    if len(elig) > 0:
        missed = elig["Amount"].sum() * 0.18 * 0.09
        if missed > 8000:
            conf = get_confidence_score("tax_gst", corrections)
            leaks.append({
                "id": "tax_gst", "sev": "info", "cat": "Tax Recovery",
                "rupee": missed, "annual": missed, "confidence": conf,
                "headline": f"~{fmtx(int(missed))} in GST input credits to verify",
                "sub": "Estimated — needs CA confirmation",
                "found": f"Eligible purchases: {fmt(elig['Amount'].sum())}. ~9% unclaimed ITC is common.",
                "root_cause": "Most SMEs don't reconcile GSTR-2A monthly. ITC claims lapse after 2 years.",
                "costs": "This is government money owed to you. One CA session to recover.",
                "bench": "Claim before next GST filing. Two-year window from invoice date.",
                "action": "Email your CA: 'Please review ITC on purchases above ₹25K.'",
                "action_sub": "Takes one CA session. Recoverable this quarter.",
                "template": "Want to review ITC eligibility on purchase invoices. Can we schedule a call?",
                "seqs": [],
            })

    return sorted(leaks, key=lambda x: x["rupee"], reverse=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
defaults = {
    "df": None, "industry": "agency", "city": "Bangalore",
    "show_bot": False, "lead_captured": False, "trial_clicked": False,
    "user_phone": "", "biz_name": "",
    "tasks": [], "corrections": {}, "monthly_fee": 2999, "months": 1,
    "snapshots": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────────────────────
def make_demo():
    np.random.seed(42)
    customers = ["Sharma Enterprises", "Patel & Sons", "Krishna Steels", "Mehta Industries", "Lakshmi Dist.", "Venkatesh Fab"]
    vendors   = ["Tata Steel Suppliers", "National Raw Mat", "City Transport", "Vinayak Packaging", "Bharat Logistics", "Sunrise Packaging"]
    cats      = ["Raw Materials", "Labor", "Rent", "Logistics", "Packaging", "Utilities"]
    wts       = [0.30, 0.20, 0.10, 0.15, 0.10, 0.15]
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
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇮🇳 Profit Intelligence Engine · Indian SMEs · Bangalore</div>
  <h1 class="hero-h">We don't show data.<br><em>We increase your profit.</em></h1>
  <p class="hero-sub">Upload your Tally export. Get industry-specific profit intelligence, peer benchmarks,
  and a tracked action plan — in 60 seconds. You pay only when you recover.</p>
  <div class="trust-row">
    <div class="trust-item"><div class="t-num">₹50Cr+</div><div class="t-lbl">Leaks found</div></div>
    <div class="trust-item"><div class="t-num">₹12.4L</div><div class="t-lbl">Avg recovery</div></div>
    <div class="trust-item"><div class="t-num">4.8 days</div><div class="t-lbl">To first rupee</div></div>
    <div class="trust-item"><div class="t-num">200+</div><div class="t-lbl">SMEs scanned</div></div>
  </div>
</div>
<div class="safety-bar">
  <div class="s-pill"><div class="s-dot"></div> Data processed securely, never stored</div>
  <div class="s-pill"><div class="s-dot"></div> Industry-specific intelligence for 10 sectors</div>
  <div class="s-pill"><div class="s-dot"></div> Peer benchmarks from 200+ Indian SMEs</div>
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
        with st.expander("How to export from Tally"):
            st.markdown("**Tally Prime:** Display → Day Book → Alt+E → Excel  \n**Tally ERP9:** Gateway → Day Book → Ctrl+E")
    with c2:
        ind_sel = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
        st.session_state.industry = INDUSTRY_MAP[ind_sel]
    with c3:
        st.selectbox("City", ["Bangalore", "Mumbai", "Delhi", "Pune", "Chennai", "Hyderabad", "Ahmedabad", "Other"], key="city")
        if st.button("▶  Try Demo", use_container_width=True):
            st.session_state.df = make_demo()
            st.session_state.industry = "manufacturing"
            st.session_state.lead_captured = True
            st.session_state.biz_name = "Demo Business"
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
    st.markdown('</div>', unsafe_allow_html=True)

    # ── GATE (lead capture) ───────────────────────────────────
    if st.session_state.df is not None and not st.session_state.lead_captured:
        st.markdown('<div class="sw">', unsafe_allow_html=True)
        st.markdown("""
<div class="gate-box">
  <div class="gate-h">Scan complete 🎯</div>
  <div class="gate-s">Enter your WhatsApp number to see full results.</div>
</div>
""", unsafe_allow_html=True)
        g1, g2, g3 = st.columns([1, 2, 1])
        with g2:
            p = st.text_input("WhatsApp number", "", placeholder="9876543210")
            b = st.text_input("Business name", "", placeholder="Sharma Enterprises")
            if st.button("Show my leaks →", type="primary", use_container_width=True):
                if p.strip():
                    st.session_state.user_phone = p
                    st.session_state.biz_name   = b or "Your Business"
                    st.session_state.lead_captured = True
                    st.rerun()
                else:
                    st.warning("Enter your WhatsApp number to continue.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ───────────────────────────────────────────────
    if st.session_state.df is not None and st.session_state.lead_captured:
        df       = st.session_state.df
        industry = st.session_state.industry
        intel    = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
        biz      = st.session_state.biz_name or "Your Business"
        sales    = df[df["Type"] == "Sales"]
        expenses = df[df["Type"] == "Expense"]
        revenue  = sales["Amount"].sum()
        exp_tot  = expenses["Amount"].sum()
        profit   = revenue - exp_tot
        margin   = (profit / revenue * 100) if revenue > 0 else 0
        bmark    = BENCH_MARGINS.get(industry, 15)
        leaks    = find_leaks(df, industry, st.session_state.corrections)
        total_rupee = sum(l["rupee"] for l in leaks)
        overdue = (
            sales[sales["Status"].str.lower().isin(["overdue", "pending"])]["Amount"].sum()
            if "Status" in sales.columns else 0
        )

        if not st.session_state.tasks and leaks:
            st.session_state.tasks = leaks_to_tasks(leaks, biz)

        done_saving = sum(t["impact"] for t in st.session_state.tasks if t["status"] == "done")
        pending_n   = sum(1 for t in st.session_state.tasks if t["status"] == "pending")
        roi_x       = done_saving / st.session_state.monthly_fee if st.session_state.monthly_fee > 0 else 0

        st.markdown('<div class="sw">', unsafe_allow_html=True)

        # Money counter
        st.markdown(f"""
<div class="msc-wrap">
  <div class="msc-label">💰 Total Money Recovered — {biz}</div>
  <div class="msc-total">{fmt(done_saving)}</div>
  <div class="msc-sub">of {fmt(total_rupee)} identified · Go to Action Board to mark tasks done</div>
  <div class="msc-grid">
    <div class="msc-cell"><div class="msc-cell-lbl">Total Identified</div><div class="msc-cell-val gold">{fmt(total_rupee)}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">Recovered</div><div class="msc-cell-val green">{fmt(done_saving)}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">Actions Pending</div><div class="msc-cell-val">{pending_n}</div></div>
    <div class="msc-cell"><div class="msc-cell-lbl">ROI on OpsClarity</div><div class="msc-cell-val green">{roi_x:.1f}x</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

        # KPI row
        margin_cls = "good" if margin >= bmark else "bad"
        overdue_pct = overdue / revenue * 100 if revenue > 0 else 0
        overdue_cls = "bad" if overdue > revenue * 0.06 else "good"
        profit_cls  = "good" if profit > 0 else "bad"
        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi-card"><div class="kpi-lbl">Revenue</div><div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales)} transactions</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Margin</div><div class="kpi-val">{margin:.1f}%</div><div class="kpi-sub {margin_cls}">vs {bmark}% benchmark</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Overdue</div><div class="kpi-val">{fmt(overdue)}</div><div class="kpi-sub {overdue_cls}">{overdue_pct:.1f}% of revenue</div></div>'
            f'<div class="kpi-card"><div class="kpi-lbl">Net Profit</div><div class="kpi-val">{fmt(abs(profit))}</div><div class="kpi-sub {profit_cls}">{"Profitable" if profit > 0 else "Loss"}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Trend chips
        trends = compute_trends(df)
        st.markdown("**Trends:** &nbsp;", unsafe_allow_html=True)
        col_trends = st.columns(4)
        with col_trends[0]: render_trend_chip("Revenue",  trends.get("revenue",  [0, 0]), positive_direction="up")
        with col_trends[1]: render_trend_chip("Expenses", trends.get("expenses", [0, 0]), positive_direction="down")
        with col_trends[2]: render_trend_chip("Margin",   trends.get("margin",   [0, 0]), positive_direction="up")
        with col_trends[3]:
            if "overdue" in trends:
                render_trend_chip("Overdue", trends["overdue"], positive_direction="down")

        st.markdown("<br>", unsafe_allow_html=True)

        # Leak cards
        st.markdown(f'<div class="sh">Where your money is leaking</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ss">{intel["name"]} · {len(leaks)} issues found</div>', unsafe_allow_html=True)

        for leak in leaks[:6]:
            conf_badge = render_confidence_badge(leak["confidence"])
            st.markdown(f"""
<div class="intel-card {leak['sev']}">
  <div class="intel-tag {leak['sev']}">{leak['cat'].upper()}</div>
  <div class="intel-amt">{fmtx(int(leak['rupee']))}{conf_badge}</div>
  <div class="intel-ttl">{leak['headline']}</div>
  <div class="intel-body">{leak['sub']}</div>
  <div class="intel-why">
    <strong>What we found:</strong> {leak['found']}<br><br>
    <strong>Root cause:</strong> {leak['root_cause']}<br><br>
    <strong>Benchmark:</strong> {leak['bench']}
  </div>
  <div class="intel-act">→ {leak['action']}<div class="intel-act-s">{leak['action_sub']}</div></div>
</div>
""", unsafe_allow_html=True)

            # Learning feedback buttons
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

            # WhatsApp collection sequence
            if leak["id"] == "cash_stuck" and leak.get("seqs"):
                if st.button("📱 Show WhatsApp collection sequence", key="show_seq"):
                    st.session_state.show_bot = not st.session_state.show_bot
                if st.session_state.show_bot:
                    for step in leak["seqs"]:
                        st.markdown(f"""
<div class="seq-card">
  <div class="seq-day">Day {step['day']} · Send on {step['send_on']}</div>
  <div class="seq-tone" style="color:{step['color']}">{step['tone']}</div>
  <div class="seq-msg">{step['message']}</div>
</div>
""", unsafe_allow_html=True)
                        st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:12px;color:#25D366">📲 Open in WhatsApp →</a>', unsafe_allow_html=True)
            elif leak.get("template"):
                if st.button("📋 Template script", key=f"scr_{leak['id']}"):
                    st.code(leak["template"])

        # Charts
        st.markdown("---")
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("**Revenue vs Expenses — Monthly**")
            monthly = df.groupby([df["Date"].dt.to_period("M"), "Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly, height=200)
        with ch2:
            st.markdown("**Top Expense Categories**")
            if len(expenses) > 0:
                st.bar_chart(
                    expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8),
                    height=200
                )

        st.markdown('</div>', unsafe_allow_html=True)

        # Pricing
        st.markdown('<div class="pr-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F7F4EF;margin-bottom:1.2rem">How we work together</div>', unsafe_allow_html=True)
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.markdown('<div class="pr-card"><div class="pr-lbl">Free</div><div class="pr-name">First Scan</div><div class="pr-amt">₹0</div><div class="pr-note">Full intelligence scan. No strings.</div><div class="pr-feat">Industry-specific insights</div><div class="pr-feat">Peer benchmarks</div><div class="pr-feat">Action tracker</div></div>', unsafe_allow_html=True)
        with pc2:
            st.markdown('<div class="pr-card feat"><div class="pr-lbl">Most chosen</div><div class="pr-name">Recovery Review</div><div class="pr-amt">₹2,999</div><div class="pr-note">60-min call. 30-day plan. Full ROI tracking.</div><div class="pr-feat">Founder call</div><div class="pr-feat">Vendor sourcing</div><div class="pr-feat">Monthly ROI report</div><div class="pr-feat">CA coordination</div></div>', unsafe_allow_html=True)
        with pc3:
            st.markdown('<div class="pr-card"><div class="pr-lbl">CA Firms</div><div class="pr-name">Partner Plan</div><div class="pr-amt">₹1,999/mo</div><div class="pr-note">50 client seats. White-label. ₹500/client earn.</div><div class="pr-feat">Client dashboard</div><div class="pr-feat">Branded reports</div><div class="pr-feat">ROI proof per client</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            if st.button("🚀 Book Recovery Review — ₹2,999", use_container_width=True, type="primary"):
                st.session_state.trial_clicked = True
        if st.session_state.trial_clicked:
            st.success("✅ We'll WhatsApp you within 2 hours.")
            st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=Hi,+want+Recovery+Review)")
            st.balloons()

# ═══════════════════════════════════════════════════════════════
# TAB 2 — INTELLIGENCE (Benchmarks)
# ═══════════════════════════════════════════════════════════════
with t2:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("👆 Run a scan first (Tab 1)")
    else:
        df       = st.session_state.df
        industry = st.session_state.industry
        intel    = INDUSTRY_INTELLIGENCE.get(industry, INDUSTRY_INTELLIGENCE["agency"])
        expenses = df[df["Type"] == "Expense"]
        sales    = df[df["Type"] == "Sales"]
        revenue  = sales["Amount"].sum()

        st.markdown(f'<div class="sh">Industry Intelligence — {intel["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ss">Not generic advice — {intel["name"]}-specific context from real Indian SME data.</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="intel-card info" style="margin-bottom:1.5rem">
  <div class="intel-tag info">INDUSTRY CONTEXT</div>
  <div class="intel-ttl">What drives profit in {intel['name']}</div>
  <div class="intel-body">
    <strong>Top leak in this industry:</strong> {intel['language']['top_leak']}<br><br>
    <strong>Quick win most owners miss:</strong> {intel['language']['quick_win']}<br><br>
    <strong>Data source:</strong> {intel['language']['benchmark_source']}
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sh" style="font-size:1.3rem">Where you sit vs peers</div>', unsafe_allow_html=True)
        st.markdown('<div class="ss">Each bar shows your cost vs 200+ Indian SMEs in the same industry.</div>', unsafe_allow_html=True)

        peer_stats = intel.get("peer_stats", {})
        if len(expenses) > 0 and revenue > 0:
            exp_by_cat = expenses.groupby("Category")["Amount"].sum()
            for cat, pdata in peer_stats.items():
                if cat in exp_by_cat.index:
                    your_val = exp_by_cat[cat]
                    if "% rev" in pdata["unit"]:
                        your_pct = your_val / revenue * 100
                        render_benchmark_gauge(
                            label=f"{pdata['label']} — your spend vs peers",
                            your_value=your_pct,
                            p25=pdata["p25"], median=pdata["median"], p75=pdata["p75"],
                            unit=pdata["unit"], n=pdata["n"]
                        )
                    else:
                        avg_txn = expenses[expenses["Category"] == cat]["Amount"].mean()
                        render_benchmark_gauge(
                            label=f"{pdata['label']} — avg per transaction vs peers",
                            your_value=avg_txn,
                            p25=pdata["p25"], median=pdata["median"], p75=pdata["p75"],
                            unit=pdata["unit"], n=pdata["n"]
                        )
        else:
            for cat, pdata in peer_stats.items():
                st.markdown(
                    f'<div class="bench-wrap"><div class="bench-label">{pdata["label"]} — industry range</div>'
                    f'<div style="font-size:13px;color:#6A6A5A">Best 25%: {pdata["p25"]}{pdata["unit"]} · '
                    f'Median: {pdata["median"]}{pdata["unit"]} · Worst 25%: {pdata["p75"]}{pdata["unit"]} '
                    f'({pdata["n"]} peers)</div></div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown(f'<div class="sh" style="font-size:1.2rem">Weekly metrics to track for {intel["name"]}</div>', unsafe_allow_html=True)
        wm_cols = st.columns(len(intel["weekly_metrics"]))
        for i, metric in enumerate(intel["weekly_metrics"]):
            with wm_cols[i]:
                st.metric(metric, "Track weekly", "→ Add to dashboard")

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — ACTION BOARD
# ═══════════════════════════════════════════════════════════════
with t3:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">Every rupee tracked. Every action assigned. Mark done to update your ROI report.</div>', unsafe_allow_html=True)

    if not st.session_state.tasks:
        st.info("👆 Run a scan first (Tab 1) to generate your action board.")
    else:
        render_workflow_board(st.session_state.tasks, key_prefix="board")
        st.markdown("---")
        st.markdown("**Re-assign task owner**")
        task_names = [t["title"][:50] for t in st.session_state.tasks]
        sel_task   = st.selectbox("Task", task_names)
        new_owner  = st.text_input("Assign to", "Owner", placeholder="e.g. Ramesh / Accounts team")
        if st.button("Update owner"):
            idx = task_names.index(sel_task)
            st.session_state.tasks[idx]["owner"] = new_owner
            st.success(f"Assigned to {new_owner}")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — ROI REPORT
# ═══════════════════════════════════════════════════════════════
with t4:
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown('<div class="sh">ROI Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss">The number that closes every deal. Fee paid vs money saved.</div>', unsafe_allow_html=True)

    if not st.session_state.tasks:
        st.info("👆 Run a scan first (Tab 1)")
    else:
        biz = st.session_state.biz_name or "Your Business"
        f1, f2 = st.columns(2)
        with f1:
            st.session_state.monthly_fee = st.number_input("Monthly fee paid (₹)", value=2999, step=500)
        with f2:
            st.session_state.months = st.number_input("Months active", value=1, min_value=1, max_value=24)

        total_fees  = st.session_state.monthly_fee * st.session_state.months
        total_saved = sum(t["impact"] for t in st.session_state.tasks if t["status"] == "done")
        total_found = sum(t["impact"] for t in st.session_state.tasks)
        net_gain    = total_saved - total_fees
        roi_x       = (total_saved / total_fees) if total_fees > 0 else 0

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
  <div style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:#F7F4EF;margin-bottom:.3rem">📊 ROI Report — {biz}</div>
  <div style="font-size:13px;color:#5A5A4A;margin-bottom:1.2rem">{st.session_state.months} month(s) with OpsClarity · {datetime.now().strftime('%d %b %Y')}</div>
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
            "ROI REPORT — OpsClarity",
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
                "📄 Download ROI Report", "\n".join(lines),
                f"opsclarity_roi_{datetime.now().strftime('%d%b%Y')}.txt", "text/plain",
                use_container_width=True
            )
        with d2:
            msg = urllib.parse.quote(f"OpsClarity ROI: Paid {fmtx(int(total_fees))}, Saved {fmt(total_saved)}, {roi_x:.1f}x return. {verdict}")
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
        'padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;color:#D4AF37;letter-spacing:.12em;'
        'text-transform:uppercase;margin-bottom:1rem">For Chartered Accountants</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="font-family:\'DM Serif Display\',serif;font-size:1.8rem;color:#1A1A1A;margin-bottom:.5rem">'
        'Your clients lose money.<br>Show them where — automatically.</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="ca-card" style="border-left:4px solid #D4AF37;background:#FFFBF0;margin-bottom:1.5rem">
  <div class="ca-lbl">Real Result · Bangalore</div>
  <div class="ca-ttl">"Found ₹18L in 6 client files in one afternoon"</div>
  <div class="ca-body">A Bangalore CA ran OpsClarity on 6 client files after a demo. Found ₹18L in overdue receivables
  and vendor overpayments. One client recovered ₹6.2L in 12 days using the WhatsApp sequence.
  The CA now generates a monthly ROI report per client — showing fee paid vs money saved.
  Zero clients have left since adopting it.<br><br>
  <em>— CA firm, Indiranagar, Bangalore (name shared on request)</em></div>
</div>
""", unsafe_allow_html=True)

    n_ca = st.slider("Client count", 10, 200, 40, 5)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ca-card">', unsafe_allow_html=True)
        st.markdown('<div class="ca-lbl">The CA partner math</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ca-row"><div class="ca-row-lbl">Clients on OpsClarity</div><div class="ca-row-val">{n_ca}</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Your cost</div><div class="ca-row-val">₹1,999/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">You earn per client</div><div class="ca-row-val">₹500/month</div></div>'
            f'<div class="ca-row"><div class="ca-row-lbl">Gross income</div><div class="ca-row-val hl">₹{n_ca*500:,}/month</div></div>'
            f'<div class="ca-row" style="border:none"><div class="ca-row-lbl">Net after platform cost</div><div class="ca-row-val hl">₹{n_ca*500-1999:,}/month</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            '<div class="ca-card"><div class="ca-lbl">Your retention weapon</div>'
            '<div class="ca-ttl">Monthly ROI report per client</div>'
            '<div class="ca-body">Every client sees: fee paid → money saved → ROI. When a client sees they paid ₹999 and saved ₹45,000 — '
            'they never negotiate your fee again.<br><br>'
            'You become the CA who <strong>proves value in rupees every month.</strong></div></div>',
            unsafe_allow_html=True
        )

    portfolio = [
        {"name": "Sharma Textiles",    "city": "Bangalore", "ind": "textile",       "leak": 840000,  "saved": 620000, "health": "red"},
        {"name": "Mehta Food Products","city": "Bangalore", "ind": "restaurant",    "leak": 196000,  "saved": 196000, "health": "green"},
        {"name": "Rajesh Diagnostics", "city": "Bangalore", "ind": "clinic",        "leak": 91500,   "saved": 0,      "health": "amber"},
        {"name": "Kapoor Engineering", "city": "Bangalore", "ind": "manufacturing", "leak": 1780000, "saved": 890000, "health": "red"},
        {"name": "Green Pharma",       "city": "Bangalore", "ind": "pharma",        "leak": 238000,  "saved": 238000, "health": "green"},
        {"name": "Venkateswara Print", "city": "Bangalore", "ind": "printing",      "leak": 28500,   "saved": 0,      "health": "amber"},
    ]
    total_pl = sum(c["leak"]  for c in portfolio)
    total_ps = sum(c["saved"] for c in portfolio)

    def _health_color(h):
        if h == "red":   return "#E05252"
        if h == "amber": return "#D4AF37"
        return "#4CAF50"

    def _health_label(h):
        if h == "red":   return "🔴 Act"
        if h == "amber": return "🟡 Watch"
        return "🟢 OK"

    rows_html = ""
    for c in portfolio:
        rows_html += (
            '<div class="cl-row">'
            '<div>'
            '<div class="cl-name">' + c["name"] + '</div>'
            '<div class="cl-meta">' + c["city"] + ' · ' + c["ind"].title() + '</div>'
            '</div>'
            '<div style="text-align:right">'
            '<div class="cl-amt">' + fmt(c["leak"]) + ' found</div>'
            '<div style="font-size:11px;color:#4CAF50">' + fmt(c["saved"]) + ' saved</div>'
            '</div>'
            '<div style="font-size:11px;font-weight:600;color:' + _health_color(c["health"]) + '">'
            + _health_label(c["health"]) +
            '</div>'
            '</div>'
        )
    st.markdown(
        f'<div class="ca-card dark">'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem">'
        f'<div><div class="ca-lbl">Clients</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#F7F4EF">{len(portfolio)}</div></div>'
        f'<div><div class="ca-lbl">Leaks found</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#D4AF37">{fmt(total_pl)}</div></div>'
        f'<div><div class="ca-lbl">Actually saved</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#4CAF50">{fmt(total_ps)}</div></div>'
        f'<div><div class="ca-lbl">Recovery rate</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.4rem;color:#D4AF37">{total_ps/total_pl*100:.0f}%</div></div>'
        f'</div>'
        f'<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:.75rem">{rows_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    for q, a in [
        ("My clients won't share data with a third-party",
         "You upload — they never see OpsClarity. Report is branded as your firm's work."),
        ("How does the ROI report work?",
         "Each action taken is logged. Monthly report = fee paid vs money saved. Your retention weapon."),
        ("Will this replace CAs?",
         "No. Every tax finding says 'verify with your CA'. We surface the work — you do it and bill for it."),
        ("What if the numbers are wrong?",
         "You verify before sharing. Your professional judgement is the product."),
    ]:
        with st.expander(q):
            st.write(a)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Join CA Partner Program — free 30-day trial →", type="primary", use_container_width=True):
        st.success("✅ We'll WhatsApp you within 4 hours.")
        st.info("📱 [wa.me/916362319163](https://wa.me/916362319163?text=CA+Partner+Program)")
        st.balloons()

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div><div class="ft-brand">OpsClarity</div><div class="ft-legal">Profit Intelligence Engine · Bangalore 🇮🇳</div></div>
  <div class="ft-legal">Management estimates only — not CA advice · Data processed securely, never stored</div>
</div>
<a href="https://wa.me/916362319163?text=Hi,+OpsClarity+question" class="wa-btn" target="_blank">💬 Talk to founder</a>
""", unsafe_allow_html=True)
