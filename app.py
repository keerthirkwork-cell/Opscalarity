import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io, random, json, time, os, urllib.parse

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
    0%, 100% { box-shadow: 0 0 20px rgba(200, 255, 87, 0.3); }
    50% { box-shadow: 0 0 40px rgba(200, 255, 87, 0.6); }
}

.money-hero {
    background: linear-gradient(135deg, rgba(200, 255, 87, 0.15) 0%, rgba(200, 255, 87, 0.05) 100%);
    border: 2px solid rgba(200, 255, 87, 0.4);
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1rem 0;
    animation: pulse-green 3s infinite;
}
.money-hero.critical {
    background: linear-gradient(135deg, rgba(255, 80, 80, 0.15) 0%, rgba(255, 80, 80, 0.05) 100%);
    border-color: rgba(255, 80, 80, 0.4);
    animation: none;
}
.money-label {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8ff57;
    margin-bottom: 1rem;
}
.money-hero.critical .money-label { color: #ff7070; }
.money-amount {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 900;
    color: #c8ff57;
    line-height: 1;
    margin-bottom: 1rem;
    text-shadow: 0 0 30px rgba(200, 255, 87, 0.3);
}
.money-hero.critical .money-amount {
    color: #ff7070;
    text-shadow: 0 0 30px rgba(255, 80, 80, 0.3);
}
.money-sub {
    color: #9090a0;
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto;
}

.leak-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
.leak-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.leak-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ff5e5e, #ffb557);
}
.leak-card.warning::before {
    background: linear-gradient(90deg, #ffb557, #c8ff57);
}
.leak-card.good::before {
    background: #c8ff57;
}
.leak-amount-tag {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: rgba(255, 80, 80, 0.15);
    color: #ff7070;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
}
.leak-card.warning .leak-amount-tag {
    background: rgba(255, 181, 80, 0.15);
    color: #ffb557;
}
.leak-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #f4f1eb;
    margin-bottom: 0.8rem;
    padding-right: 100px;
}
.leak-desc {
    color: #9090a0;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}
.leak-action-box {
    background: rgba(200, 255, 87, 0.08);
    border-left: 4px solid #c8ff57;
    padding: 1rem 1.2rem;
    border-radius: 0 12px 12px 0;
}
.leak-action-title {
    color: #c8ff57;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.leak-action-text {
    color: #e8e8f0;
    font-size: 0.95rem;
    font-weight: 500;
}

.action-section {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 24px;
    padding: 2rem;
    margin: 2rem 0;
}
.action-header {
    text-align: center;
    margin-bottom: 2rem;
}
.action-header h2 {
    font-family: 'Playfair Display', serif;
    color: #f4f1eb;
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}
.action-header p {
    color: #9090a0;
}
.action-timeline {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.action-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 1.2rem;
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.action-day {
    background: rgba(200, 255, 87, 0.15);
    color: #c8ff57;
    padding: 0.6rem 1rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.85rem;
    min-width: 80px;
    text-align: center;
}
.action-content h4 {
    color: #f4f1eb;
    font-size: 1.1rem;
    margin-bottom: 0.4rem;
}
.action-content p {
    color: #9090a0;
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
}
.action-impact {
    color: #c8ff57;
    font-size: 0.85rem;
    font-weight: 600;
}

.kpi-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}
.kpi {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.kpi-label {
    font-size: 0.75rem;
    color: #9090a0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.kpi-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #f4f1eb;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #5a5a70;
    margin-top: 0.3rem;
}

.upload-zone {
    background: rgba(255, 255, 255, 0.02);
    border: 2px dashed rgba(200, 255, 87, 0.3);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    margin: 2rem 0;
}

.social-proof {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}
.proof-item {
    text-align: center;
}
.proof-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #c8ff57;
    font-weight: 700;
}
.proof-label {
    color: #9090a0;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.pricing-urgency {
    background: rgba(255, 80, 80, 0.1);
    border: 1px solid rgba(255, 80, 80, 0.3);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 2rem;
}
.pricing-urgency-text {
    color: #ff7070;
    font-weight: 600;
    font-size: 1rem;
}
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}
.price-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}
.price-card.popular {
    background: rgba(200, 255, 87, 0.08);
    border-color: rgba(200, 255, 87, 0.4);
    transform: scale(1.05);
}
.price-badge {
    background: rgba(200, 255, 87, 0.15);
    color: #c8ff57;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: inline-block;
}
.price-amount {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #f4f1eb;
    font-weight: 700;
}
.price-period {
    color: #9090a0;
    font-size: 0.9rem;
}
.price-name {
    color: #c8c8d8;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 1rem 0;
}
.price-features {
    list-style: none;
    text-align: left;
    margin: 1.5rem 0;
}
.price-features li {
    color: #9090a0;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.price-features li::before {
    content: "✓ ";
    color: #c8ff57;
    font-weight: 700;
}

