import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import random

# Page config
st.set_page_config(
    page_title="OpsClarity",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
}

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Hero */
.hero {
    text-align: center;
    padding: 4rem 2rem 3rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c8ff57;
    border: 1px solid rgba(200,255,87,0.3);
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    background: rgba(200,255,87,0.05);
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    color: #f0ede8;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}
.hero-title span { color: #c8ff57; font-style: italic; }
.hero-sub {
    font-size: 1.1rem;
    color: #6b6b7a;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
    font-weight: 300;
}

/* Upload zone */
.upload-zone {
    background: rgba(255,255,255,0.02);
    border: 1.5px dashed rgba(200,255,87,0.25);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    transition: all 0.3s;
    margin: 1.5rem 0;
}
.upload-zone:hover {
    border-color: rgba(200,255,87,0.6);
    background: rgba(200,255,87,0.03);
}

/* Metric cards */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 2rem 0;
}
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.metric-card.green::before { background: linear-gradient(90deg, #c8ff57, transparent); }
.metric-card.red::before { background: linear-gradient(90deg, #ff5757, transparent); }
.metric-card.blue::before { background: linear-gradient(90deg, #57b8ff, transparent); }
.metric-card.amber::before { background: linear-gradient(90deg, #ffb557, transparent); }

.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a4a5a;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #f0ede8;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-delta {
    font-size: 12px;
    color: #c8ff57;
    font-weight: 500;
}
.metric-delta.neg { color: #ff5757; }

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #f0ede8;
    margin: 2.5rem 0 1rem;
    letter-spacing: -0.01em;
}

/* Insight cards */
.insight-card {
    background: rgba(200,255,87,0.05);
    border: 1px solid rgba(200,255,87,0.15);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 10px;
}
.insight-card .insight-icon {
    font-size: 18px;
    margin-bottom: 6px;
}
.insight-card .insight-text {
    font-size: 14px;
    color: #c8c8d4;
    line-height: 1.6;
}
.insight-card .insight-text strong { color: #c8ff57; font-weight: 600; }

/* Invoice table */
.invoice-row {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: #c8c8d4;
}
.invoice-row:hover { background: rgba(255,255,255,0.02); }
.overdue-badge {
    background: rgba(255,87,87,0.15);
    color: #ff5757;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
}
.paid-badge {
    background: rgba(200,255,87,0.1);
    color: #c8ff57;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
}

/* Paywall */
.paywall {
    background: linear-gradient(135deg, rgba(200,255,87,0.08), rgba(200,255,87,0.02));
    border: 1px solid rgba(200,255,87,0.2);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    margin: 2rem 0;
}
.paywall-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #f0ede8;
    margin-bottom: 0.75rem;
}
.paywall-sub {
    color: #6b6b7a;
    font-size: 14px;
    margin-bottom: 2rem;
    font-weight: 300;
}
.price-tag {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #c8ff57;
    line-height: 1;
}
.price-tag span { font-size: 1.2rem; color: #6b6b7a; font-family: 'DM Sans', sans-serif; font-weight: 300; }

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 2rem 0;
}

/* Streamlit overrides */
.stButton > button {
    background: #c8ff57 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #d8ff77 !important;
    transform: translateY(-1px) !important;
}

.stFileUploader {
    background: transparent !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(200,255,87,0.25) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f0ede8 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b6b7a !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(200,255,87,0.1) !important;
    color: #c8ff57 !important;
}

h1, h2, h3 { color: #f0ede8 !important; }

.stMarkdown p { color: #9494a8; }

.element-container { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── SAMPLE DATA GENERATOR ───────────────────────────────────────────────────

def generate_sample_data():
    """Generate realistic Indian SME sample data"""
    random.seed(42)
    np.random.seed(42)

    customers = ["Ravi Enterprises", "Meena Stores", "Krishna Traders", "Sunita Foods",
                 "Ramesh & Sons", "Lakshmi Textiles", "Suresh Auto Parts", "Priya Catering",
                 "Deepak Electronics", "Anita Pharmacy"]

    categories = {
        "Sales": ["Product Sales", "Service Income", "Commission"],
        "Expenses": ["Raw Materials", "Staff Salary", "Rent", "Electricity",
                     "Transport", "Marketing", "Misc Expenses", "GST Paid"]
    }

    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="ME")
    records = []

    for month in months:
        # Sales entries
        for _ in range(random.randint(15, 30)):
            records.append({
                "Date": month - timedelta(days=random.randint(0, 28)),
                "Type": "Sales",
                "Category": random.choice(categories["Sales"]),
                "Party": random.choice(customers),
                "Amount": round(random.uniform(5000, 85000), 0),
                "Status": random.choice(["Paid", "Paid", "Paid", "Overdue", "Pending"]),
                "Invoice_No": f"INV-{random.randint(1000,9999)}"
            })
        # Expense entries
        for cat in categories["Expenses"]:
            records.append({
                "Date": month - timedelta(days=random.randint(0, 28)),
                "Type": "Expense",
                "Category": cat,
                "Party": "Vendor",
                "Amount": round(random.uniform(2000, 45000), 0),
                "Status": "Paid",
                "Invoice_No": f"EXP-{random.randint(1000,9999)}"
            })

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


def parse_uploaded_file(file):
    """Parse user uploaded CSV/Excel"""
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Try to standardize common column names
        col_map = {}
        for col in df.columns:
            cl = col.lower().strip()
            if any(x in cl for x in ["date", "dt"]): col_map[col] = "Date"
            elif any(x in cl for x in ["amount", "amt", "value", "total"]): col_map[col] = "Amount"
            elif any(x in cl for x in ["type", "txn", "transaction"]): col_map[col] = "Type"
            elif any(x in cl for x in ["category", "cat", "head"]): col_map[col] = "Category"
            elif any(x in cl for x in ["party", "customer", "vendor", "name"]): col_map[col] = "Party"
            elif any(x in cl for x in ["status", "paid", "payment"]): col_map[col] = "Status"

        df = df.rename(columns=col_map)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        if "Amount" in df.columns:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        if "Month" not in df.columns and "Date" in df.columns:
            df["Month"] = df["Date"].dt.to_period("M").astype(str)
        if "Type" not in df.columns:
            df["Type"] = "Sales"
        if "Status" not in df.columns:
            df["Status"] = "Paid"
        return df, True
    except Exception as e:
        return None, False


def fmt_inr(val):
    """Format as Indian Rupees"""
    if val >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.1f}Cr"
    elif val >= 1_00_000:
        return f"₹{val/1_00_000:.1f}L"
    elif val >= 1000:
        return f"₹{val/1000:.1f}k"
    return f"₹{val:.0f}"


# ─── CHART HELPERS ───────────────────────────────────────────────────────────

def revenue_trend_chart(df):
    sales = df[df["Type"] == "Sales"].groupby("Month")["Amount"].sum()
    expenses = df[df["Type"] == "Expense"].groupby("Month")["Amount"].sum()
    merged = pd.DataFrame({"Revenue": sales, "Expenses": expenses}).fillna(0).sort_index()
    return merged

def expense_donut(df):
    exp = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
    exp = exp.sort_values("Amount", ascending=False).set_index("Category")
    return exp

def top_customers_chart(df):
    cust = df[df["Type"] == "Sales"].groupby("Party")["Amount"].sum().reset_index()
    cust = cust.sort_values("Amount", ascending=False).head(8).set_index("Party")
    return cust

def monthly_profit_chart(df):
    sales = df[df["Type"] == "Sales"].groupby("Month")["Amount"].sum()
    expenses = df[df["Type"] == "Expense"].groupby("Month")["Amount"].sum()
    profit = (sales - expenses).fillna(0).sort_index()
    return pd.DataFrame({"Profit": profit})


def generate_insights(df):
    insights = []
    sales = df[df["Type"] == "Sales"]
    expenses = df[df["Type"] == "Expense"]

    total_rev = sales["Amount"].sum()
    total_exp = expenses["Amount"].sum()
    profit = total_rev - total_exp
    margin = (profit / total_rev * 100) if total_rev > 0 else 0

    # Top expense
    top_exp = expenses.groupby("Category")["Amount"].sum().idxmax()
    top_exp_pct = expenses.groupby("Category")["Amount"].sum().max() / total_exp * 100

    # Overdue
    overdue = df[df["Status"] == "Overdue"]["Amount"].sum() if "Status" in df.columns else 0

    # Best customer
    best_cust = sales.groupby("Party")["Amount"].sum().idxmax() if len(sales) > 0 else "N/A"
    best_cust_rev = sales.groupby("Party")["Amount"].sum().max() if len(sales) > 0 else 0

    if margin > 20:
        insights.append(("◈", f"Your profit margin is <strong>{margin:.1f}%</strong> — healthy for an SME. Keep controlling {top_exp}."))
    elif margin > 0:
        insights.append(("▲", f"Margin is thin at <strong>{margin:.1f}%</strong>. Your biggest cost is <strong>{top_exp} ({top_exp_pct:.0f}% of expenses)</strong> — review this first."))
    else:
        insights.append(("⚠", f"You're running at a <strong>loss of {fmt_inr(abs(profit))}</strong> this period. Expenses exceed revenue by {abs(margin):.1f}%."))

    insights.append(("◆", f"<strong>{best_cust}</strong> is your most valuable customer at <strong>{fmt_inr(best_cust_rev)}</strong>. Protect this relationship."))

    if overdue > 0:
        insights.append(("◉", f"<strong>{fmt_inr(overdue)} stuck in overdue invoices</strong>. Follow up this week — that's cash sitting outside your business."))

    insights.append(("◐", f"<strong>{top_exp}</strong> is eating <strong>{top_exp_pct:.0f}%</strong> of your expenses. Benchmark against industry averages to see if you can reduce."))

    return insights


# ─── MAIN APP ────────────────────────────────────────────────────────────────

# Hero section
st.markdown("""
<div class="hero">
    <div class="hero-badge">◈ Fix My Itch — SME Intelligence</div>
    <h1 class="hero-title">Your business,<br><span>finally clear.</span></h1>
    <p class="hero-sub">Upload your Tally export or any Excel sheet. Get instant P&L, expense breakdown, overdue invoices, and plain-language insights — in 30 seconds.</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "df" not in st.session_state:
    st.session_state.df = None
if "used_free" not in st.session_state:
    st.session_state.used_free = False
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# Upload section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Drop your Tally CSV, Excel, or GST export here",
        type=["csv", "xlsx", "xls"],
        help="Supports Tally exports, Excel sheets, GST portal downloads"
    )

    st.markdown("<div style='text-align:center; margin: 0.5rem 0; color: #3a3a4a; font-size:13px;'>— or —</div>", unsafe_allow_html=True)

    if st.button("◈  Try with sample data  (Bengaluru restaurant)", use_container_width=True):
        st.session_state.df = generate_sample_data()
        st.session_state.used_free = True

if uploaded_file:
    df, ok = parse_uploaded_file(uploaded_file)
    if ok:
        st.session_state.df = df
        st.session_state.used_free = True
    else:
        st.error("Couldn't parse this file. Try a CSV with columns: Date, Amount, Type, Category, Party")

# ─── DASHBOARD ───────────────────────────────────────────────────────────────

if st.session_state.df is not None:
    df = st.session_state.df

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # KPI Cards
    total_rev = df[df["Type"] == "Sales"]["Amount"].sum()
    total_exp = df[df["Type"] == "Expense"]["Amount"].sum()
    profit = total_rev - total_exp
    margin = (profit / total_rev * 100) if total_rev > 0 else 0
    overdue_amt = df[df["Status"] == "Overdue"]["Amount"].sum() if "Status" in df.columns else 0

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">{fmt_inr(total_rev)}</div>
            <div class="metric-delta">↑ All time</div>
        </div>
        <div class="metric-card red">
            <div class="metric-label">Total Expenses</div>
            <div class="metric-value">{fmt_inr(total_exp)}</div>
            <div class="metric-delta neg">↓ Review top costs</div>
        </div>
        <div class="metric-card {'green' if profit >= 0 else 'red'}">
            <div class="metric-label">Net Profit</div>
            <div class="metric-value">{fmt_inr(abs(profit))}</div>
            <div class="metric-delta {'neg' if profit < 0 else ''}">{'▲' if profit >= 0 else '▼'} {abs(margin):.1f}% margin</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-label">Overdue Invoices</div>
            <div class="metric-value">{fmt_inr(overdue_amt)}</div>
            <div class="metric-delta neg">Collect now</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Insights
    st.markdown("<div class='section-header'>◈ Plain-language insights</div>", unsafe_allow_html=True)
    insights = generate_insights(df)
    for icon, text in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-icon">{icon}</div>
            <div class="insight-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Charts
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue & Expenses", "Expense Breakdown", "Top Customers", "Monthly Profit"])

    with tab1:
        st.markdown("<div class='section-header'>Revenue vs Expenses trend</div>", unsafe_allow_html=True)
        st.line_chart(revenue_trend_chart(df), use_container_width=True)

    with tab2:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("<div class='section-header'>Where money is going</div>", unsafe_allow_html=True)
            st.bar_chart(expense_donut(df), use_container_width=True)
        with col_b:
            st.markdown("<div class='section-header'>Expense breakdown</div>", unsafe_allow_html=True)
            exp_table = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
            exp_table = exp_table.sort_values("Amount", ascending=False)
            exp_table["Share"] = (exp_table["Amount"] / exp_table["Amount"].sum() * 100).round(1)
            exp_table["Amount_fmt"] = exp_table["Amount"].apply(fmt_inr)
            st.dataframe(
                exp_table[["Category", "Amount_fmt", "Share"]].rename(
                    columns={"Amount_fmt": "Amount", "Share": "% of total"}),
                hide_index=True, use_container_width=True
            )

    with tab3:
        st.markdown("<div class='section-header'>Top customers by revenue</div>", unsafe_allow_html=True)
        st.bar_chart(top_customers_chart(df), use_container_width=True)

    with tab4:
        st.markdown("<div class='section-header'>Monthly profit / loss</div>", unsafe_allow_html=True)
        st.bar_chart(monthly_profit_chart(df), use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Invoice tracker
    st.markdown("<div class='section-header'>◉ Invoice tracker</div>", unsafe_allow_html=True)

    if "Status" in df.columns:
        inv_df = df[df["Type"] == "Sales"][["Date", "Invoice_No", "Party", "Amount", "Status"]].copy() if "Invoice_No" in df.columns else df[df["Type"] == "Sales"][["Date", "Party", "Amount", "Status"]].copy()
        inv_df = inv_df.sort_values("Status", ascending=True).head(15)

        col_filter1, col_filter2 = st.columns([2, 4])
        with col_filter1:
            status_filter = st.selectbox("Filter by status", ["All", "Overdue", "Pending", "Paid"])

        if status_filter != "All":
            inv_df = inv_df[inv_df["Status"] == status_filter]

        st.dataframe(
            inv_df.assign(Amount=inv_df["Amount"].apply(fmt_inr)),
            hide_index=True,
            use_container_width=True,
            column_config={
                "Status": st.column_config.TextColumn("Status"),
                "Amount": st.column_config.TextColumn("Amount"),
            }
        )

    # Paywall
    if not st.session_state.unlocked:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="paywall">
            <div class="paywall-title">You've seen what clarity feels like.</div>
            <div class="paywall-sub">Unlock monthly auto-reports, WhatsApp summaries, GST readiness checks, and PDF export for your CA.</div>
            <div class="price-tag">₹2,999 <span>/ month</span></div>
            <div style="margin-top: 0.5rem; font-size: 12px; color: #3a3a4a;">Cancel anytime. No contracts.</div>
        </div>
        """, unsafe_allow_html=True)

        col_pay1, col_pay2, col_pay3 = st.columns([1, 1, 1])
        with col_pay2:
            if st.button("◈  Unlock full access — ₹2,999/mo", use_container_width=True):
                st.session_state.unlocked = True
                st.success("Payment integration coming soon! Add your Razorpay key in settings.")

else:
    # Empty state features list
    st.markdown("""
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 2rem 0;">
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 22px; margin-bottom: 10px;">◈</div>
            <div style="font-weight: 500; color: #f0ede8; margin-bottom: 6px; font-size: 14px;">Instant P&L</div>
            <div style="font-size: 13px; color: #4a4a5a; line-height: 1.6;">Upload any CSV. Get revenue, expenses, and net profit in 30 seconds.</div>
        </div>
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 22px; margin-bottom: 10px;">◉</div>
            <div style="font-weight: 500; color: #f0ede8; margin-bottom: 6px; font-size: 14px;">Overdue tracker</div>
            <div style="font-size: 13px; color: #4a4a5a; line-height: 1.6;">See exactly who owes you money and how much is stuck outside your business.</div>
        </div>
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 1.5rem;">
            <div style="font-size: 22px; margin-bottom: 10px;">◆</div>
            <div style="font-weight: 500; color: #f0ede8; margin-bottom: 6px; font-size: 14px;">Plain-language insights</div>
            <div style="font-size: 13px; color: #4a4a5a; line-height: 1.6;">No jargon. "Your raw material costs jumped 34% — here's why it matters."</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
