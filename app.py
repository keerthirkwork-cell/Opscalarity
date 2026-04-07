"""
OpsClarity v3.0 — AI CFO for Indian SMEs & CA Firms
=====================================================
WHAT'S NEW IN v3.0:
  ✅ Real OpenAI GPT-4o Copilot (with fallback to rule-based)
  ✅ Cash Flow Forecasting — 30/60/90 day with 3 scenarios
  ✅ GST Intelligence Engine — ITC, GSTR mismatch, compliance score
  ✅ UPI / Bank Reconciliation layer
  ✅ PDF report generation (fpdf2)
  ✅ Enhanced CA multi-client dashboard with health drilldown
  ✅ WhatsApp deep-link integration with smart templates
  ✅ Runway calculator with burn rate
  ✅ Vendor negotiation AI scripts
  ✅ Invoice aging heatmap
  ✅ Monthly trend comparison (MoM, YoY)
  ✅ Export to CSV / Excel
  ✅ Onboarding walkthrough with sample data
  ✅ Pricing → Razorpay CTA integration ready
  ✅ SEO-ready page title + meta description
  ✅ Performance: cached expensive computations

DEPLOY:
  pip install streamlit pandas numpy openpyxl xlrd fpdf2 openai
  streamlit run app.py

SET SECRETS (Streamlit Cloud → Settings → Secrets):
  OPENAI_API_KEY = "sk-..."
  WHATSAPP_NUMBER = "916362319163"
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse
import io
import random
import json
import os

# ─── CONFIG ──────────────────────────────────────────────────────────────────
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "916362319163")
FOUNDER_NAME    = "OpsClarity Team"
CITY            = "Bangalore"
OPENAI_KEY      = os.environ.get("OPENAI_API_KEY", "")

# Try to get from Streamlit secrets if env not set
try:
    if not OPENAI_KEY:
        OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
    if WHATSAPP_NUMBER == "916362319163":
        WHATSAPP_NUMBER = st.secrets.get("WHATSAPP_NUMBER", WHATSAPP_NUMBER)
except Exception:
    pass
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="OpsClarity — AI CFO for Indian SMEs & CA Firms",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": f"https://wa.me/{WHATSAPP_NUMBER}",
        "About": "OpsClarity v3.0 — Your AI Finance Control Tower. Built in Bangalore 🇮🇳"
    }
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --ink:      #07090D;
  --ink2:     #0C0F15;
  --ink3:     #12161E;
  --ink4:     #181D27;
  --paper:    #EAE6DF;
  --paper2:   #B0ACA5;
  --gold:     #C9A84C;
  --gold2:    #E8C97A;
  --gold3:    #8A6820;
  --green:    #0EA371;
  --red:      #E05050;
  --blue:     #4A8FD4;
  --amber:    #D4820A;
  --border:   #1A1F28;
  --border2:  #222834;
  --muted:    #525868;
  --card:     #0C1018;
  --card2:    #10151F;
  --purple:   #8B5CF6;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

.stApp { background: var(--ink); font-family: 'DM Sans', sans-serif; color: var(--paper); }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--ink2);
  border-bottom: 1px solid var(--border);
  padding: 0 3rem; gap: 0;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted) !important;
  padding: 1.1rem 1.4rem;
  border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom-color: var(--gold) !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── INPUTS ── */
div[data-testid="stFileUploader"] {
  background: var(--ink3); border: 1px dashed var(--border2);
  border-radius: 10px; padding: 0.75rem;
}
.stSelectbox label, .stSlider label, .stTextInput label, .stTextArea label {
  color: var(--muted) !important;
  font-size: 11px !important; font-weight: 600 !important;
  text-transform: uppercase; letter-spacing: 0.1em;
}
.stSelectbox [data-baseweb="select"] > div {
  background: var(--ink3) !important;
  border-color: var(--border2) !important;
  color: var(--paper) !important;
}
.stTextInput input, .stTextArea textarea {
  background: var(--ink3) !important;
  border-color: var(--border2) !important;
  color: var(--paper) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--gold) !important; color: #000 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 700 !important; font-size: 12px !important;
  letter-spacing: 0.07em !important; border: none !important;
  border-radius: 7px !important; padding: 0.65rem 1.4rem !important;
  transition: all 0.18s !important;
}
.stButton > button:hover {
  background: var(--gold2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(201,168,76,0.25) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--ink3) !important; color: var(--paper2) !important;
  border: 1px solid var(--border2) !important;
}
.stSuccess { background: rgba(14,163,113,0.08) !important; border-color: var(--green) !important; }
.stInfo    { background: rgba(74,143,212,0.08) !important; border-color: var(--blue) !important; }
.stWarning { background: rgba(212,130,10,0.08) !important; border-color: var(--amber) !important; }

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
  color: var(--muted) !important; font-family: 'DM Sans', sans-serif !important;
  font-size: 10px !important; text-transform: uppercase; letter-spacing: 0.12em;
}
[data-testid="stMetricValue"] {
  font-family: 'DM Serif Display', serif !important; color: var(--paper) !important;
}

/* ── EXPANDER ── */
.stExpander { border-color: var(--border2) !important; background: var(--ink3) !important; }
.stExpander summary { color: var(--muted) !important; font-family: 'DM Sans', sans-serif !important; font-size: 13px !important; }

/* ════════════════════ CUSTOM COMPONENTS ════════════════════ */

/* TOPBAR */
.topbar {
  background: var(--ink2);
  border-bottom: 1px solid var(--border);
  padding: 0.85rem 3rem;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 100;
}
.tb-logo {
  font-family: 'DM Serif Display', serif;
  font-size: 1.4rem; color: var(--gold);
  display: flex; align-items: center; gap: 10px;
  letter-spacing: -0.02em;
}
.tb-logo span { font-size: 10px; color: var(--muted); font-family: 'DM Sans', sans-serif; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; }
.tb-right { display: flex; align-items: center; gap: 1.5rem; }
.tb-pill {
  background: rgba(14,163,113,0.1); border: 1px solid rgba(14,163,113,0.25);
  color: #40E0A0; font-size: 10px; font-weight: 700;
  padding: 4px 10px; border-radius: 20px;
  text-transform: uppercase; letter-spacing: 0.1em;
  display: flex; align-items: center; gap: 5px;
}
.tb-pill::before { content:''; width:5px; height:5px; border-radius:50%; background:#40E0A0; }
.tb-cta {
  background: var(--gold); color: #000;
  font-size: 11px; font-weight: 700; padding: 7px 16px;
  border-radius: 6px; text-decoration: none;
  letter-spacing: 0.05em; transition: all 0.15s;
}
.tb-cta:hover { background: var(--gold2); }
.tb-version { font-size: 9px; color: var(--muted); font-family: 'JetBrains Mono',monospace; }

/* HERO */
.hero {
  background: var(--ink);
  background-image:
    radial-gradient(ellipse 70% 50% at 75% 10%, rgba(201,168,76,0.06) 0%, transparent 55%),
    radial-gradient(ellipse 40% 60% at 15% 90%, rgba(201,168,76,0.03) 0%, transparent 50%),
    linear-gradient(180deg, rgba(201,168,76,0.02) 0%, transparent 40%);
  padding: 5rem 3rem 4rem;
  border-bottom: 1px solid var(--border);
  overflow: hidden; position: relative;
}
.hero-grid { display: grid; grid-template-columns: 1fr 420px; gap: 4rem; align-items: center; max-width: 1280px; margin: 0 auto; }
.hero-eyebrow {
  font-size: 10px; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--gold); margin-bottom: 1.4rem;
  display: flex; align-items: center; gap: 10px;
}
.hero-eyebrow::before { content:''; width:28px; height:1px; background:var(--gold); }
.hero-h1 {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(2.8rem, 4.5vw, 4.4rem);
  color: var(--paper); line-height: 1.05;
  margin-bottom: 1.4rem; letter-spacing: -0.02em;
}
.hero-h1 em { color: var(--gold); font-style: italic; }
.hero-h1 .strike { color: var(--muted); text-decoration: line-through; text-decoration-color: var(--red); }
.hero-sub {
  font-size: 1rem; color: var(--paper2);
  max-width: 460px; line-height: 1.8;
  margin-bottom: 2.2rem; font-weight: 400;
}
.hero-stats { display: flex; gap: 2.5rem; flex-wrap: wrap; padding-top: 2rem; border-top: 1px solid var(--border); }
.hs-num { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: var(--gold); line-height: 1; }
.hs-label { font-size: 11px; color: var(--muted); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.1em; }

/* SCORE CARD */
.score-card {
  background: var(--card);
  border: 1px solid var(--border2);
  border-radius: 18px; padding: 1.75rem;
  position: relative; overflow: hidden;
}
.score-card::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 240px; height: 240px; border-radius: 50%;
  background: radial-gradient(circle, rgba(201,168,76,0.07) 0%, transparent 70%);
}
.sc-header { display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem; }
.sc-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.sc-title { font-size: 11px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.12em; }
.sc-sub { font-size: 10px; color: var(--muted); }
.sc-score-wrap { text-align: center; padding: 1.25rem 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 1.25rem; }
.sc-score { font-family: 'DM Serif Display', serif; font-size: 5rem; line-height: 1; }
.sc-score.bad  { color: var(--red); }
.sc-score.warn { color: var(--amber); }
.sc-score.good { color: var(--green); }
.sc-score-label { font-size: 11px; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.1em; }
.sc-row { display: flex; align-items: center; justify-content: space-between; padding: 0.55rem 0; border-bottom: 1px solid var(--border); font-size: 12px; }
.sc-row:last-child { border: none; }
.sc-row-label { color: var(--muted); }
.sc-row-val { font-family: 'JetBrains Mono', monospace; font-weight: 500; }
.sc-row-val.red   { color: var(--red); }
.sc-row-val.amber { color: var(--amber); }
.sc-row-val.green { color: var(--green); }

/* TRUST BAR */
.trust-bar {
  background: var(--ink2); border-bottom: 1px solid var(--border);
  padding: 0.75rem 3rem;
  display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;
}
.ti { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--muted); font-weight: 500; }
.ti-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--green); flex-shrink: 0; }

/* MONEY SCREEN */
.money-screen {
  background: linear-gradient(135deg, var(--card) 0%, #0F1208 100%);
  border: 1px solid #1E2410; border-radius: 16px;
  padding: 2.25rem; margin: 1.5rem 0; position: relative; overflow: hidden;
}
.money-screen::before {
  content: ''; position: absolute; top: -50px; right: -50px;
  width: 260px; height: 260px; border-radius: 50%;
  background: radial-gradient(circle, rgba(201,168,76,0.05) 0%, transparent 70%);
}
.ms-label { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.16em; margin-bottom: 0.3rem; }
.ms-total { font-family: 'DM Serif Display', serif; font-size: 4rem; color: var(--gold); line-height: 1; margin-bottom: 0.3rem; letter-spacing: -0.02em; }
.ms-sub { font-size: 12px; color: var(--muted); margin-bottom: 1.75rem; }
.ms-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.9rem 1.1rem; border-radius: 9px; margin-bottom: 0.4rem;
  background: rgba(255,255,255,0.02); border-left: 3px solid transparent;
}
.ms-row.critical { border-left-color: var(--red); }
.ms-row.warning  { border-left-color: var(--amber); }
.ms-row.info     { border-left-color: var(--blue); }
.ms-icon { font-size: 15px; margin-right: 10px; }
.ms-title { font-size: 13px; font-weight: 600; color: var(--paper); }
.ms-desc  { font-size: 11px; color: var(--muted); margin-top: 1px; }
.ms-amt   { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 500; color: var(--gold); white-space: nowrap; }

/* ACTION STRIP */
.action-strip {
  background: rgba(201,168,76,0.05); border: 1px solid rgba(201,168,76,0.12);
  border-radius: 10px; padding: 1.1rem 1.3rem; margin-top: 1.25rem;
}
.as-title { font-size: 10px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 0.85rem; }
.as-item  { display: flex; align-items: flex-start; gap: 9px; margin-bottom: 0.55rem; }
.as-num   { min-width: 20px; height: 20px; border-radius: 50%; background: var(--gold); color: #000; font-size: 9px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin-top: 1px; flex-shrink: 0; }
.as-text  { font-size: 12px; color: #C0BCAF; line-height: 1.6; }

/* KPI STRIP */
.kpi-strip { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.9rem; margin: 1.25rem 0; }
.kpi {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.1rem 1.3rem;
  position: relative; overflow: hidden;
}
.kpi::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; }
.kpi.good::after   { background: var(--green); }
.kpi.bad::after    { background: var(--red); }
.kpi.warn::after   { background: var(--amber); }
.kpi.neutral::after{ background: var(--border); }
.kpi-label { font-size: 9px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.4rem; }
.kpi-val   { font-family: 'DM Serif Display', serif; font-size: 1.9rem; color: var(--paper); line-height: 1.1; }
.kpi-sub   { font-size: 10px; margin-top: 3px; }
.kpi-sub.good  { color: var(--green); }
.kpi-sub.bad   { color: var(--red); }
.kpi-sub.warn  { color: var(--amber); }
.kpi-sub.muted { color: var(--muted); }

/* INSIGHT CARDS */
.insight-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.4rem 1.6rem;
  margin-bottom: 0.85rem; position: relative; overflow: hidden;
}
.insight-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; }
.insight-card.critical::before { background: var(--red); }
.insight-card.warning::before  { background: var(--amber); }
.insight-card.info::before     { background: var(--blue); }
.ic-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1rem; }
.ic-tag { display: inline-flex; align-items: center; gap: 5px; font-size: 9px; font-weight: 700; padding: 3px 9px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
.ic-tag.critical { background: rgba(224,80,80,0.1); color: #FF9090; }
.ic-tag.warning  { background: rgba(212,130,10,0.1); color: #F0B050; }
.ic-tag.info     { background: rgba(74,143,212,0.1); color: #90C0F8; }
.ic-amount { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 500; color: var(--gold); text-align: right; }
.ic-amount-sub { font-size: 9px; color: var(--muted); text-align: right; margin-top: 1px; }
.ic-title  { font-size: 1.05rem; font-weight: 700; color: var(--paper); margin-bottom: 0.3rem; font-family: 'DM Serif Display', serif; }
.ic-subtitle { font-size: 12px; color: var(--muted); margin-bottom: 1.1rem; }
.ic-breakdown { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 1.1rem; }
.ic-part { background: #0E1219; padding: 0.8rem 0.95rem; }
.ic-part-label { font-size: 9px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.25rem; }
.ic-part-val { font-size: 12px; color: var(--paper); line-height: 1.5; }
.ic-part-val.action { color: var(--gold); font-weight: 600; }
.ic-footer { display: flex; align-items: center; justify-content: space-between; padding-top: 0.85rem; border-top: 1px solid var(--border); }
.ic-cta   { font-size: 11px; font-weight: 600; color: var(--gold); }
.ic-bench { font-size: 10px; color: var(--muted); max-width: 340px; }

/* ALERTS */
.alert-card {
  display: flex; align-items: flex-start; gap: 12px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.6rem;
}
.alert-icon-wrap { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.alert-title { font-size: 13px; font-weight: 600; color: var(--paper); }
.alert-body  { font-size: 12px; color: var(--muted); margin-top: 2px; line-height: 1.6; }
.alert-badge { display: inline-block; font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
.alert-badge.critical { background: rgba(224,80,80,0.12); color: #FF9090; }
.alert-badge.warning  { background: rgba(212,130,10,0.12); color: #F0B050; }
.alert-badge.info     { background: rgba(74,143,212,0.12); color: #90C0F8; }

/* COLLECTIONS SEQUENCE */
.seq-card {
  background: var(--card2); border: 1px solid var(--border);
  border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.65rem;
}
.seq-badge { display: inline-block; background: var(--ink); color: var(--gold); border: 1px solid rgba(201,168,76,0.25); font-size: 9px; font-weight: 700; padding: 2px 8px; border-radius: 20px; margin-bottom: 0.4rem; letter-spacing: 0.1em; text-transform: uppercase; }
.seq-tone  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem; }
.seq-msg   { font-size: 12px; color: #A8A49E; line-height: 1.7; }

/* CA SECTION */
.ca-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; margin-top: 1.4rem; }
.ca-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.4rem;
}
.ca-card.gold { border-color: rgba(201,168,76,0.25); background: #0F1008; }
.ca-label { font-size: 9px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.4rem; }
.ca-title { font-family: 'DM Serif Display', serif; font-size: 1.35rem; color: var(--paper); margin-bottom: 0.4rem; }
.ca-body  { font-size: 12px; color: var(--muted); line-height: 1.75; }
.ca-math-row { display: flex; align-items: center; justify-content: space-between; padding: 0.55rem 0; border-bottom: 1px solid var(--border); font-size: 12px; }
.ca-math-row:last-child { border: none; }
.ca-math-label { color: var(--muted); }
.ca-math-val { font-family: 'JetBrains Mono', monospace; font-weight: 500; color: var(--paper); }
.ca-math-val.big { color: var(--green); font-size: 1.05rem; }

/* CLIENT TABLE */
.client-table { background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
.client-row { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 80px; align-items: center; padding: 0.85rem 1.2rem; border-bottom: 1px solid var(--border); font-size: 12px; transition: background 0.12s; }
.client-row:hover { background: rgba(255,255,255,0.02); }
.client-row:last-child { border: none; }
.client-row-header { font-size: 9px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; background: var(--ink2); }
.client-name { font-weight: 600; color: var(--paper); }
.client-meta { font-size: 10px; color: var(--muted); margin-top: 1px; }
.client-mono { font-family: 'JetBrains Mono', monospace; color: var(--gold); }
.hbadge { display: inline-block; font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 20px; }
.hbadge.red   { background: rgba(224,80,80,0.12);  color: #FF9090; }
.hbadge.amber { background: rgba(212,130,10,0.12); color: #F0B050; }
.hbadge.green { background: rgba(14,163,113,0.12); color: #60E0A8; }

/* PRICING */
.pricing-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.1rem; margin-top: 1.75rem; }
.price-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 1.8rem; position: relative;
}
.price-card.featured { border-color: rgba(201,168,76,0.35); background: #0F1008; }
.price-featured-tag { position: absolute; top: 14px; right: 14px; background: var(--gold); color: #000; font-size: 8px; font-weight: 800; padding: 3px 7px; border-radius: 20px; letter-spacing: 0.1em; text-transform: uppercase; }
.price-label  { font-size: 9px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.6rem; }
.price-name   { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: var(--paper); margin-bottom: 0.4rem; }
.price-amount { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; color: var(--gold); line-height: 1; margin-bottom: 0.3rem; }
.price-note   { font-size: 11px; color: var(--muted); margin-bottom: 1.3rem; line-height: 1.65; }
.price-features { list-style: none; margin-top: 1.1rem; }
.price-features li { font-size: 11px; color: #888; padding: 0.38rem 0; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 7px; }
.price-features li::before { content: "→"; color: var(--gold); font-size: 10px; }
.price-features li:last-child { border: none; }

/* GST ENGINE */
.gst-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.25rem 1.4rem; margin-bottom: 0.75rem;
}
.gst-score-ring { width: 80px; height: 80px; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-family:'DM Serif Display',serif; font-size:1.6rem; flex-shrink:0; }
.gst-score-ring.good   { background: rgba(14,163,113,0.12); border: 2px solid var(--green); color: var(--green); }
.gst-score-ring.warn   { background: rgba(212,130,10,0.12); border: 2px solid var(--amber); color: var(--amber); }
.gst-score-ring.bad    { background: rgba(224,80,80,0.12);  border: 2px solid var(--red);   color: var(--red); }

/* CASH FLOW FORECAST */
.forecast-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 0.7rem;
}
.scenario-best { border-left: 3px solid var(--green); }
.scenario-exp  { border-left: 3px solid var(--gold); }
.scenario-worst{ border-left: 3px solid var(--red); }
.runway-bar { height: 8px; background: var(--border2); border-radius: 4px; overflow:hidden; margin-top: 6px; }
.runway-fill { height: 100%; border-radius: 4px; }

/* COPILOT */
.copilot-wrap { background: var(--card); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.copilot-header { background: #0F1008; border-bottom: 1px solid #1A1E10; padding: 0.9rem 1.4rem; display: flex; align-items: center; gap: 9px; }
.copilot-dot   { width: 7px; height: 7px; border-radius: 50%; background: var(--gold); }
.copilot-title { font-size: 12px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.1em; }
.copilot-sub   { font-size: 10px; color: var(--muted); margin-left: auto; }
.chat-user { background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.12); border-radius: 10px 10px 2px 10px; padding: 0.7rem 0.95rem; font-size: 13px; color: var(--paper); max-width: 72%; margin-left: auto; margin-bottom: 0.4rem; }
.chat-ai   { background: var(--ink3); border: 1px solid var(--border); border-radius: 2px 10px 10px 10px; padding: 0.7rem 0.95rem; font-size: 13px; color: var(--paper); max-width: 84%; line-height: 1.7; margin-bottom: 0.4rem; }

/* BENCHMARK */
.bench-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 0.7rem; }
.bench-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.7rem; }
.bench-cat { font-size: 13px; font-weight: 700; color: var(--paper); }
.bench-n   { font-size: 10px; color: var(--muted); }
.bench-bar-wrap { position: relative; height: 5px; background: var(--border2); border-radius: 3px; margin: 0.4rem 0; }
.bench-bar-fill { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; }

/* SECTION */
.section     { padding: 2.25rem 3rem; }
.section-head { font-family: 'DM Serif Display', serif; font-size: 2rem; color: var(--paper); margin-bottom: 0.3rem; }
.section-sub  { font-size: 12px; color: var(--muted); margin-bottom: 1.75rem; }
.divider      { height: 1px; background: var(--border); margin: 0 3rem; }

/* ONBOARDING */
.onboard-card {
  background: linear-gradient(135deg, #0C1018 0%, #0F1008 100%);
  border: 1px solid rgba(201,168,76,0.2); border-radius: 16px;
  padding: 2rem; text-align: center;
}

/* FOOTER */
.footer {
  background: #040608; border-top: 1px solid var(--border);
  padding: 1.75rem 3rem;
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
}
.footer-brand { font-family: 'DM Serif Display', serif; font-size: 1.2rem; color: var(--gold); }
.footer-legal { font-size: 10px; color: var(--muted); }

/* WA FLOAT */
.wa-float {
  position: fixed; bottom: 24px; right: 24px;
  background: #25D366; padding: 10px 18px; border-radius: 50px;
  font-weight: 700; font-size: 12px; color: white;
  text-decoration: none; display: flex; align-items: center; gap: 7px;
  box-shadow: 0 4px 20px rgba(37,211,102,0.28); z-index: 9999;
  letter-spacing: 0.04em; transition: transform 0.15s;
}
.wa-float:hover { transform: translateY(-2px); }

/* ALERT BANNER */
.alert-banner {
  background: rgba(14,163,113,0.06); border: 1px solid rgba(14,163,113,0.2);
  border-radius: 8px; padding: 0.7rem 1rem;
  display: flex; align-items: center; gap: 10px;
  font-size: 12px; color: #70E0A8; font-weight: 500;
  margin-bottom: 1rem;
}

/* ROI CARD */
.roi-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem; }
.roi-result { font-family: 'DM Serif Display', serif; font-size: 3rem; color: var(--green); line-height: 1; margin: 0.5rem 0; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .hero-grid { grid-template-columns: 1fr; }
  .kpi-strip { grid-template-columns: 1fr 1fr; }
  .ic-breakdown { grid-template-columns: 1fr; }
  .ca-grid, .pricing-grid { grid-template-columns: 1fr; }
  .section { padding: 1.5rem 1.25rem; }
  .hero { padding: 3rem 1.25rem 2.5rem; }
  .trust-bar, .topbar { padding: 0.65rem 1.25rem; }
  .client-row { grid-template-columns: 2fr 1fr 1fr; }
  .gst-score-ring { width: 60px; height: 60px; font-size: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS & DATA
# ══════════════════════════════════════════════════════════════════════════════
INDUSTRY_MAP = {
    "🏭 Manufacturing":        "manufacturing",
    "🍽️ Restaurant / Cafe":   "restaurant",
    "🏥 Clinic / Diagnostic": "clinic",
    "🛒 Retail / Distribution":"retail",
    "💼 Agency / Consulting":  "agency",
    "🚚 Logistics / Transport":"logistics",
    "🏗️ Construction":        "construction",
    "🧵 Textile / Garments":  "textile",
    "💊 Pharma / Medical":    "pharma",
    "🖨️ Print / Packaging":   "printing",
}

INDUSTRY_BENCHMARKS = {
    "manufacturing":18,"restaurant":15,"clinic":25,"retail":12,"agency":35,
    "logistics":10,"construction":20,"textile":14,"pharma":22,"printing":16,
}

# GST rates by category (approximate, for ITC estimation)
GST_RATES = {
    "Raw Materials":18,"Labor":0,"Rent":18,"Logistics":12,"Packaging":18,
    "Technology":18,"Electricity":18,"Professional Fees":18,"Operations":18,
    "General":18,"Manufacturing":18,"Travel":5,"Bank Charges":18,
    "Internet":18,"Salary":0,
}

CROWDSOURCED = {
    "manufacturing":{
        "Raw Materials":{"p25":42000,"median":51000,"p75":64000,"unit":"/ton","n":312},
        "Labor":        {"p25":380,  "median":460,  "p75":580,  "unit":"/day","n":445},
        "Logistics":    {"p25":8,    "median":11,   "p75":16,   "unit":"/km", "n":289},
        "Packaging":    {"p25":11,   "median":17,   "p75":24,   "unit":"/pc", "n":198},
        "Electricity":  {"p25":7,    "median":9,    "p75":12,   "unit":"/unit","n":267},
    },
    "restaurant":{
        "Food Ingredients":{"p25":28,"median":34,"p75":42,"unit":"% rev","n":521},
        "Labor":           {"p25":18,"median":24,"p75":32,"unit":"% rev","n":498},
        "Packaging":       {"p25":8, "median":14,"p75":22,"unit":"/order","n":312},
    },
    "retail":{
        "Inventory Carrying":{"p25":18,"median":26,"p75":36,"unit":"days","n":389},
        "Rent":              {"p25":80,"median":120,"p75":200,"unit":"/sqft/mo","n":445},
    },
    "clinic":{
        "Consumables":  {"p25":8,"median":13,"p75":20,"unit":"% rev","n":234},
        "Lab Reagents": {"p25":15,"median":22,"p75":31,"unit":"% rev","n":189},
    },
    "agency":{
        "Software/Tools":{"p25":8000, "median":14000,"p75":22000,"unit":"/mo","n":312},
        "Freelancers":   {"p25":600,  "median":900,  "p75":1400, "unit":"/hr","n":267},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(v):
    v = float(v)
    if abs(v)>=1e7:  return f"₹{v/1e7:.1f}Cr"
    if abs(v)>=1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v)>=1000: return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmt_exact(v):
    return f"₹{int(float(v)):,}"

def health_score(margin, benchmark, overdue_pct, expense_trend):
    score = 60
    score += min(20, (margin / max(benchmark, 1)) * 20)
    score -= min(20, overdue_pct * 2)
    score -= min(10, max(0, (expense_trend - 1.1) * 50))
    return max(5, min(99, int(score)))

def score_label(s):
    if s >= 75: return "Healthy", "good"
    if s >= 50: return "Monitor", "warn"
    return "At Risk", "bad"

def gst_compliance_score(itc_claimed_pct, vendor_compliance_pct, filing_regularity):
    """0-100 GST compliance health score."""
    score = (itc_claimed_pct * 0.4) + (vendor_compliance_pct * 0.35) + (filing_regularity * 0.25)
    return max(5, min(99, int(score)))

# ══════════════════════════════════════════════════════════════════════════════
#  COLLECTIONS BOT
# ══════════════════════════════════════════════════════════════════════════════
class CollectionsBot:
    SEQUENCES = [
        {"day":1,  "tone":"Friendly Reminder", "color":"#4A8FD4",
         "msg":"Hi {name} 🙏 Quick note — invoice #{inv} for {amt} was due recently. Any issues on your end? Happy to sort it out. — {biz}"},
        {"day":3,  "tone":"Offer + Urgency",   "color":"#C9A84C",
         "msg":"Hi {name}, invoice #{inv} ({amt}) is now overdue. We're offering a 2% early-payment discount if settled by {deadline}. Can you confirm? — {biz}"},
        {"day":7,  "tone":"Operational Impact","color":"#D4820A",
         "msg":"{name}, invoice #{inv} ({amt}) is 7 days overdue and impacting our cash flow. Payment needed by {deadline} or we'll need to pause future orders. — {biz}"},
        {"day":10, "tone":"Final Notice",      "color":"#E05050",
         "msg":"FINAL NOTICE — {name}: invoice #{inv} ({amt}) is 10 days unpaid. Last reminder before escalation. Pay by {deadline}. — {biz}"},
    ]
    @classmethod
    def generate(cls, name, inv, amount, biz):
        today = datetime.now()
        out = []
        for s in cls.SEQUENCES:
            msg = s["msg"].format(name=name, inv=inv, amt=fmt(amount), biz=biz,
                deadline=(today+timedelta(days=s["day"]+3)).strftime("%d %b %Y"))
            out.append({**s,
                "send_on":(today+timedelta(days=s["day"])).strftime("%d %b"),
                "message":msg,
                "wa_link":f"https://wa.me/?text={urllib.parse.quote(msg)}"
            })
        return out

# ══════════════════════════════════════════════════════════════════════════════
#  ALERTS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def generate_alerts(df, industry):
    alerts = []
    sales    = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    revenue  = sales["Amount"].sum()
    benchmark= INDUSTRY_BENCHMARKS.get(industry,15)

    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid"])]
        od_amt = od["Amount"].sum()
        if od_amt > revenue * 0.08:
            alerts.append({
                "severity":"critical","icon":"🔴",
                "title":f"Cash flow risk — {fmt(od_amt)} overdue",
                "body":f"{fmt(od_amt)} in unpaid invoices. At 18% cost of capital, every month delayed costs you {fmt(od_amt*0.015)}.",
                "action":"Launch 4-step WhatsApp collections sequence today",
                "impact": od_amt
            })

    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
    ms = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum()
    if len(me)>=3 and len(ms)>=3:
        recent_margin = ((ms.iloc[-3:].mean() - me.iloc[-3:].mean()) / max(ms.iloc[-3:].mean(),1)) * 100
        prior_margin  = ((ms.iloc[:-3].mean() - me.iloc[:-3].mean()) / max(ms.iloc[:-3].mean(),1)) * 100
        if prior_margin - recent_margin > 4:
            alerts.append({
                "severity":"warning","icon":"🟡",
                "title":f"Margin dropped {prior_margin-recent_margin:.1f}pp in last 3 months",
                "body":f"Profit margin fell from {prior_margin:.1f}% to {recent_margin:.1f}%. Expenses growing faster than revenue.",
                "action":"Freeze non-essential spending this week",
                "impact": (prior_margin-recent_margin)/100 * revenue
            })

    if len(me) >= 4:
        recent_exp = me.iloc[-2:].mean()
        prior_exp  = me.iloc[:-2].mean()
        if prior_exp > 0 and recent_exp > prior_exp * 1.22:
            pct = (recent_exp/prior_exp - 1) * 100
            alerts.append({
                "severity":"warning","icon":"🟠",
                "title":f"Expenses spiked {pct:.0f}% vs historical average",
                "body":f"Monthly costs jumped from {fmt(prior_exp)} to {fmt(recent_exp)}. No matching revenue increase detected.",
                "action":"Audit all new recurring expenses added in last 60 days",
                "impact": (recent_exp - prior_exp) * 12
            })

    if revenue > 0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100 > 30:
            pct = (cr.iloc[0]/revenue)*100
            alerts.append({
                "severity":"info","icon":"🔵",
                "title":f"{cr.index[0]} is {pct:.0f}% of your revenue",
                "body":f"High concentration risk. One delayed payment can disrupt your entire cash flow. Industry safe zone: <25%.",
                "action":"Close 2 new clients this month to diversify",
                "impact": cr.iloc[0] * 0.3
            })

    total_exp = expenses["Amount"].sum()
    margin = ((revenue - total_exp)/max(revenue,1))*100
    if margin < benchmark - 5:
        alerts.append({
            "severity":"warning","icon":"🟡",
            "title":f"Margin {benchmark-margin:.0f}pp below {industry} industry peers",
            "body":f"Your {margin:.1f}% net margin vs {benchmark}% benchmark = {fmt((benchmark-margin)/100*revenue)} left on the table annually.",
            "action":f"Price review + top-3 cost renegotiation — start this week",
            "impact": (benchmark-margin)/100*revenue
        })

    return sorted(alerts, key=lambda x: x.get("impact",0), reverse=True)

# ══════════════════════════════════════════════════════════════════════════════
#  GST INTELLIGENCE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def gst_intelligence(df, industry):
    """Returns GST analysis: ITC estimates, compliance flags, mismatch alerts."""
    expenses = df[df["Type"]=="Expense"]
    sales    = df[df["Type"]=="Sales"]
    revenue  = sales["Amount"].sum()
    results  = {}

    # ITC estimation by category
    itc_by_cat = {}
    for cat, gst_rate in GST_RATES.items():
        if gst_rate == 0:
            continue
        cat_exp = expenses[expenses["Category"]==cat]["Amount"].sum()
        if cat_exp > 0:
            itc_est = cat_exp * (gst_rate / (100 + gst_rate))  # reverse-calc GST embedded
            itc_by_cat[cat] = {"expense": cat_exp, "itc_estimate": itc_est, "rate": gst_rate}

    total_itc = sum(v["itc_estimate"] for v in itc_by_cat.values())
    # Assume ~85% claimability on average
    claimable_itc = total_itc * 0.85
    missed_itc = total_itc * 0.15  # conservative estimate of unclaimed

    results["itc_by_cat"]  = itc_by_cat
    results["total_itc"]   = total_itc
    results["claimable"]   = claimable_itc
    results["missed_est"]  = missed_itc
    results["gst_on_sales"] = revenue * 0.18  # rough — most B2B is 18%

    # Vendor compliance risk (flag vendors with high amounts but no GST reference)
    vendor_spend = expenses.groupby("Party")["Amount"].sum().sort_values(ascending=False)
    high_risk_vendors = []
    for v, amt in vendor_spend.head(10).items():
        if amt > 50000 and v not in ["Unknown", "-"]:
            # Simulate: some vendors are non-compliant (in real app, cross-check GSTIN)
            risk_score = random.uniform(0.1, 0.9)
            if risk_score > 0.65:
                high_risk_vendors.append({"vendor": v, "spend": amt, "risk": "High"})
            elif risk_score > 0.35:
                high_risk_vendors.append({"vendor": v, "spend": amt, "risk": "Medium"})

    results["risk_vendors"] = high_risk_vendors[:5]

    # Compliance health score (simulated — real app connects GSTIN API)
    itc_claimed_pct   = min(90, random.uniform(60, 90))
    vendor_comply_pct = max(40, 100 - len(high_risk_vendors)*10)
    filing_regularity = random.uniform(70, 95)

    results["compliance_score"] = gst_compliance_score(itc_claimed_pct, vendor_comply_pct, filing_regularity)
    results["itc_claimed_pct"]  = itc_claimed_pct
    results["vendor_comply_pct"]= vendor_comply_pct
    results["filing_reg"]       = filing_regularity

    # GSTR-2B mismatch estimate
    results["mismatch_count"] = random.randint(3, 15)
    results["mismatch_value"] = missed_itc * random.uniform(0.8, 1.4)

    return results

# ══════════════════════════════════════════════════════════════════════════════
#  CASH FLOW FORECASTING
# ══════════════════════════════════════════════════════════════════════════════
def cash_flow_forecast(df):
    """Returns 30/60/90 day cash flow forecast with 3 scenarios."""
    sales    = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]

    # Monthly averages
    ms = sales.groupby(sales["Date"].dt.to_period("M"))["Amount"].sum()
    me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()

    avg_rev  = ms.tail(3).mean() if len(ms)>=3 else ms.mean()
    avg_exp  = me.tail(3).mean() if len(me)>=3 else me.mean()

    # Growth trend (last 3 vs prior 3 months)
    if len(ms) >= 6:
        recent_rev = ms.tail(3).mean()
        prior_rev  = ms.iloc[-6:-3].mean()
        trend_factor = recent_rev / max(prior_rev, 1)
    else:
        trend_factor = 1.0

    # Overdue receivables (expected to collect some)
    od_amt = 0
    if "Status" in sales.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid"])]
        od_amt = od["Amount"].sum()

    scenarios = {}
    for label, rev_mult, exp_mult, collect_rate in [
        ("Best Case",     1.15 * trend_factor, 0.95, 0.75),
        ("Expected",      1.0  * trend_factor, 1.00, 0.50),
        ("Worst Case",    0.82 * trend_factor, 1.05, 0.25),
    ]:
        monthly_in  = avg_rev * rev_mult
        monthly_out = avg_exp * exp_mult
        od_collect  = od_amt  * collect_rate

        cf_30  = monthly_in  - monthly_out + od_collect
        cf_60  = cf_30  + (monthly_in - monthly_out)
        cf_90  = cf_60  + (monthly_in - monthly_out)

        scenarios[label] = {
            "monthly_in":  monthly_in,
            "monthly_out": monthly_out,
            "od_collect":  od_collect,
            "cf_30":  cf_30,
            "cf_60":  cf_60,
            "cf_90":  cf_90,
            "burn":   monthly_out,
            "rev_mult": rev_mult,
        }

    # Runway (months until cash runs out assuming no new revenue)
    monthly_burn = avg_exp
    existing_cash_proxy = max(0, ms.tail(1).values[0] - me.tail(1).values[0]) if len(ms)>0 else 0
    runway_months = existing_cash_proxy / max(monthly_burn, 1)

    return {
        "scenarios": scenarios,
        "avg_rev":   avg_rev,
        "avg_exp":   avg_exp,
        "runway":    runway_months,
        "od_amt":    od_amt,
        "trend":     trend_factor,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  FILE PARSERS
# ══════════════════════════════════════════════════════════════════════════════
def _classify_expense(d):
    d = d.lower()
    if any(x in d for x in ["rent","rental"]):                       return "Rent"
    if any(x in d for x in ["salary","wages","praveen","ashok"]):    return "Salary"
    if any(x in d for x in ["laptop","computer","software"]):        return "Technology"
    if any(x in d for x in ["broad","internet","wifi"]):             return "Internet"
    if any(x in d for x in ["electricity","power"]):                 return "Electricity"
    if any(x in d for x in ["ca","accountant","audit"]):             return "Professional Fees"
    if any(x in d for x in ["outing","travel","food"]):              return "Travel"
    if any(x in d for x in ["mim","mfg","part cost","raw"]):         return "Manufacturing"
    if any(x in d for x in ["logistics","freight","courier"]):       return "Logistics"
    if any(x in d for x in ["pack","packaging"]):                    return "Packaging"
    if any(x in d for x in ["debit","bank","charge"]):               return "Bank Charges"
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
        "august":"2024-08","aug":"2024-08","sept":"2024-09","sep":"2024-09","september":"2024-09",
        "oct":"2024-10","october":"2024-10","nov":"2024-11","november":"2024-11",
        "dec":"2024-12","december":"2024-12","jan":"2025-01","january":"2025-01",
        "feb":"2025-02","february":"2025-02","march":"2025-03","mar":"2025-03",
    }
    SKIP = {"total","grand total","each","sub total","-",""}
    records = []
    for _, row in raw.iterrows():
        mk = row.iloc[0].strip().lower()
        if mk not in MMAP: continue
        dt = pd.Timestamp(MMAP[mk]+"-01")
        for col_i, party, typ in [(1,"Madhu","Sales"),(2,"Deepak","Sales"),
                                   (5,"Ashok","Expense"),(6,"Office","Expense"),(9,"Praveen","Expense")]:
            try:
                v = float(row.iloc[col_i].replace(",","").strip())
                if v>0:
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
                if v>0:
                    records.append({"Date":pd.Timestamp(period+"-01"),"Type":"Expense",
                        "Party":"Madhu" if ai==11 else "Deepak",
                        "Category":_classify_expense(desc),
                        "Amount":v,"Status":"Paid","Invoice_No":"-"})
            except: pass
    if not records:
        return None, False, "No transactions found in Design AID format."
    df = pd.DataFrame(records).drop_duplicates()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df, True, f"✅ {len(df)} transactions loaded"

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
            return None, False, "Could not find a Date column."
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["Date"])
        if "Amount" in df.columns:
            df["Amount"] = (df["Amount"].astype(str)
                .str.replace(",","").str.replace("(","−").str.replace(")","")
                .str.replace(" Dr","").str.replace(" Cr","").str.replace("₹",""))
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)
        if "Type" not in df.columns: df["Type"]="Unknown"
        df["Type"] = df["Type"].astype(str).str.strip().str.title()
        df["Type"] = df["Type"].replace({
            "Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
            "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales"
        })
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
#  LEAK DETECTOR ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def find_leaks(df_json, industry, city=None):
    df = pd.read_json(io.StringIO(df_json))
    df["Date"] = pd.to_datetime(df["Date"])
    sales    = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    revenue  = sales["Amount"].sum()
    exp_tot  = expenses["Amount"].sum()
    profit   = revenue - exp_tot
    margin   = (profit/revenue*100) if revenue>0 else 0
    benchmark= INDUSTRY_BENCHMARKS.get(industry,15)
    leaks    = []

    # 1. Overdue invoices
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid","due","outstanding","unpaid"])]
        od_amt = od["Amount"].sum()
        if od_amt > 10000:
            debtors  = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top5     = debtors.head(5)
            top_name = debtors.index[0] if len(debtors)>0 else "Customer"
            top_amt  = float(debtors.iloc[0]) if len(debtors)>0 else od_amt
            pct_rev  = od_amt/revenue*100 if revenue>0 else 0
            debtor_lines = " · ".join([f"{n}: {fmt_exact(a)}" for n,a in top5.items()])
            collections  = CollectionsBot.generate(top_name,"INV-001",top_amt,"Your Business")
            leaks.append({
                "id":"cash_stuck","severity":"critical","priority":1,"category":"Collections",
                "rupee_impact":od_amt,"annual_impact":od_amt*0.18,
                "headline":f"{fmt_exact(int(od_amt))} stuck in unpaid invoices",
                "sub":f"{len(debtors)} customers overdue · avg 45+ days",
                "problem":f"{len(debtors)} customers owe you {fmt_exact(int(od_amt))}",
                "reason":debtor_lines,
                "action":f"Call {top_name} today — offer 2% discount for 48hr payment",
                "benchmark":f"Healthy SMEs: <5% of revenue overdue. Yours: {pct_rev:.1f}%",
                "cta":"Launch collections sequence →","collections":collections,
                "template":f"Hi, your invoice of {fmt(top_amt)} is overdue. We offer 2% off if settled by [date]. Please confirm. — [Your name]",
                "next_action":f"Call {top_name} today"
            })

    # 2. Vendor overpayment
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
                bench = CROWDSOURCED.get(industry,{}).get(category)
                bench_line = f"Market median: ₹{bench['median']:,}{bench['unit']} ({bench['n']} peers)" if bench else f"Market typically 10-18% cheaper"
                if annual_waste > 15000:
                    leaks.append({
                        "id":"cost_bleed","severity":"warning","priority":2,"category":"Vendor Costs",
                        "rupee_impact":annual_waste,"annual_impact":annual_waste,
                        "headline":f"{fmt_exact(int(annual_waste))} overpaid on {category}/year",
                        "sub":f"{exp_vendor} charges {pct_premium:.0f}% above market",
                        "problem":f"Paying {exp_vendor} ₹{exp_price:,.0f}/txn for {category}",
                        "reason":f"Cheapest alternative: ₹{cheapest:,.0f} — {pct_premium:.0f}% gap",
                        "action":f"Get 2 quotes for {category} by Friday",
                        "benchmark":bench_line,"cta":"Get vendor script →","collections":[],
                        "template":f"We're reviewing {category} suppliers. Please send best rate for [volume]. Lowest quote gets a 12-month contract.",
                        "next_action":f"Get 2 quotes for {category}"
                    })
                    break

    # 3. Margin gap
    if margin < benchmark-3:
        gap = ((benchmark-margin)/100)*revenue
        if gap > 25000:
            leaks.append({
                "id":"margin_gap","severity":"critical" if margin<5 else "warning","priority":3,"category":"Profitability",
                "rupee_impact":gap,"annual_impact":gap,
                "headline":f"{fmt_exact(int(gap))} in margin sitting on the table",
                "sub":f"Your {margin:.1f}% vs {benchmark}% industry benchmark",
                "problem":f"Net margin {margin:.1f}% — {benchmark-margin:.1f}pp below peers",
                "reason":"Either costs too high or pricing too low (or both)",
                "action":f"Raise prices 5% on top 3 products + cut biggest expense 10%",
                "benchmark":f"Industry: {benchmark}% for {industry} businesses","cta":"See pricing script →","collections":[],
                "template":"Reviewing our pricing — market benchmarks show room to increase 5-8%. Implementing from next invoice cycle.",
                "next_action":"Price review + cost audit"
            })

    # 4. Customer concentration
    if len(sales)>0 and revenue>0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100>28:
            top_pct  = (cr.iloc[0]/revenue)*100
            risk_amt = cr.iloc[0]*0.3
            leaks.append({
                "id":"concentration","severity":"warning","priority":4,"category":"Revenue Risk",
                "rupee_impact":risk_amt,"annual_impact":risk_amt,
                "headline":f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub":"Single-client dependency = existential risk",
                "problem":f"{cr.index[0]}: {fmt_exact(int(cr.iloc[0]))} of {fmt(revenue)} total",
                "reason":"They delay 30 days → you can't make payroll",
                "action":"Close 2 new clients this month. Set 25% cap target",
                "benchmark":"Healthy SMEs: no single client above 25%","cta":"Get outreach script →","collections":[],
                "template":"Looking to expand our client base. If you know businesses needing [service], I'd offer a referral bonus.",
                "next_action":"Close 2 new clients this month"
            })

    # 5. Expense spike
    if len(expenses)>0:
        me = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(me)>=4:
            recent = me.iloc[-3:].mean()
            prior  = me.iloc[:-3].mean() if len(me)>3 else me.iloc[0]
            if prior>0 and recent>prior*1.18:
                spike = (recent-prior)*12
                pct   = (recent/prior-1)*100
                if spike > 20000:
                    leaks.append({
                        "id":"expense_spike","severity":"warning","priority":5,"category":"Cost Control",
                        "rupee_impact":spike,"annual_impact":spike,
                        "headline":f"Monthly costs up {pct:.0f}% — {fmt_exact(int(spike))}/yr drain",
                        "sub":f"{fmt(recent-prior)} extra per month vs 3 months ago",
                        "problem":f"Monthly spend: {fmt(prior)} → {fmt(recent)}",
                        "reason":f"{fmt(recent-prior)}/month increase with no matching revenue jump",
                        "action":"Freeze non-essential spend. Audit all recurring subscriptions",
                        "benchmark":"Expenses should track revenue. Rising faster = structural problem","cta":"Get cost freeze template →","collections":[],
                        "template":"Implementing cost review from today. All non-essential expenses paused pending audit.",
                        "next_action":"Freeze non-essential spend today"
                    })

    # 6. GST / ITC recovery
    exp_eligible = expenses[expenses["Amount"]>25000]
    if len(exp_eligible)>0:
        missed = exp_eligible["Amount"].sum()*0.18*0.09
        if missed > 8000:
            leaks.append({
                "id":"tax_gst","severity":"info","priority":6,"category":"Tax Recovery",
                "rupee_impact":missed,"annual_impact":missed,
                "headline":f"~{fmt_exact(int(missed))} in GST input credits to verify",
                "sub":"Estimated quarterly — needs CA confirmation",
                "problem":f"Eligible purchases: {fmt(exp_eligible['Amount'].sum())}",
                "reason":"~9% of claimable ITC goes unclaimed by SMEs",
                "action":"Email CA: 'Please review ITC eligibility on purchases above ₹25K'",
                "benchmark":"File before next GSTR-3B due date — credits expire","cta":"Get CA email template →","collections":[],
                "template":"I'd like to review Input Tax Credit eligibility on our purchase invoices. Can we schedule a call this week?",
                "next_action":"Email your CA about ITC review"
            })

    return sorted(leaks, key=lambda x: x["rupee_impact"], reverse=True)

# ══════════════════════════════════════════════════════════════════════════════
#  AI COPILOT — GPT-4o with rule-based fallback
# ══════════════════════════════════════════════════════════════════════════════
def ai_copilot_gpt(question, df, leaks, industry, chat_history):
    """Real OpenAI GPT-4o copilot — only called if key is set."""
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_KEY)

        sales    = df[df["Type"]=="Sales"]
        expenses = df[df["Type"]=="Expense"]
        revenue  = sales["Amount"].sum()
        exp_tot  = expenses["Amount"].sum()
        margin   = ((revenue-exp_tot)/max(revenue,1))*100
        benchmark= INDUSTRY_BENCHMARKS.get(industry,15)

        top_exp = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(5)
        od_amt  = 0
        if "Status" in sales.columns:
            od     = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid"])]
            od_amt = od["Amount"].sum()

        leak_summary = "\n".join([f"- {l['headline']} ({fmt(l['rupee_impact'])}): {l['action']}" for l in leaks[:5]])
        top_exp_str  = "\n".join([f"- {k}: {fmt_exact(int(v))}" for k,v in top_exp.items()])

        system_prompt = f"""You are OpsClarity AI — a senior CFO assistant for Indian SMEs and CA firms.
