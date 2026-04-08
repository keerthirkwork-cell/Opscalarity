
""",
        unsafe_allow_html=True,
    )


def render_pricing_block() -> None:
    st.markdown(
        """
<div class="grid3" style="margin-top:1rem">
  <div class="card">
    <span class="tag">Starter</span>
    <div class="title" style="margin-top:.5rem">Rs 1,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For single operators and small firms managing up to 10 clients.</div>
    <div class="part-v" style="margin-top:.8rem">Includes health scoring, decision dashboard, action inbox, GST checks, cash forecast, and branded reports.</div>
  </div>
  <div class="card" style="border-color:rgba(201,168,76,.35);background:#0F1008">
    <span class="tag">Growth</span>
    <div class="title" style="margin-top:.5rem">Rs 4,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For CA firms managing active client portfolios every month.</div>
    <div class="part-v" style="margin-top:.8rem">Adds multi-client portfolio view, recurring advisory workflow, GST follow-up depth, and automation queue support.</div>
  </div>
  <div class="card">
    <span class="tag">Partner</span>
    <div class="title" style="margin-top:.5rem">Rs 9,999 / month</div>
    <div class="part-v" style="margin-top:.5rem">For firms standardizing advisory workflows across a larger team.</div>
    <div class="part-v" style="margin-top:.8rem">Adds white-label operating cadence, higher-volume portfolio usage, and premium onboarding support.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def next_review_date() -> str:
    return (datetime.now() + timedelta(days=30)).strftime("%d %b %Y")