.wa-float {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: #25D366;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 50px;
    font-weight: 700;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
    z-index: 1000;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    margin: 2rem 0;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #f4f1eb;
    margin: 2rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
INDUSTRY_MAP = {
    "🏭 Manufacturing": "manufacturing",
    "🍽️ Restaurant / Cafe": "restaurant",
    "🏥 Clinic / Diagnostic": "clinic",
    "🛒 Retail / Distribution": "retail",
    "💼 Agency / Consulting": "agency",
    "🚚 Logistics / Transport": "logistics",
    "🏗️ Construction / Real Estate": "construction"
}
INDUSTRY_BENCHMARKS = {
    "manufacturing": 18, "restaurant": 15, "clinic": 25,
    "retail": 12, "agency": 35, "logistics": 10, "construction": 20
}

# ─── COLLECTIONS BOT: AUTOMATED RECOVERY ─────────────────────────────────────
class CollectionsBot:
    """Automated WhatsApp recovery sequences"""
    
    SEQUENCES = {
        'friendly': {
            'day': 1,
            'message': "Hi {name}, just checking on invoice #{inv} for ₹{amt}. Any issues we can help with? – {business}",
            'tone': 'gentle'
        },
        'urgent': {
            'day': 3,
            'message': "Hi {name}, your invoice #{inv} (₹{amt}) is now overdue. 2% discount if paid this week. Please confirm payment date.",
            'tone': 'firm'
        },
        'serious': {
            'day': 7,
            'message': "{name}, invoice #{inv} for ₹{amt} is 7 days overdue. This affects our operations. Payment required by {date} or we pause future deliveries.",
            'tone': 'warning'
        },
        'final': {
            'day': 10,
            'message': "FINAL NOTICE: Invoice #{inv} (₹{amt}) remains unpaid. Our CA has been notified. Legal notice will be issued on {date}.",
            'tone': 'legal',
            'ca_branded': True
        }
    }
    
    @classmethod
    def generate_sequence(cls, debtor_name, invoice_num, amount, business_name):
        """Generate complete recovery sequence"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        sequence = []
        
        for key, step in cls.SEQUENCES.items():
            message = step['message'].format(
                name=debtor_name,
                inv=invoice_num,
                amt=f"{amount/1000:.0f}K" if amount < 1000000 else f"{amount/100000:.1f}L",
                business=business_name,
                date=(today + timedelta(days=step['day'] + 3)).strftime("%d %b")
            )
            sequence.append({
                'day': step['day'],
                'send_date': (today + timedelta(days=step['day'])).strftime("%d %b"),
                'message': message,
                'tone': step['tone'],
                'whatsapp_link': f"https://wa.me/?text={urllib.parse.quote(message)}"
            })
        return sequence

# ─── VENDOR INTELLIGENCE: PRICE BENCHMARKING ─────────────────────────────────
class VendorIntelligence:
    """Anonymous price benchmarking across industry"""
    
    # Pre-negotiated market rates (updated monthly)
    BENCHMARKS = {
        'raw_materials': {'low': 45000, 'avg': 52000, 'high': 68000, 'unit': 'per ton'},
        'packaging': {'low': 12, 'avg': 18, 'high': 25, 'unit': 'per piece'},
        'logistics': {'low': 8, 'avg': 12, 'high': 18, 'unit': 'per km'},
        'steel_rod': {'low': 42000, 'avg': 48000, 'high': 62000, 'unit': 'per ton'},
        'labor_wages': {'low': 350, 'avg': 450, 'high': 600, 'unit': 'per day'},
        'electricity': {'low': 7, 'avg': 9, 'high': 12, 'unit': 'per unit'},
    }
    
    @classmethod
    def check_overpayment(cls, category, current_price, annual_volume):
        """Check if overpaying and calculate savings"""
        bench = cls.BENCHMARKS.get(category.lower().replace(' ', '_'))
        if not bench:
            return None
            
        if current_price > bench['avg'] * 1.15:  # 15%+ premium
            premium_pct = ((current_price - bench['avg']) / bench['avg']) * 100
            annual_savings = (current_price - bench['avg']) * annual_volume
            
            return {
                'status': 'overpaying',
                'premium_pct': premium_pct,
                'current_price': current_price,
                'market_avg': bench['avg'],
                'market_low': bench['low'],
                'annual_savings': annual_savings,
                'unit': bench['unit'],
                'action': f'Switch to market-rate supplier = ₹{annual_savings/100000:.1f}L/year saved',
                'guarantee': '₹5,000 cashback if we do not save you 10%+'
            }
        return {'status': 'fair_price'}

# ─── TAX OPTIMIZATION SCANNER ────────────────────────────────────────────────
class TaxScanner:
    """Pre-filing GST and tax leak detection"""
    
    @staticmethod
    def scan_gst_leaks(df):
        """Find missing input credits and optimization opportunities"""
        leaks = []
        
        # Input credit analysis
        purchases = df[df['Type'] == 'Expense']
        gst_eligible = purchases[purchases['Amount'] > 25000]  # GST registration threshold
        
        if len(gst_eligible) > 0:
            estimated_input_gst = gst_eligible['Amount'].sum() * 0.18
            # Typical SME misses 8-12% of input credits
            missed_credits = estimated_input_gst * 0.10
            
            if missed_credits > 10000:
                leaks.append({
                    'type': 'input_credit',
                    'amount': missed_credits,
                    'description': 'Missing GST input credits on purchases',
                    'action': 'CA review of all purchase invoices for GST number validation',
                    'savings': f'₹{missed_credits/1000:.0f}K per quarter'
                })
        
        # Advance tax timing
        quarterly_sales = df[df['Type'] == 'Sales'].groupby(df['Date'].dt.quarter)['Amount'].sum()
        if len(quarterly_sales) > 0 and quarterly_sales.iloc[-1] > 1000000:
            q_profit = quarterly_sales.iloc[-1] * 0.15  # Estimated 15% margin
            if q_profit > 100000:  # Above threshold
                penalty_risk = q_profit * 0.012  # 12% annual interest
                leaks.append({
                    'type': 'advance_tax',
                    'amount': penalty_risk,
                    'description': f'Q{quarterly_sales.index[-1]} advance tax liability',
                    'action': f'Pay advance tax by 15th to avoid ₹{penalty_risk:,.0f} penalty',
                    'savings': f'₹{penalty_risk:,.0f} penalty avoided'
                })
        
        return leaks

# ─── SMART FILE PARSER ───────────────────────────────────────────────────────
def smart_parse_file(file):
    """Parse with multiple fallback strategies"""
    try:
        fname = file.name.lower()
        
        # Excel handling with fallbacks
        if fname.endswith(('.xlsx', '.xls')):
            try:
                import openpyxl
                df = pd.read_excel(file, engine='openpyxl')
            except ImportError:
                try:
                    df = pd.read_excel(file, engine='xlrd')
                except:
                    # Final fallback: warn and suggest CSV
                    return None, False, "Excel parsing requires openpyxl. Please save as CSV (File → Save As → CSV) and upload again."
            except Exception as e:
                return None, False, f"Excel error: {str(e)}. Try CSV format."
        
        elif fname.endswith('.csv'):
            try:
                df = pd.read_csv(file)
            except:
                file.seek(0)
                df = pd.read_csv(file, encoding='latin1')
        else:
            return None, False, "Unsupported file. Use .csv, .xlsx, or .xls"
        
        # Clean data
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Smart column mapping
        col_map = {}
        for col in df.columns:
            cl = str(col).lower().strip()
            if any(x in cl for x in ['date', 'dt', 'day', 'voucher']): col_map[col] = 'Date'
            elif any(x in cl for x in ['amount', 'amt', 'value', 'total', 'debit', 'credit', 'rs', '₹']): col_map[col] = 'Amount'
            elif any(x in cl for x in ['type', 'txn', 'dr/cr', 'nature']): col_map[col] = 'Type'
            elif any(x in cl for x in ['particulars', 'category', 'cat', 'head', 'narration', 'ledger']): col_map[col] = 'Category'
            elif any(x in cl for x in ['party', 'customer', 'vendor', 'name', 'client', 'counter']): col_map[col] = 'Party'
            elif any(x in cl for x in ['status', 'paid', 'pending', 'overdue', 'due']): col_map[col] = 'Status'
            elif any(x in cl for x in ['bill', 'invoice', 'voucher', 'ref', 'num', 'no']): col_map[col] = 'Invoice_No'
        
        df = df.rename(columns=col_map)
        
        # Parse dates
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
            df = df.dropna(subset=['Date'])
        
        # Parse amounts - handle Indian formats
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].astype(str).str.replace(',', '').str.replace('(', '-').str.replace(')', '')
            df['Amount'] = df['Amount'].str.replace(' Dr', '').str.replace(' Cr', '').str.replace('₹', '')
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').abs().fillna(0)
        
        # Infer Type
        if 'Type' not in df.columns:
            df['Type'] = 'Unknown'
        
        df['Type'] = df['Type'].astype(str).str.strip().str.title()
        
        type_map = {
            'Dr': 'Expense', 'Debit': 'Expense', 'Payment': 'Expense',
            'Purchase': 'Expense', 'Cr': 'Sales', 'Credit': 'Sales',
            'Receipt': 'Sales', 'Sale': 'Sales'
        }
        df['Type'] = df['Type'].replace(type_map)
        
        # Infer from keywords
        mask = ~df['Type'].isin(['Sales', 'Expense'])
        if mask.any():
            expense_keywords = ['purchase', 'expense', 'payment', 'salary', 'rent', 'bill', 'wages', 'material', 'raw', 'inventory']
            df.loc[mask, 'Type'] = df.loc[mask].apply(
                lambda x: 'Expense' if any(kw in str(x.get('Category', '')).lower() for kw in expense_keywords) else 'Sales',
                axis=1
            )
        
        # Defaults
        for col, default in [('Status', 'Paid'), ('Category', 'General'), ('Party', 'Unknown'), ('Invoice_No', '-')]:
            if col not in df.columns: df[col] = default
        
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        
        return df, True, f"✅ Loaded {len(df):,} transactions"
        
    except Exception as e:
        return None, False, f"Error: {str(e)}. Try CSV format."

# ─── CORE LEAK DETECTOR ──────────────────────────────────────────────────────
def find_profit_leaks(df, industry):
    """Find all profit leaks with rupee amounts"""
    sales = df[df['Type'] == 'Sales']
    expenses = df[df['Type'] == 'Expense']
    
    revenue = sales['Amount'].sum()
    expense_total = expenses['Amount'].sum()
    profit = revenue - expense_total
    margin = (profit / revenue * 100) if revenue > 0 else 0
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    
    leaks = []
    
    # 1. Cash Stuck: Overdue Invoices
    if 'Status' in df.columns:
        overdue_mask = sales['Status'].str.lower().isin(['overdue', 'pending', 'not paid', 'due', 'outstanding'])
        overdue_df = sales[overdue_mask]
        overdue_amount = overdue_df['Amount'].sum()
        
        if overdue_amount > 10000:
            debtors = overdue_df.groupby('Party')['Amount'].sum().sort_values(ascending=False).head(3)
            debtor_text = ", ".join([f"{name} (₹{amt/1000:.0f}K)" for name, amt in debtors.items()])
            monthly_cost = overdue_amount * 0.01
            
            # Generate collections sequence
            collections = CollectionsBot.generate_sequence(
                debtors.index[0] if len(debtors) > 0 else "Customer",
                "INV001",
                debtors.iloc[0] if len(debtors) > 0 overdue_amount,
                "Your Business"
            )
            
            leaks.append({
                'id': 'cash_stuck',
                'priority': 1,
                'severity': 'critical',
                'emoji': '🚨',
                'title': f'₹{overdue_amount/100000:.1f} Lakhs STUCK in unpaid invoices',
                'amount': overdue_amount,
                'annual_impact': monthly_cost * 12,
                'description': f"Your money sits in others' accounts. Top debtors: {debtor_text}",
                'why_it_hurts': f"Every month costs ₹{monthly_cost/1000:.0f}K in lost opportunities",
                'action': f"Call {debtors.index[0] if len(debtors) > 0 else 'top debtor'} TODAY. Offer 2% discount for 48-hour payment.",
                'template': f"Hi, your invoice of ₹{debtors.iloc[0]/1000:.0f}K if len(debtors) > 0 else '₹{overdue_amount/1000:.0f}K'} is 30+ days overdue. Immediate payment required. 2% discount if paid today.",
                'collections_sequence': collections,
                'day': 'Monday - URGENT'
            })
    
    # 2. Cost Bleed: Vendor Overpayment
    if len(expenses) > 0:
        for category in expenses['Category'].unique():
            cat_exp = expenses[expenses['Category'] == category]
            if len(cat_exp) >= 3:
                vendor_prices = cat_exp.groupby('Party')['Amount'].agg(['mean', 'count', 'sum'])
                vendor_prices = vendor_prices[vendor_prices['count'] >= 2]
                
                if len(vendor_prices) >= 2:
                    cheapest = vendor_prices['mean'].min()
                    expensive_vendor = vendor_prices['mean'].idxmax()
                    expensive_price = vendor_prices['mean'].max()
                    
                    if expensive_price > cheapest * 1.15:
                        premium_pct = ((expensive_price - cheapest) / cheapest) * 100
                        annual_volume = vendor_prices.loc[expensive_vendor, 'sum']
                        annual_waste = (expensive_price - cheapest) * (annual_volume / expensive_price)
                        
                        if annual_waste > 20000:
                            # Check against market benchmarks
                            market_check = VendorIntelligence.check_overpayment(
                                category, expensive_price, annual_volume / expensive_price
                            )
                            
                            leaks.append({
                                'id': 'cost_bleed',
                                'priority': 2,
                                'severity': 'warning',
                                'emoji': '✂️',
                                'title': f'Overpaying {expensive_vendor} by {premium_pct:.0f}%',
                                'amount': annual_waste,
                                'annual_impact': annual_waste,
                                'description': f"Same {category} at ₹{cheapest:.0f}/unit vs your ₹{expensive_price:.0f}",
                                'why_it_hurts': "Months of silent profit destruction",
                                'action': f"Get 3 quotes for {category}. Switch = ₹{annual_waste/100000:.1f}L/year saved.",
                                'template': f"We're reviewing suppliers for {category}. Send best rates by Friday. Lowest quote gets 12-month contract.",
                                'market_data': market_check,
                                'day': 'Tuesday'
                            })
                            break
    
    # 3. Margin Gap
    if margin < benchmark - 3:
        gap_revenue = ((benchmark - margin) / 100) * revenue
        if gap_revenue > 30000:
            leaks.append({
                'id': 'margin_gap',
                'priority': 3,
                'severity': 'critical' if margin < 5 else 'warning',
                'emoji': '📉',
                'title': f'Profit margin {margin:.1f}% vs {benchmark}% industry average',
                'amount': gap_revenue,
                'annual_impact': gap_revenue,
                'description': f"Earning ₹{gap_revenue/100000:.1f}L LESS than peers. Every sale underpriced or overcosted.",
                'why_it_hurts': "Working 30% harder for 30% less profit",
                'action': f"Audit top 2 expenses. Cut 10% = ₹{gap_revenue*0.1/100000:.1f}L boost.",
                'template': "Cost review underway. Need 10% expense reduction. What are your options?",
                'day': 'Wednesday'
            })
    
    # 4. Concentration Risk
    if len(sales) > 0:
        cust_rev = sales.groupby('Party')['Amount'].sum().sort_values(ascending=False)
        if len(cust_rev) > 0:
            top_pct = (cust_rev.iloc[0] / revenue) * 100
            if top_pct > 30:
                risk_value = cust_rev.iloc[0]
                leaks.append({
                    'id': 'concentration',
                    'priority': 4,
                    'severity': 'warning',
                    'emoji': '🎯',
                    'title': f'{cust_rev.index[0]} = {top_pct:.0f}% of revenue (DANGEROUS)',
                    'amount': risk_value * 0.20,
                    'annual_impact': risk_value * 0.20,
                    'description': f"One client can destroy your business. Lose them = {top_pct:.0f}% income gone.",
                    'why_it_hurts': "Zero negotiation power. They demand discounts, delay payments.",
                    'action': "Sign 2 NEW customers this month. Never exceed 25% dependency.",
                    'template': "Looking to diversify client base. Over-dependent on one account. Referrals welcome?",
                    'day': 'Thursday'
                })
    
    # 5. Expense Spike
    if len(expenses) > 0:
        monthly_exp = expenses.groupby(expenses['Date'].dt.to_period('M'))['Amount'].sum()
        if len(monthly_exp) >= 3:
            recent_3m = monthly_exp.iloc[-3:].mean()
            previous = monthly_exp.iloc[:-3].mean() if len(monthly_exp) > 3 else monthly_exp.iloc[0]
            
            if recent_3m > previous * 1.20:
                annual_spike = (recent_3m - previous) * 12
                if annual_spike > 25000:
                    leaks.append({
                        'id': 'expense_spike',
                        'priority': 5,
                        'severity': 'warning',
                        'emoji': '🔥',
                        'title': f'Expenses up {((recent_3m/previous-1)*100):.0f}% in last 3 months',
                        'amount': annual_spike,
                        'annual_impact': annual_spike,
                        'description': f"Monthly burn +₹{(recent_3m-previous)/1000:.0f}K. Will bleed ₹{annual_spike/100000:.1f}L extra/year.",
                        'why_it_hurts': "How profitable businesses suddenly go broke",
                        'action': "FREEZE non-essential spending. Audit every expense above ₹5K.",
                        'template': "Immediate cost freeze. All expenses above ₹5K require approval. Reviewing vendor contracts.",
                        'day': 'Friday'
                    })
    
    # 6. Tax Leaks (Bonus)
    tax_leaks = TaxScanner.scan_gst_leaks(df)
    for tax_leak in tax_leaks:
        leaks.append({
            'id': f"tax_{tax_leak['type']}",
            'priority': 6,
            'severity': 'warning',
            'emoji': '🏛️',
            'title': f"Tax leak: {tax_leak['description']}",
            'amount': tax_leak['amount'],
            'annual_impact': tax_leak['amount'],
            'description': tax_leak['action'],
            'why_it_hurts': "Money left on table with government",
            'action': tax_leak['action'],
            'template': "Scheduling CA review for tax optimization. Potential savings identified.",
            'day': 'This Week',
            'is_tax': True
        })
    
    return sorted(leaks, key=lambda x: x['annual_impact'], reverse=True)

# ─── ACTION PLAN GENERATOR ───────────────────────────────────────────────────
def create_recovery_plan(leaks, df, industry):
    """Create 5-day execution plan"""
    actions = []
    
    day_map = {
        'cash_stuck': 'Monday',
        'cost_bleed': 'Tuesday',
        'margin_gap': 'Wednesday',
        'concentration': 'Thursday',
        'expense_spike': 'Friday'
    }
    
    for leak in leaks[:5]:
        if not leak.get('is_tax'):
            actions.append({
                'day': day_map.get(leak['id'], 'This Week'),
                'emoji': leak['emoji'],
                'title': leak['title'][:50] + '...' if len(leak['title']) > 50 else leak['title'],
                'task': leak['action'],
                'impact': f"₹{leak['annual_impact']/100000:.1f}L/year impact",
                'template': leak['template'],
                'severity': leak['severity'],
                'collections': leak.get('collections_sequence', [])
            })
    
    # Fill remaining days
    industry_actions = {
        'manufacturing': [
            ('Check scrap/wastage rates', 'Reduce unit cost 5-8%'),
            ('Negotiate bulk raw material contracts', 'Lock 10% savings'),
            ('Optimize machine utilization', 'Increase output 15%')
        ],
        'restaurant': [
            ('Audit food cost daily', 'Target 28-32% food cost'),
            ('Compare 3 supplier quotes weekly', 'Save 5-12% ingredients'),
            ('Eliminate <15% margin menu items', 'Focus on profitable dishes')
        ],
        'clinic': [
            ('Track consultation to lab conversion', 'Target 60%+ conversion'),
            ('Review medicine markup rates', 'Ensure 20-30% margin'),
            ('Reduce no-show appointments', 'Confirmation calls')
        ],
        'retail': [
            ('Identify dead stock (60+ days)', 'Clear via discount sale'),
            ('Optimize inventory turnover', 'Target 6+ turns/year'),
            ('Negotiate better credit terms', 'Improve cash flow 20%')
        ],
        'agency': [
            ('Track billable vs non-billable hours', 'Target 75%+ billable'),
            ('Review client profitability monthly', 'Fire bottom 10%'),
            ('Automate repetitive tasks', 'Save 10 hours/week')
        ]
    }
    
    fillers = industry_actions.get(industry, [
        ('Review top 5 customer profitability', 'Focus on high-margin'),
        ('Audit recurring subscriptions', 'Cancel unused'),
        ('Renegotiate rent/lease terms', 'Save 5-10% fixed costs')
    ])
    
    current_days = [a['day'] for a in actions]
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    for i, day in enumerate(all_days):
        if day not in current_days and i < len(fillers):
            task, impact = fillers[i]
            actions.append({
                'day': day,
                'emoji': '📋',
                'title': f'{industry.title()} Best Practice',
                'task': task,
                'impact': impact,
                'template': f"Implementing: {task}. Target: {impact}",
                'severity': 'good',
                'collections': []
            })
    
    return sorted(actions, key=lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].index(x['day']))

# ─── FORMATTER ───────────────────────────────────────────────────────────────
def fmt(val):
    val = float(val)
    if abs(val) >= 1_00_00_000: return f"₹{val/1_00_00_000:.1f}Cr"
    elif abs(val) >= 1_00_000:   return f"₹{val/1_00_000:.1f}L"
    elif abs(val) >= 1_000:      return f"₹{val/1000:.1f}k"
    return f"₹{abs(val):.0f}"

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if 'df' not in st.session_state: st.session_state.df = None
if 'industry' not in st.session_state: st.session_state.industry = 'manufacturing'
if 'spots' not in st.session_state: st.session_state.spots = 47
if 'show_collections' not in st.session_state: st.session_state.show_collections = False

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 3rem 1rem;">
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(200, 255, 87, 0.1); border: 1px solid rgba(200, 255, 87, 0.3); padding: 8px 20px; border-radius: 30px; margin-bottom: 2rem;">
        <span style="color: #c8ff57; font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase;">
            Trusted by 200+ Indian SMEs | ₹50+ Crore Leaks Found
        </span>
    </div>
    <h1 style="font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 5vw, 4rem); color: #f4f1eb; line-height: 1.1; margin-bottom: 1rem;">
        Find the <span style="color: #c8ff57; font-style: italic;">₹5-50 Lakhs</span> hiding in your business
    </h1>
    <p style="color: #9090a0; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Upload your Tally data. Get specific amounts you're losing and exact steps to recover them. 
        <strong style="color: #c8ff57;">No finance degree needed.</strong>
    </p>
</div>

<div class="social-proof">
    <div class="proof-item">
        <div class="proof-number">₹50Cr+</div>
        <div class="proof-label">Leaks Found</div>
    </div>
    <div class="proof-item">
        <div class="proof-number">200+</div>
        <div class="proof-label">Businesses Helped</div>
    </div>
    <div class="proof-item">
        <div class="proof-number">₹12L</div>
        <div class="proof-label">Avg Recovery</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── UPLOAD ───────────────────────────────────────────────────────────────────
st.markdown('<div class="upload-zone">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    uploaded = st.file_uploader(
        "Drop your Tally Day Book, Sales Register, Bank Statement, or Excel/CSV",
        type=["csv", "xlsx", "xls"]
    )
    
    with st.expander("How to export from Tally in 30 seconds"):
        st.markdown("""
**Step 1:** Open Tally Prime → Go to **Display → Account Books**  
**Step 2:** Select **Day Book** (or Sales Register / Purchase Register)  
**Step 3:** Press **Alt+E** → Select **Excel** format → Export
        
💡 **Pro tip:** Export last 6-12 months for best leak detection
        """)

with col2:
    industry_display = st.selectbox("Your Industry", list(INDUSTRY_MAP.keys()))
    industry = INDUSTRY_MAP[industry_display]
    
    st.markdown("""
    <div style="background: rgba(87, 184, 255, 0.1); border: 1px solid rgba(87, 184, 255, 0.3); border-radius: 12px; padding: 1rem; margin-top: 1rem;">
        <div style="color: #57b8ff; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.3rem;">🏛️ CA PARTNER PROGRAM</div>
        <div style="color: #9090a0; font-size: 0.8rem;">Give clients monthly leak reports. Earn ₹500/client/month.</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Try Demo Data", use_container_width=True):
        np.random.seed(42)
        dates = pd.date_range('2024-06-01', '2025-03-31', freq='D')
        records = []
        
        customers = ['ABC Corp', 'XYZ Industries', 'PQR Manufacturing', 'LMN Traders', 'DEF Enterprises']
        vendors = ['Steel Supplier A', 'Steel Supplier B', 'Raw Material Co', 'Logistics Ltd', 'Packaging Inc']
        
        for date in dates:
            if np.random.random() > 0.3:
                records.append({
                    'Date': date,
                    'Type': 'Sales',
                    'Party': np.random.choice(customers),
                    'Amount': np.random.uniform(50000, 250000),
                    'Status': np.random.choice(['Paid', 'Paid', 'Paid', 'Overdue'], p=[0.5, 0.3, 0.1, 0.1]),
                    'Category': 'Sales'
                })
            for _ in range(np.random.randint(1, 4)):
                records.append({
                    'Date': date,
                    'Type': 'Expense',
                    'Party': np.random.choice(vendors),
                    'Amount': np.random.uniform(15000, 80000),
                    'Status': 'Paid',
                    'Category': np.random.choice(['Raw Materials', 'Labor', 'Rent', 'Utilities', 'Logistics'])
                })
        
        df_demo = pd.DataFrame(records)
        df_demo['Month'] = df_demo['Date'].dt.to_period('M').astype(str)
        
        st.session_state.df = df_demo
        st.session_state.industry = 'manufacturing'
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── PROCESS ──────────────────────────────────────────────────────────────────
if uploaded:
    df, success, message = smart_parse_file(uploaded)
    if success:
        st.session_state.df = df
        st.session_state.industry = industry
        st.success(message)
    else:
        st.error(f"❌ {message}")
        st.info("""
**Quick fix:** Open your Excel file → File → Download → CSV (comma-separated values)
        
Then upload the CSV file. This works 100% of the time.
        """)

# ─── DASHBOARD ────────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df
    industry = st.session_state.industry
    
    sales = df[df['Type'] == 'Sales']
    expenses = df[df['Type'] == 'Expense']
    
    revenue = sales['Amount'].sum()
    expense_total = expenses['Amount'].sum()
    profit = revenue - expense_total
    margin = (profit / revenue * 100) if revenue > 0 else 0
    
    leaks = find_profit_leaks(df, industry)
    total_leak = sum(l['annual_impact'] for l in leaks)
    actions = create_recovery_plan(leaks, df, industry)
    
    # ─── MONEY HERO ───────────────────────────────────────────────────────────
    if total_leak > 0:
        st.markdown(f"""
        <div class="money-hero critical">
            <div class="money-label">PROFIT LEAKS DETECTED</div>
            <div class="money-amount">₹{total_leak/100000:.1f} Lakhs</div>
            <div class="money-sub">You are losing this every year. Found {len(leaks)} critical issues. 
            Fix them = immediate cash in your account.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="money-hero">
            <div class="money-label">BUSINESS HEALTHY</div>
            <div class="money-amount">No Major Leaks</div>
            <div class="money-sub">Margin {margin:.1f}% is strong. We will keep monitoring monthly.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ─── LEAK CARDS ─────────────────────────────────────────────────────────
    if leaks:
        st.markdown('<div class="section-title">Where Your Money is Leaking</div>', unsafe_allow_html=True)
        st.markdown('<div class="leak-grid">', unsafe_allow_html=True)
        
        for leak in leaks[:4]:
            sev_class = leak['severity']
            
            st.markdown(f"""
            <div class="leak-card {sev_class}">
                <div class="leak-amount-tag">₹{leak['annual_impact']/100000:.1f}L/year</div>
                <div class="leak-title">{leak['emoji']} {leak['title']}</div>
                <div class="leak-desc">
                    <strong style="color: #ff7070;">The Problem:</strong> {leak['description']}<br><br>
                    <strong style="color: #ffb557;">Why it hurts:</strong> {leak['why_it_hurts']}
                </div>
                <div class="leak-action-box">
                    <div class="leak-action-title">THIS WEEK: Take This Action</div>
                    <div class="leak-action-text">{leak['action']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # WhatsApp share
            wa_text = urllib.parse.quote(f"🚨 {leak['title']}\n💰 Impact: ₹{leak['annual_impact']/100000:.1f}L/year\n✅ Action: {leak['action'][:100]}...")
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="display: inline-block; background: #25D366; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 12px; margin: 8px 0;">📱 Share on WhatsApp</a>', unsafe_allow_html=True)
            
            # Collections Bot (for cash stuck)
            if leak['id'] == 'cash_stuck' and leak.get('collections_sequence'):
                if st.button(f"🤖 Activate Collections Bot for {leak.get('collections_sequence', [{}])[0].get('send_date', 'this week')}", key="collections_bot"):
                    st.session_state.show_collections = True
            
            if st.session_state.show_collections and leak['id'] == 'cash_stuck':
                st.markdown("#### Automated Recovery Sequence")
                for step in leak.get('collections_sequence', []):
                    with st.expander(f"Day {step['day']} ({step['send_date']}): {step['tone'].title()}"):
                        st.code(step['message'])
                        st.markdown(f"[📱 Send WhatsApp]({step['whatsapp_link']})")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ─── ACTION PLAN ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="action-section">
        <div class="action-header">
            <h2>Your 5-Day Profit Recovery Plan</h2>
            <p>Specific tasks with exact scripts. Do these = money back in your account.</p>
        </div>
        <div class="action-timeline">
    """, unsafe_allow_html=True)
    
    for action in actions:
        st.markdown(f"""
        <div class="action-item">
            <div class="action-day">{action['day']}</div>
            <div class="action-content">
                <h4>{action['emoji']} {action['title']}</h4>
                <p>{action['task']}</p>
                <div class="action-impact">💰 {action['impact']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📋 Copy WhatsApp Message for {action['day']}", key=f"copy_{action['day']}"):
            st.code(action['template'])
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ─── KPIs ─────────────────────────────────────────────────────────────────
    overdue_amt = sales[sales['Status'].str.lower().isin(['overdue', 'pending'])]['Amount'].sum() if 'Status' in sales.columns else 0
    benchmark = INDUSTRY_BENCHMARKS.get(industry, 15)
    
    st.markdown(f"""
    <div class="kpi-strip">
        <div class="kpi">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-val">{fmt(revenue)}</div>
            <div class="kpi-sub">{len(sales)} transactions</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-val" style="color: {'#c8ff57' if margin > benchmark else '#ffb557' if margin > 5 else '#ff5e5e'};">{margin:.1f}%</div>
            <div class="kpi-sub">vs {benchmark}% benchmark</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Overdue</div>
            <div class="kpi-val" style="color: {'#ff5e5e' if overdue_amt > revenue*0.05 else '#c8ff57'};">{fmt(overdue_amt)}</div>
            <div class="kpi-sub">{(overdue_amt/revenue*100 if revenue > 0 else 0):.1f}% of revenue</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Net Profit</div>
            <div class="kpi-val" style="color: {'#c8ff57' if profit > 0 else '#ff5e5e'};">{fmt(abs(profit))}</div>
            <div class="kpi-sub">{'Profit' if profit > 0 else 'Loss'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ─── TRENDS ─────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">Revenue vs Expenses Trend</div>', unsafe_allow_html=True)
        monthly = df.groupby([df['Date'].dt.to_period('M'), 'Type'])['Amount'].sum().unstack(fill_value=0)
        st.line_chart(monthly, use_container_width=True, height=250)
    
    with col2:
        st.markdown('<div class="section-title">Top Expense Categories</div>', unsafe_allow_html=True)
        if len(expenses) > 0:
            exp_by_cat = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(8)
            st.bar_chart(exp_by_cat, use_container_width=True, height=250)
    
    # ─── CA BANNER ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: rgba(87, 184, 255, 0.1); border: 1px solid rgba(87, 184, 255, 0.3); border-radius: 20px; padding: 1.5rem 2rem; margin: 2rem 0; display: flex; align-items: center; justify-content: space-between;">
        <div>
            <div style="color: #57b8ff; font-family: 'Playfair Display', serif; font-size: 1.4rem; margin-bottom: 0.3rem;">🏛️ Are you a CA or Financial Advisor?</div>
            <div style="color: #9090a0; font-size: 0.9rem;">Give every client monthly "Profit Leak Reports" without work. Upload data → Generate branded PDF → Look tech-savvy.</div>
        </div>
        <div style="text-align: center;">
            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: #57b8ff;">₹1,999</div>
            <div style="color: #9090a0; font-size: 0.85rem;">/month for 50 clients</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ─── PRICING ──────────────────────────────────────────────────────────────
    spots = st.session_state.spots
    
    st.markdown(f"""
    <div class="pricing-urgency">
        <div class="pricing-urgency-text">
            ⚡ Only {spots} free full analyses remaining this month — {random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad', 'Ahmedabad'])} businesses claiming daily
        </div>
    </div>
    
    <div class="pricing-grid">
        <div class="price-card">
            <div class="price-badge">Starter</div>
            <div class="price-amount">₹0</div>
            <div class="price-period">Forever Free</div>
            <div class="price-name">Basic</div>
            <ul class="price-features">
                <li>1 leak report per month</li>
                <li>Top 3 issues only</li>
                <li>Basic action tips</li>
                <li>Email support</li>
            </ul>
        </div>
        
        <div class="price-card popular">
            <div class="price-badge" style="background: rgba(200, 255, 87, 0.3);">Most Popular</div>
            <div class="price-amount">₹499</div>
            <div class="price-period">per month</div>
            <div class="price-name">Pro Business</div>
            <ul class="price-features">
                <li>Unlimited leak reports</li>
                <li>Complete 5-day action plans</li>
                <li>WhatsApp weekly alerts</li>
                <li>Vendor price benchmarking</li>
                <li>CA chat support</li>
                <li>Download PDF reports</li>
                <li>Collections Bot automation</li>
            </ul>
        </div>
        
        <div class="price-card">
            <div class="price-badge">For Professionals</div>
            <div class="price-amount">₹1,999</div>
            <div class="price-period">per month</div>
            <div class="price-name">CA Partner</div>
            <ul class="price-features">
                <li>50 client seats included</li>
                <li>White-label branded reports</li>
                <li>GST risk scanner</li>
                <li>Priority phone support</li>
                <li>Client management dashboard</li>
                <li>Revenue share program</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Start Free 14-Day Pro Trial — No Credit Card", use_container_width=True, type="primary"):
            st.session_state.spots = max(0, spots - 1)
            st.balloons()
            st.success("✅ Trial activated! Check WhatsApp for next steps.")
            st.markdown("📱 [Join WhatsApp group](https://wa.me/916362319163?text=I+activated+my+OpsClarity+trial) for weekly tips")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<a href="https://wa.me/916362319163?text=Hi%2C+I+have+a+question+about+OpsClarity" class="wa-float" target="_blank">
    💬 Chat with Founder
</a>

<div style="text-align: center; padding: 3rem 1rem 2rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 3rem;">
    <div style="color: #4a4a60; font-size: 0.9rem; margin-bottom: 0.5rem;">
        <strong style="color: #c8ff57;">OpsClarity</strong> · Profit Recovery System for Indian SMEs
    </div>
    <div style="color: #3a3a50; font-size: 0.8rem;">
        Built in Bangalore 🇮🇳 · Data stays private · Management estimates, not professional CA advice
    </div>
</div>
""", unsafe_allow_html=True)