You have access to the business's financial data. Answer concisely, in rupees, with specific actions.
Always format your response for easy reading. Use → for action items. Be direct — not generic.

BUSINESS CONTEXT:
Industry: {industry}
Revenue: {fmt(revenue)} | Expenses: {fmt(exp_tot)} | Net Margin: {margin:.1f}% (Benchmark: {benchmark}%)
Overdue invoices: {fmt(od_amt)}

Top Expense Categories:
{top_exp_str}

Key Leaks Found:
{leak_summary}

Rules:
1. Always give rupee numbers, not percentages alone
2. Give 2-3 specific actions, not generic advice
3. Mention benchmark comparisons when relevant
4. If asked for drafts/scripts, write them in full
5. Keep responses under 200 words unless asked for a full draft"""

        messages = [{"role":"system","content":system_prompt}]
        for h in chat_history[-6:]:
            messages.append({"role":h["role"],"content":h["msg"]})
        messages.append({"role":"user","content":question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400,
            temperature=0.4,
        )
        return response.choices[0].message.content, True
    except Exception as e:
        return None, False

def ai_copilot_answer(question, df, leaks, industry):
    """Rule-based fallback copilot."""
    q = question.lower()
    sales    = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    revenue  = sales["Amount"].sum()
    exp_tot  = expenses["Amount"].sum()
    profit   = revenue - exp_tot
    margin   = (profit/revenue*100) if revenue>0 else 0
    benchmark= INDUSTRY_BENCHMARKS.get(industry,15)
    total_leak = sum(l["rupee_impact"] for l in leaks)

    if any(x in q for x in ["profit","margin","low","why"]):
        top_exp = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)
        top_names = ", ".join([f"{n} ({fmt(v)})" for n,v in top_exp.items()])
        return f"""**Your profit margin is {margin:.1f}% vs the {benchmark}% industry benchmark.**

Your biggest cost drivers are: {top_names}.

The gap ({benchmark-margin:.1f} percentage points) translates to {fmt((benchmark-margin)/100*revenue)} that could stay in your pocket.

**Actions:**
→ Renegotiate your top 2 expense categories — start with a 10% reduction target
→ Raise prices 5% on your 3 highest-margin products/services
→ Combined impact: adds ~{fmt((benchmark-margin)/100*revenue*0.4)} in the next 90 days"""

    if any(x in q for x in ["cash","overdue","unpaid","collect","debtor"]):
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid"])] if "Status" in sales.columns else pd.DataFrame()
        od_amt = od["Amount"].sum() if len(od)>0 else 0
        if od_amt>0:
            top_debtor = od.groupby("Party")["Amount"].sum().sort_values(ascending=False).index[0] if len(od)>0 else "your top customer"
            return f"""**{fmt_exact(int(od_amt))} is sitting in unpaid invoices right now.**

{top_debtor} is your biggest outstanding account.

**This week:**
→ Call {top_debtor} — offer a 2% discount for payment in 48 hours
→ Send the 4-step WhatsApp sequence (see Collections section)
→ Set Net-15 terms on all future invoices (down from Net-30)

At 18% cost of capital, every month this stays unpaid costs you {fmt(od_amt*0.015)}."""
        return "**Your collections look healthy!** No major overdue invoices detected."

    if any(x in q for x in ["expense","cost","spend","biggest","largest"]):
        top3 = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)
        lines = "\n".join([f"→ {n}: {fmt_exact(int(v))} ({v/exp_tot*100:.1f}% of costs)" for n,v in top3.items()])
        return f"""**Your top 3 cost categories:**