st.markdown(
st.markdown(f'<div class="hero"><div class="hero-grid"><div><div class="eyebrow">Built in Bangalore for Indian CAs and SMEs</div><div class="h1">Your business has a dashboard.<br>Now get a <em>CFO.</em></div><div class="sub">OpsClarity turns Tally and finance exports into client health reports with money leaks, overdue cash, GST ITC risk, reconciliation gaps, cash runway, and exact weekly actions.</div></div>{card}</div></div>', unsafe_allow_html=True)
render_trust_strip()

tabs = st.tabs(["Client Brief", "Scan", "Decision Dashboard", "Advisory Brief", "Action Inbox", "Alerts", "AI Copilot", "GST", "Reconciliation", "Cash Forecast", "Clients", "Reports & Automations", "Tally Import"])
tabs = st.tabs(["Overview", "Scan", "Decision Dashboard", "Advisory Brief", "Action Inbox", "Alerts", "AI Copilot", "GST", "Reconciliation", "Cash Forecast", "Clients", "Reports & Automations", "Tally Import"])

with tabs[0]:
    st.markdown('<div class="section"><div class="section-head">Client Brief</div><div class="section-sub">Health score, top risk, recommended actions, GST follow-up, runway, and report export.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section"><div class="section-head">Overview</div><div class="section-sub">Your operating summary for this client: what matters now, what to do next, and what to review this month.</div>', unsafe_allow_html=True)
    if st.session_state.df is None:
        st.info("No client data loaded yet. Start with a Tally export or finance file to generate the first brief.")
        render_getting_started()
""",
            unsafe_allow_html=True,
        )
        st.subheader("Subscriptions")
        render_pricing_block()
        if st.session_state.role == "OpsClarity Admin" and st.button("Load Example Client Data", use_container_width=True):
            st.session_state.df = make_demo_data(client_name)
            save_client_snapshot(st.session_state.df, tenant_id, client_id, client_name, st.session_state.industry)
        brief = ca_client_brief(df, industry, client_name)
        leaks = find_leaks(df.to_json(date_format="iso"), industry)
        fc = cash_flow_forecast(df)
        alerts = alerts_engine(df, industry)
        ba = before_after_summary(tenant_id, client_id)
        top_leak = leaks[0] if leaks else None
        st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Health Score</div><div class="kpi-val">{brief["health_score"]}</div><div class="kpi-sub">{brief["status"]}</div></div><div class="kpi"><div class="kpi-label">Top Leak</div><div class="kpi-val">{fmt(top_leak["rupee_impact"] if top_leak else 0)}</div><div class="kpi-sub">{top_leak["category"] if top_leak else "No critical leak"}</div></div><div class="kpi"><div class="kpi-label">Runway</div><div class="kpi-val">{fc["runway"]:.1f}</div><div class="kpi-sub">months</div></div><div class="kpi"><div class="kpi-label">GST Score</div><div class="kpi-val">{brief["gst_score"]}</div><div class="kpi-sub">ITC + vendor risk</div></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card" style="margin-top:1rem"><span class="tag">Advisory Summary</span><div class="title">{brief["main_issue"]}</div><div class="part-v" style="margin-top:.6rem">{brief["why_it_matters"]}</div></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="grid3" style="margin-top:1rem">
  <div class="card">
    <span class="tag">This Month</span>
    <div class="title" style="margin-top:.5rem">Priority Operating Rhythm</div>
    <div class="part-v" style="margin-top:.6rem">1. Upload latest books or Tally export</div>
    <div class="part-v">2. Resolve the top 3 actions in Action Inbox</div>
    <div class="part-v">3. Review GST mismatches and overdue invoices</div>
    <div class="part-v">4. Export report and schedule the next review for {next_review_date()}</div>
  </div>
  <div class="card">
    <span class="tag">Recurring Value</span>
    <div class="title" style="margin-top:.5rem">{fmt(sum(float(l["rupee_impact"]) for l in leaks[:3]))}</div>
    <div class="part-v" style="margin-top:.6rem">Visible opportunity across the top 3 decision items for this client right now.</div>
  </div>
  <div class="card">
    <span class="tag">Alert Load</span>
    <div class="title" style="margin-top:.5rem">{len(alerts)}</div>
    <div class="part-v" style="margin-top:.6rem">Open risk signals across collections, costs, cash, and margin performance.</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("This Week")
            st.markdown("1. Review Advisory Brief")
            st.markdown("2. Download PDF")
            st.markdown("3. Queue follow-up actions")
        if ba["has_history"]:
            st.subheader("What Changed Since Last Review")
            st.markdown(f'<div class="grid4"><div class="kpi"><div class="kpi-label">Leak Change</div><div class="kpi-val">{fmt(ba["leak_delta"])}</div></div><div class="kpi"><div class="kpi-label">Health Change</div><div class="kpi-val">{ba["score_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">GST Change</div><div class="kpi-val">{ba["gst_delta"]:+.0f}</div></div><div class="kpi"><div class="kpi-label">Runway Change</div><div class="kpi-val">{ba["runway_delta"]:+.1f}</div></div></div>', unsafe_allow_html=True)
        pdf = generate_pdf_report(df, leaks, industry, st.session_state.ca_firm)
        if pdf:
            st.download_button("Download Branded Report", pdf, file_name=f"OpsClarity_Report_{datetime.now():%Y%m%d}.pdf", mime="application/pdf", use_container_width=True)
        st.subheader("Subscriptions")
        render_pricing_block()
        if RAZORPAY_PAYMENT_LINK:
            st.link_button("Manage Subscription", payment_cta_url("OpsClarity Subscription"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    else:
        leaks = find_leaks(st.session_state.df.to_json(date_format="iso"), st.session_state.industry)
        pdf = generate_pdf_report(st.session_state.df, leaks, st.session_state.industry, st.session_state.ca_firm)
        if pdf:
        if pdf:
            st.download_button("Download Branded PDF", pdf, file_name=f"OpsClarity_Report_{datetime.now():%Y%m%d}.pdf", mime="application/pdf")
        csv = io.StringIO()
        st.session_state.df.to_csv(csv, index=False)
        st.download_button("Export Cleaned CSV", csv.getvalue(), file_name=f"OpsClarity_Data_{datetime.now():%Y%m%d}.csv", mime="text/csv")
        csv = io.StringIO()
        st.session_state.df.to_csv(csv, index=False)
        st.download_button("Export Cleaned CSV", csv.getvalue(), file_name=f"OpsClarity_Data_{datetime.now():%Y%m%d}.csv", mime="text/csv")
        jobs = read_json(AUTOMATIONS_FILE).get(f"{tenant_id}:{client_id}", [])
        st.subheader("Automation Queue")
        if jobs:
            st.dataframe(pd.DataFrame(jobs), use_container_width=True)
        else:
            st.info("No automation tasks queued yet. Open the Execution tab and click Queue on an action.")
        if jobs:
            st.dataframe(pd.DataFrame(jobs), use_container_width=True)
        else:
            st.info("No automation tasks queued yet. Open the Execution tab and click Queue on an action.")
        st.markdown(
            f"""
<div class="card" style="margin-top:1rem">
  <span class="tag">Monthly Delivery</span>
  <div class="part-v" style="margin-top:.6rem">Use this area at month-end to export the client report, hand off the action list, and maintain a recurring advisory cadence for the next review on {next_review_date()}.</div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[12]:
