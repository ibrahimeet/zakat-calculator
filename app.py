import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Zakat Calculator",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

  /* Force all text visible */
  html, body, [class*="css"], p, span, div, label {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
  }

  .main, .block-container, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
  }

  /* Hero */
  .hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin-bottom: 24px;
  }
  .hero-title {
    font-family: 'Amiri', serif !important;
    font-size: 2.8em;
    color: #f0d060 !important;
    margin: 0;
  }
  .hero-subtitle { color: #94a3b8 !important; font-size: 1.05em; margin-top: 8px; }

  /* Cards */
  .metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px 20px;
    margin: 6px 0;
  }
  .metric-label { color: #94a3b8 !important; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1.5px; }
  .metric-value { color: #f0d060 !important; font-size: 1.7em; font-weight: 600; margin-top: 4px; }
  .metric-value.blue  { color: #38bdf8 !important; }
  .metric-value.green { color: #22c55e !important; }
  .metric-value.red   { color: #ef4444 !important; }

  /* Section headers */
  .section-header {
    background: linear-gradient(90deg, #1e293b, transparent);
    border-left: 4px solid #f0d060;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    color: #f0d060 !important;
    font-weight: 600;
    font-size: 1.05em;
    margin: 20px 0 12px 0;
  }

  /* Price rows */
  .price-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 14px;
    border-bottom: 1px solid #1e293b;
    border-radius: 6px;
    align-items: center;
  }
  .price-row:hover { background: #1e293b; }
  .price-label { color: #e2e8f0 !important; font-size: 1em; }
  .price-val   { color: #f0d060 !important; font-weight: 600; font-size: 1em; }

  /* Info boxes */
  .info-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
    margin: 10px 0;
    font-size: 0.9em;
    line-height: 1.7;
    color: #cbd5e1 !important;
  }
  .info-box strong { color: #f0d060 !important; }
  .info-box p, .info-box span { color: #cbd5e1 !important; }

  /* Zakat result */
  .zakat-result {
    background: linear-gradient(135deg, #f0d06010, #f0d06025);
    border: 2px solid #f0d060;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    margin: 20px 0;
  }
  .zakat-amount {
    font-family: 'Amiri', serif !important;
    font-size: 3.2em;
    color: #f0d060 !important;
    font-weight: 700;
  }

  /* Badges */
  .badge-yes {
    background: #22c55e20; border: 1.5px solid #22c55e;
    color: #22c55e !important; padding: 8px 20px;
    border-radius: 30px; font-weight: 600; display: inline-block;
  }
  .badge-no {
    background: #ef444420; border: 1.5px solid #ef4444;
    color: #ef4444 !important; padding: 8px 20px;
    border-radius: 30px; font-weight: 600; display: inline-block;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b;
  }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] .stSelectbox label { color: #e2e8f0 !important; }

  /* Inputs */
  .stNumberInput label { color: #cbd5e1 !important; }
  .stNumberInput > div > div > input {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border-color: #334155 !important;
  }
  .stSelectbox label { color: #cbd5e1 !important; }
  .stRadio label { color: #cbd5e1 !important; }
  .stTextInput label { color: #cbd5e1 !important; }
  input, select, textarea { color: #e2e8f0 !important; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: #1e293b !important;
    border-radius: 10px; gap: 4px; padding: 4px;
  }
  .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 8px; }
  .stTabs [aria-selected="true"] {
    background: #f0d06025 !important;
    color: #f0d060 !important;
  }

  /* Captions & small text */
  .stCaption, [data-testid="stCaptionContainer"] { color: #64748b !important; }
  small { color: #94a3b8 !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { color: #e2e8f0 !important; }

  /* Divider */
  hr { border-color: #334155 !important; }

  /* Headings */
  h1, h2, h3, h4 { color: #f0d060 !important; }
  
  /* Expander */
  .streamlit-expanderHeader { color: #e2e8f0 !important; }
  .streamlit-expanderContent { color: #cbd5e1 !important; background: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LIVE PRICE FETCHER
# ─────────────────────────────────────────
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_prices(api_key=""):
    if api_key and api_key != "":
        try:
            headers = {"x-access-token": api_key}
            g = requests.get("https://www.goldapi.io/api/XAU/INR", headers=headers, timeout=6).json()
            s = requests.get("https://www.goldapi.io/api/XAG/INR", headers=headers, timeout=6).json()
            g24 = g["price"] / 31.1035
            sil = s["price"] / 31.1035
            return {
                "source": "🟢 Live (goldapi.io)",
                "gold_24k": round(g24, 2),
                "gold_22k": round(g24 * 22/24, 2),
                "gold_18k": round(g24 * 18/24, 2),
                "gold_14k": round(g24 * 14/24, 2),
                "silver":   round(sil, 2),
                "fetched": datetime.now().strftime("%d %b %Y %I:%M %p")
            }
        except:
            pass
    # Fallback approximate prices
    return {
        "source": "🔴 Approximate (add API key for live)",
        "gold_24k": 7800, "gold_22k": 7150,
        "gold_18k": 5850, "gold_14k": 4550,
        "silver": 95,
        "fetched": "Manual"
    }


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0'>
      <div style='font-size:2.5em'>🕌</div>
      <div style='color:#f0d060;font-family:Amiri,serif;font-size:1.4em;font-weight:700'>Zakat Calculator</div>
      <div style='color:#64748b;font-size:0.8em'>Islamic Wealth Purification</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**🔑 Live Price API Key**")
    import os
    api_key = st.secrets.get("GOLD_API_KEY", "")
    st.caption("💡 [Get free key at goldapi.io](https://www.goldapi.io)")

    st.divider()

    st.markdown("**⚙️ Settings**")
    nisab_standard = st.radio(
        "Nisab Standard",
        ["Silver (Recommended)", "Gold"],
        help="Silver Nisab is lower and more inclusive. Most contemporary scholars recommend it."
    )

    madhab = st.selectbox(
        "School of Thought",
        ["Hanafi", "Shafi'i", "Maliki", "Hanbali"],
        help="Affects how gold jewelry and stocks are treated"
    )

    st.divider()
    st.markdown("""
    <div class='info-box'>
      <strong style='color:#f0d060'>📖 Key Facts</strong><br><br>
      • Zakat rate: <strong>2.5%</strong><br>
      • Gold Nisab: <strong>87.48g</strong><br>
      • Silver Nisab: <strong>612.36g</strong><br>
      • Holding period: <strong>1 Lunar Year</strong>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# FETCH PRICES
# ─────────────────────────────────────────
prices = fetch_prices(api_key)
NISAB_GOLD_G   = 87.48
NISAB_SILVER_G = 612.36
nisab_gold_val   = prices["gold_24k"] * NISAB_GOLD_G
nisab_silver_val = prices["silver"]   * NISAB_SILVER_G


# ─────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────
st.markdown(f"""
<div class='hero-banner'>
  <div class='hero-title'>🕌 Zakat Calculator</div>
  <div class='hero-subtitle'>Calculate your annual Zakat with live gold & silver prices in Indian Rupees</div>
  <div style='margin-top:12px;color:#475569;font-size:0.8em'>
    Prices: {prices['source']} &nbsp;|&nbsp; {prices['fetched']}
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Guide", "💰 Metal Prices", "📝 Assets & Liabilities", "📊 Results", "❓ FAQ"
])


# ══════════════════════════════════════════
# TAB 1 — GUIDE
# ══════════════════════════════════════════
with tab1:
    st.markdown("### 📖 How to Use This Calculator")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='info-box'>
          <strong style='color:#f0d060'>What is Zakat?</strong><br><br>
          Zakat is one of the Five Pillars of Islam — an obligatory annual charity of <strong>2.5%</strong>
          on wealth that exceeds the <strong>Nisab threshold</strong> and has been held for
          one complete <strong>lunar year (Hawl)</strong>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box' style='margin-top:12px'>
          <strong style='color:#f0d060'>📐 Calculation Steps</strong><br><br>
          1️⃣ &nbsp;Add all <strong>zakatable assets</strong><br>
          2️⃣ &nbsp;Subtract <strong>short-term debts</strong><br>
          3️⃣ &nbsp;Check if net wealth ≥ <strong>Nisab</strong><br>
          4️⃣ &nbsp;Pay <strong>2.5%</strong> of net zakatable wealth
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-box'>
          <strong style='color:#22c55e'>✅ INCLUDE (Zakatable)</strong><br><br>
          • Cash at home & bank savings<br>
          • Gold & silver holdings<br>
          • Stocks & mutual funds<br>
          • Business inventory (for sale)<br>
          • Receivables (money owed to you)<br>
          • Rental income savings<br>
          • Cryptocurrency
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box' style='margin-top:12px'>
          <strong style='color:#ef4444'>❌ EXCLUDE (Not Zakatable)</strong><br><br>
          • Primary home / residence<br>
          • Personal-use car<br>
          • Household furniture & appliances<br>
          • Personal clothing & accessories<br>
          • Business machinery / equipment<br>
          • Long-term locked pension
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧭 Navigate to the tabs above:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**💰 Metal Prices**\nView today's live gold & silver rates in INR")
    with c2:
        st.info("**📝 Assets & Liabilities**\nEnter your financial details")
    with c3:
        st.info("**📊 Results**\nSee your Zakat amount with charts")


# ══════════════════════════════════════════
# TAB 2 — METAL PRICES
# ══════════════════════════════════════════
with tab2:
    st.markdown("### 💰 Live Metal Prices — Indian Rupees (INR)")

    col1, col2 = st.columns([3, 2])

    with col1:
        metals_data = [
            ("🥇 Gold 24K (Pure)", "gold_24k"),
            ("🥇 Gold 22K (Jewelry)", "gold_22k"),
            ("🥇 Gold 18K", "gold_18k"),
            ("🥇 Gold 14K", "gold_14k"),
            ("🥈 Silver", "silver"),
        ]
        for label, key in metals_data:
            per_g  = prices[key]
            per_10 = per_g * 10
            per_tola = per_g * 11.66
            st.markdown(f"""
            <div class='price-row'>
              <span class='price-label'>{label}</span>
              <span>
                <span class='price-val'>₹{per_g:,.2f}/g</span>
                <span style='color:#475569;font-size:0.85em;margin-left:12px'>₹{per_10:,.0f}/10g</span>
                <span style='color:#475569;font-size:0.85em;margin-left:12px'>₹{per_tola:,.0f}/tola</span>
              </span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-label'>Gold Nisab (87.48g × 24K)</div>
          <div class='metric-value'>₹{nisab_gold_val:,.0f}</div>
        </div>
        <div class='metric-card'>
          <div class='metric-label'>Silver Nisab (612.36g)</div>
          <div class='metric-value blue'>₹{nisab_silver_val:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='info-box' style='margin-top:12px'>
          <strong style='color:#f0d060'>💡 About Nisab</strong><br><br>
          The Silver Nisab (₹{nisab_silver_val:,.0f}) is <em>lower</em> and
          more widely recommended. Using Gold Nisab (₹{nisab_gold_val:,.0f})
          is also valid but fewer people would qualify.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**✏️ Manual Price Override**")
    st.caption("If live API is unavailable, update prices manually here:")
    oc1, oc2, oc3, oc4, oc5 = st.columns(5)
    with oc1: prices["gold_24k"] = st.number_input("Gold 24K (₹/g)", value=float(prices["gold_24k"]), step=10.0)
    with oc2: prices["gold_22k"] = st.number_input("Gold 22K (₹/g)", value=float(prices["gold_22k"]), step=10.0)
    with oc3: prices["gold_18k"] = st.number_input("Gold 18K (₹/g)", value=float(prices["gold_18k"]), step=10.0)
    with oc4: prices["gold_14k"] = st.number_input("Gold 14K (₹/g)", value=float(prices["gold_14k"]), step=10.0)
    with oc5: prices["silver"]   = st.number_input("Silver (₹/g)",   value=float(prices["silver"]),   step=1.0)

    # Recalculate Nisab after manual override
    nisab_gold_val   = prices["gold_24k"] * NISAB_GOLD_G
    nisab_silver_val = prices["silver"]   * NISAB_SILVER_G


# ══════════════════════════════════════════
# TAB 3 — ASSETS & LIABILITIES
# ══════════════════════════════════════════
with tab3:
    st.markdown("### 📝 Enter Your Assets & Liabilities")
    st.caption("All amounts in Indian Rupees (₹). Enter 0 for items that don't apply.")

    # ── SECTION A: CASH ──────────────────
    st.markdown("<div class='section-header'>💰 Section A — Cash & Bank Balances</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: cash_home  = st.number_input("Cash at Home (₹)", 0.0, step=500.0, help="Physical currency at home")
    with c2: savings    = st.number_input("Savings/Current Account (₹)", 0.0, step=1000.0, help="Total across all bank accounts")
    with c3: fds        = st.number_input("Fixed Deposits (₹)", 0.0, step=1000.0, help="Only FDs maturing within this lunar year")
    c4, c5 = st.columns(2)
    with c4: pf         = st.number_input("Provident Fund (₹)", 0.0, step=1000.0, help="Accessible portion — 10% rule will be applied")
    with c5: forex      = st.number_input("Foreign Currency in ₹", 0.0, step=500.0, help="Convert foreign currency to INR first")

    # ── SECTION B: GOLD & SILVER ─────────
    st.markdown("<div class='section-header'>🥇 Section B — Gold & Silver (Enter weight in grams)</div>", unsafe_allow_html=True)
    st.caption("💡 Value is auto-calculated using today's live prices above")

    gc1, gc2, gc3, gc4, gc5 = st.columns(5)
    with gc1:
        g24 = st.number_input("Gold 24K (grams)", 0.0, step=0.5)
        st.caption(f"= ₹{g24 * prices['gold_24k']:,.0f}")
    with gc2:
        g22 = st.number_input("Gold 22K (grams)", 0.0, step=0.5)
        st.caption(f"= ₹{g22 * prices['gold_22k']:,.0f}")
    with gc3:
        g18 = st.number_input("Gold 18K (grams)", 0.0, step=0.5)
        st.caption(f"= ₹{g18 * prices['gold_18k']:,.0f}")
    with gc4:
        g14 = st.number_input("Gold 14K (grams)", 0.0, step=0.5)
        st.caption(f"= ₹{g14 * prices['gold_14k']:,.0f}")
    with gc5:
        sil = st.number_input("Silver (grams)", 0.0, step=1.0)
        st.caption(f"= ₹{sil * prices['silver']:,.0f}")

    if madhab == "Hanafi":
        st.markdown("""<div class='info-box'>ℹ️ <strong>Hanafi ruling:</strong> All gold & silver is zakatable, including personal jewelry.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='info-box'>ℹ️ <strong>Note:</strong> Some scholars exempt normal personal jewelry. Include only what your madhab considers zakatable.</div>""", unsafe_allow_html=True)

    # ── SECTION C: INVESTMENTS ───────────
    st.markdown("<div class='section-header'>📈 Section C — Investments</div>", unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1: stocks    = st.number_input("Stocks / Mutual Funds (₹)", 0.0, step=1000.0, help="Current market value")
    with ic2: crypto    = st.number_input("Cryptocurrency (₹)", 0.0, step=100.0, help="Current INR value")
    with ic3: nsc       = st.number_input("NSC / Post Office Savings (₹)", 0.0, step=500.0)
    ic4, ic5 = st.columns(2)
    with ic4: bonds     = st.number_input("Bonds / Debentures (₹)", 0.0, step=500.0)
    with ic5: other_inv = st.number_input("Other Investments (₹)", 0.0, step=500.0)

    stocks_method = st.radio(
        "How to calculate Zakat on stocks?",
        ["Full market value (2.5% of total) — Simple", "Zakatable portion only (~30%) — Detailed"],
        horizontal=True
    )
    stocks_zakatable = stocks if "Full" in stocks_method else stocks * 0.30

    # ── SECTION D: BUSINESS ──────────────
    st.markdown("<div class='section-header'>🏪 Section D — Business Assets</div>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns(3)
    with bc1: inventory   = st.number_input("Trade Inventory (₹)", 0.0, step=1000.0, help="Value of goods held for sale")
    with bc2: receivables = st.number_input("Money Owed to You (₹)", 0.0, step=500.0, help="Amounts clients/customers owe you")
    with bc3: biz_cash    = st.number_input("Business Cash/Bank (₹)", 0.0, step=1000.0)

    # ── SECTION E: OTHER ─────────────────
    st.markdown("<div class='section-header'>🏠 Section E — Other Zakatable Assets</div>", unsafe_allow_html=True)
    oc1, oc2, oc3 = st.columns(3)
    with oc1: rental_sav  = st.number_input("Rental Income Savings (₹)", 0.0, step=500.0)
    with oc2: agri        = st.number_input("Agricultural Produce (₹)", 0.0, step=500.0)
    with oc3: other_asset = st.number_input("Other Zakatable Assets (₹)", 0.0, step=500.0)

    st.divider()

    # ── LIABILITIES ───────────────────────
    st.markdown("<div class='section-header'>📉 Liabilities — Short-Term Debts (Due This Year Only)</div>", unsafe_allow_html=True)
    st.caption("⚠️ Only include debts due within this lunar year. Do NOT include home mortgage or long-term car loans.")
    lc1, lc2, lc3 = st.columns(3)
    with lc1: personal_loan = st.number_input("Personal Loan Due (₹)", 0.0, step=500.0)
    with lc2: credit_card   = st.number_input("Credit Card Balance (₹)", 0.0, step=100.0)
    with lc3: rent_arrears  = st.number_input("Rent Arrears Owed (₹)", 0.0, step=500.0)
    lc4, lc5 = st.columns(2)
    with lc4: biz_loan      = st.number_input("Business Loan Due (₹)", 0.0, step=500.0)
    with lc5: other_debt    = st.number_input("Other Short-Term Debts (₹)", 0.0, step=500.0)


# ══════════════════════════════════════════
# CALCULATIONS (shared between tabs)
# ══════════════════════════════════════════
metals_val      = (g24 * prices["gold_24k"] + g22 * prices["gold_22k"] +
                   g18 * prices["gold_18k"] + g14 * prices["gold_14k"] +
                   sil * prices["silver"])

cash_total      = cash_home + savings + fds + pf * 0.10 + forex
invest_total    = stocks_zakatable + crypto + nsc + bonds + other_inv
biz_total       = inventory + receivables + biz_cash
other_total     = rental_sav + agri + other_asset

total_assets    = cash_total + metals_val + invest_total + biz_total + other_total
total_liab      = personal_loan + credit_card + rent_arrears + biz_loan + other_debt
net_zakatable   = max(0.0, total_assets - total_liab)

nisab_threshold = nisab_silver_val if "Silver" in nisab_standard else nisab_gold_val
nisab_met       = net_zakatable >= nisab_threshold
zakat_due       = net_zakatable * 0.025 if nisab_met else 0.0


# ══════════════════════════════════════════
# TAB 4 — RESULTS
# ══════════════════════════════════════════
with tab4:
    st.markdown("### 📊 Your Zakat Results")

    # Top metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>Total Assets</div>
          <div class='metric-value'>₹{total_assets:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>Total Liabilities</div>
          <div class='metric-value red'>₹{total_liab:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>Net Zakatable Wealth</div>
          <div class='metric-value blue'>₹{net_zakatable:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>Nisab Threshold ({nisab_standard.split()[0]})</div>
          <div class='metric-value'>₹{nisab_threshold:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    # Nisab status
    if nisab_met:
        st.markdown(f"""
        <div style='text-align:center;margin:20px 0'>
          <span class='badge-yes'>✅ Zakat IS Obligatory — Your wealth exceeds the Nisab</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:center;margin:20px 0'>
          <span class='badge-no'>❌ Zakat Not Yet Obligatory — Wealth is below Nisab (₹{nisab_threshold - net_zakatable:,.0f} short)</span>
        </div>""", unsafe_allow_html=True)

    # Zakat due box
    monthly = zakat_due / 12
    st.markdown(f"""
    <div class='zakat-result'>
      <div style='color:#94a3b8;font-size:0.85em;text-transform:uppercase;letter-spacing:2px'>ZAKAT DUE (2.5%)</div>
      <div class='zakat-amount'>₹{zakat_due:,.0f}</div>
      {'<div style="color:#94a3b8;font-size:0.9em;margin-top:8px">Monthly equivalent: ₹' + f'{monthly:,.0f}' + '/month</div>' if zakat_due > 0 else ''}
    </div>
    """, unsafe_allow_html=True)

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Donut — Asset Distribution
        cat_labels = ["Cash & Bank", "Gold & Silver", "Investments", "Business", "Other"]
        cat_values = [cash_total, metals_val, invest_total, biz_total, other_total]
        cat_colors = ["#f0d060", "#c0c0c0", "#38bdf8", "#f97316", "#a78bfa"]
        filtered   = [(l, v, c) for l, v, c in zip(cat_labels, cat_values, cat_colors) if v > 0]

        if filtered:
            fl, fv, fc = zip(*filtered)
            fig1 = go.Figure(go.Pie(
                labels=list(fl), values=list(fv), hole=0.55,
                marker=dict(colors=list(fc)),
                textinfo="label+percent",
                textfont=dict(size=11)
            ))
            fig1.update_layout(
                title=dict(text="Asset Distribution", font=dict(color="#f0d060", size=14)),
                paper_bgcolor="#1e293b", plot_bgcolor="#1e293b",
                font=dict(color="#e2e8f0"),
                margin=dict(t=40, b=10, l=10, r=10),
                showlegend=False,
                height=320
            )
            fig1.add_annotation(
                text=f"₹{total_assets/100000:.1f}L<br>Total",
                x=0.5, y=0.5, font=dict(size=13, color="#f0d060"), showarrow=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Enter asset values to see the distribution chart.")

    with chart_col2:
        # Bar — Wealth Overview
        fig2 = go.Figure(go.Bar(
            x=["Total Assets", "Liabilities", "Net Zakatable", "Zakat Due"],
            y=[total_assets, total_liab, net_zakatable, zakat_due],
            marker_color=["#f0d060", "#ef4444", "#38bdf8", "#22c55e"],
            text=[f"₹{v:,.0f}" for v in [total_assets, total_liab, net_zakatable, zakat_due]],
            textposition="outside",
            textfont=dict(size=10)
        ))
        fig2.update_layout(
            title=dict(text="Wealth Overview", font=dict(color="#f0d060", size=14)),
            paper_bgcolor="#1e293b", plot_bgcolor="#1e293b",
            font=dict(color="#e2e8f0"),
            yaxis=dict(gridcolor="#334155", tickformat=","),
            margin=dict(t=40, b=10),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Detailed breakdown table
    st.markdown("### 📋 Detailed Breakdown")
    breakdown = {
        "Category": ["Cash & Bank", "Gold & Silver", "Investments", "Business Assets", "Other Assets",
                     "— TOTAL ASSETS —", "Liabilities", "— NET ZAKATABLE WEALTH —", "Zakat Due (2.5%)"],
        "Amount (₹)": [cash_total, metals_val, invest_total, biz_total, other_total,
                        total_assets, -total_liab, net_zakatable, zakat_due]
    }
    df = pd.DataFrame(breakdown)
    df["Amount (₹)"] = df["Amount (₹)"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Download button
    csv = pd.DataFrame({
        "Field": breakdown["Category"],
        "Amount": [cash_total, metals_val, invest_total, biz_total, other_total,
                   total_assets, total_liab, net_zakatable, zakat_due]
    }).to_csv(index=False)
    st.download_button(
        "⬇️ Download Results as CSV",
        csv,
        file_name=f"Zakat_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


# ══════════════════════════════════════════
# TAB 5 — FAQ
# ══════════════════════════════════════════
with tab5:
    st.markdown("### ❓ Frequently Asked Questions")

    faqs = [
        ("Is Zakat on ALL gold, including jewelry?",
         "Scholars differ. The **Hanafi** school considers all gold/silver zakatable, including personal jewelry. **Shafi'i, Maliki, and Hanbali** schools may exempt normal personal jewelry worn regularly. Enter only what your madhab considers zakatable, or consult your local imam."),
        ("Which Nisab should I use — Gold or Silver?",
         "Most contemporary scholars (including Mufti Taqi Usmani) recommend **Silver Nisab** as it is lower and ensures more Muslims fulfil the obligation, with more wealth reaching the poor. Gold Nisab is also valid. This calculator lets you choose in the sidebar."),
        ("What about my home loan / mortgage?",
         "Your **primary home is NOT zakatable**. For mortgage debt, most scholars say you can deduct only the installment(s) **due within the current lunar year** — not the full outstanding loan amount. Long-term car loans are similarly not fully deductible."),
        ("How do I calculate Zakat on stocks & mutual funds?",
         "**Method 1 (Simple):** Pay 2.5% on the full current market value. **Method 2 (Detailed):** Calculate only on the company's zakatable underlying assets (cash + inventory), typically ~25–40% of market value. Method 1 is easier and more conservative."),
        ("What are the 8 categories eligible to receive Zakat?",
         "Based on the Quran (9:60): 1) The poor (Fuqara), 2) The needy (Masakin), 3) Zakat administrators, 4) Those whose hearts are to be reconciled, 5) Those in bondage (freeing), 6) The debt-ridden (Gharimin), 7) In the way of Allah (Fi Sabilillah), 8) Stranded travelers (Ibn al-Sabil)."),
        ("When should I pay Zakat?",
         "Once your wealth has been **above Nisab for one complete lunar year** (Hawl = ~354 days). Many Muslims choose to pay during **Ramadan** for extra blessings, but any time is valid. Set a reminder on the Islamic date your wealth first reached Nisab."),
        ("Where can I pay Zakat in India?",
         "• Your **local mosque or masjid** Zakat committee\n• **Islamic Relief India** — islamicreliefindia.org\n• **Human Welfare Foundation (HWF)**\n• **Zakat Foundation of India**\n• Directly to individuals from the 8 eligible categories"),
    ]

    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(a)

    st.divider()
    st.markdown("""
    <div class='info-box' style='text-align:center'>
      ⚠️ <strong>Disclaimer:</strong> This calculator is a guide only. For authoritative Islamic rulings
      specific to your situation, please consult a <strong>qualified Islamic scholar</strong> or your local imam.
      Zakat calculations may vary by school of thought (madhab).
    </div>
    """, unsafe_allow_html=True)