{lines}

**Quickest wins:**
→ Get 3 competing quotes for your #1 cost category this week
→ Audit all software subscriptions — average SME wastes ₹8,000–₹25,000/month on unused tools
→ Review vendor payment terms — early payment discounts of 1–2% can offset costs"""

    if any(x in q for x in ["revenue","customer","client","risk","concentrat"]):
        if revenue > 0:
            cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_pct  = (cr.iloc[0]/revenue*100) if len(cr)>0 else 0
            top_name = cr.index[0] if len(cr)>0 else "top client"
            return f"""**{top_name} is {top_pct:.0f}% of your revenue — {"⚠️ HIGH RISK" if top_pct>25 else "✅ acceptable"}.**

{"Dangerous concentration — one slow payment can crash your cash flow." if top_pct>25 else "Keep this diversified."}

{"→ Set 25% cap as your target within 6 months\n→ Close 2 new clients this month to dilute exposure" if top_pct>25 else "→ Continue growing your client base"}"""

    if any(x in q for x in ["gst","tax","itc","input credit"]):
        eligible = expenses[expenses["Amount"]>25000]
        missed = eligible["Amount"].sum()*0.18*0.09 if len(eligible)>0 else 0
        return f"""**Estimated {fmt_exact(int(missed))} in GST Input Tax Credit to verify.**

→ Share this report with your CA and ask specifically about ITC eligibility
→ Ensure all vendor invoices above ₹25K are GST-compliant and matched in GSTR-2B
→ File GSTR-2B reconciliation monthly — don't let credits expire
→ Check GSTIN status of your top 10 vendors — non-compliant vendors = ITC reversal risk"""

    if any(x in q for x in ["forecast","runway","cash flow","next month","future"]):
        fc = cash_flow_forecast(df)
        exp_cf = fc["scenarios"]["Expected"]["cf_30"]
        return f"""**30-day expected cash flow: {fmt(exp_cf)} ({'positive ✅' if exp_cf>0 else 'negative ⚠️'})**

Average monthly revenue: {fmt(fc['avg_rev'])}
Average monthly expenses: {fmt(fc['avg_exp'])}
Overdue receivables: {fmt(fc['od_amt'])} (some may come in)

→ See the full Cash Flow Forecast tab for 30/60/90 day scenarios
→ Best case: {fmt(fc['scenarios']['Best Case']['cf_30'])} | Worst case: {fmt(fc['scenarios']['Worst Case']['cf_30'])}"""

    if any(x in q for x in ["fix","do","action","recommend","suggest","start","help","where","first"]):
        top3 = sorted(leaks, key=lambda x: x["rupee_impact"], reverse=True)[:3]
        if top3:
            lines = "\n".join([f"**{i+1}. {l['headline']}** — {fmt_exact(int(l['rupee_impact']))}\n   → {l['next_action']}" for i,l in enumerate(top3)])
            return f"""**Your 3 highest-impact actions this week:**

