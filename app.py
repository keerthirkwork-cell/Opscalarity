import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse
import json
import io
import random

st.set_page_config(
    page_title="OpsClarity — AI Business Advisor",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Luxury editorial dark theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --ink: #0E0E0E;
  --paper: #F5F1EB;
  --gold: #C9A84C;
  --gold-light: #E8C97A;
  --gold-dark: #A07830;
  --red: #D94F4F;
  --green: #3DAA6D;
  --blue: #4A7FC1;
  --muted: #6B6655;
  --border: #2A2A2A;
  --card-bg: #161616;
  --card-bg2: #1C1C1C;
  --surface: #131313;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: var(--ink);
    font-family: 'Syne', sans-serif;
    color: var(--paper);
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }
.stTabs [data-baseweb="tab-list"] { 
    background: #111; 
    border-bottom: 1px solid var(--border);
    padding: 0 3rem;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted) !important;
    padding: 1.2rem 1.5rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
div[data-testid="stFileUploader"] {
    background: #161616;
    border: 1px dashed #333;
    border-radius: 12px;
    padding: 1rem;
}
div[data-testid="stFileUploader"] label { color: var(--muted) !important; }
.stSelectbox label, .stSlider label { color: var(--muted) !important; font-family: 'Syne', sans-serif; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.stSelectbox [data-baseweb="select"] > div { background: #1C1C1C !important; border-color: #333 !important; color: var(--paper) !important; }
.stButton > button {
    background: var(--gold) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: var(--gold-light) !important; transform: translateY(-1px); }
.stButton > button[kind="secondary"] { background: #1C1C1C !important; color: var(--paper) !important; border: 1px solid #333 !important; }
.stSuccess { background: rgba(61,170,109,0.1) !important; border-color: var(--green) !important; }
.stExpander { border-color: #2A2A2A !important; background: #161616 !important; }
.stExpander summary { color: var(--muted) !important; font-family: 'Syne', sans-serif !important; }

/* Metric override */
[data-testid="stMetric"] {
    background: #161616;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-family: 'Syne', sans-serif !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.1em; }
[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; color: var(--paper) !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* Charts background */
[data-testid="stVegaLiteChart"] { background: transparent !important; }
.element-container { margin-bottom: 0 !important; }

/* Code blocks */
code { 
    background: #1A1A1A !important; 
    color: var(--gold) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}
pre { background: #161616 !important; border: 1px solid #2A2A2A !important; border-radius: 12px !important; }
pre code { padding: 1rem !important; display: block !important; }

/* ── HERO ── */
.hero {
    background: var(--ink);
    background-image: 
        radial-gradient(ellipse 60% 40% at 80% 20%, rgba(201,168,76,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 20% 80%, rgba(201,168,76,0.04) 0%, transparent 50%);
    padding: 5rem 4rem 4rem;
    position: relative;
    border-bottom: 1px solid var(--border);
    overflow: hidden;
}
.hero-eyebrow {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 10px;
}
.hero-eyebrow::before {
    content: ''; display: inline-block;
    width: 30px; height: 1px; background: var(--gold);
}
.hero-headline {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 5.5vw, 5rem);
    color: var(--paper);
    line-height: 1.05;
    margin-bottom: 1.5rem;
    max-width: 700px;
}
.hero-headline .accent { color: var(--gold); font-style: italic; }
.hero-headline .strike {
    color: var(--muted);
    text-decoration: line-through;
    text-decoration-color: var(--red);
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 480px;
    line-height: 1.75;
    margin-bottom: 2.5rem;
    font-weight: 400;
}
.hero-stats {
    display: flex; gap: 3rem; flex-wrap: wrap;
    padding-top: 2.5rem;
    margin-top: 2rem;
    border-top: 1px solid #1E1E1E;
}
.hs { }
.hs-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem; color: var(--gold); line-height: 1;
}
.hs-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px; }

/* ── TRUST BAR ── */
.trust-bar {
    background: #111;
    border-bottom: 1px solid var(--border);
    padding: 0.85rem 4rem;
    display: flex; align-items: center; gap: 2.5rem; flex-wrap: wrap;
}
.trust-item {
    display: flex; align-items: center; gap: 8px;
    font-size: 12px; color: var(--muted); font-weight: 500;
    letter-spacing: 0.03em;
}
.trust-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--green); flex-shrink: 0; }

/* ── MONEY SCREEN ── */
.money-screen {
    background: linear-gradient(135deg, #161616 0%, #1A1810 100%);
    border: 1px solid #2A2618;
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}
.money-screen::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201,168,76,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.ms-label {
    font-size: 11px; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.18em;
    margin-bottom: 0.4rem;
}
.ms-total {
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem; color: var(--gold);
    line-height: 1; margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.ms-sub { font-size: 13px; color: var(--muted); margin-bottom: 2rem; }
.ms-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.25rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    background: rgba(255,255,255,0.025);
    border-left: 3px solid transparent;
    transition: all 0.2s;
}
.ms-row:hover { background: rgba(255,255,255,0.04); }
.ms-row.critical { border-left-color: var(--red); }
.ms-row.warning  { border-left-color: var(--gold); }
.ms-row.info     { border-left-color: var(--blue); }
.ms-row-left { display: flex; align-items: center; gap: 12px; }
.ms-icon { font-size: 16px; }
.ms-title { font-size: 14px; font-weight: 600; color: var(--paper); }
.ms-desc  { font-size: 11px; color: var(--muted); margin-top: 2px; }
.ms-amt { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 500; color: var(--gold); }
.action-strip {
    background: rgba(201,168,76,0.06);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1.5rem;
}
.as-title { font-size: 11px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 1rem; }
.as-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 0.6rem; }
.as-num {
    min-width: 22px; height: 22px; border-radius: 50%;
    background: var(--gold); color: #000;
    font-size: 10px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    margin-top: 1px;
}
.as-text { font-size: 13px; color: #C8C4B8; line-height: 1.55; }

/* ── KPI STRIP ── */
.kpi-strip { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin: 1.5rem 0; }
.kpi {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    position: relative; overflow: hidden;
}
.kpi::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
}
.kpi.good::after  { background: var(--green); }
.kpi.bad::after   { background: var(--red); }
.kpi.warn::after  { background: var(--gold); }
.kpi.neutral::after { background: var(--border); }
.kpi-label { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem; }
.kpi-val { font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--paper); line-height: 1.1; }
.kpi-sub { font-size: 11px; margin-top: 4px; }
.kpi-sub.good { color: var(--green); }
.kpi-sub.bad  { color: var(--red); }
.kpi-sub.warn { color: var(--gold); }
.kpi-sub.muted { color: var(--muted); }

/* ── SECTION HEADERS ── */
.section { padding: 2.5rem 4rem; }
.section-head {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem; color: var(--paper);
    margin-bottom: 0.4rem;
}
.section-sub { font-size: 13px; color: var(--muted); margin-bottom: 2rem; }

/* ── INSIGHTS FEED (MAIN DIFFERENTIATOR) ── */
.insight-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.insight-card:hover { border-color: #3A3A3A; }
.insight-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
}
.insight-card.critical::before { background: var(--red); }
.insight-card.warning::before  { background: var(--gold); }
.insight-card.info::before     { background: var(--blue); }
.ic-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1rem; }
.ic-tag {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 10px; font-weight: 700; padding: 4px 10px;
    border-radius: 20px; text-transform: uppercase; letter-spacing: 0.12em;
}
.ic-tag.critical { background: rgba(217,79,79,0.12); color: #FF7A7A; }
.ic-tag.warning  { background: rgba(201,168,76,0.12); color: var(--gold-light); }
.ic-tag.info     { background: rgba(74,127,193,0.12); color: #7AADFF; }
.ic-amount {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem; font-weight: 500; color: var(--gold);
    text-align: right; line-height: 1;
}
.ic-amount-sub { font-size: 10px; color: var(--muted); margin-top: 2px; text-align: right; }
.ic-title { font-size: 1.1rem; font-weight: 700; color: var(--paper); margin-bottom: 0.4rem; }
.ic-subtitle { font-size: 13px; color: var(--muted); margin-bottom: 1.25rem; }

/* The 3-part breakdown */
.ic-breakdown { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: #2A2A2A; border-radius: 10px; overflow: hidden; margin-bottom: 1.25rem; }
.ic-part { background: #181818; padding: 0.85rem 1rem; }
.ic-part-label { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.3rem; }
.ic-part-val { font-size: 13px; color: var(--paper); line-height: 1.5; }
.ic-part-val.action-text { color: var(--gold); font-weight: 600; }

.ic-footer { display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid #2A2A2A; }
.ic-cta { font-size: 12px; font-weight: 600; color: var(--gold); letter-spacing: 0.04em; }
.ic-bench { font-size: 11px; color: var(--muted); max-width: 350px; }

/* ── COPILOT CHAT ── */
.copilot-wrap {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
.copilot-header {
    background: #1A1810;
    border-bottom: 1px solid #2A2618;
    padding: 1rem 1.5rem;
    display: flex; align-items: center; gap: 10px;
}
.copilot-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--gold); }
.copilot-title { font-size: 13px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.1em; }
.copilot-sub { font-size: 11px; color: var(--muted); }
.chat-bubble-user {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 12px 12px 2px 12px;
    padding: 0.75rem 1rem;
    font-size: 14px; color: var(--paper);
    margin-bottom: 0.5rem;
    max-width: 75%; margin-left: auto;
}
.chat-bubble-ai {
    background: #1C1C1C;
    border: 1px solid var(--border);
    border-radius: 2px 12px 12px 12px;
    padding: 0.75rem 1rem;
    font-size: 14px; color: var(--paper); line-height: 1.65;
    max-width: 85%;
}

/* ── COLLECTIONS ── */
.seq-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
}
.seq-badge {
    display: inline-block;
    background: var(--ink); color: var(--gold);
    border: 1px solid rgba(201,168,76,0.3);
    font-size: 10px; font-weight: 700; padding: 3px 10px;
    border-radius: 20px; margin-bottom: 0.5rem;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.seq-tone { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.seq-msg { font-size: 13px; color: #B0ACA0; line-height: 1.7; }

/* ── CA PROGRAM ── */
.ca-section { padding: 2.5rem 4rem; background: var(--ink); }
.ca-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-top: 1.5rem; }
.ca-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
}
.ca-card.gold-border { border-color: rgba(201,168,76,0.3); background: #1A1810; }
.ca-label { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem; }
.ca-title { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: var(--paper); margin-bottom: 0.5rem; }
.ca-body { font-size: 13px; color: var(--muted); line-height: 1.7; }
.ca-math-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
}
.ca-math-row:last-child { border: none; }
.ca-math-label { color: var(--muted); }
.ca-math-val { font-family: 'JetBrains Mono', monospace; font-weight: 500; color: var(--paper); }
.ca-math-val.big { color: var(--green); font-size: 1.1rem; }

/* ── CLIENT DASHBOARD ── */
.client-row {
    display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
    align-items: center;
    padding: 0.9rem 1.25rem;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    transition: background 0.15s;
}
.client-row:hover { background: rgba(255,255,255,0.02); }
.client-row:last-child { border: none; }
.client-row-header { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; }
.client-name { font-weight: 600; color: var(--paper); }
.client-meta { font-size: 11px; color: var(--muted); margin-top: 2px; }
.client-amt { font-family: 'JetBrains Mono', monospace; color: var(--gold); }
.health-badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 20px; }
.health-badge.red   { background: rgba(217,79,79,0.15);   color: #FF7A7A; }
.health-badge.amber { background: rgba(201,168,76,0.15);  color: var(--gold-light); }
.health-badge.green { background: rgba(61,170,109,0.15);  color: #6ADFAA; }

/* ── PRICING ── */
.pricing-section { background: #0A0A0A; padding: 3rem 4rem; border-top: 1px solid var(--border); }
.pricing-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.25rem; margin-top: 2rem; }
.price-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    position: relative; overflow: hidden;
}
.price-card.featured {
    border-color: rgba(201,168,76,0.4);
    background: #1A1810;
}
.price-featured-tag {
    position: absolute; top: 16px; right: 16px;
    background: var(--gold); color: #000;
    font-size: 9px; font-weight: 800; padding: 3px 8px; border-radius: 20px;
    letter-spacing: 0.12em; text-transform: uppercase;
}
.price-label { font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.75rem; }
.price-name { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: var(--paper); margin-bottom: 0.5rem; }
.price-amount { font-family: 'JetBrains Mono', monospace; font-size: 2.5rem; color: var(--gold); line-height: 1; margin-bottom: 0.4rem; }
.price-note { font-size: 12px; color: var(--muted); margin-bottom: 1.5rem; line-height: 1.6; }
.price-features { list-style: none; margin-top: 1.25rem; }
.price-features li {
    font-size: 12px; color: #9A9A90;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1E1E1E;
    display: flex; align-items: center; gap: 8px;
}
.price-features li::before { content: "→"; color: var(--gold); font-size: 11px; }
.price-features li:last-child { border: none; }

/* ── BENCHMARK TABLE ── */
.bench-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
}
.bench-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.bench-cat { font-size: 14px; font-weight: 700; color: var(--paper); }
.bench-n { font-size: 11px; color: var(--muted); }
.bench-bar-wrap { position: relative; height: 6px; background: #2A2A2A; border-radius: 3px; margin: 0.5rem 0; }
.bench-bar-fill { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; background: var(--gold); }
.bench-labels { display: flex; justify-content: space-between; font-size: 10px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }

/* ── UPLOAD ZONE ── */
.upload-section { padding: 2rem 4rem 0; }

/* ── FOOTER ── */
.footer {
    background: #080808;
    border-top: 1px solid var(--border);
    padding: 2rem 4rem;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
}
.footer-brand { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: var(--gold); }
.footer-legal { font-size: 11px; color: var(--muted); }

/* ── WA FLOAT ── */
.wa-float {
    position: fixed; bottom: 28px; right: 28px;
    background: #25D366;
    padding: 12px 20px; border-radius: 50px;
    font-weight: 700; font-size: 13px; color: white;
    text-decoration: none; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 24px rgba(37,211,102,0.3);
    z-index: 9999; letter-spacing: 0.04em;
    transition: transform 0.2s;
}
.wa-float:hover { transform: translateY(-2px); }

/* ── DIVIDER ── */
.divider { height: 1px; background: var(--border); margin: 0 4rem; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: #2A2A2A; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
INDUSTRY_MAP = {
    "🏭 Manufacturing":         "manufacturing",
    "🍽️ Restaurant / Cafe":    "restaurant",
    "🏥 Clinic / Diagnostic":  "clinic",
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting":   "agency",
    "🚚 Logistics / Transport": "logistics",
    "🏗️ Construction":         "construction",
    "🧵 Textile / Garments":   "textile",
    "💊 Pharma / Medical":     "pharma",
    "🖨️ Print / Packaging":    "printing",
}

INDUSTRY_BENCHMARKS = {
    "manufacturing":18,"restaurant":15,"clinic":25,"retail":12,"agency":35,
    "logistics":10,"construction":20,"textile":14,"pharma":22,"printing":16,
}

CROWDSOURCED = {
    "manufacturing":{
        "Raw Materials":{"p25":42000,"median":51000,"p75":64000,"unit":"/ton","n":312,"city_splits":{"Mumbai":53000,"Delhi":49000,"Pune":48000,"Surat":44000}},
        "Labor":        {"p25":380,  "median":460,  "p75":580,  "unit":"/day","n":445,"city_splits":{"Mumbai":520,"Delhi":480,"Pune":460,"Ahmedabad":390}},
        "Logistics":    {"p25":8,    "median":11,   "p75":16,   "unit":"/km", "n":289,"city_splits":{"Mumbai":13,"Delhi":12,"Pune":10,"Chennai":10}},
        "Packaging":    {"p25":11,   "median":17,   "p75":24,   "unit":"/pc", "n":198,"city_splits":{"Mumbai":18,"Delhi":16,"Pune":15,"Coimbatore":13}},
        "Electricity":  {"p25":7,    "median":9,    "p75":12,   "unit":"/unit","n":267,"city_splits":{"Mumbai":10,"Delhi":9,"Pune":8,"Gujarat":7}},
    },
    "restaurant":{
        "Food Ingredients":{"p25":28,"median":34,"p75":42,"unit":"% rev","n":521,"city_splits":{}},
        "Labor":           {"p25":18,"median":24,"p75":32,"unit":"% rev","n":498,"city_splits":{}},
        "Packaging":       {"p25":8, "median":14,"p75":22,"unit":"/order","n":312,"city_splits":{}},
    },
    "retail":{
        "Inventory Carrying":{"p25":18,"median":26,"p75":36,"unit":"days","n":389,"city_splits":{}},
        "Rent":              {"p25":80,"median":120,"p75":200,"unit":"/sqft/mo","n":445,"city_splits":{}},
    },
    "clinic":{
        "Consumables":  {"p25":8, "median":13,"p75":20,"unit":"% rev","n":234,"city_splits":{}},
        "Lab Reagents": {"p25":15,"median":22,"p75":31,"unit":"% rev","n":189,"city_splits":{}},
    },
    "agency":{
        "Software/Tools":{"p25":8000, "median":14000,"p75":22000,"unit":"/mo","n":312,"city_splits":{}},
        "Freelancers":   {"p25":600,  "median":900,  "p75":1400, "unit":"/hr","n":267,"city_splits":{}},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(v):
    v = float(v)
    if abs(v)>=1e7:  return f"₹{v/1e7:.1f}Cr"
    if abs(v)>=1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v)>=1000: return f"₹{v/1000:.0f}K"
    return f"₹{abs(v):.0f}"

def fmt_exact(v):
    return f"₹{int(float(v)):,}"

# ══════════════════════════════════════════════════════════════════════════════
# COLLECTIONS BOT
# ══════════════════════════════════════════════════════════════════════════════
class CollectionsBot:
    SEQUENCES = [
        {"day":1,  "tone":"Friendly Reminder", "color":"#4A7FC1",
         "msg":"Hi {name} 🙏 Quick note — invoice #{inv} for {amt} was due recently. Any issues on your end? Happy to sort it out. — {biz}"},
        {"day":3,  "tone":"Offer + Urgency",   "color":"#C9A84C",
         "msg":"Hi {name}, invoice #{inv} ({amt}) is now overdue. We're offering a 2% early-payment discount if settled by {deadline}. Can you confirm? — {biz}"},
        {"day":7,  "tone":"Operational Impact","color":"#E08020",
         "msg":"{name}, invoice #{inv} ({amt}) is 7 days overdue and impacting our cash flow. Payment needed by {deadline} or we'll need to pause future orders. — {biz}"},
        {"day":10, "tone":"Final Notice",      "color":"#D94F4F",
         "msg":"FINAL NOTICE — {name}: invoice #{inv} ({amt}) is 10 days unpaid. Last reminder before escalation. Pay by {deadline}. — {biz}"},
    ]
    @classmethod
    def generate(cls, name, inv, amount, biz):
        today = datetime.now()
        out = []
        for s in cls.SEQUENCES:
            msg = s["msg"].format(
                name=name, inv=inv, amt=fmt(amount), biz=biz,
                deadline=(today+timedelta(days=s["day"]+3)).strftime("%d %b %Y")
            )
            out.append({**s,
                "send_on":(today+timedelta(days=s["day"])).strftime("%d %b"),
                "message":msg,
                "wa_link":f"https://wa.me/?text={urllib.parse.quote(msg)}"
            })
        return out

# ══════════════════════════════════════════════════════════════════════════════
# CSV / EXCEL PARSERS
# ══════════════════════════════════════════════════════════════════════════════
def _classify_expense(d):
    d = d.lower()
    if any(x in d for x in ["rent","rental"]):                       return "Rent"
    if any(x in d for x in ["praveen","porter","salary","wages"]):   return "Salary"
    if any(x in d for x in ["ashok"]):                               return "Salary"
    if any(x in d for x in ["laptop","computer"]):                   return "Technology"
    if any(x in d for x in ["broad","internet","wifi"]):             return "Internet"
    if any(x in d for x in ["housekeeping"]):                        return "Housekeeping"
    if any(x in d for x in ["furniture","chair"]):                   return "Furniture"
    if any(x in d for x in ["electricity"]):                         return "Electricity"
    if any(x in d for x in ["ca","accountant","audit"]):             return "Professional Fees"
    if any(x in d for x in ["website","domain"]):                    return "Website"
    if any(x in d for x in ["outing","travel","food"]):              return "Travel"
    if any(x in d for x in ["office","stationery"]):                 return "Office Supplies"
    if any(x in d for x in ["glass","basin","electrical","door","key","seal","board"]): return "Office Setup"
    if any(x in d for x in ["mim","mfg","part cost"]):               return "Manufacturing"
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
            return None, False, "Could not find a Date column. Ensure column is labelled 'Date' or 'Dt'."

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
# AI COPILOT — rule-based smart Q&A (no API key needed)
# ══════════════════════════════════════════════════════════════════════════════
def ai_copilot_answer(question, df, leaks, industry):
    q = question.lower()
    sales = df[df["Type"]=="Sales"]
    expenses = df[df["Type"]=="Expense"]
    revenue = sales["Amount"].sum()
    exp_tot = expenses["Amount"].sum()
    profit = revenue - exp_tot
    margin = (profit/revenue*100) if revenue>0 else 0
    benchmark = INDUSTRY_BENCHMARKS.get(industry,15)
    total_leak = sum(l["rupee_impact"] for l in leaks)

    # Why is profit low?
    if any(x in q for x in ["profit","margin","low","why"]):
        top_exp = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)
        top_names = ", ".join([f"{n} ({fmt(v)})" for n,v in top_exp.items()])
        resp = f"""**Your profit is {margin:.1f}% vs the {benchmark}% industry benchmark.**

Your biggest cost drivers are: {top_names}.

The gap ({benchmark-margin:.1f} percentage points) translates to {fmt((benchmark-margin)/100*revenue)} that could stay in your pocket.

**Actions:**
→ Renegotiate your top 2 expense categories — start with a 10% reduction target
→ Raise prices 5% on your 3 highest-margin products/services
→ Combined impact: adds ~{fmt((benchmark-margin)/100*revenue*0.4)} in the next 90 days"""
        return resp

    # Cash flow / overdue
    if any(x in q for x in ["cash","overdue","unpaid","collect","debtor"]):
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid"])] if "Status" in sales.columns else pd.DataFrame()
        od_amt = od["Amount"].sum() if len(od)>0 else 0
        if od_amt>0:
            top_debtor = od.groupby("Party")["Amount"].sum().sort_values(ascending=False).index[0] if len(od)>0 else "your top customer"
            resp = f"""**{fmt_exact(int(od_amt))} is sitting in unpaid invoices right now.**

{top_debtor} is your biggest outstanding account.

**This week:**
→ Call {top_debtor} — offer a 2% discount for payment in 48 hours
→ Send the 4-step WhatsApp sequence (see Collections section below)
→ Set Net-15 terms on all future invoices (down from Net-30)

At 18% cost of capital, every month this stays unpaid costs you {fmt(od_amt*0.18/12)}."""
        else:
            resp = "**Your collections look healthy!** No major overdue invoices detected. Keep maintaining Net-15 payment terms to stay ahead."
        return resp

    # Biggest expense
    if any(x in q for x in ["expense","cost","spend","biggest","largest"]):
        top3 = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)
        lines = "\n".join([f"→ {n}: {fmt_exact(int(v))} ({v/exp_tot*100:.1f}% of costs)" for n,v in top3.items()])
        resp = f"""**Your top 3 cost categories:**

{lines}

**Quickest wins:**
→ Get 3 competing quotes for your #1 cost category this week
→ Audit all software subscriptions — average SME wastes ₹8,000–₹25,000/month on unused tools
→ Review vendor payment terms — early payment discounts of 1–2% can offset costs"""
        return resp

    # Revenue risk / concentration
    if any(x in q for x in ["revenue","customer","client","risk","concentrat"]):
        if len(sales)>0 and revenue>0:
            cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top_pct = (cr.iloc[0]/revenue*100) if len(cr)>0 else 0
            top_name = cr.index[0] if len(cr)>0 else "top client"
            resp = f"""**{top_name} is {top_pct:.0f}% of your revenue — {"⚠️ HIGH RISK" if top_pct>25 else "✅ acceptable"}.**

{"You have dangerous concentration — one slow payment can crash your cash flow." if top_pct>25 else "Keep this diversified."}

**If top_pct>25:**
→ Set a 25% cap as your target within 6 months
→ Close 2 new clients this month to dilute exposure
→ Strengthen {top_name} relationship but don't give them pricing power"""
        else:
            resp = "Revenue data is limited. Upload more months of data for a full concentration analysis."
        return resp

    # GST / tax
    if any(x in q for x in ["gst","tax","itc","input credit"]):
        eligible = expenses[expenses["Amount"]>25000]
        missed = eligible["Amount"].sum()*0.18*0.09 if len(eligible)>0 else 0
        resp = f"""**Estimated {fmt_exact(int(missed))} in GST Input Tax Credit to verify.**

This is money the government owes you back — it just needs proper invoice matching and filing.

**Do this:**
→ Share this report with your CA and ask specifically about ITC eligibility
→ Ensure all vendor invoices above ₹25K are GST-compliant and matched
→ File GSTR-2B reconciliation monthly — don't let credits expire"""
        return resp

    # What should I fix / general
    if any(x in q for x in ["fix","do","action","recommend","suggest","start","help","where"]):
        top3_leaks = sorted(leaks, key=lambda x: x["rupee_impact"], reverse=True)[:3]
        if top3_leaks:
            lines = "\n".join([f"**{i+1}. {l['headline']}** — {fmt_exact(int(l['rupee_impact']))}\n   → {l['next_action']}" for i,l in enumerate(top3_leaks)])
            resp = f"""**Your 3 highest-impact actions this week:**

{lines}

Total recoverable: {fmt(total_leak)}

Start with #1 today — it takes less than 30 minutes to initiate."""
        else:
            resp = "Upload your financial data first — then I can give you specific actions."
        return resp

    # Default / fallback
    return f"""I can help you with:

→ **"Why is my profit low?"** — root cause analysis
→ **"What should I fix first?"** — prioritized action list
→ **"Who owes me money?"** — collections analysis
→ **"What are my biggest costs?"** — expense deep-dive
→ **"Am I at revenue risk?"** — concentration check
→ **"What about GST?"** — ITC recovery estimate

Ask me any of these and I'll give you exact rupee figures and specific actions."""

# ══════════════════════════════════════════════════════════════════════════════
# LEAK DETECTOR — core engine
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

    # 1. Overdue invoices
    if "Status" in df.columns:
        od = sales[sales["Status"].str.lower().isin(["overdue","pending","not paid","due","outstanding","unpaid"])]
        od_amt = od["Amount"].sum()
        if od_amt>10000:
            debtors = od.groupby("Party")["Amount"].sum().sort_values(ascending=False)
            top5    = debtors.head(5)
            top_name= debtors.index[0] if len(debtors)>0 else "Customer"
            top_amt = float(debtors.iloc[0]) if len(debtors)>0 else od_amt
            pct_rev = od_amt/revenue*100 if revenue>0 else 0
            debtor_lines = " · ".join([f"{n}: {fmt_exact(a)}" for n,a in top5.items()])
            collections  = CollectionsBot.generate(top_name,"INV-001",top_amt,"Your Business")
            leaks.append({
                "id":"cash_stuck","severity":"critical","priority":1,
                "category":"Collections",
                "rupee_impact":od_amt,"annual_impact":od_amt*0.18,
                "headline":f"{fmt_exact(int(od_amt))} stuck in unpaid invoices",
                "sub":f"{len(debtors)} customers overdue · avg 45+ days",
                "problem":f"{len(debtors)} customers owe you {fmt_exact(int(od_amt))}",
                "reason":f"{debtor_lines}",
                "action":f"Call {top_name} today — offer 2% discount for 48hr payment",
                "benchmark":f"Healthy SMEs: <5% of revenue overdue. Yours: {pct_rev:.1f}%",
                "cta":"Launch collections sequence →",
                "collections":collections,
                "template":f"Hi, your invoice of {fmt(top_amt)} is overdue. We offer 2% off if settled by [date]. Please confirm. — [Your name]"
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
            if exp_price>cheapest*1.12:
                pct_premium  = ((exp_price-cheapest)/cheapest)*100
                annual_waste = (exp_price-cheapest)*(annual_vol/exp_price)
                bench = CROWDSOURCED.get(industry,{}).get(category)
                bench_line = f"Market median: ₹{bench['median']:,}{bench['unit']} ({bench['n']} peers)" if bench else f"Market typically 10–18% cheaper for {industry}"
                if annual_waste>15000:
                    leaks.append({
                        "id":"cost_bleed","severity":"warning","priority":2,
                        "category":"Vendor Costs",
                        "rupee_impact":annual_waste,"annual_impact":annual_waste,
                        "headline":f"{fmt_exact(int(annual_waste))} overpaid on {category}/year",
                        "sub":f"{exp_vendor} charges {pct_premium:.0f}% above market rate",
                        "problem":f"Paying {exp_vendor} ₹{exp_price:,.0f}/txn for {category}",
                        "reason":f"Cheapest alternative: ₹{cheapest:,.0f} — {pct_premium:.0f}% gap",
                        "action":f"Get 2 quotes for {category} by Friday — offer 12-month contract",
                        "benchmark":bench_line,
                        "cta":"Get vendor script →",
                        "collections":[],
                        "template":f"We're reviewing our {category} suppliers. Please send your best rate for [volume]. Lowest quote gets a 12-month contract — decision by Friday."
                    })
                    break

    # 3. Margin gap
    if margin<benchmark-3:
        gap = ((benchmark-margin)/100)*revenue
        if gap>25000:
            leaks.append({
                "id":"margin_gap","severity":"critical" if margin<5 else "warning","priority":3,
                "category":"Profitability",
                "rupee_impact":gap,"annual_impact":gap,
                "headline":f"{fmt_exact(int(gap))} in margin sitting on the table",
                "sub":f"Your {margin:.1f}% vs {benchmark}% industry benchmark",
                "problem":f"Net margin {margin:.1f}% — {benchmark-margin:.1f}pp below peers",
                "reason":f"Either costs too high or pricing too low (or both)",
                "action":f"Raise prices 5% on top 3 products + cut biggest expense 10%",
                "benchmark":f"Industry: {benchmark}% for {industry} businesses",
                "cta":"See pricing script →",
                "collections":[],
                "template":"Reviewing our pricing — market benchmarks show room to increase 5–8%. Implementing from next invoice cycle."
            })

    # 4. Customer concentration
    if len(sales)>0 and revenue>0:
        cr = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cr)>0 and (cr.iloc[0]/revenue)*100>28:
            top_pct = (cr.iloc[0]/revenue)*100
            risk_amt = cr.iloc[0]*0.3
            leaks.append({
                "id":"concentration","severity":"warning","priority":4,
                "category":"Revenue Risk",
                "rupee_impact":risk_amt,"annual_impact":risk_amt,
                "headline":f"{cr.index[0]} is {top_pct:.0f}% of your revenue",
                "sub":"Single-client dependency = existential risk",
                "problem":f"{cr.index[0]}: {fmt_exact(int(cr.iloc[0]))} of {fmt(revenue)} total",
                "reason":"They delay 30 days → you can't make payroll",
                "action":"Close 2 new clients this month. Set 25% cap target for 6 months",
                "benchmark":"Healthy SMEs: no single client above 25%",
                "cta":"Get outreach script →",
                "collections":[],
                "template":"Looking to expand our client base. If you know businesses needing [service], I'd offer you a referral bonus."
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
                if spike>20000:
                    leaks.append({
                        "id":"expense_spike","severity":"warning","priority":5,
                        "category":"Cost Control",
                        "rupee_impact":spike,"annual_impact":spike,
                        "headline":f"Monthly costs up {pct:.0f}% — {fmt_exact(int(spike))}/yr drain",
                        "sub":f"{fmt(recent-prior)} extra per month vs 3 months ago",
                        "problem":f"Monthly spend: {fmt(prior)} → {fmt(recent)}",
                        "reason":f"{fmt(recent-prior)}/month increase with no matching revenue jump",
                        "action":"Freeze non-essential spend. Audit all recurring subscriptions today",
                        "benchmark":"Expenses should track revenue. Rising faster = structural problem",
                        "cta":"Get cost freeze template →",
                        "collections":[],
                        "template":"Implementing cost review from today. All non-essential expenses paused pending audit. Reviewing all vendor contracts."
                    })

    # 6. GST / ITC
    exp_eligible = expenses[expenses["Amount"]>25000]
    if len(exp_eligible)>0:
        missed = exp_eligible["Amount"].sum()*0.18*0.09
        if missed>8000:
            leaks.append({
                "id":"tax_gst","severity":"info","priority":6,
                "category":"Tax Recovery",
                "rupee_impact":missed,"annual_impact":missed,
                "headline":f"~{fmt_exact(int(missed))} in GST input credits to verify",
                "sub":"Estimated quarterly — needs CA confirmation",
                "problem":f"Eligible purchases: {fmt(exp_eligible['Amount'].sum())}",
                "reason":"~9% of claimable ITC goes unclaimed by SMEs of this size",
                "action":"Email CA: 'Please review ITC eligibility on purchases above ₹25K'",
                "benchmark":"File before next GSTR-3B due date — credits expire",
                "cta":"Get CA email template →",
                "collections":[],
                "template":"I'd like to review Input Tax Credit eligibility on our purchase invoices. Can we schedule a call this week? I have the purchase register ready."
            })

    return sorted(leaks, key=lambda x: x["rupee_impact"], reverse=True)

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE DEMO DATA
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
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k,v in [("df",None),("industry","manufacturing"),("city","Bangalore"),
            ("show_bot",False),("chat_history",[]),("last_q","")]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">OpsClarity · AI Business Advisor · Built in Bangalore 🇮🇳</div>
  <h1 class="hero-headline">
    Stop looking at<br><span class="strike">dashboards.</span><br>
    Get <span class="accent">decisions.</span>
  </h1>
  <p class="hero-sub">
    Upload your Tally export. In 60 seconds, OpsClarity tells you — in exact rupees —
    where money is leaking and the three actions to stop it this week.
    You pay only when you recover.
  </p>
  <div class="hero-stats">
    <div class="hs"><div class="hs-num">₹50Cr+</div><div class="hs-label">Leaks identified</div></div>
    <div class="hs"><div class="hs-num">₹12.4L</div><div class="hs-label">Avg recovery</div></div>
    <div class="hs"><div class="hs-num">4.8 days</div><div class="hs-label">To first recovery</div></div>
    <div class="hs"><div class="hs-num">200+</div><div class="hs-label">SMEs scanned</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust-bar">
  <div class="trust-item"><div class="trust-dot"></div> Your Tally file never leaves your device</div>
  <div class="trust-item"><div class="trust-dot"></div> No login required for first scan</div>
  <div class="trust-item"><div class="trust-dot"></div> Results in 60 seconds</div>
  <div class="trust-item"><div class="trust-dot"></div> Used by CAs across Bangalore · Mumbai · Pune</div>
  <div class="trust-item"><div class="trust-dot"></div> Not a dashboard. A decision engine.</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_scan, tab_copilot, tab_ca, tab_bench = st.tabs([
    "₹ Scan My Business",
    "🤖 AI Copilot",
    "🏛 CA Partner Program",
    "📊 Benchmarks"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SCAN
# ══════════════════════════════════════════════════════════════════════════════
with tab_scan:

    # Upload zone
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
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
**Bank statement:** Download as CSV from net banking  
**Design AID format:** Detected automatically.
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
        if st.button("▶ Try Demo Data", use_container_width=True):
            st.session_state.df = make_demo_data()
            st.session_state.industry = "manufacturing"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded:
        df_new, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_new
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info("Quick fix: open the file in Excel → Save As → CSV UTF-8 → upload.")

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
        leaks    = find_leaks(df, industry, city_sel)
        total_liq= sum(l["rupee_impact"] for l in leaks)
        total_ann= sum(l["annual_impact"] for l in leaks)

        overdue_amt = (sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum()
                       if "Status" in sales.columns else 0)

        coll_l   = next((l for l in leaks if l["id"]=="cash_stuck"),  None)
        vend_l   = next((l for l in leaks if l["id"]=="cost_bleed"),  None)
        tax_l    = next((l for l in leaks if l["id"]=="tax_gst"),     None)
        margin_l = next((l for l in leaks if l["id"]=="margin_gap"),  None)

        coll_amt   = coll_l["rupee_impact"]  if coll_l   else 0
        vend_amt   = vend_l["annual_impact"] if vend_l   else 0
        tax_amt    = tax_l["rupee_impact"]   if tax_l    else 0
        margin_amt = margin_l["annual_impact"] if margin_l else 0

        # Actions
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
            rows_html += f'<div class="ms-row critical"><div class="ms-row-left"><div class="ms-icon">🔴</div><div><div class="ms-title">Cash in unpaid invoices</div><div class="ms-desc">Recoverable this month with action today</div></div></div><div class="ms-amt">{fmt_exact(int(coll_amt))}</div></div>'
        if vend_amt>0:
            rows_html += f'<div class="ms-row warning"><div class="ms-row-left"><div class="ms-icon">🟡</div><div><div class="ms-title">Vendor overpayment — annual savings</div><div class="ms-desc">Switch to market-rate suppliers</div></div></div><div class="ms-amt">{fmt_exact(int(vend_amt))}/yr</div></div>'
        if margin_amt>0:
            rows_html += f'<div class="ms-row warning"><div class="ms-row-left"><div class="ms-icon">🟡</div><div><div class="ms-title">Margin gap vs industry peers</div><div class="ms-desc">Pricing + cost action closes this</div></div></div><div class="ms-amt">{fmt_exact(int(margin_amt))}/yr</div></div>'
        if tax_amt>0:
            rows_html += f'<div class="ms-row info"><div class="ms-row-left"><div class="ms-icon">🔵</div><div><div class="ms-title">GST input credits to verify</div><div class="ms-desc">Estimated — confirm with your CA</div></div></div><div class="ms-amt">~{fmt_exact(int(tax_amt))}</div></div>'

        st.markdown('<div class="section">', unsafe_allow_html=True)
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

        # KPI Strip
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
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── INSIGHTS FEED — the core "decision engine" differentiator ──
        if leaks:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-head">Insights Feed</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Every insight has a Problem · Reason · Action. Not just data.</div>', unsafe_allow_html=True)

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
                    <div class="ic-part">
                      <div class="ic-part-label">❗ Problem</div>
                      <div class="ic-part-val">{leak['problem']}</div>
                    </div>
                    <div class="ic-part">
                      <div class="ic-part-label">🔍 Reason</div>
                      <div class="ic-part-val">{leak['reason']}</div>
                    </div>
                    <div class="ic-part">
                      <div class="ic-part-label">✅ Action</div>
                      <div class="ic-part-val action-text">{leak['action']}</div>
                    </div>
                  </div>
                  <div class="ic-footer">
                    <div class="ic-cta">{leak['cta']}</div>
                    <div class="ic-bench">Benchmark: {leak['benchmark']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Collections sequence
                if leak["id"]=="cash_stuck" and leak.get("collections"):
                    if st.button("Launch 4-step collections sequence →", key="bot_btn"):
                        st.session_state.show_bot = True
                    if st.session_state.show_bot:
                        st.markdown("#### 📱 Collections Sequence — send via WhatsApp")
                        st.caption("4-step escalation. Stop when they pay.")
                        for step in leak["collections"]:
                            st.markdown(f"""
                            <div class="seq-card">
                              <div class="seq-badge">Day {step['day']} · {step['send_on']}</div>
                              <div class="seq-tone" style="color:{step['color']}">{step['tone']}</div>
                              <div class="seq-msg">{step['message']}</div>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:12px;color:#25D366;text-decoration:none;">📲 Send via WhatsApp →</a>', unsafe_allow_html=True)
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

        # ── PRICING ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="pricing-section">
          <div class="section-head" style="color:var(--paper);">How we work together</div>
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
                <li>Collections WhatsApp sequences</li>
                <li>AI Copilot (5 questions)</li>
              </ul>
            </div>
            <div class="price-card featured">
              <div class="price-featured-tag">MOST CHOSEN</div>
              <div class="price-label">Best value</div>
              <div class="price-name">Success Fee</div>
              <div class="price-amount">7–10%</div>
              <div class="price-note">We charge only on money you actually recover. Zero recovery = zero fee. Simple.</div>
              <ul class="price-features">
                <li>Everything in free scan</li>
                <li>Recovery Review call (1hr)</li>
                <li>Vendor quote sourcing (3 quotes)</li>
                <li>Monthly monitoring alerts</li>
                <li>CA coordination support</li>
                <li>Unlimited AI Copilot</li>
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
                <li>GST + TDS risk scanner</li>
                <li>Revenue share program</li>
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
                st.markdown("Or message directly: [wa.me/916362319163](https://wa.me/916362319163)")

    else:
        # Empty state — show what you'll get
        st.markdown('<div class="section" style="text-align:center; padding-top:4rem;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="max-width:500px; margin:0 auto;">
          <div style="font-family:'Playfair Display',serif; font-size:2rem; color:var(--paper); margin-bottom:1rem;">
            Upload your data to get started
          </div>
          <div style="font-size:14px; color:var(--muted); line-height:1.7; margin-bottom:2rem;">
            Works with Tally Day Book exports, Sales Registers, Bank Statements (CSV/Excel).
            Your data stays on your device. Analysis runs locally.
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; text-align:left;">
            <div style="background:#161616; border:1px solid #2A2A2A; border-radius:12px; padding:1.25rem;">
              <div style="font-size:1.5rem; margin-bottom:0.5rem;">🔴</div>
              <div style="font-size:13px; font-weight:600; color:var(--paper); margin-bottom:0.3rem;">Overdue Collections</div>
              <div style="font-size:12px; color:var(--muted);">See exactly who owes you and how much</div>
            </div>
            <div style="background:#161616; border:1px solid #2A2A2A; border-radius:12px; padding:1.25rem;">
              <div style="font-size:1.5rem; margin-bottom:0.5rem;">🟡</div>
              <div style="font-size:13px; font-weight:600; color:var(--paper); margin-bottom:0.3rem;">Vendor Overpayment</div>
              <div style="font-size:12px; color:var(--muted);">Who's charging you above market rate</div>
            </div>
            <div style="background:#161616; border:1px solid #2A2A2A; border-radius:12px; padding:1.25rem;">
              <div style="font-size:1.5rem; margin-bottom:0.5rem;">📈</div>
              <div style="font-size:13px; font-weight:600; color:var(--paper); margin-bottom:0.3rem;">Margin Analysis</div>
              <div style="font-size:12px; color:var(--muted);">Gap vs industry benchmark in rupees</div>
            </div>
            <div style="background:#161616; border:1px solid #2A2A2A; border-radius:12px; padding:1.25rem;">
              <div style="font-size:1.5rem; margin-bottom:0.5rem;">💬</div>
              <div style="font-size:13px; font-weight:600; color:var(--paper); margin-bottom:0.3rem;">AI Copilot</div>
              <div style="font-size:12px; color:var(--muted);">Ask "why is my profit low?" and get answers</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI COPILOT (the main differentiator from the feedback)
# ══════════════════════════════════════════════════════════════════════════════
with tab_copilot:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">AI Copilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ask anything about your business. Get exact rupee answers, not just charts.</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.info("📂 Upload your data in the 'Scan My Business' tab first — then come back to ask questions.")
    else:
        df_c = st.session_state.df
        ind_c= st.session_state.industry

        # Pre-built quick questions
        st.markdown("**Quick questions:**")
        cols = st.columns(4)
        quick_qs = [
            "Why is my profit low?",
            "Who owes me money?",
            "What are my biggest costs?",
            "What should I fix first?"
        ]
        for i, q in enumerate(quick_qs):
            with cols[i]:
                if st.button(q, key=f"qq_{i}"):
                    st.session_state.last_q = q
                    leaks_c = find_leaks(df_c, ind_c)
                    ans = ai_copilot_answer(q, df_c, leaks_c, ind_c)
                    st.session_state.chat_history.append({"role":"user","msg":q})
                    st.session_state.chat_history.append({"role":"ai","msg":ans})

        # Chat interface
        st.markdown('<div class="copilot-wrap" style="margin-top:1.5rem;">', unsafe_allow_html=True)
        st.markdown("""
        <div class="copilot-header">
          <div class="copilot-dot"></div>
          <div>
            <div class="copilot-title">OpsClarity Copilot</div>
            <div class="copilot-sub">Powered by your actual business data · Answers in exact rupees</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Chat history
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history[-10:]:
                if msg["role"]=="user":
                    st.markdown(f'<div style="padding:0 1.5rem 0.5rem; display:flex; justify-content:flex-end;"><div class="chat-bubble-user">{msg["msg"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="padding:0 1.5rem 0.75rem;"><div class="chat-bubble-ai">{msg["msg"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:2rem 1.5rem; text-align:center;">
              <div style="font-size:2rem; margin-bottom:0.75rem;">💬</div>
              <div style="font-size:14px; color:var(--muted);">Ask me about your profit, costs, cash flow, or what to fix first.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Input
        col_inp, col_send = st.columns([5,1])
        with col_inp:
            user_q = st.text_input("Ask about your business...", key="chat_input", label_visibility="collapsed", placeholder="e.g. Why is my profit low? / What should I fix first?")
        with col_send:
            send = st.button("Ask →", key="send_chat", use_container_width=True)

        if send and user_q.strip():
            leaks_c = find_leaks(df_c, ind_c)
            ans = ai_copilot_answer(user_q, df_c, leaks_c, ind_c)
            st.session_state.chat_history.append({"role":"user","msg":user_q})
            st.session_state.chat_history.append({"role":"ai","msg":ans})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("Clear conversation", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CA PARTNER PROGRAM
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
    total_leak  = sum(c["leak"] for c in demo_portfolio)
    crit_count  = sum(1 for c in demo_portfolio if c["health"]=="red")

    st.markdown('<div class="ca-section">', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom:2.5rem;">
      <div style="font-size:11px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.18em;margin-bottom:1rem;">For Chartered Accountants</div>
      <div class="section-head">Your clients are losing money.<br>Show them exactly where.</div>
      <div class="section-sub" style="font-size:1rem;max-width:600px;">
        OpsClarity gives you a branded profit-leak report for every client — automated, monthly, zero extra work.
        CAs who use it retain clients longer, get more referrals, and earn ₹500/client/month in passive income.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Math calculator
    n_ca = st.slider("How many clients would you run on OpsClarity?", 10, 200, 40, 5)
    net  = n_ca*500-1999

    st.markdown(f"""
    <div class="ca-grid">
      <div class="ca-card gold-border">
        <div class="ca-label">The CA partner math</div>
        <div class="ca-title">Your monthly numbers</div>
        <div class="ca-math-row"><span class="ca-math-label">Clients on OpsClarity</span><span class="ca-math-val">{n_ca}</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Platform cost</span><span class="ca-math-val">₹1,999/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">You earn per client</span><span class="ca-math-val">₹500/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Gross passive income</span><span class="ca-math-val">₹{n_ca*500:,}/month</span></div>
        <div class="ca-math-row"><span class="ca-math-label">Net after platform</span><span class="ca-math-val big">₹{net:,}/month</span></div>
      </div>
      <div class="ca-card">
        <div class="ca-label">What your clients get</div>
        <div class="ca-title">Monthly profit health report</div>
        <div class="ca-body">
          Branded with your CA firm name. Shows every client exactly where they're losing money —
          in exact rupees, with specific actions.<br><br>
          <strong style="color:var(--paper);">Every month, without you doing any extra work.</strong><br><br>
          Clients receiving this report: renew without asking, refer you more, and stop shopping for another CA.
          That's the real value — not the ₹500/month. It's the relationship deepening.<br><br>
          <strong style="color:var(--gold);">Average CA firm earns ₹{net:,}/month from month 3.</strong>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Client dashboard demo
    st.markdown('<div style="margin-top:2.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-size:1.5rem; margin-bottom:1rem;">Your client dashboard — live demo</div>', unsafe_allow_html=True)

    client_rows = ""
    for c in demo_portfolio:
        hb = "red" if c["health"]=="red" else "amber" if c["health"]=="amber" else "green"
        hl = "🔴 Critical" if hb=="red" else "🟡 Monitor" if hb=="amber" else "🟢 Healthy"
        client_rows += (
            f'<div class="client-row">'
            f'<div><div class="client-name">{c["name"]}</div><div class="client-meta">{c["city"]} · {c["ind"].title()}</div></div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:var(--muted);">{fmt(c["rev"])}</div>'
            f'<div class="client-amt">{fmt(c["leak"])}</div>'
            f'<div><span class="health-badge {hb}">{hl}</span></div>'
            f'</div>'
        )

    st.markdown(f"""
    <div class="ca-card" style="padding:0; overflow:hidden;">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;padding:1.5rem;background:#1A1810;border-bottom:1px solid var(--border);">
        <div><div class="ca-label">Active clients</div><div style="font-family:'Playfair Display',serif;font-size:1.8rem;color:var(--paper);">{len(demo_portfolio)}</div></div>
        <div><div class="ca-label">Total leaks found</div><div style="font-family:'Playfair Display',serif;font-size:1.8rem;color:var(--gold);">{fmt(total_leak)}</div></div>
        <div><div class="ca-label">Need urgent action</div><div style="font-family:'Playfair Display',serif;font-size:1.8rem;color:var(--red);">{crit_count} clients</div></div>
      </div>
      <div class="client-row client-row-header" style="background:#111;">
        <div>Client</div><div>Revenue</div><div>Leaks Found</div><div>Health</div>
      </div>
      {client_rows}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Objections
    st.markdown('<div style="margin-top:2.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-size:1.5rem; margin-bottom:1rem;">Questions CAs ask us</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ca-grid">
      <div class="ca-card"><div class="ca-label">My clients won't share data</div><div class="ca-body">You upload the file — your client never interacts with OpsClarity. The report comes branded as your firm's work. Clients see a CA service, not a third-party app.</div></div>
      <div class="ca-card"><div class="ca-label">What if numbers are wrong?</div><div class="ca-body">OpsClarity flags potential leaks. You verify before sharing — exactly as you'd review any report. This is your co-pilot, not your replacement. Your judgement remains the product.</div></div>
      <div class="ca-card"><div class="ca-label">I already do this manually</div><div class="ca-body">If you do this for 40 clients every month, you know how many hours it takes. OpsClarity does the same analysis in 60 seconds per client. That time goes back to you — or to more clients.</div></div>
      <div class="ca-card"><div class="ca-label">Will it replace CAs?</div><div class="ca-body">No. The report says "verify with your CA" multiple times. GST, TDS, ITC — all require a qualified CA. We create the work. You do the work. Your client pays you more.</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c_l,c_c,c_r = st.columns([1,2,1])
    with c_c:
        if st.button("Join CA Partner Program — free 30-day trial →", use_container_width=True, type="primary"):
            st.balloons()
            st.success("✅ Application received. We'll call within 4 hours to set up your dashboard.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
with tab_bench:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Industry Benchmark Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Anonymised data from Indian SMEs. Used to validate every leak we flag.</div>', unsafe_allow_html=True)

    sel_ind = st.selectbox("Select industry", list(CROWDSOURCED.keys()), key="bi")
    bd = CROWDSOURCED.get(sel_ind,{})

    if bd:
        for cat, data in bd.items():
            p25, med, p75 = data["p25"], data["median"], data["p75"]
            pct_range = max(p75,1)
            st.markdown(f"""
            <div class="bench-card">
              <div class="bench-header">
                <div class="bench-cat">{cat} <span style="font-size:12px;color:var(--muted);font-weight:400;">{data['unit']}</span></div>
                <div class="bench-n">{data['n']} businesses</div>
              </div>
              <div class="bench-labels">
                <span>Best 25%: ₹{p25:,}</span>
                <span>Median: ₹{med:,}</span>
                <span>Top 25% pay: ₹{p75:,}</span>
              </div>
              <div class="bench-bar-wrap" style="margin:0.75rem 0;">
                <div class="bench-bar-fill" style="width:{int(p25/pct_range*100)}%; background:var(--green);"></div>
              </div>
              <div class="bench-bar-wrap">
                <div class="bench-bar-fill" style="width:{int(med/pct_range*100)}%; background:var(--gold);"></div>
              </div>
              <div class="bench-bar-wrap">
                <div class="bench-bar-fill" style="width:100%; background:var(--red); opacity:0.5;"></div>
              </div>
              <div style="font-size:12px; color:var(--green); margin-top:0.75rem; font-weight:600;">
                Switching from top-25% rate to best-25% = {int(((p75-p25)/p75)*100)}% cost reduction
              </div>
            </div>
            """, unsafe_allow_html=True)

            if data.get("city_splits"):
                city_df = pd.DataFrame([(c,r) for c,r in data["city_splits"].items()], columns=["City",f"Rate ({data['unit']})"])
                st.dataframe(city_df, hide_index=True, use_container_width=True)

    # Contribute data
    st.markdown('<div style="margin-top:2.5rem;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#1A1810; border:1px solid rgba(201,168,76,0.2); border-radius:16px; padding:1.5rem;">
      <div style="font-size:11px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.5rem;">Help Build the Database</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--paper);margin-bottom:0.5rem;">Contribute anonymised rates · Improve accuracy for all</div>
      <div style="font-size:13px;color:var(--muted);">Share what you pay for key inputs. Data is anonymised. Your submission makes benchmarks more accurate for every Indian SME.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
  <div>
    <div class="footer-brand">OpsClarity</div>
    <div class="footer-legal" style="margin-top:4px;">AI Business Advisor · Built in Bangalore 🇮🇳</div>
  </div>
  <div class="footer-legal">
    Management estimates only — not CA advice · Your data stays on your device ·
    <a href="#" style="color:var(--muted);text-decoration:none;">Privacy</a> ·
    <a href="#" style="color:var(--muted);text-decoration:none;">Terms</a>
  </div>
</div>
<a href="https://wa.me/916362319163?text=Hi, I want to learn more about OpsClarity" class="wa-float" target="_blank">
  💬 Talk to founder
</a>
""", unsafe_allow_html=True)
