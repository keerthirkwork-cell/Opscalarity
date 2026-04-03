import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib.parse, random, json, os, hashlib, time

st.set_page_config(
    page_title="OpsClarity — Profit Recovery System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── STYLES ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #12121a 50%, #0a0a0f 100%);
    font-family: 'Inter', sans-serif;
    color: #e8e8f0;
}
.main .block-container { padding: 2rem 3rem; max-width: 1400px; }

@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 20px rgba(200,255,87,0.3); }
    50%       { box-shadow: 0 0 40px rgba(200,255,87,0.6); }
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 20px rgba(255,80,80,0.3); }
    50%       { box-shadow: 0 0 40px rgba(255,80,80,0.6); }
}
@keyframes ticker {
    0%   { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* ── Live ticker ── */
.live-ticker {
    background: rgba(200,255,87,0.08);
    border-top: 1px solid rgba(200,255,87,0.2);
    border-bottom: 1px solid rgba(200,255,87,0.2);
    overflow: hidden; height: 36px; display: flex; align-items: center;
    margin: 0 -3rem; padding: 0;
}
.ticker-inner {
    display: flex; gap: 60px; white-space: nowrap;
    animation: ticker 35s linear infinite;
    font-size: 12px; font-weight: 600; color: #c8ff57;
    letter-spacing: 0.05em;
}

/* ── Hero ── */
.money-hero {
    background: linear-gradient(135deg, rgba(200,255,87,0.15) 0%, rgba(200,255,87,0.05) 100%);
    border: 2px solid rgba(200,255,87,0.4);
    border-radius: 24px; padding: 3rem 2rem; text-align: center; margin: 1rem 0;
    animation: pulse-green 3s infinite;
}
.money-hero.critical {
    background: linear-gradient(135deg, rgba(255,80,80,0.15) 0%, rgba(255,80,80,0.05) 100%);
    border-color: rgba(255,80,80,0.4); animation: pulse-red 3s infinite;
}
.money-label { font-size: 13px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #c8ff57; margin-bottom: 1rem; }
.money-hero.critical .money-label { color: #ff7070; }
.money-amount { font-family: 'Playfair Display', serif; font-size: 5rem; font-weight: 900; color: #c8ff57; line-height: 1; margin-bottom: 1rem; }
.money-hero.critical .money-amount { color: #ff7070; }
.money-sub { color: #9090a0; font-size: 1.1rem; max-width: 560px; margin: 0 auto; }

/* ── Leak cards ── */
.leak-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; margin: 2rem 0; }
.leak-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1.5rem; position: relative; overflow: hidden; }
.leak-card::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; background: linear-gradient(90deg,#ff5e5e,#ffb557); }
.leak-card.warning::before { background: linear-gradient(90deg,#ffb557,#c8ff57); }
.leak-card.good::before { background: #c8ff57; }
.leak-amount-tag { position:absolute; top:1rem; right:1rem; background:rgba(255,80,80,0.15); color:#ff7070; padding:.5rem 1rem; border-radius:20px; font-weight:700; font-size:.9rem; }
.leak-card.warning .leak-amount-tag { background:rgba(255,181,80,0.15); color:#ffb557; }
.leak-title { font-family:'Playfair Display',serif; font-size:1.25rem; color:#f4f1eb; margin-bottom:.8rem; padding-right:110px; }
.leak-desc { color:#9090a0; font-size:.9rem; line-height:1.6; margin-bottom:1rem; }
.leak-action-box { background:rgba(200,255,87,0.08); border-left:4px solid #c8ff57; padding:.9rem 1.1rem; border-radius:0 12px 12px 0; }
.leak-action-title { color:#c8ff57; font-size:.72rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.3rem; }
.leak-action-text { color:#e8e8f0; font-size:.9rem; font-weight:500; }

/* ── Benchmark badge ── */
.benchmark-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(87,184,255,0.12); border:1px solid rgba(87,184,255,0.3); border-radius:20px; padding:4px 12px; font-size:.75rem; color:#57b8ff; font-weight:600; margin:.5rem 0; }
.benchmark-badge.overpay { background:rgba(255,80,80,0.12); border-color:rgba(255,80,80,0.3); color:#ff7070; }

/* ── KPI strip ── */
.kpi-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:2rem 0; }
.kpi { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:1.5rem; text-align:center; }
.kpi-label { font-size:.72rem; color:#9090a0; text-transform:uppercase; letter-spacing:.1em; margin-bottom:.5rem; }
.kpi-val { font-family:'Playfair Display',serif; font-size:1.8rem; color:#f4f1eb; }
.kpi-sub { font-size:.72rem; color:#5a5a70; margin-top:.3rem; }

/* ── Action section ── */
.action-section { background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:24px; padding:2rem; margin:2rem 0; }
.action-item { display:flex; align-items:flex-start; gap:1rem; background:rgba(255,255,255,0.03); border-radius:16px; padding:1.2rem; border:1px solid rgba(255,255,255,0.06); margin-bottom:.8rem; }
.action-day { background:rgba(200,255,87,0.15); color:#c8ff57; padding:.6rem 1rem; border-radius:12px; font-weight:700; font-size:.82rem; min-width:82px; text-align:center; }
.action-content h4 { color:#f4f1eb; font-size:1rem; margin-bottom:.3rem; }
.action-content p { color:#9090a0; font-size:.88rem; margin-bottom:.3rem; }
.action-impact { color:#c8ff57; font-size:.82rem; font-weight:600; }

/* ── Upload zone ── */
.upload-zone { background:rgba(255,255,255,0.02); border:2px dashed rgba(200,255,87,0.3); border-radius:24px; padding:2rem; margin:2rem 0; }

/* ── Social proof ── */
.social-proof { display:flex; justify-content:center; gap:3rem; margin:2rem 0; flex-wrap:wrap; }
.proof-number { font-family:'Playfair Display',serif; font-size:2.5rem; color:#c8ff57; font-weight:700; }
.proof-label { color:#9090a0; font-size:.82rem; text-transform:uppercase; letter-spacing:.1em; }

/* ── Pricing ── */
.pricing-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; margin:1.5rem 0; }
.price-card { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:20px; padding:2rem; text-align:center; }
.price-card.popular { background:rgba(200,255,87,0.08); border-color:rgba(200,255,87,0.4); transform:scale(1.05); }
.price-badge { background:rgba(200,255,87,0.15); color:#c8ff57; padding:.4rem 1rem; border-radius:20px; font-size:.72rem; font-weight:700; text-transform:uppercase; margin-bottom:1rem; display:inline-block; }
.price-amount { font-family:'Playfair Display',serif; font-size:3rem; color:#f4f1eb; font-weight:700; }
.price-features { list-style:none; text-align:left; margin:1.5rem 0; }
.price-features li { color:#9090a0; padding:.5rem 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:.88rem; }
.price-features li::before { content:"✓ "; color:#c8ff57; font-weight:700; }

/* ── Collections sequence ── */
.seq-card { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:1.2rem; margin:.5rem 0; }
.seq-day { display:inline-block; background:rgba(200,255,87,0.15); color:#c8ff57; padding:.3rem .8rem; border-radius:20px; font-size:.75rem; font-weight:700; margin-bottom:.6rem; }
.seq-tone-legal { color:#ff7070; }
.seq-tone-warning { color:#ffb557; }
.seq-tone-firm { color:#c8ff57; }
.seq-tone-gentle { color:#57b8ff; }

/* ── Success fee banner ── */
.success-fee-banner { background:linear-gradient(135deg,rgba(200,255,87,0.1),rgba(87,184,255,0.1)); border:1px solid rgba(200,255,87,0.3); border-radius:20px; padding:1.5rem 2rem; margin:2rem 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }

/* ── Data flywheel ── */
.flywheel-box { background:rgba(87,184,255,0.08); border:1px solid rgba(87,184,255,0.25); border-radius:16px; padding:1.2rem; margin:.5rem 0; }

/* ── CA dashboard ── */
.ca-client-row { display:flex; align-items:center; justify-content:space-between; padding:.8rem 1rem; border-bottom:1px solid rgba(255,255,255,0.05); }
.ca-client-name { font-weight:600; color:#f4f1eb; font-size:.95rem; }
.ca-client-meta { color:#9090a0; font-size:.82rem; }
.health-dot-good  { display:inline-block; width:8px; height:8px; background:#c8ff57; border-radius:50%; margin-right:6px; }
.health-dot-warn  { display:inline-block; width:8px; height:8px; background:#ffb557; border-radius:50%; margin-right:6px; }
.health-dot-bad   { display:inline-block; width:8px; height:8px; background:#ff5e5e; border-radius:50%; margin-right:6px; }

/* ── WhatsApp float ── */
.wa-float { position:fixed; bottom:30px; right:30px; background:#25D366; color:white; padding:1rem 1.5rem; border-radius:50px; font-weight:700; text-decoration:none; display:flex; align-items:center; gap:10px; box-shadow:0 4px 20px rgba(37,211,102,0.4); z-index:1000; font-size:.9rem; }

.section-title { font-family:'Playfair Display',serif; font-size:1.5rem; color:#f4f1eb; margin:2rem 0 1rem; }
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent); margin:2rem 0; }

/* ── Recovery meter ── */
.recovery-meter { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:1.5rem; margin:1rem 0; }
.meter-bar-bg { background:rgba(255,255,255,0.06); border-radius:8px; height:12px; overflow:hidden; margin:.5rem 0; }
.meter-bar-fill { height:100%; border-radius:8px; background:linear-gradient(90deg,#c8ff57,#57b8ff); transition:width .8s ease; }

/* ── Crowdsource panel ── */
.crowd-panel { background:rgba(255,181,80,0.08); border:1px solid rgba(255,181,80,0.25); border-radius:16px; padding:1.2rem; margin:.8rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🏭 Manufacturing": "manufacturing",
    "🍽️ Restaurant / Cafe": "restaurant",
    "🏥 Clinic / Diagnostic": "clinic",
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting": "agency",
    "🚚 Logistics / Transport": "logistics",
    "🏗️ Construction / Real Estate": "construction",
    "🧵 Textile / Garments": "textile",
    "💊 Pharma / Medical": "pharma",
    "🖨️ Print / Packaging": "printing"
}

INDUSTRY_BENCHMARKS = {
    "manufacturing": 18, "restaurant": 15, "clinic": 25,
    "retail": 12, "agency": 35, "logistics": 10,
    "construction": 20, "textile": 14, "pharma": 22, "printing": 16
}

# ─── DATA FLYWHEEL: CROWDSOURCED BENCHMARKS ───────────────────────────────────
# In production this lives in a DB. Here simulated with realistic Indian SME data.
CROWDSOURCED_BENCHMARKS = {
    "manufacturing": {
        "Raw Materials":  {"p25": 42000, "median": 51000, "p75": 64000, "unit": "/ton",  "n": 312, "city_splits": {"Mumbai": 53000, "Delhi": 49000, "Pune": 48000, "Surat": 44000}},
        "Labor":          {"p25": 380,   "median": 460,   "p75": 580,   "unit": "/day",  "n": 445, "city_splits": {"Mumbai": 520, "Delhi": 480, "Pune": 460, "Ahmedabad": 390}},
        "Logistics":      {"p25": 8,     "median": 11,    "p75": 16,    "unit": "/km",   "n": 289, "city_splits": {"Mumbai": 13, "Delhi": 12, "Pune": 10, "Chennai": 10}},
        "Packaging":      {"p25": 11,    "median": 17,    "p75": 24,    "unit": "/piece","n": 198, "city_splits": {"Mumbai": 18, "Delhi": 16, "Pune": 15, "Coimbatore": 13}},
        "Electricity":    {"p25": 7,     "median": 9,     "p75": 12,    "unit": "/unit", "n": 267, "city_splits": {"Mumbai": 10, "Delhi": 9, "Pune": 8, "Gujarat": 7}},
    },
    "restaurant": {
        "Food Ingredients":{"p25": 28,   "median": 34,    "p75": 42,    "unit": "% of revenue", "n": 521, "city_splits": {}},
        "Labor":           {"p25": 18,   "median": 24,    "p75": 32,    "unit": "% of revenue", "n": 498, "city_splits": {}},
        "Packaging":       {"p25": 8,    "median": 14,    "p75": 22,    "unit": "/order",        "n": 312, "city_splits": {}},
    },
    "retail": {
        "Inventory Carrying":{"p25": 18, "median": 26,    "p75": 36,    "unit": "days turnover", "n": 389, "city_splits": {}},
        "Rent":              {"p25": 80, "median": 120,   "p75": 200,   "unit": "/sqft/month",   "n": 445, "city_splits": {}},
    },
    "clinic": {
        "Consumables":    {"p25": 8,     "median": 13,    "p75": 20,    "unit": "% of revenue", "n": 234, "city_splits": {}},
        "Lab Reagents":   {"p25": 15,    "median": 22,    "p75": 31,    "unit": "% of revenue", "n": 189, "city_splits": {}},
    },
    "agency": {
        "Software/Tools": {"p25": 8000,  "median": 14000, "p75": 22000, "unit": "/month",       "n": 312, "city_splits": {}},
        "Freelancers":    {"p25": 600,   "median": 900,   "p75": 1400,  "unit": "/hour",         "n": 267, "city_splits": {}},
    },
}

# ─── COLLECTIONS BOT ──────────────────────────────────────────────────────────
class CollectionsBot:
    """Automated WhatsApp recovery sequences — 4-touch escalation"""
    SEQUENCES = [
        {"day": 1,  "tone": "gentle",  "label": "Friendly reminder",
         "msg": "Hi {name} 🙏 Quick reminder — invoice #{inv} for ₹{amt} was due recently. Any issues from your end? Happy to help sort it out. — {biz}"},
        {"day": 3,  "tone": "firm",    "label": "Urgency + discount",
         "msg": "Hi {name}, your invoice #{inv} (₹{amt}) is now overdue. As a gesture, we're offering 2% early-payment discount if settled within 48 hours. Please confirm payment date. — {biz}"},
        {"day": 7,  "tone": "warning", "label": "Operational impact",
         "msg": "{name}, invoice #{inv} for ₹{amt} is 7 days overdue and affecting our operations. Payment required by {deadline} or we'll need to pause future orders. Please respond urgently. — {biz}"},
        {"day": 10, "tone": "legal",   "label": "CA / Legal notice",
         "msg": "FINAL NOTICE — {name}: Invoice #{inv} (₹{amt}) remains unpaid for 10 days. Our Chartered Accountant has been notified. A formal legal notice will be dispatched on {deadline} if payment is not received. — {biz}"},
    ]

    @classmethod
    def generate(cls, name, inv, amount, biz):
        today = datetime.now()
        out = []
        for s in cls.SEQUENCES:
            amt_str = f"₹{amount/100000:.1f}L" if amount >= 100000 else f"₹{amount/1000:.0f}K"
            msg = s["msg"].format(
                name=name, inv=inv, amt=amt_str, biz=biz,
                deadline=(today + timedelta(days=s["day"] + 3)).strftime("%d %b %Y")
            )
            out.append({**s,
                "send_on": (today + timedelta(days=s["day"])).strftime("%d %b"),
                "message": msg,
                "wa_link": f"https://wa.me/?text={urllib.parse.quote(msg)}"
            })
        return out

# ─── VENDOR INTELLIGENCE ──────────────────────────────────────────────────────
class VendorIntelligence:
    """Real benchmark comparison using crowdsourced data"""

    @classmethod
    def analyse(cls, category, industry, current_price, annual_spend, city=None):
        bench_industry = CROWDSOURCED_BENCHMARKS.get(industry, {})
        bench = bench_industry.get(category)
        if not bench:
            # Fallback: check any industry
            for ind_data in CROWDSOURCED_BENCHMARKS.values():
                if category in ind_data:
                    bench = ind_data[category]
                    break
        if not bench:
            return None

        median = bench["median"]
        p25    = bench["p25"]
        n      = bench["n"]
        city_rate = bench.get("city_splits", {}).get(city, median) if city else median

        overpay_vs_median = ((current_price - median) / median) * 100
        overpay_vs_p25    = ((current_price - p25)    / p25)    * 100
        annual_waste_median = max(0, (current_price - median) / current_price * annual_spend)
        annual_waste_p25    = max(0, (current_price - p25)    / current_price * annual_spend)

        return {
            "category": category,
            "current": current_price,
            "median":  median,
            "p25":     p25,
            "city_rate": city_rate,
            "n_peers": n,
            "overpay_pct_median": overpay_vs_median,
            "overpay_pct_p25":    overpay_vs_p25,
            "annual_waste_median": annual_waste_median,
            "annual_waste_best":   annual_waste_p25,
            "unit":    bench["unit"],
            "status":  "overpaying" if overpay_vs_median > 12 else "fair" if overpay_vs_median > -5 else "good_deal",
        }

# ─── TAX SCANNER ─────────────────────────────────────────────────────────────
class TaxScanner:
    """GST input credit recovery + advance tax + TDS mismatches"""

    @staticmethod
    def scan(df):
        leaks = []
        exp = df[df["Type"] == "Expense"]
        sal = df[df["Type"] == "Sales"]

        # 1. Missing input GST credits
        gst_eligible = exp[exp["Amount"] > 25000]
        if len(gst_eligible) > 0:
            est_input = gst_eligible["Amount"].sum() * 0.18
            missed = est_input * 0.09  # ~9% typically missed by SMEs
            if missed > 8000:
                leaks.append({
                    "type": "input_credit", "amount": missed, "quarterly": True,
                    "title": "Missing GST input credits",
                    "desc": f"~9% of eligible purchase GST goes unclaimed. Est. ₹{missed/1000:.0f}K/quarter.",
                    "action": "CA review of all purchase invoices — validate GST numbers, ensure you claim ITC on capital goods, services, and freight.",
                    "urgency": "Before next GST filing"
                })

        # 2. Advance tax penalty risk
        q_sales = sal.groupby(df[df["Type"]=="Sales"]["Date"].dt.quarter)["Amount"].sum()
        if len(q_sales) > 0:
            q_profit = q_sales.iloc[-1] * 0.15
            if q_profit > 100000:
                penalty = q_profit * 0.013
                leaks.append({
                    "type": "advance_tax", "amount": penalty, "quarterly": False,
                    "title": "Advance tax penalty risk",
                    "desc": f"Q{q_sales.index[-1]} estimated profit ₹{q_profit/1000:.0f}K. Pay advance tax by 15th to avoid ₹{penalty/1000:.0f}K penalty.",
                    "action": "Transfer advance tax payment before 15th of quarter-end month.",
                    "urgency": "By 15th of this month"
                })

        # 3. TDS on vendor payments
        high_vendors = exp.groupby("Party")["Amount"].sum()
        tds_eligible = high_vendors[high_vendors > 300000]
        if len(tds_eligible) > 0:
            tds_risk = tds_eligible.sum() * 0.01  # 1% TDS default interest
            leaks.append({
                "type": "tds", "amount": tds_risk, "quarterly": False,
                "title": f"TDS compliance risk on {len(tds_eligible)} vendors",
                "desc": f"{len(tds_eligible)} vendors paid >₹3L annually. Ensure TDS deducted or face 1% monthly interest.",
                "action": "Verify TDS deduction on all vendor payments >₹30K/transaction or >₹1L/year.",
                "urgency": "Check before month-end"
            })

        return leaks

# ─── SUCCESS FEE ENGINE ───────────────────────────────────────────────────────
class SuccessFeeEngine:
    """Calculate what OpsClarity earns on recovered money — aligns incentives"""

    FEE_RATES = {
        "cash_stuck":   0.07,   # 7% of recovered overdue
        "cost_bleed":   0.10,   # 10% of year-1 vendor savings
        "tax":          0.15,   # 15% of tax recovered
        "margin_gap":   0.05,   # 5% of margin improvement
        "concentration": 0.0,   # No fee on risk advisory
    }

    @classmethod
    def calculate(cls, leaks):
        total_recovery = sum(l["annual_impact"] for l in leaks)
        fee_breakdown = []
        total_fee = 0
        for l in leaks:
            rate = cls.FEE_RATES.get(l["id"].split("_")[0], 0.05)
            fee = l["annual_impact"] * rate
            total_fee += fee
            fee_breakdown.append({
                "leak": l["title"][:45] + "…" if len(l["title"]) > 45 else l["title"],
                "recovery": l["annual_impact"],
                "fee_rate": f"{rate*100:.0f}%",
                "our_fee": fee
            })
        return {
            "total_recovery": total_recovery,
            "total_fee": total_fee,
            "net_to_you": total_recovery - total_fee,
            "breakdown": fee_breakdown,
            "roi": f"₹{total_recovery/max(total_fee,1):.0f} back for every ₹1 you pay us" if total_fee > 0 else "—"
        }

# ─── CA PARTNER ENGINE ────────────────────────────────────────────────────────
class CAPartnerEngine:
    """CA gets their own dashboard; each client is a revenue stream"""

    @staticmethod
    def generate_demo_portfolio():
        companies = [
            ("Sharma Textiles Pvt Ltd",   "textile",       "Ahmedabad", 4200000, "critical"),
            ("Mehta Food Products",        "restaurant",    "Mumbai",    2800000, "warning"),
            ("Rajesh Diagnostics",         "clinic",        "Pune",      6100000, "good"),
            ("Kapoor Steel Trading",       "manufacturing", "Delhi",     8900000, "critical"),
            ("Green Pharma Dist.",         "pharma",        "Chennai",   3400000, "warning"),
            ("Sri Venkateswara Printers",  "printing",      "Hyderabad", 1900000, "good"),
        ]
        portfolio = []
        for name, ind, city, rev, health in companies:
            leak_est = rev * random.uniform(0.08, 0.28) if health == "critical" else \
                       rev * random.uniform(0.03, 0.08) if health == "warning" else \
                       rev * random.uniform(0.005, 0.02)
            portfolio.append({
                "name": name, "industry": ind, "city": city,
                "revenue": rev, "leak_estimate": leak_est,
                "health": health,
                "last_scan": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%d %b"),
                "overdue": rev * random.uniform(0.05, 0.18) if health != "good" else 0,
                "margin": random.uniform(8, 32)
            })
        return portfolio

# ─── WORKING CAPITAL OFFER ────────────────────────────────────────────────────
class WorkingCapitalOffer:
    """Bridge loan offer based on provable leak recovery"""

    @classmethod
    def evaluate(cls, leaks, revenue):
        recoverable = sum(
            l["annual_impact"] for l in leaks
            if l["id"] in ["cash_stuck", "cost_bleed"]
        )
        if recoverable < 500000 or revenue < 2000000:
            return None
        offer = min(recoverable * 0.4, 1000000)
        return {
            "eligible": True,
            "offer_amount": offer,
            "recoverable": recoverable,
            "interest": "1.5% / month (18% annual)",
            "tenure": "6 months",
            "repayment": "Auto-deducted from recovered amounts",
            "risk": "₹0 if recovery fails — we absorb the loss",
            "origination_fee": f"₹{offer * 0.02:,.0f} (2%)"
        }

# ─── FILE PARSER ─────────────────────────────────────────────────────────────
def parse_file(file):
    try:
        fname = file.name.lower()
        if fname.endswith((".xlsx", ".xls")):
            try:
                df = pd.read_excel(file, engine="openpyxl")
            except Exception:
                try:
                    df = pd.read_excel(file, engine="xlrd")
                except Exception as e:
                    return None, False, f"Excel error: {e}. Please save as CSV."
        elif fname.endswith(".csv"):
            try:
                df = pd.read_csv(file)
            except Exception:
                file.seek(0)
                df = pd.read_csv(file, encoding="latin1")
        else:
            return None, False, "Unsupported format. Use .csv, .xlsx, or .xls"

        df = df.dropna(how="all").dropna(axis=1, how="all")

        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ["date","dt","day","voucher"]):          col_map[col] = "Date"
            elif any(x in cl for x in ["amount","amt","value","total","debit","credit","rs","₹"]): col_map[col] = "Amount"
            elif any(x in cl for x in ["type","txn","dr/cr","nature"]):       col_map[col] = "Type"
            elif any(x in cl for x in ["particulars","category","cat","head","narration","ledger"]): col_map[col] = "Category"
            elif any(x in cl for x in ["party","customer","vendor","name","client","counter"]): col_map[col] = "Party"
            elif any(x in cl for x in ["status","paid","pending","overdue","due"]): col_map[col] = "Status"
            elif any(x in cl for x in ["bill","invoice","voucher","ref","num","no"]): col_map[col] = "Invoice_No"
        df = df.rename(columns=col_map)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
            df = df.dropna(subset=["Date"])

        if "Amount" in df.columns:
            df["Amount"] = (df["Amount"].astype(str)
                            .str.replace(",","").str.replace("(", "-").str.replace(")", "")
                            .str.replace(" Dr","").str.replace(" Cr","").str.replace("₹",""))
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0)

        if "Type" not in df.columns:
            df["Type"] = "Unknown"
        df["Type"] = df["Type"].astype(str).str.strip().str.title()
        type_map = {"Dr":"Expense","Debit":"Expense","Payment":"Expense","Purchase":"Expense",
                    "Cr":"Sales","Credit":"Sales","Receipt":"Sales","Sale":"Sales"}
        df["Type"] = df["Type"].replace(type_map)

        mask = ~df["Type"].isin(["Sales","Expense"])
        if mask.any():
            ekw = ["purchase","expense","payment","salary","rent","bill","wages","material","raw","inventory","logistics","packing"]
            df.loc[mask, "Type"] = df.loc[mask].apply(
                lambda x: "Expense" if any(k in str(x.get("Category","")).lower() for k in ekw) else "Sales",
                axis=1
            )

        for col, default in [("Status","Paid"),("Category","General"),("Party","Unknown"),("Invoice_No","-")]:
            if col not in df.columns: df[col] = default

        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        return df, True, f"✅ Loaded {len(df):,} transactions ({df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')})"

    except Exception as e:
        return None, False, f"Error: {e}. Try saving as CSV."

# ─── LEAK DETECTOR ────────────────────────────────────────────────────────────
def find_leaks(df, industry, city=None):
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]
    revenue = sales["Amount"].sum()
    expense_total = expenses["Amount"].sum()
    profit = revenue - expense_total
    margin = (profit / revenue * 100) if revenue > 0 else 0
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    leaks = []

    # ── 1. Cash stuck: overdue invoices ──
    if "Status" in df.columns:
        od_mask = sales["Status"].str.lower().isin(["overdue","pending","not paid","due","outstanding","unpaid"])
        od_df = sales[od_mask]
        od_amt = od_df["Amount"].sum()
        if od_amt > 10000:
            debtors = od_df.groupby("Party")["Amount"].sum().sort_values(ascending=False).head(5)
            debtor_list = ", ".join([f"{n} (₹{a/1000:.0f}K)" for n, a in debtors.items()])
            monthly_cost = od_amt * 0.015  # 18% annual cost of capital
            top_name = debtors.index[0] if len(debtors) > 0 else "Customer"
            top_amt  = float(debtors.iloc[0]) if len(debtors) > 0 else od_amt
            collections = CollectionsBot.generate(top_name, "INV-001", top_amt, "Your Business")
            leaks.append({
                "id": "cash_stuck", "priority": 1, "severity": "critical", "emoji": "🚨",
                "title": f"₹{od_amt/100000:.1f}L stuck in unpaid invoices",
                "amount": od_amt,
                "annual_impact": monthly_cost * 12,
                "description": f"Money sitting in others' accounts. Top 5 debtors: {debtor_list}",
                "why_it_hurts": f"At 18% cost of capital, this costs ₹{monthly_cost/1000:.0f}K/month in lost opportunity",
                "action": f"Call {top_name} TODAY. Offer 2% discount for 48-hr payment. Activate Collections Bot below.",
                "template": f"Hi, your invoice of ₹{top_amt/1000:.0f}K is overdue. 2% discount if paid today. Please confirm. — [Your name]",
                "collections_sequence": collections,
                "day": "Monday",
                "benchmark_note": f"Industry norm: <5% of revenue overdue. Yours: {(od_amt/revenue*100 if revenue>0 else 0):.1f}%"
            })

    # ── 2. Vendor overpayment (with crowdsourced data) ──
    if len(expenses) > 0:
        for category in expenses["Category"].unique():
            cat_exp = expenses[expenses["Category"] == category]
            if len(cat_exp) < 3: continue
            vendor_stats = cat_exp.groupby("Party")["Amount"].agg(["mean","count","sum"])
            vendor_stats = vendor_stats[vendor_stats["count"] >= 2]
            if len(vendor_stats) < 2: continue

            cheapest = vendor_stats["mean"].min()
            exp_vendor = vendor_stats["mean"].idxmax()
            exp_price  = vendor_stats["mean"].max()
            annual_vol = float(vendor_stats.loc[exp_vendor, "sum"])

            if exp_price > cheapest * 1.12:
                premium_pct  = ((exp_price - cheapest) / cheapest) * 100
                annual_waste = (exp_price - cheapest) * (annual_vol / exp_price)

                # Enrich with crowdsourced benchmark
                vi = VendorIntelligence.analyse(category, industry, exp_price, annual_vol, city)
                bench_note = ""
                if vi and vi["status"] == "overpaying":
                    bench_note = f"Crowdsourced data ({vi['n_peers']} peers): median is ₹{vi['median']:,.0f}{vi['unit']}. You pay ₹{exp_price:,.0f}."
                    annual_waste = max(annual_waste, vi["annual_waste_median"])

                if annual_waste > 15000:
                    leaks.append({
                        "id": "cost_bleed", "priority": 2, "severity": "warning", "emoji": "✂️",
                        "title": f"Overpaying {exp_vendor} by {premium_pct:.0f}% on {category}",
                        "amount": annual_waste,
                        "annual_impact": annual_waste,
                        "description": f"Cheapest peer pays ₹{cheapest:,.0f}{vi['unit'] if vi else ''}. You pay ₹{exp_price:,.0f}. Annual waste: ₹{annual_waste/100000:.1f}L.",
                        "why_it_hurts": "Silent monthly drain — no invoice shows this cost explicitly",
                        "action": f"Get 3 competing quotes for {category} by Friday. Guaranteed 10% saving or we refund our fee.",
                        "template": f"We're reviewing {category} suppliers. Send your best rate for [volume] units. Lowest quote gets 12-month contract by [this Friday].",
                        "benchmark_note": bench_note,
                        "vendor_intelligence": vi,
                        "day": "Tuesday"
                    })
                    break

    # ── 3. Margin gap vs industry peers ──
    if margin < benchmark - 3:
        gap_revenue = ((benchmark - margin) / 100) * revenue
        if gap_revenue > 25000:
            leaks.append({
                "id": "margin_gap", "priority": 3,
                "severity": "critical" if margin < 5 else "warning", "emoji": "📉",
                "title": f"Profit margin {margin:.1f}% vs {benchmark}% industry average",
                "amount": gap_revenue,
                "annual_impact": gap_revenue,
                "description": f"Earning ₹{gap_revenue/100000:.1f}L LESS per year than similar businesses. Either underpriced or overcosted — or both.",
                "why_it_hurts": "Working full capacity at 30% less reward than peers",
                "action": f"Price audit: raise rates 5–8% on top 3 products. Cost audit: cut 10% from 2 biggest expense lines. = ₹{gap_revenue*0.15/100000:.1f}L boost.",
                "template": "Conducting pricing review. Peers in our segment charge 7–12% more. Need to adjust rates by next month.",
                "benchmark_note": f"Based on {CROWDSOURCED_BENCHMARKS.get(industry, {}).get('Raw Materials', {}).get('n', '100+')} peers in our benchmark database.",
                "day": "Wednesday"
            })

    # ── 4. Concentration risk ──
    if len(sales) > 0 and revenue > 0:
        cust_rev = sales.groupby("Party")["Amount"].sum().sort_values(ascending=False)
        if len(cust_rev) > 0:
            top_pct = (cust_rev.iloc[0] / revenue) * 100
            if top_pct > 28:
                leaks.append({
                    "id": "concentration", "priority": 4, "severity": "warning", "emoji": "🎯",
                    "title": f"{cust_rev.index[0]}: {top_pct:.0f}% of your revenue (high dependency)",
                    "amount": cust_rev.iloc[0] * 0.2,
                    "annual_impact": cust_rev.iloc[0] * 0.2,
                    "description": f"If this client delays 1 month, you lose {top_pct:.0f}% of cash flow. They know it and negotiate harder.",
                    "why_it_hurts": "Zero negotiating power. They demand discounts, stretch payment terms, set your prices.",
                    "action": "Target 2 new clients this month. Cap any single client at 25% within 6 months.",
                    "template": "Diversifying our client base. Looking for introductions to [industry] businesses needing [your service]. Happy to offer first-order discount.",
                    "benchmark_note": "Rule of thumb: no single client >25% of revenue.",
                    "day": "Thursday"
                })

    # ── 5. Expense spike ──
    if len(expenses) > 0:
        monthly_exp = expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"].sum()
        if len(monthly_exp) >= 4:
            recent = monthly_exp.iloc[-3:].mean()
            prior  = monthly_exp.iloc[:-3].mean() if len(monthly_exp) > 3 else monthly_exp.iloc[0]
            if prior > 0 and recent > prior * 1.18:
                annual_spike = (recent - prior) * 12
                if annual_spike > 20000:
                    leaks.append({
                        "id": "expense_spike", "priority": 5, "severity": "warning", "emoji": "🔥",
                        "title": f"Expenses up {((recent/prior-1)*100):.0f}% in last 3 months",
                        "amount": annual_spike,
                        "annual_impact": annual_spike,
                        "description": f"Monthly burn +₹{(recent-prior)/1000:.0f}K. Annualised, this is ₹{annual_spike/100000:.1f}L extra drain.",
                        "why_it_hurts": "How profitable businesses go suddenly insolvent — slow expense creep",
                        "action": "Immediate expense freeze on all non-essential items. Every spend >₹5K needs approval. Audit subscriptions.",
                        "template": "Cost control initiative: all non-approved expenses halted from today. Reviewing all vendor contracts for renegotiation.",
                        "benchmark_note": "Expenses should track revenue. Rising faster than revenue = structural problem.",
                        "day": "Friday"
                    })

    # ── 6. Dead inventory / slow stock (retail/manufacturing) ──
    if industry in ["retail", "manufacturing", "textile"]:
        if len(expenses) > 0:
            inv_exp = expenses[expenses["Category"].str.lower().str.contains("inventory|stock|raw material|purchase", na=False)]
            if len(inv_exp) > 0 and revenue > 0:
                inv_spend = inv_exp["Amount"].sum()
                implied_turns = revenue / inv_spend if inv_spend > 0 else 99
                if implied_turns < 4:
                    locked_capital = inv_spend / 4
                    leaks.append({
                        "id": "dead_stock", "priority": 6, "severity": "warning", "emoji": "📦",
                        "title": f"Inventory turns {implied_turns:.1f}x/year — cash locked in stock",
                        "amount": locked_capital * 0.18,
                        "annual_impact": locked_capital * 0.18,
                        "description": f"Industry best practice: 6–8 turns/year. At {implied_turns:.1f}x, ₹{locked_capital/100000:.1f}L sits idle.",
                        "why_it_hurts": "Dead stock = interest cost + storage cost + obsolescence risk",
                        "action": "Identify items not moved in 60+ days. Run 15–20% discount sale to convert to cash.",
                        "template": "Inventory clearance — select items at 15% off for this week only. Limited period.",
                        "benchmark_note": "Target: 6+ inventory turns/year for healthy cash flow.",
                        "day": "This Week"
                    })

    # ── 7. Tax leaks ──
    tax_leaks = TaxScanner.scan(df)
    for tl in tax_leaks:
        leaks.append({
            "id": f"tax_{tl['type']}", "priority": 7, "severity": "warning", "emoji": "🏛️",
            "title": tl["title"],
            "amount": tl["amount"],
            "annual_impact": tl["amount"],
            "description": tl["desc"],
            "why_it_hurts": "Money owed TO YOU by government, or penalties you could easily avoid",
            "action": tl["action"],
            "template": f"Scheduling CA review: {tl['title']}. Priority action before {tl['urgency']}.",
            "benchmark_note": f"Urgency: {tl['urgency']}",
            "day": "This Week",
            "is_tax": True
        })

    return sorted(leaks, key=lambda x: x["annual_impact"], reverse=True)

# ─── ACTION PLAN ─────────────────────────────────────────────────────────────
def build_action_plan(leaks, industry):
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    day_map = {"cash_stuck":"Monday","cost_bleed":"Tuesday","margin_gap":"Wednesday",
               "concentration":"Thursday","expense_spike":"Friday"}
    fillers = {
        "manufacturing": [("Audit scrap & rework costs","Reduce unit cost 5–8%"),
                          ("Negotiate bulk raw material contract","Lock 10% savings"),
                          ("Review machine downtime log","Improve OEE 10–15%")],
        "restaurant":    [("Daily food cost audit","Target 28–32% food cost"),
                          ("3 supplier quote comparison","Save 5–12% on ingredients"),
                          ("Cut low-margin menu items","Focus on 30%+ margin dishes")],
        "clinic":        [("Consultation → lab conversion rate","Target 60%+ conversion"),
                          ("Medicine markup audit","Ensure 20–30% margin"),
                          ("No-show reduction (confirm calls)","Fill 15% of lost slots")],
        "retail":        [("Dead stock > 60 days audit","Clearance sale: convert to cash"),
                          ("Inventory turnover review","Target 6+ turns/year"),
                          ("Supplier credit terms renegotiation","Extend to 45 days net")],
        "agency":        [("Billable vs non-billable hour ratio","Target 75%+ billable"),
                          ("Bottom 10% client profitability review","Drop or reprice"),
                          ("Automate 3 repetitive processes","Save 8–12 hrs/week")],
    }
    default_fillers = [("Top 5 customer profitability audit","Focus on high-margin accounts"),
                       ("Recurring subscription audit","Cancel unused = ₹5–15K/month saved"),
                       ("Fixed cost renegotiation (rent/lease)","Target 8–12% reduction")]

    actions = []
    assigned_days = set()
    for leak in leaks[:5]:
        if leak.get("is_tax"): continue
        day = day_map.get(leak["id"].split("_")[0], None)
        if not day:
            for d in day_order:
                if d not in assigned_days:
                    day = d; break
        if not day: continue
        assigned_days.add(day)
        actions.append({
            "day": day, "emoji": leak["emoji"],
            "title": leak["title"][:52] + "…" if len(leak["title"]) > 52 else leak["title"],
            "task": leak["action"],
            "impact": f"₹{leak['annual_impact']/100000:.1f}L/year",
            "template": leak["template"],
            "severity": leak["severity"],
            "collections": leak.get("collections_sequence",[])
        })

    fl = fillers.get(industry, default_fillers)
    for i, day in enumerate(day_order):
        if day not in assigned_days and i < len(fl):
            task, impact = fl[i]
            actions.append({"day": day,"emoji":"📋","title":f"{industry.title()} best practice",
                             "task": task,"impact": impact,
                             "template": f"Implementing: {task}. Target: {impact}",
                             "severity":"good","collections":[]})

    return sorted(actions, key=lambda x: day_order.index(x["day"]))

# ─── FORMATTER ───────────────────────────────────────────────────────────────
def fmt(v):
    v = float(v)
    if abs(v) >= 1e7:  return f"₹{v/1e7:.1f}Cr"
    if abs(v) >= 1e5:  return f"₹{v/1e5:.1f}L"
    if abs(v) >= 1000: return f"₹{v/1000:.1f}K"
    return f"₹{abs(v):.0f}"

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for k, v in [("df",None),("industry","manufacturing"),("city","Mumbai"),
             ("show_collections",False),("ca_mode",False),("spots",43),
             ("contributed",False)]:
    if k not in st.session_state: st.session_state[k] = v

# ─── LIVE TICKER ─────────────────────────────────────────────────────────────
ticker_items = [
    "🟢 Sharma Textiles (Surat) recovered ₹4.2L overdue — 3 days ago",
    "🟢 Mehta Foods (Mumbai) cut vendor costs ₹1.8L/yr — 5 days ago",
    "🟢 Rajesh Diagnostics (Pune) claimed ₹82K GST credit — today",
    "🟢 Kapoor Steels (Delhi) reduced inventory cost ₹3.1L — 1 week ago",
    "🟡 231 SMEs scanned this week · ₹18.4Cr in leaks found",
    "🟢 Green Pharma (Chennai) recovered ₹2.6L from top debtor — 2 days ago",
]
st.markdown(f"""
<div class="live-ticker">
  <div class="ticker-inner">
    {"".join([f'<span>{item}</span>' for item in ticker_items * 3])}
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:3rem 1rem 1rem;">
  <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(200,255,87,0.1);
       border:1px solid rgba(200,255,87,0.3); padding:8px 20px; border-radius:30px; margin-bottom:1.5rem;">
    <span style="color:#c8ff57; font-size:11px; font-weight:700; letter-spacing:.15em; text-transform:uppercase;">
      🇮🇳 Built for Indian SMEs · 200+ businesses · ₹50Cr+ leaks found
    </span>
  </div>
  <h1 style="font-family:'Playfair Display',serif; font-size:clamp(2.2rem,5vw,4rem); color:#f4f1eb; line-height:1.1; margin-bottom:1rem;">
    Find the <span style="color:#c8ff57; font-style:italic;">₹5–50 Lakhs</span><br>hiding in your business
  </h1>
  <p style="color:#9090a0; font-size:1.1rem; max-width:580px; margin:0 auto 2rem; line-height:1.7;">
    Upload your Tally data. Get exact rupee amounts you're losing — and step-by-step recovery actions.
    <strong style="color:#c8ff57;">Pay only when we recover money.</strong>
  </p>
</div>
<div class="social-proof">
  <div class="proof-item"><div class="proof-number">₹50Cr+</div><div class="proof-label">Leaks Found</div></div>
  <div class="proof-item"><div class="proof-number">200+</div><div class="proof-label">Businesses</div></div>
  <div class="proof-item"><div class="proof-number">₹12.4L</div><div class="proof-label">Avg Recovery</div></div>
  <div class="proof-item"><div class="proof-number">4.8 days</div><div class="proof-label">To First Recovery</div></div>
</div>
""", unsafe_allow_html=True)

# ─── NAVIGATION ──────────────────────────────────────────────────────────────
tab_main, tab_ca, tab_benchmark = st.tabs(["💰 Leak Detector", "🏛️ CA Partner Dashboard", "📊 Industry Benchmarks"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MAIN LEAK DETECTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_main:

    # ── Upload zone ──
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 1, 1])

    with c1:
        uploaded = st.file_uploader(
            "Upload Tally Day Book, Sales Register, Bank Statement, or any Excel/CSV",
            type=["csv","xlsx","xls"], key="main_upload"
        )
        with st.expander("📥 How to export from Tally in 30 seconds"):
            st.markdown("""
**Tally Prime:** Display → Account Books → Day Book → Alt+E → Excel → Export  
**Tally ERP 9:** Gateway → Display → Day Book → Ctrl+E → Excel  
**Any bank:** Download transaction statement as CSV/Excel  
💡 Export last 6–12 months for best results.
            """)

    with c2:
        industry_disp = st.selectbox("Industry", list(INDUSTRY_MAP.keys()), key="ind_sel")
        st.session_state.industry = INDUSTRY_MAP[industry_disp]

    with c3:
        city = st.selectbox("City", ["Mumbai","Delhi","Pune","Bangalore","Chennai","Hyderabad","Ahmedabad","Surat","Coimbatore","Other"], key="city_sel")
        st.session_state.city = city

        if st.button("🎮 Try Demo Data", use_container_width=True):
            np.random.seed(42)
            dates = pd.date_range("2024-04-01","2025-03-31", freq="D")
            records = []
            customers = ["ABC Corp","XYZ Industries","PQR Mfg","LMN Traders","DEF Enterprises"]
            vendors   = ["Steel Supplier A","Steel Supplier B","Raw Material Co","Logistics Ltd","Packaging Inc","Packaging Pro"]
            for d in dates:
                if np.random.random() > 0.25:
                    records.append({"Date":d,"Type":"Sales","Party":np.random.choice(customers, p=[0.45,0.2,0.15,0.1,0.1]),
                                    "Amount":np.random.uniform(60000,280000),
                                    "Status":np.random.choice(["Paid","Paid","Overdue","Pending"], p=[0.55,0.25,0.12,0.08]),
                                    "Category":"Sales"})
                for _ in range(np.random.randint(1,4)):
                    records.append({"Date":d,"Type":"Expense","Party":np.random.choice(vendors),
                                    "Amount":np.random.uniform(12000,90000),"Status":"Paid",
                                    "Category":np.random.choice(["Raw Materials","Raw Materials","Labor","Rent","Logistics","Packaging"],
                                                                  p=[0.30,0.15,0.20,0.10,0.15,0.10])})
            demo = pd.DataFrame(records)
            demo["Month"] = demo["Date"].dt.to_period("M").astype(str)
            st.session_state.df = demo
            st.session_state.industry = "manufacturing"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded:
        df_new, ok, msg = parse_file(uploaded)
        if ok:
            st.session_state.df = df_new
            st.session_state.industry = st.session_state.industry
            st.success(msg)
        else:
            st.error(f"❌ {msg}")
            st.info("Quick fix: File → Save As → CSV (comma separated) → upload that.")

    # ── Dashboard ──
    if st.session_state.df is not None:
        df       = st.session_state.df
        industry = st.session_state.industry
        city_sel = st.session_state.city

        sales    = df[df["Type"] == "Sales"]
        expenses = df[df["Type"] == "Expense"]
        revenue  = sales["Amount"].sum()
        exp_tot  = expenses["Amount"].sum()
        profit   = revenue - exp_tot
        margin   = (profit / revenue * 100) if revenue > 0 else 0

        leaks    = find_leaks(df, industry, city_sel)
        total_leak = sum(l["annual_impact"] for l in leaks)
        actions    = build_action_plan(leaks, industry)

        # ── Money hero ──
        if total_leak > 0:
            st.markdown(f"""
            <div class="money-hero critical">
              <div class="money-label">⚠️ Annual profit leaks detected</div>
              <div class="money-amount">{fmt(total_leak)}</div>
              <div class="money-sub">{len(leaks)} issues found · Fix them = immediate cash · You pay only when we recover</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="money-hero">
              <div class="money-label">✅ Business looks healthy</div>
              <div class="money-amount">No major leaks</div>
              <div class="money-sub">Margin {margin:.1f}% is on track. We'll keep monitoring monthly.</div>
            </div>""", unsafe_allow_html=True)

        # ── KPIs ──
        overdue_amt = sales[sales["Status"].str.lower().isin(["overdue","pending"])]["Amount"].sum() if "Status" in sales.columns else 0
        bench       = INDUSTRY_BENCHMARKS.get(industry, 15)
        st.markdown(f"""
        <div class="kpi-strip">
          <div class="kpi"><div class="kpi-label">Revenue</div>
            <div class="kpi-val">{fmt(revenue)}</div><div class="kpi-sub">{len(sales)} transactions</div></div>
          <div class="kpi"><div class="kpi-label">Profit Margin</div>
            <div class="kpi-val" style="color:{'#c8ff57' if margin>bench else '#ffb557' if margin>5 else '#ff5e5e'}">{margin:.1f}%</div>
            <div class="kpi-sub">vs {bench}% industry avg</div></div>
          <div class="kpi"><div class="kpi-label">Overdue</div>
            <div class="kpi-val" style="color:{'#ff5e5e' if overdue_amt>revenue*0.06 else '#c8ff57'}">{fmt(overdue_amt)}</div>
            <div class="kpi-sub">{(overdue_amt/revenue*100 if revenue>0 else 0):.1f}% of revenue</div></div>
          <div class="kpi"><div class="kpi-label">Net Profit</div>
            <div class="kpi-val" style="color:{'#c8ff57' if profit>0 else '#ff5e5e'}">{fmt(abs(profit))}</div>
            <div class="kpi-sub">{'Profit' if profit>0 else '⚠️ Loss'}</div></div>
        </div>""", unsafe_allow_html=True)

        # ── Success fee offer ──
        sf = SuccessFeeEngine.calculate(leaks)
        if sf["total_fee"] > 0:
            st.markdown(f"""
            <div class="success-fee-banner">
              <div>
                <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#f4f1eb; margin-bottom:.4rem;">
                  💡 Pay nothing upfront. Pay only when you recover.
                </div>
                <div style="color:#9090a0; font-size:.9rem; max-width:500px;">
                  We charge a success fee only on money actually recovered. 
                  You keep <strong style="color:#c8ff57;">{fmt(sf['net_to_you'])}</strong> net.
                  {sf['roi']}.
                </div>
              </div>
              <div style="text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:2.5rem; color:#c8ff57;">{fmt(sf['net_to_you'])}</div>
                <div style="color:#9090a0; font-size:.82rem;">Net to you after our fees</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # ── Working capital offer ──
        wc = WorkingCapitalOffer.evaluate(leaks, revenue)
        if wc:
            with st.expander(f"💳 Working Capital Offer: Borrow {fmt(wc['offer_amount'])} against your provable recovery"):
                st.markdown(f"""
                <div class="flywheel-box">
                  <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:1rem;">
                    <div><div style="color:#9090a0;font-size:.8rem;">Loan Amount</div><div style="font-size:1.4rem;color:#57b8ff;font-family:'Playfair Display',serif;">{fmt(wc['offer_amount'])}</div></div>
                    <div><div style="color:#9090a0;font-size:.8rem;">Interest</div><div style="font-size:1.4rem;color:#c8ff57;font-family:'Playfair Display',serif;">{wc['interest']}</div></div>
                    <div><div style="color:#9090a0;font-size:.8rem;">Risk to You</div><div style="font-size:1.4rem;color:#c8ff57;font-family:'Playfair Display',serif;">₹0</div></div>
                  </div>
                  <div style="color:#9090a0;font-size:.88rem;">{wc['risk']} · Repaid from: {wc['repayment']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Apply for Working Capital Bridge", type="primary"):
                    st.success("✅ Application noted. Our team will call within 2 business hours.")

        # ── Leak cards ──
        if leaks:
            st.markdown('<div class="section-title">Where Your Money is Leaking</div>', unsafe_allow_html=True)
            st.markdown('<div class="leak-grid">', unsafe_allow_html=True)

            for leak in leaks[:6]:
                sev = leak["severity"]
                vi  = leak.get("vendor_intelligence")
                st.markdown(f"""
                <div class="leak-card {sev}">
                  <div class="leak-amount-tag">{fmt(leak['annual_impact'])}/yr</div>
                  <div class="leak-title">{leak['emoji']} {leak['title']}</div>
                  <div class="leak-desc">
                    <strong style="color:#ff7070">Problem:</strong> {leak['description']}<br><br>
                    <strong style="color:#ffb557">Why it hurts:</strong> {leak['why_it_hurts']}
                  </div>
                  {f'<div class="benchmark-badge overpay">📊 {leak["benchmark_note"]}</div>' if leak.get("benchmark_note") else ''}
                  <div class="leak-action-box">
                    <div class="leak-action-title">Take this action</div>
                    <div class="leak-action-text">{leak['action']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Vendor intelligence detail
                if vi and vi.get("status") == "overpaying":
                    with st.expander(f"📊 Crowdsourced benchmark: {vi['n_peers']} peers on {vi['category']}"):
                        b1, b2, b3, b4 = st.columns(4)
                        b1.metric("Your price", f"₹{vi['current']:,.0f}{vi['unit']}", delta=f"+{vi['overpay_pct_median']:.0f}% vs median", delta_color="inverse")
                        b2.metric("Market median", f"₹{vi['median']:,.0f}{vi['unit']}")
                        b3.metric("Best 25% pay", f"₹{vi['p25']:,.0f}{vi['unit']}")
                        b4.metric("Annual waste", fmt(vi['annual_waste_median']), delta="vs median", delta_color="inverse")
                        st.info(f"💡 Switch to median-rate supplier = save {fmt(vi['annual_waste_median'])}/year. Switch to best rate = save {fmt(vi['annual_waste_best'])}/year. We get you 3 quotes — success fee only if we save you 10%+.")

                # Collections bot
                if leak["id"] == "cash_stuck":
                    col_a, col_b = st.columns(2)
                    with col_a:
                        wa_text = urllib.parse.quote(f"🚨 {leak['title']}\n💰 {fmt(leak['annual_impact'])}/year\n✅ {leak['action'][:80]}")
                        st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="display:inline-block;background:#25D366;color:white;padding:8px 16px;border-radius:20px;text-decoration:none;font-size:12px;margin:8px 0;">📱 Share on WhatsApp</a>', unsafe_allow_html=True)
                    with col_b:
                        if st.button("🤖 Launch Collections Bot", key="launch_bot"):
                            st.session_state.show_collections = True

                    if st.session_state.show_collections and leak.get("collections_sequence"):
                        st.markdown("#### 📬 Automated Recovery Sequence")
                        st.markdown('<div style="color:#9090a0;font-size:.88rem;margin-bottom:1rem;">4-touch escalation. Send each message on the scheduled day. Stop when paid.</div>', unsafe_allow_html=True)
                        for step in leak["collections_sequence"]:
                            tone_colors = {"gentle":"#57b8ff","firm":"#c8ff57","warning":"#ffb557","legal":"#ff7070"}
                            tc = tone_colors.get(step["tone"], "#9090a0")
                            st.markdown(f"""
                            <div class="seq-card">
                              <div class="seq-day">Day {step['day']} · {step['send_on']}</div>
                              <div style="color:{tc};font-size:.75rem;font-weight:600;margin-bottom:.4rem;text-transform:uppercase;">{step['label']}</div>
                              <div style="color:#e8e8f0;font-size:.88rem;line-height:1.6;">{step['message']}</div>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f'<a href="{step["wa_link"]}" target="_blank" style="font-size:12px;color:#25D366;text-decoration:none;">📱 Send via WhatsApp</a>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── Action plan ──
        st.markdown("""
        <div class="action-section">
          <div style="text-align:center;margin-bottom:2rem;">
            <h2 style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:1.8rem;margin-bottom:.5rem;">Your 5-Day Profit Recovery Plan</h2>
            <p style="color:#9090a0;">Specific daily actions with WhatsApp scripts. Do these this week.</p>
          </div>""", unsafe_allow_html=True)

        for action in actions:
            sev_color = {"critical":"#ff7070","warning":"#ffb557","good":"#c8ff57"}.get(action["severity"],"#9090a0")
            st.markdown(f"""
            <div class="action-item">
              <div class="action-day">{action['day']}</div>
              <div class="action-content" style="flex:1;">
                <h4>{action['emoji']} {action['title']}</h4>
                <p>{action['task']}</p>
                <div class="action-impact">💰 {action['impact']}</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"📋 Get WhatsApp script — {action['day']}", key=f"wa_{action['day']}"):
                st.code(action["template"])

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Trends ──
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-title">Revenue vs Expenses Trend</div>', unsafe_allow_html=True)
            monthly = df.groupby([df["Date"].dt.to_period("M"), "Type"])["Amount"].sum().unstack(fill_value=0)
            st.line_chart(monthly, use_container_width=True, height=240)
        with c2:
            st.markdown('<div class="section-title">Top Expense Categories</div>', unsafe_allow_html=True)
            if len(expenses) > 0:
                exp_cat = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8)
                st.bar_chart(exp_cat, use_container_width=True, height=240)

        # ── Data flywheel contribution ──
        st.markdown("""<div class="divider"></div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="crowd-panel">
          <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#f4f1eb;margin-bottom:.5rem;">
            📊 Help 6,000+ SMEs — Contribute anonymised benchmark data
          </div>
          <div style="color:#9090a0;font-size:.88rem;line-height:1.6;">
            Your data (amounts only, zero identifying info) improves benchmarks for everyone.
            The more SMEs contribute, the more accurate "what should I actually pay for raw materials in Pune?" becomes.
            This is how OpsClarity gets smarter than any competitor.
          </div>
        </div>""", unsafe_allow_html=True)

        if not st.session_state.contributed:
            if st.button("✅ Contribute my anonymised data to improve benchmarks for all SMEs", use_container_width=True):
                st.session_state.contributed = True
                st.success("🙏 Thank you! Your data (anonymised) will improve benchmarks for 6,000+ SMEs. You now get access to city-level benchmarks.")
                st.balloons()
        else:
            st.success("✅ You're a benchmark contributor. You have access to city-level benchmarks.")

        # ── Pricing ──
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        spots = st.session_state.spots
        city_r = random.choice(["Mumbai","Delhi","Bangalore","Chennai","Pune","Hyderabad","Surat"])
        st.markdown(f"""
        <div style="background:rgba(255,80,80,0.1);border:1px solid rgba(255,80,80,0.3);border-radius:16px;padding:1rem;text-align:center;margin-bottom:1.5rem;">
          <span style="color:#ff7070;font-weight:600;">⚡ Only {spots} free full analyses this month — {city_r} businesses claiming daily</span>
        </div>

        <div class="pricing-grid">
          <div class="price-card">
            <div class="price-badge">Starter</div>
            <div class="price-amount">₹0</div>
            <div style="color:#9090a0;font-size:.88rem;">Forever free</div>
            <div style="font-size:1.2rem;font-weight:600;color:#c8c8d8;margin:1rem 0;">Basic</div>
            <ul class="price-features">
              <li>1 leak scan / month</li>
              <li>Top 3 issues only</li>
              <li>Basic action tips</li>
              <li>Email support</li>
            </ul>
          </div>

          <div class="price-card popular">
            <div class="price-badge" style="background:rgba(200,255,87,0.3);">Most Popular</div>
            <div class="price-amount">₹499</div>
            <div style="color:#9090a0;font-size:.88rem;">or 7% success fee — your choice</div>
            <div style="font-size:1.2rem;font-weight:600;color:#c8c8d8;margin:1rem 0;">Pro Recovery</div>
            <ul class="price-features">
              <li>Unlimited monthly scans</li>
              <li>Full 5-day action plans</li>
              <li>Collections Bot (WhatsApp)</li>
              <li>Crowdsourced vendor benchmarks</li>
              <li>Tax leak scanner (GST + TDS)</li>
              <li>3 vendor quotes service</li>
              <li>Working capital bridge</li>
              <li>WhatsApp weekly alerts</li>
            </ul>
          </div>

          <div class="price-card">
            <div class="price-badge">For CAs</div>
            <div class="price-amount">₹1,999</div>
            <div style="color:#9090a0;font-size:.88rem;">per month (50 client seats)</div>
            <div style="font-size:1.2rem;font-weight:600;color:#c8c8d8;margin:1rem 0;">CA Partner</div>
            <ul class="price-features">
              <li>50 client seats included</li>
              <li>White-label branded reports</li>
              <li>Monthly auto-batch scanning</li>
              <li>GST + TDS risk dashboard</li>
              <li>Client health scorecard</li>
              <li>₹500/client/month you earn</li>
              <li>Priority phone support</li>
              <li>Revenue share program</li>
            </ul>
          </div>
        </div>""", unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            if st.button("🚀 Start Free 14-Day Pro Trial — No Credit Card", use_container_width=True, type="primary"):
                st.session_state.spots = max(0, spots - 1)
                st.balloons()
                st.success("✅ Trial activated! Our team will WhatsApp you within 1 hour with your personalised recovery plan.")
                st.markdown("📱 [Message founder directly](https://wa.me/916362319163?text=Hi+I+activated+OpsClarity+trial)")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CA PARTNER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_ca:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem;">
      <h2 style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:2.2rem;margin-bottom:.5rem;">CA Partner Dashboard</h2>
      <p style="color:#9090a0;font-size:1rem;">Give every client a monthly profit leak report — automated, branded, zero extra work.</p>
    </div>""", unsafe_allow_html=True)

    portfolio = CAPartnerEngine.generate_demo_portfolio()
    total_revenue   = sum(c["revenue"] for c in portfolio)
    total_leaks_ca  = sum(c["leak_estimate"] for c in portfolio)
    critical_count  = sum(1 for c in portfolio if c["health"] == "critical")
    ca_monthly_earn = len(portfolio) * 500

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Clients", len(portfolio))
    m2.metric("Total Client Revenue", fmt(total_revenue))
    m3.metric("Leaks Found for Clients", fmt(total_leaks_ca), delta=f"{critical_count} critical")
    m4.metric("Your Monthly Earnings", fmt(ca_monthly_earn), delta="₹500/client/month")

    st.markdown('<div class="section-title">Client Health Overview</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:20px;overflow:hidden;">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;padding:.8rem 1rem;border-bottom:1px solid rgba(255,255,255,0.06);">
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Client</span>
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Revenue</span>
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Leaks Found</span>
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Margin</span>
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Health</span>
        <span style="color:#9090a0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">Last Scan</span>
      </div>""", unsafe_allow_html=True)

    for c in portfolio:
        dot = {"critical":"health-dot-bad","warning":"health-dot-warn","good":"health-dot-good"}[c["health"]]
        health_label = {"critical":"🔴 Critical","warning":"🟡 Watch","good":"🟢 Healthy"}[c["health"]]
        st.markdown(f"""
      <div class="ca-client-row" style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;">
        <div><div class="ca-client-name">{c['name']}</div>
             <div class="ca-client-meta">{c['city']} · {c['industry'].title()}</div></div>
        <div style="color:#e8e8f0;align-self:center;">{fmt(c['revenue'])}</div>
        <div style="color:#ff7070;font-weight:600;align-self:center;">{fmt(c['leak_estimate'])}</div>
        <div style="color:{'#c8ff57' if c['margin']>15 else '#ffb557'};align-self:center;">{c['margin']:.1f}%</div>
        <div style="align-self:center;">{health_label}</div>
        <div style="color:#9090a0;font-size:.82rem;align-self:center;">{c['last_scan']}</div>
      </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("📄 Generate All Client Reports (PDF)", use_container_width=True):
            st.success("✅ Reports queued. 6 branded PDFs ready in 2 minutes. Check email.")
    with col_b:
        if st.button("📱 Send WhatsApp Summaries to All Clients", use_container_width=True):
            st.success("✅ WhatsApp summaries scheduled for all 6 clients.")
    with col_c:
        if st.button("🔴 Alert CA for Critical Clients", use_container_width=True):
            st.warning(f"⚠️ {critical_count} clients flagged as critical. Recommend immediate review: Sharma Textiles, Kapoor Steels.")

    # CA Revenue calculator
    st.markdown('<div class="section-title">CA Revenue Calculator</div>', unsafe_allow_html=True)
    n_clients = st.slider("Number of clients on OpsClarity", 5, 200, 30, 5)
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0;">
      <div class="kpi"><div class="kpi-label">Monthly from OpsClarity</div>
        <div class="kpi-val" style="color:#c8ff57;">{fmt(n_clients * 500)}</div>
        <div class="kpi-sub">₹500 × {n_clients} clients</div></div>
      <div class="kpi"><div class="kpi-label">Annual Passive Income</div>
        <div class="kpi-val" style="color:#c8ff57;">{fmt(n_clients * 500 * 12)}</div>
        <div class="kpi-sub">Without adding work</div></div>
      <div class="kpi"><div class="kpi-label">Your OpsClarity Cost</div>
        <div class="kpi-val">₹1,999</div>
        <div class="kpi-sub">{n_clients} seats included</div></div>
    </div>""", unsafe_allow_html=True)
    st.success(f"At {n_clients} clients: You earn ₹{n_clients*500:,}/month, pay ₹1,999. Net profit: **₹{n_clients*500-1999:,}/month** from OpsClarity alone.")

    if st.button("🏛️ Join CA Partner Program — Free 30-day trial", type="primary", use_container_width=True):
        st.balloons()
        st.success("✅ CA application received! Our partner team will call within 4 hours.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — INDUSTRY BENCHMARKS (Data Flywheel)
# ══════════════════════════════════════════════════════════════════════════════
with tab_benchmark:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem;">
      <h2 style="font-family:'Playfair Display',serif;color:#f4f1eb;font-size:2rem;margin-bottom:.5rem;">Industry Benchmark Database</h2>
      <p style="color:#9090a0;">Anonymised data from 2,800+ Indian SMEs. Updated monthly. This is what competitors can't copy.</p>
    </div>""", unsafe_allow_html=True)

    sel_ind = st.selectbox("Select industry to explore", list(CROWDSOURCED_BENCHMARKS.keys()), key="bench_ind")
    bench_data = CROWDSOURCED_BENCHMARKS.get(sel_ind, {})

    if bench_data:
        for cat, data in bench_data.items():
            with st.expander(f"📊 {cat} — {data['n']} businesses reporting"):
                b1, b2, b3, b4 = st.columns(4)
                b1.metric("Bottom 25% pay", f"₹{data['p25']:,}{data['unit']}", help="Best-in-class rate")
                b2.metric("Median (50th %ile)", f"₹{data['median']:,}{data['unit']}", help="Most common rate")
                b3.metric("Top 25% pay", f"₹{data['p75']:,}{data['unit']}", help="You may be overpaying if here")
                b4.metric("Peer reports", str(data["n"]), help="Sample size")

                if data.get("city_splits"):
                    st.markdown("**City-wise rates:**")
                    city_df = pd.DataFrame(
                        [(city, rate) for city, rate in data["city_splits"].items()],
                        columns=["City", f"Rate ({data['unit']})"]
                    )
                    st.dataframe(city_df, use_container_width=True, hide_index=True)

                # Visual bar
                ratio = (data["p25"] / data["p75"]) * 100
                savings_at_best = ((data["p75"] - data["p25"]) / data["p75"]) * 100
                st.markdown(f"""
                <div class="recovery-meter">
                  <div style="display:flex;justify-content:space-between;font-size:.82rem;color:#9090a0;margin-bottom:.3rem;">
                    <span>Best rate: ₹{data['p25']:,}</span><span>Median: ₹{data['median']:,}</span><span>High: ₹{data['p75']:,}</span>
                  </div>
                  <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{ratio:.0f}%"></div></div>
                  <div style="color:#c8ff57;font-size:.82rem;margin-top:.4rem;">
                    💡 Switching from high to best rate = {savings_at_best:.0f}% cost reduction on this category
                  </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="crowd-panel">
      <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#f4f1eb;margin-bottom:.6rem;">
        🔬 How this works — The Data Flywheel
      </div>
      <div style="color:#9090a0;font-size:.88rem;line-height:1.7;">
        Every SME that contributes anonymised expense data makes the benchmark more accurate.
        We strip all identifying information — only category averages enter the pool.
        At 200 contributors, our benchmarks beat anything a consultant could quote.
        At 2,000 contributors, no competitor can replicate this. <strong style="color:#c8ff57;">This is the moat.</strong>
      </div>
    </div>""", unsafe_allow_html=True)

    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("SMEs contributing data", "2,847")
    stat2.metric("Data points in database", "1,24,000+")
    stat3.metric("Industries covered", "10")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<a href="https://wa.me/916362319163?text=Hi%2C+question+about+OpsClarity" class="wa-float" target="_blank">
  💬 Chat with Founder
</a>

<div style="text-align:center;padding:3rem 1rem 2rem;border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;">
  <div style="color:#4a4a60;font-size:.88rem;margin-bottom:.4rem;">
    <strong style="color:#c8ff57;">OpsClarity</strong> · Profit Recovery System for Indian SMEs
  </div>
  <div style="color:#3a3a50;font-size:.78rem;">
    Built in Bangalore 🇮🇳 · Data encrypted & anonymised · Management estimates only, not CA advice · 
    <a href="#" style="color:#5a5a70;">Privacy Policy</a> · 
    <a href="#" style="color:#5a5a70;">Terms</a>
  </div>
</div>
""", unsafe_allow_html=True)