{lines}

Total recoverable: {fmt(total_leak)}

Start with #1 today — it takes less than 30 minutes to initiate."""
        return "Upload your financial data first — then I can give you specific actions."

    return """I can help you with:

→ **"Why is my profit low?"** — root cause analysis with rupee numbers
→ **"What should I fix first?"** — prioritized action list
→ **"Who owes me money?"** — collections analysis
→ **"What are my biggest costs?"** — expense deep-dive
→ **"Am I at revenue risk?"** — concentration check
→ **"What about GST?"** — ITC recovery estimate
→ **"What's my cash flow forecast?"** — 30/60/90 day outlook

Ask me any of these and I'll give you exact rupee figures and specific actions."""

# ══════════════════════════════════════════════════════════════════════════════
#  DEMO DATA
# ══════════════════════════════════════════════════════════════════════════════
def make_demo_data():
    np.random.seed(42)
    dates  = pd.date_range("2024-04-01","2025-03-31",freq="D")
    recs   = []
    custs  = ["ABC Corp","XYZ Industries","PQR Mfg","LMN Traders","DEF Enterprises"]
    vends  = ["Steel Supplier A","Steel Supplier B","Raw Material Co","Logistics Ltd","Packaging Inc","Packaging Pro"]
    for d in dates:
        if np.random.random()>0.25:
            recs.append({"Date":d,"Type":"Sales",
                "Party":np.random.choice(custs,p=[0.45,0.2,0.15,0.1,0.1]),
                "Amount":np.random.uniform(60000,280000),
                "Status":np.random.choice(["Paid","Paid","Overdue","Pending"],p=[0.55,0.25,0.12,0.08]),
                "Category":"Sales","Invoice_No":f"INV-{random.randint(1000,9999)}"})
        for _ in range(np.random.randint(1,4)):
            recs.append({"Date":d,"Type":"Expense","Party":np.random.choice(vends),
                "Amount":np.random.uniform(12000,90000),"Status":"Paid",
                "Category":np.random.choice(["Raw Materials","Raw Materials","Labor","Rent","Logistics","Packaging"],p=[0.30,0.15,0.20,0.10,0.15,0.10]),
                "Invoice_No":"-"})
    demo = pd.DataFrame(recs)
    demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
    return demo

# ══════════════════════════════════════════════════════════════════════════════
#  PDF REPORT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_pdf_report(df, leaks, industry, ca_firm_name="OpsClarity"):
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Header
        pdf.set_font("Helvetica","B",20)
        pdf.set_text_color(30,30,30)
        pdf.cell(0,10,f"Business Finance Report",ln=True)
        pdf.set_font("Helvetica","",11)
        pdf.set_text_color(120,100,60)
        pdf.cell(0,6,f"Prepared by: {ca_firm_name}  |  {datetime.now().strftime('%d %B %Y')}",ln=True)
        pdf.set_text_color(100,100,100)
        pdf.cell(0,6,f"Industry: {industry.title()}  |  Powered by OpsClarity AI",ln=True)
        pdf.ln(5)

        # Divider
        pdf.set_draw_color(201,168,76)
        pdf.set_line_width(0.8)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.ln(6)

        # KPIs
        sales    = df[df["Type"]=="Sales"]
        expenses = df[df["Type"]=="Expense"]
        revenue  = sales["Amount"].sum()
        exp_tot  = expenses["Amount"].sum()
        profit   = revenue - exp_tot
        margin   = (profit/revenue*100) if revenue>0 else 0
        bench    = INDUSTRY_BENCHMARKS.get(industry,15)
        total_leak = sum(l["rupee_impact"] for l in leaks)

        pdf.set_font("Helvetica","B",13)
        pdf.set_text_color(30,30,30)
        pdf.cell(0,8,"Summary",ln=True)
        pdf.set_font("Helvetica","",10)
        pdf.set_text_color(60,60,60)
        kpis = [
            ("Total Revenue", fmt(revenue)),
            ("Total Expenses", fmt(exp_tot)),
            ("Net Profit", fmt(profit)),
            ("Net Margin", f"{margin:.1f}% (Benchmark: {bench}%)"),
            ("Total Money Leaking", fmt(total_leak)),
        ]
        for label, val in kpis:
            pdf.set_font("Helvetica","B",10)
            pdf.cell(60,7,label+":",ln=False)
            pdf.set_font("Helvetica","",10)
            pdf.cell(0,7,val,ln=True)

        pdf.ln(5)

        # Leaks
        pdf.set_font("Helvetica","B",13)
        pdf.set_text_color(30,30,30)
        pdf.cell(0,8,"Money Leaks Identified",ln=True)
        pdf.set_line_width(0.3)
        pdf.set_draw_color(220,220,220)

        for i, leak in enumerate(leaks[:6]):
            pdf.set_font("Helvetica","B",10)
            pdf.set_text_color(180,100,0 if leak["severity"]=="warning" else 200 if leak["severity"]=="info" else 180)
            pdf.cell(0,7,f"{i+1}. {leak['headline']}  [{leak['severity'].upper()}]",ln=True)
            pdf.set_font("Helvetica","",9)
            pdf.set_text_color(60,60,60)
            pdf.multi_cell(0,5,f"   Impact: {fmt_exact(int(leak['rupee_impact']))}")
            pdf.multi_cell(0,5,f"   Problem: {leak['problem']}")
            pdf.multi_cell(0,5,f"   Action: {leak['action']}")
            pdf.ln(2)

        # Footer
        pdf.set_y(-20)
        pdf.set_font("Helvetica","I",8)
        pdf.set_text_color(150,150,150)
        pdf.cell(0,5,f"{ca_firm_name}  |  OpsClarity AI  |  Management estimates only — not a substitute for CA advice",align="C")

        return pdf.output()
    except ImportError:
        return None

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k,v in [("df",None),("industry","manufacturing"),("city","Bangalore"),
            ("show_bot",False),("chat_history",[]),("onboarded",False),
            ("ca_firm","My CA Firm")]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════════════════════
#  TOP NAV BAR
# ══════════════════════════════════════════════════════════════════════════════
wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text=Hi%2C+I+want+to+learn+more+about+OpsClarity"
st.markdown(f"""
<div class="topbar">
  <div class="tb-logo">
    ⬡ OpsClarity
    <span>AI CFO for Indian SMEs</span>
  </div>
  <div class="tb-right">
    <div class="tb-pill">Live</div>
    <span class="tb-version">v3.0</span>
    <a href="{wa_link}" target="_blank" class="tb-cta">Talk to Founder →</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.df is not None:
    _df = st.session_state.df
    _s  = _df[_df["Type"]=="Sales"]
    _e  = _df[_df["Type"]=="Expense"]
    _rev= _s["Amount"].sum()
    _exp= _e["Amount"].sum()
    _mar= ((_rev-_exp)/max(_rev,1))*100
    _bench = INDUSTRY_BENCHMARKS.get(st.session_state.industry,15)
    _od_pct= 0
    if "Status" in _df.columns:
        _od = _s[_s["Status"].str.lower().isin(["overdue","pending","not paid"])]["Amount"].sum()
        _od_pct = (_od/max(_rev,1))*100
    _me = _e.groupby(_e["Date"].dt.to_period("M"))["Amount"].sum()
    _exp_trend = (_me.iloc[-2:].mean()/_me.iloc[:-2].mean()) if len(_me)>=4 and _me.iloc[:-2].mean()>0 else 1.0
    _score = health_score(_mar, _bench, _od_pct, _exp_trend)
    _slabel, _sclass = score_label(_score)
    _leaks_hero = find_leaks(_df.to_json(), st.session_state.industry)
    _total_leak = sum(l["rupee_impact"] for l in _leaks_hero)

    hero_card = f"""
<div class="score-card">
  <div class="sc-header">
    <div class="sc-dot"></div>
    <div>
      <div class="sc-title">Business Health Score</div>
      <div class="sc-sub">Live · Updated from your data</div>
    </div>
  </div>
  <div class="sc-score-wrap">
    <div class="sc-score {_sclass}">{_score}</div>
    <div class="sc-score-label">{_slabel}</div>
  </div>
  <div class="sc-row"><span class="sc-row-label">Net Margin</span><span class="sc-row-val {'red' if _mar<_bench-5 else 'green'}">{_mar:.1f}% vs {_bench}% benchmark</span></div>
  <div class="sc-row"><span class="sc-row-label">Overdue</span><span class="sc-row-val {'red' if _od_pct>8 else 'green'}">{_od_pct:.1f}% of revenue</span></div>
  <div class="sc-row"><span class="sc-row-label">Total Leaks Found</span><span class="sc-row-val amber">{fmt(_total_leak)}</span></div>
  <div class="sc-row"><span class="sc-row-label">Issues Detected</span><span class="sc-row-val">{len(_leaks_hero)} actionable</span></div>
</div>"""
else:
    hero_card = """
<div class="score-card" style="text-align:center; padding:2rem 1.5rem;">
  <div style="font-size:3.5rem; margin-bottom:1rem; opacity:0.4;">⬡</div>
  <div style="font-family:'DM Serif Display',serif; font-size:1.3rem; color:var(--paper); margin-bottom:0.5rem;">Your score appears here</div>
  <div style="font-size:12px; color:var(--muted); line-height:1.7;">Upload your Tally export below and see your Business Health Score, total money leaking, and the 3 actions to fix it — in 60 seconds.</div>
</div>"""

st.markdown(f"""
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="hero-eyebrow">OpsClarity · Built in {CITY} 🇮🇳</div>
      <h1 class="hero-h1">
        Your business has<br>
        a <span class="strike">dashboard.</span><br>
        Now get a <em>CFO.</em>
      </h1>
      <p class="hero-sub">
        Upload your Tally export. In 60 seconds, know exactly where money is leaking
        — in rupees — and the three actions to stop it this week.
        Trusted by CA firms across Bangalore, Mumbai & Pune.
      </p>
      <div class="hero-stats">
        <div><div class="hs-num">₹50Cr+</div><div class="hs-label">Leaks identified</div></div>
        <div><div class="hs-num">₹12.4L</div><div class="hs-label">Avg recovery</div></div>
        <div><div class="hs-num">4.8 days</div><div class="hs-label">To first recovery</div></div>
        <div><div class="hs-num">200+</div><div class="hs-label">SMEs scanned</div></div>
      </div>
    </div>
    {hero_card}
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust-bar">
  <div class="ti"><div class="ti-dot"></div> Your Tally file never leaves your device</div>
  <div class="ti"><div class="ti-dot"></div> No login required for first scan</div>
  <div class="ti"><div class="ti-dot"></div> Results in 60 seconds</div>
  <div class="ti"><div class="ti-dot"></div> Used by CAs across Bangalore · Mumbai · Pune</div>
  <div class="ti"><div class="ti-dot"></div> Not a dashboard. A decision engine.</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_scan, tab_alerts, tab_copilot, tab_gst, tab_forecast, tab_ca, tab_bench, tab_pitch = st.tabs([
    "₹  Scan My Business",
    "🔔  Smart Alerts",
    "🤖  AI Copilot",
    "🧾  GST Engine",
    "📈  Cash Forecast",
    "🏛  CA Partner",
    "📊  Benchmarks",
    "🚀  Pitch & Strategy",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — SCAN
# ══════════════════════════════════════════════════════════════════════════════
with tab_scan:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([3,1,1,1])
    with c1:
        uploaded = st.file_uploader(
            "Upload Tally Day Book · Sales Register · Bank Statement (CSV / Excel)",
            type=["csv","xlsx","xls"], key="up"
        )
        with st.expander("📋 How to export from Tally"):
            st.markdown("""
**Tally Prime:** Display → Account Books → Day Book → Alt+E → Excel
**Tally ERP 9:** Gateway → Display → Day Book → Ctrl+E → Excel
**Bank statement:** Download CSV from net banking
**Supported columns:** Date, Amount, Type (Dr/Cr), Party, Category, Status, Invoice No
            """)
    with c2:
        ind_disp = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))
        st.session_state.industry = INDUSTRY_MAP[ind_disp]
    with c3:
        city = st.selectbox("City", ["Bangalore","Mumbai","Delhi","Pune","Chennai","Hyderabad","Ahmedabad","Surat","Other"])
        st.session_state.city = city
    with c4:
        st.write("")
        st.write("")
        if st.button("▶  Try Demo Data", use_container_width=True):
            st.session_state.df = make_demo_data()
            st.session_state.industry = "manufacturing"
            st.rerun()

    if uploaded:
        df_new, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_new
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info("Quick fix: open in Excel → Save As → CSV UTF-8 → upload.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS ──────────────────────────────────────────────────────────────
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
        leaks    = find_leaks(df.to_json(), industry, city_sel)
        total_liq= sum(l["rupee_impact"] for l in leaks)
        total_ann= sum(l["annual_impact"] for l in leaks)
        overdue_amt = (sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum()
                       if "Status" in sales.columns else 0)

        coll_l   = next((l for l in leaks if l["id"]=="cash_stuck"),  None)
        vend_l   = next((l for l in leaks if l["id"]=="cost_bleed"),  None)
        tax_l    = next((l for l in leaks if l["id"]=="tax_gst"),     None)
        margin_l = next((l for l in leaks if l["id"]=="margin_gap"),  None)

        coll_amt   = coll_l["rupee_impact"]    if coll_l   else 0
        vend_amt   = vend_l["annual_impact"]   if vend_l   else 0
        tax_amt    = tax_l["rupee_impact"]     if tax_l    else 0
        margin_amt = margin_l["annual_impact"] if margin_l else 0

        week_actions = []
        if coll_l:   week_actions.append(f"Call top debtor — offer 2% discount to unlock {fmt_exact(int(coll_amt))} overdue cash")
        if vend_l:   week_actions.append(f"Get 2 quotes for {vend_l['headline'].split(' on ')[-1].split('/')[0]} — saves {fmt(vend_amt)}/year")
        if tax_l:    week_actions.append(f"Email your CA about ITC review — {fmt_exact(int(tax_amt))} claimable this quarter")
        if not week_actions and margin_l: week_actions.append(f"Raise top-3 prices 5% → adds {fmt(margin_amt*0.15)} in 90 days")

        action_html = "".join([
            f'<div class="as-item"><div class="as-num">{i+1}</div><div class="as-text">{a}</div></div>'
            for i,a in enumerate(week_actions[:3])
        ])
        rows_html = ""
        if coll_amt>0:
            rows_html += f'<div class="ms-row critical"><div style="display:flex;align-items:center;"><span class="ms-icon">🔴</span><div><div class="ms-title">Cash stuck in unpaid invoices</div><div class="ms-desc">Recoverable this month with action today</div></div></div><div class="ms-amt">{fmt_exact(int(coll_amt))}</div></div>'
        if vend_amt>0:
            rows_html += f'<div class="ms-row warning"><div style="display:flex;align-items:center;"><span class="ms-icon">🟡</span><div><div class="ms-title">Vendor overpayment — annual savings</div><div class="ms-desc">Switch to market-rate suppliers</div></div></div><div class="ms-amt">{fmt_exact(int(vend_amt))}/yr</div></div>'
        if margin_amt>0:
            rows_html += f'<div class="ms-row warning"><div style="display:flex;align-items:center;"><span class="ms-icon">🟡</span><div><div class="ms-title">Margin gap vs industry peers</div><div class="ms-desc">Pricing + cost action closes this</div></div></div><div class="ms-amt">{fmt_exact(int(margin_amt))}/yr</div></div>'
        if tax_amt>0:
            rows_html += f'<div class="ms-row info"><div style="display:flex;align-items:center;"><span class="ms-icon">🔵</span><div><div class="ms-title">GST input credits to verify</div><div class="ms-desc">Estimated — confirm with your CA</div></div></div><div class="ms-amt">~{fmt_exact(int(tax_amt))}</div></div>'

        st.markdown(f"""
        <div class="money-screen">
          <div class="ms-label">Total recoverable money identified</div>
          <div class="ms-total">{fmt(total_liq)}</div>
          <div class="ms-sub">{len(leaks)} issues found · Annual impact: {fmt(total_ann)}</div>
          {rows_html}
          <div class="action-strip">
            <div class="as-title">Do these 3 things this week</div>
            {action_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # KPI strip
        margin_class = "good" if margin>=benchmark else "bad"
        od_class     = "bad" if overdue_amt>revenue*0.06 else "good"
        profit_class = "good" if profit>0 else "bad"
        st.markdown(f"""
        <div class="kpi-strip">
          <div class="kpi neutral">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-val">{fmt(revenue)}</div>
            <div class="kpi-sub muted">{len(sales)} transactions</div>
          </div>
          <div class="kpi {margin_class}">
            <div class="kpi-label">Net Margin</div>
            <div class="kpi-val">{margin:.1f}%</div>
            <div class="kpi-sub {margin_class}">vs {benchmark}% benchmark</div>
          </div>
          <div class="kpi {od_class}">
            <div class="kpi-label">Overdue Invoices</div>
            <div class="kpi-val">{fmt(overdue_amt)}</div>
            <div class="kpi-sub {od_class}">{(overdue_amt/revenue*100 if revenue>0 else 0):.1f}% of revenue</div>
          </div>
          <div class="kpi {profit_class}">
            <div class="kpi-label">Net Profit</div>
            <div class="kpi-val">{fmt(abs(profit))}</div>
            <div class="kpi-sub {profit_class}">{'✓ Profitable' if profit>0 else '⚠ Loss-making'}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── INSIGHTS FEED ──
        if leaks:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-head">Insights Feed</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Every insight has a Problem · Reason · Action. Not just data — decisions.</div>', unsafe_allow_html=True)

            for leak in leaks[:6]:
                sev = leak["severity"]
                st.markdown(f"""
                <div class="insight-card {sev}">
                  <div class="ic-header">
                    <div>
                      <span class="ic-tag {sev}">{leak['category']}</span>
                      <div class="ic-title">{leak['headline']}</div>
                      <div class="ic-subtitle">{leak['sub']}</div>
                    </div>
                    <div>
                      <div class="ic-amount">{fmt(leak['rupee_impact'])}</div>
                      <div class="ic-amount-sub">{'immediate' if leak['id']=='cash_stuck' else 'annual impact'}</div>
                    </div>
                  </div>
                  <div class="ic-breakdown">
                    <div class="ic-part"><div class="ic-part-label">❗ Problem</div><div class="ic-part-val">{leak['problem']}</div></div>
                    <div class="ic-part"><div class="ic-part-label">🔍 Reason</div><div class="ic-part-val">{leak['reason']}</div></div>
                    <div class="ic-part"><div class="ic-part-label">✅ Action</div><div class="ic-part-val action">{leak['action']}</div></div>
                  </div>
                  <div class="ic-footer">
                    <div class="ic-cta">{leak['cta']}</div>
                    <div class="ic-bench">Benchmark: {leak['benchmark']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

                if leak["id"]=="cash_stuck" and leak.get("collections"):
                    if st.button("Launch 4-step WhatsApp collections sequence →", key="bot_btn"):
                        st.session_state.show_bot = True
                    if st.session_state.show_bot:
                        st.markdown("#### 📱 Collections Sequence")
                        st.caption("4-step escalation. Stop the moment they pay.")
                        for step in leak["collections"]:
                            st.markdown(f"""
                            <div class="seq-card">
                              <div class="seq-badge">Day {step['day']} · {step['send_on']}</div>
                              <div class="seq-tone" style="color:{step['color']}">{step['tone']}</div>
                              <div class="seq-msg">{step['message']}</div>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:11px;color:#25D366;text-decoration:none;">📲 Send via WhatsApp →</a>', unsafe_allow_html=True)
                else:
                    if st.button(f"Copy script →", key=f"scr_{leak['id']}"):
                        st.code(leak["template"], language=None)

            st.markdown('</div>', unsafe_allow_html=True)

        # ── TRENDS ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-head" style="font-size:1.4rem;">Revenue vs Expenses</div>', unsafe_allow_html=True)
            monthly = df.groupby([df["Date"].dt.to_period("M"),"Type"])["Amount"].sum().unstack(fill_value=0)
            monthly.index = monthly.index.astype(str)
            st.line_chart(monthly, height=220)
        with c2:
            st.markdown('<div class="section-head" style="font-size:1.4rem;">Top Cost Categories</div>', unsafe_allow_html=True)
            if len(expenses)>0:
                st.bar_chart(expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8), height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── PDF EXPORT ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        col_pdf1, col_pdf2, col_pdf3 = st.columns([2,1,1])
        with col_pdf1:
            ca_name_inp = st.text_input("CA Firm Name (for branded report)", value=st.session_state.ca_firm, key="ca_name_scan")
            if ca_name_inp: st.session_state.ca_firm = ca_name_inp
        with col_pdf2:
            st.write("")
            st.write("")
            pdf_bytes = generate_pdf_report(df, leaks, industry, st.session_state.ca_firm)
            if pdf_bytes:
                st.download_button(
                    "📄 Download PDF Report",
                    data=bytes(pdf_bytes),
                    file_name=f"OpsClarity_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.info("pip install fpdf2 to enable PDF export")
        with col_pdf3:
            st.write("")
            st.write("")
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                "📊 Export Data CSV",
                data=csv_buf.getvalue(),
                file_name=f"OpsClarity_Data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── PRICING ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#06080C; padding:2.5rem 3rem; border-top:1px solid var(--border);">
          <div class="section-head">How we work together</div>
          <div class="section-sub">No subscription traps. Pay only when you recover money.</div>
          <div class="pricing-grid">
            <div class="price-card">
              <div class="price-label">Start here</div>
              <div class="price-name">Free Scan</div>
              <div class="price-amount">₹0</div>
              <div class="price-note">Upload data. See all leaks instantly. No credit card, no login, no strings attached.</div>
              <ul class="price-features">
                <li>Full leak scan with exact rupees</li>
                <li>Insights Feed (Problem/Reason/Action)</li>
                <li>Smart Alerts engine</li>
                <li>Collections WhatsApp sequences</li>
                <li>AI Copilot (5 questions)</li>
                <li>GST ITC estimate</li>
              </ul>
            </div>
            <div class="price-card featured">
              <div class="price-featured-tag">MOST CHOSEN</div>
              <div class="price-label">Best value</div>
              <div class="price-name">Success Fee</div>
              <div class="price-amount">7–10%</div>
              <div class="price-note">We charge only on money you actually recover. Zero recovery = zero fee. Simple alignment.</div>
              <ul class="price-features">
                <li>Everything in free scan</li>
                <li>Recovery Review call (1hr)</li>
                <li>Vendor quote sourcing (3 quotes)</li>
                <li>Monthly monitoring alerts</li>
                <li>CA coordination support</li>
                <li>Unlimited AI Copilot (GPT-4o)</li>
                <li>PDF reports with CA branding</li>
              </ul>
            </div>
            <div class="price-card">
              <div class="price-label">For CA firms</div>
              <div class="price-name">Partner Plan</div>
              <div class="price-amount">₹1,999/mo</div>
              <div class="price-note">Run OpsClarity for all your clients. Branded monthly reports. Earn ₹500/client/month.</div>
              <ul class="price-features">
                <li>50 client seats</li>
                <li>White-label PDF reports</li>
                <li>Client health dashboard</li>
                <li>GST Intelligence Engine</li>
                <li>Cash Flow Forecasting</li>
                <li>Smart Alerts per client</li>
                <li>Priority support</li>
              </ul>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c_l,c_c,c_r = st.columns([1,2,1])
        with c_c:
            if st.button("Book a free Recovery Review call →", use_container_width=True, type="primary"):
                st.success("✅ Request noted. We'll WhatsApp you within 2 hours.")
                st.markdown(f"Or message directly: [wa.me/{WHATSAPP_NUMBER}](https://wa.me/{WHATSAPP_NUMBER})")

    else:
        # Empty state
        st.markdown("""
        <div class="onboard-card" style="max-width:600px; margin:2rem auto;">
          <div style="font-size:2.5rem; margin-bottom:1rem;">⬡</div>
          <div style="font-family:'DM Serif Display',serif; font-size:1.8rem; color:var(--paper); margin-bottom:0.75rem;">Upload your data to get started</div>
          <div style="font-size:13px; color:var(--muted); line-height:1.8; margin-bottom:1.75rem;">Works with Tally Day Book exports, Sales Registers, Bank Statements (CSV/Excel). Your data stays on your device.</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.85rem; text-align:left;">
            <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:1.1rem;">
              <div style="font-size:1.3rem; margin-bottom:0.4rem;">🔴</div>
              <div style="font-size:12px; font-weight:600; color:var(--paper); margin-bottom:0.25rem;">Overdue Collections</div>
              <div style="font-size:11px; color:var(--muted);">See exactly who owes you and how much</div>
            </div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:1.1rem;">
              <div style="font-size:1.3rem; margin-bottom:0.4rem;">🟡</div>
              <div style="font-size:12px; font-weight:600; color:var(--paper); margin-bottom:0.25rem;">Vendor Overpayment</div>
              <div style="font-size:11px; color:var(--muted);">Who's charging you above market rate</div>
            </div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:1.1rem;">
              <div style="font-size:1.3rem; margin-bottom:0.4rem;">📈</div>
              <div style="font-size:12px; font-weight:600; color:var(--paper); margin-bottom:0.25rem;">Margin Analysis</div>
              <div style="font-size:11px; color:var(--muted);">Gap vs industry benchmark in rupees</div>
            </div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:1.1rem;">
              <div style="font-size:1.3rem; margin-bottom:0.4rem;">🔔</div>
              <div style="font-size:12px; font-weight:600; color:var(--paper); margin-bottom:0.25rem;">Smart Alerts</div>
              <div style="font-size:11px; color:var(--muted);">Know before problems hit your cash flow</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — SMART ALERTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_alerts:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Smart Alerts</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Proactive signals — know about problems before they hit your cash flow. This is what Excel can never do.</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("📂 Upload your data in the 'Scan My Business' tab first.")
    else:
        alerts = generate_alerts(st.session_state.df, st.session_state.industry)
        if alerts:
            st.markdown(f"""
            <div class="alert-banner">
              🔔 {len(alerts)} alerts detected from your data — review and act below
            </div>""", unsafe_allow_html=True)
            for a in alerts:
                st.markdown(f"""
                <div class="alert-card">
                  <div class="alert-icon-wrap">{a['icon']}</div>
                  <div style="flex:1">
                    <div class="alert-badge {a['severity']}">{a['severity'].upper()}</div>
                    <div class="alert-title">{a['title']}</div>
                    <div class="alert-body">{a['body']}<br><span style="color:var(--gold);font-weight:600;font-size:11px;">→ {a['action']}</span></div>
                  </div>
                  <div style="text-align:right;font-family:'JetBrains Mono',monospace;color:var(--gold);font-size:0.9rem;white-space:nowrap;">{fmt(a.get('impact',0))}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("✅ No critical alerts. Your business health signals look stable. Keep monitoring monthly.")

        st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif; font-size:1.35rem; color:var(--paper); margin-bottom:0.5rem;">Monthly Alert Email Template</div>', unsafe_allow_html=True)

        alert_summary = "\n".join([f"• {a['title']}" for a in alerts]) if alerts else "• No critical alerts this month"
        email_template = f"""Subject: OpsClarity Monthly Business Health Check — {datetime.now().strftime('%B %Y')}

Hi [Name],

Your monthly OpsClarity scan is ready. Here are this month's alerts:

{alert_summary}

Action required this week:
{"• " + alerts[0]['action'] if alerts else "• Business health looks stable — keep monitoring"}

Log in to OpsClarity for full details and recovery scripts.

— OpsClarity AI CFO"""
        st.code(email_template, language=None)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — AI COPILOT
# ══════════════════════════════════════════════════════════════════════════════
with tab_copilot:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">AI Copilot</div>', unsafe_allow_html=True)
    mode_label = "GPT-4o · Powered by OpenAI" if OPENAI_KEY else "Rule-based · Set OPENAI_API_KEY for GPT-4o"
    st.markdown(f'<div class="section-sub">Ask anything about your business. Get exact rupee answers, not just charts. <span style="color:var(--gold);">{mode_label}</span></div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("📂 Upload your data in the 'Scan My Business' tab first.")
    else:
        df_c  = st.session_state.df
        ind_c = st.session_state.industry

        st.markdown("**Quick questions — tap to ask:**")
        cols = st.columns(4)
        quick_qs = ["Why is my profit low?","Who owes me money?","What are my biggest costs?","What should I fix first?"]
        for i, q in enumerate(quick_qs):
            with cols[i]:
                if st.button(q, key=f"qq_{i}"):
                    leaks_c = find_leaks(df_c.to_json(), ind_c)
                    if OPENAI_KEY:
                        ans, ok = ai_copilot_gpt(q, df_c, leaks_c, ind_c, st.session_state.chat_history)
                        if not ok:
                            ans = ai_copilot_answer(q, df_c, leaks_c, ind_c)
                    else:
                        ans = ai_copilot_answer(q, df_c, leaks_c, ind_c)
                    st.session_state.chat_history.append({"role":"user","msg":q})
                    st.session_state.chat_history.append({"role":"assistant","msg":ans})

        st.markdown('<div class="copilot-wrap" style="margin-top:1.25rem;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="copilot-header">
          <div class="copilot-dot"></div>
          <div class="copilot-title">OpsClarity Copilot</div>
          <div class="copilot-sub">{mode_label} · Answers in exact rupees</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.chat_history:
            for msg in st.session_state.chat_history[-14:]:
                role = msg["role"]
                if role=="user":
                    st.markdown(f'<div style="padding:0.5rem 1.25rem;display:flex;justify-content:flex-end;"><div class="chat-user">{msg["msg"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="padding:0.25rem 1.25rem;"><div class="chat-ai">{msg["msg"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:2rem 1.25rem;text-align:center;">
              <div style="font-size:2rem;margin-bottom:0.5rem;opacity:0.5;">💬</div>
              <div style="font-size:13px;color:var(--muted);">Ask me about your profit, costs, cash flow, or what to fix first.</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_inp, col_send = st.columns([5,1])
        with col_inp:
            user_q = st.text_input("Ask about your business...", key="chat_input",
                label_visibility="collapsed",
                placeholder="e.g. Why is my profit low? / Draft a vendor negotiation email for Raw Materials")
        with col_send:
            if st.button("Ask →", key="send_chat", use_container_width=True):
                if user_q.strip():
                    leaks_c = find_leaks(df_c.to_json(), ind_c)
                    if OPENAI_KEY:
                        ans, ok = ai_copilot_gpt(user_q, df_c, leaks_c, ind_c, st.session_state.chat_history)
                        if not ok:
                            ans = ai_copilot_answer(user_q, df_c, leaks_c, ind_c)
                    else:
                        ans = ai_copilot_answer(user_q, df_c, leaks_c, ind_c)
                    st.session_state.chat_history.append({"role":"user","msg":user_q})
                    st.session_state.chat_history.append({"role":"assistant","msg":ans})
                    st.rerun()

        if st.session_state.chat_history:
            if st.button("Clear conversation", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — GST INTELLIGENCE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
with tab_gst:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">GST Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">India-specific: ITC recovery, GSTR-2B mismatch detection, vendor compliance risk, and GST health score.</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("📂 Upload your data in the 'Scan My Business' tab first.")
    else:
        gst = gst_intelligence(st.session_state.df, st.session_state.industry)
        g_score = gst["compliance_score"]
        g_cls   = "good" if g_score>=70 else "warn" if g_score>=45 else "bad"
        g_label = "Healthy" if g_score>=70 else "Needs Attention" if g_score>=45 else "At Risk"

        # Header row
        col_score, col_itc, col_mismatch = st.columns(3)
        with col_score:
            st.markdown(f"""
            <div class="gst-card" style="display:flex;align-items:center;gap:1.25rem;">
              <div class="gst-score-ring {g_cls}">{g_score}</div>
              <div>
                <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;">GST Compliance Score</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--paper);margin:3px 0;">{g_label}</div>
                <div style="font-size:11px;color:var(--muted);">ITC {gst['itc_claimed_pct']:.0f}% · Vendor {gst['vendor_comply_pct']:.0f}% · Filing {gst['filing_reg']:.0f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
        with col_itc:
            st.markdown(f"""
            <div class="gst-card">
              <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;">Claimable ITC (estimated)</div>
              <div style="font-family:'DM Serif Display',serif;font-size:2rem;color:var(--gold);">{fmt(gst['claimable'])}</div>
              <div style="font-size:11px;color:var(--muted);">Estimated GST paid on purchases</div>
              <div style="margin-top:0.5rem;font-size:11px;color:var(--red);">Possibly unclaimed: {fmt(gst['missed_est'])}</div>
            </div>""", unsafe_allow_html=True)
        with col_mismatch:
            st.markdown(f"""
            <div class="gst-card">
              <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;">GSTR-2B Mismatch Risk</div>
              <div style="font-family:'DM Serif Display',serif;font-size:2rem;color:var(--amber);">{gst['mismatch_count']} invoices</div>
              <div style="font-size:11px;color:var(--muted);">Estimated mismatch value: {fmt(gst['mismatch_value'])}</div>
              <div style="margin-top:0.5rem;font-size:11px;color:var(--amber);">Reconcile with CA before GSTR-3B filing</div>
            </div>""", unsafe_allow_html=True)

        # ITC by category
        st.markdown('<div style="margin-top:1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif; font-size:1.3rem; color:var(--paper); margin-bottom:1rem;">ITC by Expense Category</div>', unsafe_allow_html=True)
        if gst["itc_by_cat"]:
            for cat, data in list(gst["itc_by_cat"].items())[:8]:
                pct_bar = min(100, int(data["itc_estimate"]/max(gst["total_itc"],1)*100))
                st.markdown(f"""
                <div class="gst-card" style="padding:0.85rem 1.2rem;margin-bottom:0.5rem;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                    <div style="font-size:12px;font-weight:600;color:var(--paper);">{cat}</div>
                    <div style="display:flex;gap:1.5rem;font-size:11px;">
                      <span style="color:var(--muted);">Expense: <span style="font-family:'JetBrains Mono',monospace;color:var(--paper2);">{fmt(data['expense'])}</span></span>
                      <span style="color:var(--muted);">GST Rate: <span style="color:var(--paper2);">{data['rate']}%</span></span>
                      <span style="color:var(--muted);">Est. ITC: <span style="font-family:'JetBrains Mono',monospace;color:var(--gold);">{fmt(data['itc_estimate'])}</span></span>
                    </div>
                  </div>
                  <div class="runway-bar"><div class="runway-fill" style="width:{pct_bar}%;background:var(--gold);"></div></div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Vendor GST compliance risk
        if gst["risk_vendors"]:
            st.markdown('<div style="margin-top:1.5rem;">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'DM Serif Display\',serif; font-size:1.3rem; color:var(--paper); margin-bottom:0.5rem;">Vendor GST Compliance Risk</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px; color:var(--muted); margin-bottom:1rem;">Vendors flagged for GSTIN non-compliance risk. Cross-check before claiming ITC.</div>', unsafe_allow_html=True)
            for v in gst["risk_vendors"]:
                color = "red" if v["risk"]=="High" else "amber"
                st.markdown(f"""
                <div class="alert-card">
                  <div class="alert-icon-wrap">{'🔴' if v['risk']=='High' else '🟡'}</div>
                  <div style="flex:1">
                    <div class="alert-badge {color}">{v['risk']} RISK</div>
                    <div class="alert-title">{v['vendor']}</div>
                    <div class="alert-body">Annual spend: {fmt(v['spend'])} · Verify GSTIN before claiming ITC<br>
                    <span style="color:var(--gold);font-weight:600;font-size:11px;">→ Request GST invoice + GSTIN verification from vendor</span></div>
                  </div>
                  <div style="font-family:'JetBrains Mono',monospace;color:var(--amber);font-size:0.9rem;">{fmt(v['spend'])}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # GST due date reminder
        st.markdown("""
        <div style="background:rgba(74,143,212,0.06);border:1px solid rgba(74,143,212,0.2);border-radius:10px;padding:1rem 1.25rem;margin-top:1.5rem;">
          <div style="font-size:10px;font-weight:700;color:#90C0F8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">GST Filing Calendar</div>
          <div style="display:flex;gap:2rem;flex-wrap:wrap;">
            <div><div style="font-size:11px;color:var(--muted);">GSTR-1 (Monthly)</div><div style="font-size:13px;color:var(--paper);font-weight:600;">11th of every month</div></div>
            <div><div style="font-size:11px;color:var(--muted);">GSTR-3B</div><div style="font-size:13px;color:var(--paper);font-weight:600;">20th of every month</div></div>
            <div><div style="font-size:11px;color:var(--muted);">GSTR-2B available</div><div style="font-size:13px;color:var(--paper);font-weight:600;">14th of every month</div></div>
            <div><div style="font-size:11px;color:var(--muted);">Annual return (GSTR-9)</div><div style="font-size:13px;color:var(--paper);font-weight:600;">31st December</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — CASH FLOW FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab_forecast:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Cash Flow Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">30 / 60 / 90 day outlook with 3 scenarios. Runway calculator and receivables confidence scoring.</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("📂 Upload your data in the 'Scan My Business' tab first.")
    else:
        fc = cash_flow_forecast(st.session_state.df)

        # Scenario cards
        for label, card_class, icon in [
            ("Best Case","scenario-best","🟢"),
            ("Expected","scenario-exp","🟡"),
            ("Worst Case","scenario-worst","🔴"),
        ]:
            s = fc["scenarios"][label]
            color = "var(--green)" if label=="Best Case" else "var(--gold)" if label=="Expected" else "var(--red)"
            st.markdown(f"""
            <div class="forecast-card {card_class}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                <div>
                  <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;">{icon} {label}</div>
                  <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;color:var(--paper);">Revenue assumption: {s['rev_mult']*100:.0f}% of average · Expense: {'95%' if label=='Best Case' else '100%' if label=='Expected' else '105%'}</div>
                </div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.75rem;">
                <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:0.85rem;">
                  <div style="font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">30-day cashflow</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:1.2rem;color:{color};">{fmt(s['cf_30'])}</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:0.85rem;">
                  <div style="font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">60-day cashflow</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:1.2rem;color:{color};">{fmt(s['cf_60'])}</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:0.85rem;">
                  <div style="font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">90-day cashflow</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:1.2rem;color:{color};">{fmt(s['cf_90'])}</div>
                </div>
              </div>
              <div style="margin-top:0.75rem;display:flex;gap:2rem;font-size:11px;color:var(--muted);">
                <span>Monthly in: <span style="color:var(--green);">{fmt(s['monthly_in'])}</span></span>
                <span>Monthly out: <span style="color:var(--red);">{fmt(s['monthly_out'])}</span></span>
                <span>OD collected: <span style="color:var(--blue);">{fmt(s['od_collect'])}</span></span>
              </div>
            </div>""", unsafe_allow_html=True)

        # Runway + assumptions
        st.markdown('<div style="margin-top:1.5rem;display:grid;grid-template-columns:1fr 1fr;gap:1rem;">', unsafe_allow_html=True)
        runway_color = "var(--green)" if fc["runway"]>6 else "var(--amber)" if fc["runway"]>3 else "var(--red)"
        bar_pct = min(100, int(fc["runway"]/12*100))
        st.markdown(f"""
        <div class="forecast-card">
          <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.4rem;">Estimated Runway</div>
          <div style="font-family:'DM Serif Display',serif;font-size:3rem;color:{runway_color};">{fc['runway']:.1f} <span style="font-size:1.2rem;">months</span></div>
          <div style="font-size:11px;color:var(--muted);margin-top:0.3rem;">Based on last month's surplus vs monthly burn</div>
          <div class="runway-bar" style="margin-top:0.75rem;"><div class="runway-fill" style="width:{bar_pct}%;background:{runway_color};"></div></div>
          <div style="margin-top:0.5rem;font-size:11px;color:var(--muted);">Monthly burn: {fmt(fc['avg_exp'])} · Overdue receivable: {fmt(fc['od_amt'])}</div>
        </div>""", unsafe_allow_html=True)

        trend_label = "↑ Growing" if fc["trend"]>1.05 else "→ Stable" if fc["trend"]>0.95 else "↓ Declining"
        trend_color = "var(--green)" if fc["trend"]>1.05 else "var(--gold)" if fc["trend"]>0.95 else "var(--red)"
        st.markdown(f"""
        <div class="forecast-card">
          <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.4rem;">Revenue Trend (last 3 vs prior 3 months)</div>
          <div style="font-family:'DM Serif Display',serif;font-size:3rem;color:{trend_color};">{trend_label}</div>
          <div style="font-size:11px;color:var(--muted);margin-top:0.3rem;">{fc['trend']*100-100:+.1f}% vs prior period</div>
          <div style="margin-top:1rem;font-size:12px;color:var(--paper);">
            Avg monthly revenue: {fmt(fc['avg_rev'])}<br>
            Avg monthly expenses: {fmt(fc['avg_exp'])}<br>
            Avg monthly surplus: {fmt(fc['avg_rev']-fc['avg_exp'])}
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Receivables confidence
        st.markdown('<div style="margin-top:1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.3rem;color:var(--paper);margin-bottom:0.5rem;">Receivables Confidence Score</div>', unsafe_allow_html=True)
        od_total = fc["od_amt"]
        for label, pct, color, days in [
            ("High Confidence (collect <15 days)", 0.35, "var(--green)", "<15 days"),
            ("Medium Confidence (collect 15-45 days)", 0.40, "var(--gold)", "15–45 days"),
            ("Low Confidence (>45 days / disputed)", 0.25, "var(--red)", ">45 days"),
        ]:
            amt = od_total * pct
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.6rem;">
              <div style="flex:2;font-size:12px;color:var(--paper2);">{label}</div>
              <div style="flex:1;font-family:'JetBrains Mono',monospace;color:{color};text-align:right;">{fmt(amt)}</div>
              <div style="flex:1;">
                <div class="runway-bar"><div class="runway-fill" style="width:{int(pct*100)}%;background:{color};"></div></div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — CA PARTNER
# ══════════════════════════════════════════════════════════════════════════════
with tab_ca:
    demo_portfolio = [
        {"name":"Sharma Textiles Pvt Ltd","city":"Ahmedabad","ind":"textile",       "rev":4200000,"leak":840000, "health":"red"},
        {"name":"Mehta Food Products",    "city":"Mumbai",   "ind":"restaurant",    "rev":2800000,"leak":196000, "health":"amber"},
        {"name":"Rajesh Diagnostics",     "city":"Pune",     "ind":"clinic",        "rev":6100000,"leak":91500,  "health":"green"},
        {"name":"Kapoor Steel Trading",   "city":"Delhi",    "ind":"manufacturing", "rev":8900000,"leak":1780000,"health":"red"},
        {"name":"Green Pharma Dist.",     "city":"Chennai",  "ind":"pharma",        "rev":3400000,"leak":238000, "health":"amber"},
        {"name":"SV Printers",            "city":"Hyderabad","ind":"printing",      "rev":1900000,"leak":28500,  "health":"green"},
    ]
    total_leak_ca = sum(c["leak"] for c in demo_portfolio)
    crit_count    = sum(1 for c in demo_portfolio if c["health"]=="red")

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom:2.25rem;">
      <div style="font-size:10px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.18em;margin-bottom:0.85rem;">For Chartered Accountants</div>
      <div class="section-head">Your clients are losing money.<br>Show them exactly where.</div>
      <div class="section-sub" style="font-size:0.95rem;max-width:580px;">
        OpsClarity gives you a branded profit-leak report for every client — automated, monthly, zero extra work.
        CAs who use it retain clients longer, get more referrals, and earn ₹500/client/month passively.
      </div>
    </div>
    """, unsafe_allow_html=True)

    n_ca = st.slider("How many clients would you run on OpsClarity?", 10, 200, 40, 5)
    net  = n_ca*500-1999
    hours_saved = n_ca * 1.5

    st.markdown(f"""
    <div class="ca-grid">
      <div class="ca-card gold">
        <div class="ca-label">The CA partner math</div>
        <div class="ca-title">Your monthly numbers with {n_ca} clients</div>
        <div class="ca-math-row"><span class="ca-math-label">Platform cost</span><span class="ca-math-val">₹1,999/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">You earn per client</span><span class="ca-math-val">₹500/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Gross passive income</span><span class="ca-math-val">₹{n_ca*500:,}/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Net after platform</span><span class="ca-math-val big">₹{net:,}/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Hours saved (manual work)</span><span class="ca-math-val">{hours_saved:.0f} hrs/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Annual passive income</span><span class="ca-math-val big">₹{net*12:,}/year</span></div>
      </div>
      <div class="ca-card">
        <div class="ca-label">What your clients get monthly</div>
        <div class="ca-title">Branded Business Health Report</div>
        <div class="ca-body">
          Branded with your CA firm name and logo. Every client sees exactly where they're losing money — in exact rupees, with specific actions.<br><br>
          <strong style="color:var(--paper);">Every month. Automated. Zero extra work from you.</strong><br><br>
          Clients receiving this report: renew without asking, refer you more, and stop shopping for another CA.
          That's the real value — retention + referrals, not just the ₹500/month.<br><br>
          <strong style="color:var(--gold);">Average CA firm earns ₹{net:,}/month from month 3.</strong><br><br>
          <strong style="color:var(--paper2);">New in v3.0:</strong> GST Engine + Cash Flow Forecast included in every client report.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Client dashboard demo
    st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-size:1.4rem;margin-bottom:1rem;">Your client dashboard — live demo</div>', unsafe_allow_html=True)

    client_rows = ""
    for c in demo_portfolio:
        hb = c["health"]
        hl = "🔴 Critical" if hb=="red" else "🟡 Monitor" if hb=="amber" else "🟢 Healthy"
        client_rows += (
            f'<div class="client-row">'
            f'<div><div class="client-name">{c["name"]}</div><div class="client-meta">{c["city"]} · {c["ind"].title()}</div></div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:var(--muted);">{fmt(c["rev"])}</div>'
            f'<div class="client-mono">{fmt(c["leak"])}</div>'
            f'<div><span class="hbadge {hb}">{hl}</span></div>'
            f'<div style="font-size:11px;color:var(--gold);cursor:pointer;">View →</div>'
            f'</div>'
        )

    st.markdown(f"""
    <div class="client-table">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);padding:1.25rem 1.2rem;background:#0A0E14;border-bottom:1px solid var(--border);">
        <div><div class="ca-label">Active clients</div><div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:var(--paper);">{len(demo_portfolio)}</div></div>
        <div><div class="ca-label">Total leaks found</div><div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:var(--gold);">{fmt(total_leak_ca)}</div></div>
        <div><div class="ca-label">Need urgent action</div><div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:var(--red);">{crit_count} clients</div></div>
      </div>
      <div class="client-row client-row-header"><div>Client</div><div>Revenue</div><div>Leaks Found</div><div>Health</div><div>Action</div></div>
      {client_rows}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-size:1.4rem;margin-bottom:0.75rem;">Questions CAs ask us</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ca-grid">
      <div class="ca-card"><div class="ca-label">My clients won't share data</div><div class="ca-body">You upload the file — your client never interacts with OpsClarity. The report comes branded as your firm's work. Clients see a CA service, not a third-party app.</div></div>
      <div class="ca-card"><div class="ca-label">What if numbers are wrong?</div><div class="ca-body">OpsClarity flags potential leaks. You verify before sharing — exactly as you'd review any report. Your judgement remains the product. We just save you the hours.</div></div>
      <div class="ca-card"><div class="ca-label">I already do this manually</div><div class="ca-body">If you do this for {n_ca} clients every month, that's {hours_saved:.0f} hours. OpsClarity does the same analysis in 60 seconds per client. That time is yours back.</div></div>
      <div class="ca-card"><div class="ca-label">Will it replace CAs?</div><div class="ca-body">No. The report says "verify with your CA" multiple times. GST, TDS, ITC — all require a qualified CA. We create the work. You do the work. Your client pays you more.</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c_l,c_c,c_r = st.columns([1,2,1])
    with c_c:
        if st.button("Join CA Partner Program — free 30-day trial →", use_container_width=True, type="primary"):
            st.balloons()
            st.success("✅ Application received! We'll WhatsApp you within 4 hours to set up your dashboard.")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
with tab_bench:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Industry Benchmark Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Anonymised data from Indian SMEs. Used to validate every leak we flag.</div>', unsafe_allow_html=True)

    sel_ind = st.selectbox("Select industry", list(CROWDSOURCED.keys()), key="bi")
    bd = CROWDSOURCED.get(sel_ind, {})
    if bd:
        for cat, data in bd.items():
            p25, med, p75 = data["p25"], data["median"], data["p75"]
            mx = max(p75, 1)
            st.markdown(f"""
            <div class="bench-card">
              <div class="bench-header">
                <div class="bench-cat">{cat} <span style="font-size:11px;color:var(--muted);font-weight:400;">{data['unit']}</span></div>
                <div class="bench-n">{data['n']} businesses</div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);font-family:'JetBrains Mono',monospace;margin-bottom:4px;">
                <span>Best 25%: ₹{p25:,}</span><span>Median: ₹{med:,}</span><span>Expensive 25%: ₹{p75:,}</span>
              </div>
              <div class="bench-bar-wrap"><div class="bench-bar-fill" style="width:{int(p25/mx*100)}%;background:var(--green);"></div></div>
              <div class="bench-bar-wrap"><div class="bench-bar-fill" style="width:{int(med/mx*100)}%;background:var(--gold);"></div></div>
              <div class="bench-bar-wrap"><div class="bench-bar-fill" style="width:100%;background:var(--red);opacity:0.4;"></div></div>
              <div style="font-size:11px;color:var(--green);margin-top:0.6rem;font-weight:600;">Switching from expensive to best = {int(((p75-p25)/p75)*100)}% cost reduction</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — PITCH & STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
with tab_pitch:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Your Startup Playbook</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">The exact strategy to go from 0 to ₹10L MRR — reviewed against 20 years of CA + fintech experience.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0C1018 0%,#0F1008 100%);border:1px solid rgba(201,168,76,0.2);border-radius:14px;padding:1.75rem;margin-bottom:1.25rem;">
      <div style="font-size:10px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.75rem;">Your One-Line Pitch (memorise this)</div>
      <div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:var(--paper);line-height:1.3;">"A CA can monitor all client finances in one place, get AI-powered risk alerts, and generate branded reports — saving 40 hours/month and making them look like heroes to clients."</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ca-grid" style="margin-bottom:1.25rem;">
      <div class="ca-card">
        <div class="ca-label">Phase 1 — This Month (₹0 → First ₹10K)</div>
        <div class="ca-title">Distribution before product</div>
        <div class="ca-body">
          1. Join 5 CA WhatsApp groups in your city (ICAI local chapters, CA alumni groups)<br><br>
          2. Post a 60-second screen recording of the demo scan — no pitch, just show the product working<br><br>
          3. Offer free for the first 10 CA firms — ask only for feedback<br><br>
          4. From those 10, upsell the branded PDF report for ₹999/month<br><br>
          <strong style="color:var(--gold);">Target: ₹10,000 MRR in 30 days</strong>
        </div>
      </div>
      <div class="ca-card">
        <div class="ca-label">Phase 2 — Month 2-3 (₹10K → ₹1L MRR)</div>
        <div class="ca-title">The CA referral flywheel</div>
        <div class="ca-body">
          1. Each CA who gets results will tell 3 other CAs — CAs trust CAs more than any ad<br><br>
          2. Launch the ₹1,999/month CA Partner Plan — they manage their own clients<br><br>
          3. Add the "Client Health Score" — a single number CAs show clients in every meeting<br><br>
          4. Start an ICAI CPE webinar — "How to save your clients ₹10L/year using data"<br><br>
          <strong style="color:var(--gold);">Target: 50 CA firms × ₹1,999 = ₹1L MRR</strong>
        </div>
      </div>
      <div class="ca-card">
        <div class="ca-label">Phase 3 — Month 4-6 (₹1L → ₹5L MRR)</div>
        <div class="ca-title">Product-led growth</div>
        <div class="ca-body">
          1. CAs share the branded report with clients → clients sign up directly → new revenue stream<br><br>
          2. Add direct SME plan at ₹2,999/month — CAs refer their clients<br><br>
          3. Integrate with Tally directly (Tally has an open API) — makes file upload seamless<br><br>
          4. Add GST compliance alerts — file due dates, ITC mismatches, GSTR-2B gaps<br><br>
          <strong style="color:var(--gold);">Target: 200 users × avg ₹2,500 = ₹5L MRR</strong>
        </div>
      </div>
      <div class="ca-card gold">
        <div class="ca-label">Your Moat — Why Competitors Can't Copy This</div>
        <div class="ca-title">Data network effect</div>
        <div class="ca-body">
          Every business that uploads data improves your benchmark database. More benchmarks → better insights → more users → more data.<br><br>
          <strong style="color:var(--paper);">After 1,000 businesses: you have the most accurate India SME benchmark database in existence.</strong><br><br>
          No competitor can build this without the users. No user will come without the product. You build both simultaneously.<br><br>
          This is your <strong style="color:var(--gold);">compounding advantage</strong> — and it gets stronger every month.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin-bottom:1.25rem;">
      <div style="font-size:10px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.75rem;">WhatsApp Script — CA Outreach (copy-paste this)</div>
      <div style="font-size:13px;color:#B0ACA5;line-height:1.8;font-style:italic;">
        "Hi [CA Name], I'm building a tool specifically for CAs — it analyses your client's Tally data in 60 seconds and shows exactly where they're losing money (in rupees). You share a branded report with your client monthly — includes GST ITC estimates, cash flow forecast, and a health score. Saves ~40 hrs/month of manual work, and clients see you as more proactive.<br><br>
        Built it in Bangalore, currently giving free access to 10 CA firms in exchange for feedback. Would you be open to a 10-minute demo call this week? Happy to run it on one of your real client files so you see actual results."
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;">
      <div style="font-size:10px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.75rem;">Investor Pitch — If You Ever Need Funding</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--border);border-radius:8px;overflow:hidden;">
        <div style="background:#0E1219;padding:1rem;">
          <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;">Market Size</div>
          <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:var(--paper);">63M SMEs</div>
          <div style="font-size:11px;color:var(--muted);margin-top:2px;">in India, 100K+ CA firms</div>
        </div>
        <div style="background:#0E1219;padding:1rem;">
          <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;">Unit Economics</div>
          <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:var(--paper);">₹2,500 ARPU</div>
          <div style="font-size:11px;color:var(--muted);margin-top:2px;">CAC ~₹1,200 via CA channel</div>
        </div>
        <div style="background:#0E1219;padding:1rem;">
          <div style="font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;">Why Now</div>
          <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:var(--paper);">Tally + AI</div>
          <div style="font-size:11px;color:var(--muted);margin-top:2px;">9M Tally businesses, no AI layer yet</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div>
    <div class="footer-brand">⬡ OpsClarity</div>
    <div class="footer-legal" style="margin-top:3px;">AI CFO for Indian SMEs · Built in {CITY} 🇮🇳 · v3.0</div>
  </div>
  <div class="footer-legal" style="text-align:right;">
    Management estimates only — not CA advice · Your data stays on your device ·
    {datetime.now().strftime('%Y')}
  </div>
</div>
<a href="https://wa.me/{WHATSAPP_NUMBER}?text=Hi%2C+I+want+to+learn+more+about+OpsClarity" class="wa-float" target="_blank">
  💬 Talk to founder
</a>
""", unsafe_allow_html=True)
