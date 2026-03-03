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

  html, body, [class*="css"], p, span, div, label {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
  }
  .main, .block-container, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
  }
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
  [data-testid="stSidebar"] { background: #0f172a !important; border-right: 1px solid #1e293b; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

  /* Number inputs */
  [data-testid="stNumberInput"] input {
    background-color: #1e293b !important;
    color: #f0d060 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
  }
  [data-testid="stNumberInput"] button {
    background-color: #334155 !important;
    color: #e2e8f0 !important;
    border: none !important;
  }
  [data-testid="stNumberInput"] button:hover {
    background-color: #f0d06030 !important;
    color: #f0d060 !important;
  }
  [data-testid="stNumberInput"] button p { color: #e2e8f0 !important; }
  [data-testid="stTextInput"] input {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
  }
  [data-testid="stNumberInput"] label p,
  [data-testid="stTextInput"] label p,
  [data-testid="stSelectbox"] label p,
  [data-testid="stRadio"] label p { color: #cbd5e1 !important; }

  /* Dropdowns */
  [data-baseweb="select"] * { background-color: #1e293b !important; color: #e2e8f0 !important; }
  [data-baseweb="menu"] { background-color: #1e293b !important; border: 1px solid #334155 !important; }
  [data-baseweb="option"] { background-color: #1e293b !important; color: #e2e8f0 !important; }
  [data-baseweb="option"]:hover { background-color: #f0d06020 !important; color: #f0d060 !important; }
  [data-baseweb="popover"] * { background-color: #1e293b !important; color: #e2e8f0 !important; }
  div[role="listbox"] { background-color: #1e293b !important; }
  div[role="option"] { background-color: #1e293b !important; color: #e2e8f0 !important; }
  div[role="option"]:hover { background-color: #f0d06030 !important; color: #f0d060 !important; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { background: #1e293b !important; border-radius: 10px; gap: 4px; padding: 4px; }
  .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 8px; }
  .stTabs [aria-selected="true"] { background: #f0d06025 !important; color: #f0d060 !important; }

  /* Captions */
  .stCaption, [data-testid="stCaptionContainer"] { color: #64748b !important; }
  [data-testid="stCaptionContainer"] p { color: #64748b !important; }

  /* Download button */
  .stDownloadButton button {
    background: #1e293b !important;
    color: #f0d060 !important;
    border: 1.5px solid #f0d060 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
  }
  .stDownloadButton button:hover { background: #f0d06020 !important; }
  .stDownloadButton button p { color: #f0d060 !important; }

  /* Table toolbar */
  [data-testid="stDataFrameToolbar"] { background: #1e293b !important; border-radius: 10px !important; border: 1px solid #334155 !important; }
  [data-testid="stDataFrameToolbar"] button { color: #e2e8f0 !important; background: transparent !important; }
  [data-testid="stDataFrameToolbar"] button:hover { background: #f0d06020 !important; }
  [data-testid="stDataFrameToolbar"] svg { fill: #e2e8f0 !important; stroke: #e2e8f0 !important; }

  hr { border-color: #334155 !important; }
  h1, h2, h3, h4 { color: #f0d060 !important; }

  /* HTML details/summary for FAQ */
  details {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
    overflow: hidden !important;
  }
  details summary {
    padding: 14px 18px !important;
    cursor: pointer !important;
    color: #f0d060 !important;
    font-weight: 600 !important;
    list-style: none !important;
  }
  details summary:hover { background: #f0d06010 !important; }
  details[open] summary { border-bottom: 1px solid #334155 !important; }
  details summary::-webkit-details-marker { display: none !important; }
  details summary::marker { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# VISITOR COUNTER
# ─────────────────────────────────────────
@st.cache_data(ttl=300)
def get_and_increment_count():
    try:
        r = requests.get(
            "https://api.counterapi.dev/v1/zakat-india-2024/visits/up",
            timeout=5
        )
        if r.status_code == 200:
            return r.json().get("count", None)
    except:
        pass
    try:
        r = requests.get(
            "https://hits.sh/zakat-calc-india.json",
            timeout=5
        )
        if r.status_code == 200:
            return r.json().get("total", None)
    except:
        pass
    return None

if "counted" not in st.session_state:
    st.session_state.counted = True
    get_and_increment_count.clear()


# ─────────────────────────────────────────
# LIVE PRICE FETCHER
# ─────────────────────────────────────────
@st.cache_data(ttl=3600)
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
                "gold_24k": round(g24, 2), "gold_22k": round(g24 * 22/24, 2),
                "gold_18k": round(g24 * 18/24, 2), "gold_14k": round(g24 * 14/24, 2),
                "silver": round(sil, 2),
                "fetched": datetime.now().strftime("%d %b %Y %I:%M %p")
            }
        except:
            pass
    return {
        "source": "🔴 Approximate (add API key for live prices)",
        "gold_24k": 7800, "gold_22k": 7150,
        "gold_18k": 5850, "gold_14k": 4550,
        "silver": 95, "fetched": "Manual"
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
    api_key = st.text_input(
        "goldapi.io API Key (Free)",
        placeholder="paste-your-free-key-here",
        type="password",
        help="Get a free key at goldapi.io — 100 requests/month free"
    )
    st.caption("💡 [Get free key at goldapi.io](https://www.goldapi.io)")
    st.divider()

    st.markdown("**⚙️ Settings**")
    nisab_standard = st.radio(
        "Nisab Standard",
        ["Silver (Recommended)", "Gold"],
        help="Silver Nisab is lower and more inclusive."
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

    visit_count = get_and_increment_count()
    if visit_count and visit_count > 0:
        st.markdown(f"""
        <div style='background:#1e293b;border:1px solid #334155;border-radius:10px;
                    padding:14px;text-align:center;margin-top:10px'>
          <div style='color:#64748b;font-size:0.75em;text-transform:uppercase;letter-spacing:1px'>Total Users</div>
          <div style='color:#f0d060;font-size:2em;font-weight:700'>{visit_count:,}</div>
          <div style='color:#64748b;font-size:0.75em'>Muslims calculated Zakat</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# FETCH PRICES & NISAB
# ─────────────────────────────────────────
prices           = fetch_prices(api_key)
NISAB_GOLD_G     = 87.48
NISAB_SILVER_G   = 612.36
nisab_gold_val   = prices["gold_24k"] * NISAB_GOLD_G
nisab_silver_val = prices["silver"]   * NISAB_SILVER_G


# ─────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────
visit_count = get_and_increment_count()
count_html  = f"""
  <div style='margin-top:14px;display:inline-flex;align-items:center;gap:8px;
              background:#1e293b;border:1px solid #334155;border-radius:30px;padding:6px 18px'>
    <span style='font-size:1.1em'>🕌</span>
    <span style='color:#94a3b8;font-size:0.85em'>Used by</span>
    <span style='color:#f0d060;font-weight:700;font-size:1.1em'>{visit_count:,}</span>
    <span style='color:#94a3b8;font-size:0.85em'>Muslims so far</span>
  </div>
""" if visit_count and visit_count > 0 else ""

st.markdown(f"""
<div class='hero-banner'>
  <div class='hero-title'>🕌 Zakat Calculator</div>
  <div class='hero-subtitle'>Calculate your annual Zakat with live gold &amp; silver prices in Indian Rupees</div>
  <div style='margin-top:10px;color:#475569;font-size:0.8em'>
    Prices: {prices['source']} &nbsp;|&nbsp; {prices['fetched']}
  </div>
  {count_html}
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# TABS
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
          on wealth exceeding the <strong>Nisab threshold</strong>, held for one complete <strong>lunar year (Hawl)</strong>.
        </div>
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
          • Cash at home &amp; bank savings<br>
          • Gold &amp; silver holdings<br>
          • Stocks &amp; mutual funds<br>
          • Business inventory (for sale)<br>
          • Receivables (money owed to you)<br>
          • Rental income savings<br>
          • Cryptocurrency
        </div>
        <div class='info-box' style='margin-top:12px'>
          <strong style='color:#ef4444'>❌ EXCLUDE (Not Zakatable)</strong><br><br>
          • Primary home / residence<br>
          • Personal-use car<br>
          • Household furniture &amp; appliances<br>
          • Personal clothing &amp; accessories<br>
          • Business machinery / equipment<br>
          • Long-term locked pension
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("**💰 Metal Prices**\nView today's live gold & silver rates in INR")
    with c2: st.info("**📝 Assets & Liabilities**\nEnter your financial details here")
    with c3: st.info("**📊 Results**\nSee your Zakat amount with charts")


# ══════════════════════════════════════════
# TAB 2 — METAL PRICES
# ══════════════════════════════════════════
with tab2:
    st.markdown("### 💰 Live Metal Prices — Indian Rupees (INR)")
    col1, col2 = st.columns([3, 2])
    with col1:
        for label, key in [("🥇 Gold 24K (Pure)", "gold_24k"), ("🥇 Gold 22K (Jewelry)", "gold_22k"),
                            ("🥇 Gold 18K", "gold_18k"), ("🥇 Gold 14K", "gold_14k"), ("🥈 Silver", "silver")]:
            pg = prices[key]
            st.markdown(f"""
            <div class='price-row'>
              <span class='price-label'>{label}</span>
              <span>
                <span class='price-val'>₹{pg:,.2f}/g</span>
                <span style='color:#475569;font-size:0.85em;margin-left:12px'>₹{pg*10:,.0f}/10g</span>
                <span style='color:#475569;font-size:0.85em;margin-left:12px'>₹{pg*11.66:,.0f}/tola</span>
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
        <div class='info-box' style='margin-top:12px'>
          <strong style='color:#f0d060'>💡 About Nisab</strong><br><br>
          Silver Nisab is lower and more widely recommended.
          Gold Nisab is also valid — choose in the sidebar.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**✏️ Manual Price Override**")
    st.caption("Update prices manually if live API is unavailable:")
    oc1, oc2, oc3, oc4, oc5 = st.columns(5)
    with oc1: prices["gold_24k"] = st.number_input("Gold 24K (₹/g)", value=float(prices["gold_24k"]), step=10.0)
    with oc2: prices["gold_22k"] = st.number_input("Gold 22K (₹/g)", value=float(prices["gold_22k"]), step=10.0)
    with oc3: prices["gold_18k"] = st.number_input("Gold 18K (₹/g)", value=float(prices["gold_18k"]), step=10.0)
    with oc4: prices["gold_14k"] = st.number_input("Gold 14K (₹/g)", value=float(prices["gold_14k"]), step=10.0)
    with oc5: prices["silver"]   = st.number_input("Silver (₹/g)",   value=float(prices["silver"]),   step=1.0)
    nisab_gold_val   = prices["gold_24k"] * NISAB_GOLD_G
    nisab_silver_val = prices["silver"]   * NISAB_SILVER_G


# ══════════════════════════════════════════
# TAB 3 — ASSETS & LIABILITIES
# ══════════════════════════════════════════
with tab3:
    st.markdown("### 📝 Enter Your Assets & Liabilities")
    st.caption("All amounts in Indian Rupees (₹). Enter 0 for items that don't apply.")

    st.markdown("<div class='section-header'>💰 Section A — Cash & Bank Balances</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: cash_home = st.number_input("Cash at Home (₹)", 0.0, step=500.0, help="Physical currency at home")
    with c2: savings   = st.number_input("Savings/Current Account (₹)", 0.0, step=1000.0, help="Total across all bank accounts")
    with c3: fds       = st.number_input("Fixed Deposits (₹)", 0.0, step=1000.0, help="Only FDs maturing within this lunar year")
    c4, c5 = st.columns(2)
    with c4: pf    = st.number_input("Provident Fund (₹)", 0.0, step=1000.0, help="Accessible portion — 10% rule applied")
    with c5: forex = st.number_input("Foreign Currency in ₹", 0.0, step=500.0, help="Convert to INR first")

    st.markdown("<div class='section-header'>🥇 Section B — Gold & Silver (Enter weight in grams)</div>", unsafe_allow_html=True)
    st.caption("💡 Value is auto-calculated using today's live prices")
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
        st.markdown("""<div class='info-box'>ℹ️ <strong>Hanafi ruling:</strong> All gold &amp; silver is zakatable, including personal jewelry.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='info-box'>ℹ️ <strong>Note:</strong> Some scholars exempt normal personal jewelry. Include only what your madhab considers zakatable.</div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>📈 Section C — Investments</div>", unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1: stocks    = st.number_input("Stocks / Mutual Funds (₹)", 0.0, step=1000.0, help="Current market value")
    with ic2: crypto    = st.number_input("Cryptocurrency (₹)", 0.0, step=100.0, help="Current INR value")
    with ic3: nsc       = st.number_input("NSC / Post Office Savings (₹)", 0.0, step=500.0)
    ic4, ic5 = st.columns(2)
    with ic4: bonds     = st.number_input("Bonds / Debentures (₹)", 0.0, step=500.0)
    with ic5: other_inv = st.number_input("Other Investments (₹)", 0.0, step=500.0)
    stocks_method    = st.radio("How to calculate Zakat on stocks?",
        ["Full market value (2.5% of total) — Simple", "Zakatable portion only (~30%) — Detailed"], horizontal=True)
    stocks_zakatable = stocks if "Full" in stocks_method else stocks * 0.30

    st.markdown("<div class='section-header'>🏪 Section D — Business Assets</div>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns(3)
    with bc1: inventory   = st.number_input("Trade Inventory (₹)", 0.0, step=1000.0, help="Value of goods held for sale")
    with bc2: receivables = st.number_input("Money Owed to You (₹)", 0.0, step=500.0, help="Amounts clients/customers owe you")
    with bc3: biz_cash    = st.number_input("Business Cash/Bank (₹)", 0.0, step=1000.0)

    st.markdown("<div class='section-header'>🏠 Section E — Other Zakatable Assets</div>", unsafe_allow_html=True)
    oe1, oe2, oe3 = st.columns(3)
    with oe1: rental_sav  = st.number_input("Rental Income Savings (₹)", 0.0, step=500.0)
    with oe2: agri        = st.number_input("Agricultural Produce (₹)", 0.0, step=500.0)
    with oe3: other_asset = st.number_input("Other Zakatable Assets (₹)", 0.0, step=500.0)

    st.divider()
    st.markdown("<div class='section-header'>📉 Liabilities — Short-Term Debts (Due This Year Only)</div>", unsafe_allow_html=True)
    st.caption("⚠️ Only include debts due within this lunar year. Do NOT include home mortgage or long-term car loans.")
    lc1, lc2, lc3 = st.columns(3)
    with lc1: personal_loan = st.number_input("Personal Loan Due (₹)", 0.0, step=500.0)
    with lc2: credit_card   = st.number_input("Credit Card Balance (₹)", 0.0, step=100.0)
    with lc3: rent_arrears  = st.number_input("Rent Arrears Owed (₹)", 0.0, step=500.0)
    lc4, lc5 = st.columns(2)
    with lc4: biz_loan   = st.number_input("Business Loan Due (₹)", 0.0, step=500.0)
    with lc5: other_debt = st.number_input("Other Short-Term Debts (₹)", 0.0, step=500.0)


# ══════════════════════════════════════════
# SHARED CALCULATIONS
# ══════════════════════════════════════════
metals_val    = (g24*prices["gold_24k"] + g22*prices["gold_22k"] +
                 g18*prices["gold_18k"] + g14*prices["gold_14k"] + sil*prices["silver"])
cash_total    = cash_home + savings + fds + pf*0.10 + forex
invest_total  = stocks_zakatable + crypto + nsc + bonds + other_inv
biz_total     = inventory + receivables + biz_cash
other_total   = rental_sav + agri + other_asset
total_assets  = cash_total + metals_val + invest_total + biz_total + other_total
total_liab    = personal_loan + credit_card + rent_arrears + biz_loan + other_debt
net_zakatable = max(0.0, total_assets - total_liab)
nisab_threshold = nisab_silver_val if "Silver" in nisab_standard else nisab_gold_val
nisab_met       = net_zakatable >= nisab_threshold
zakat_due       = net_zakatable * 0.025 if nisab_met else 0.0


# ══════════════════════════════════════════
# TAB 4 — RESULTS
# ══════════════════════════════════════════
with tab4:
    st.markdown("### 📊 Your Zakat Results")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Assets</div>
          <div class='metric-value'>₹{total_assets:,.0f}</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Liabilities</div>
          <div class='metric-value red'>₹{total_liab:,.0f}</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='metric-card'><div class='metric-label'>Net Zakatable Wealth</div>
          <div class='metric-value blue'>₹{net_zakatable:,.0f}</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class='metric-card'><div class='metric-label'>Nisab ({nisab_standard.split()[0]})</div>
          <div class='metric-value'>₹{nisab_threshold:,.0f}</div></div>""", unsafe_allow_html=True)

    if nisab_met:
        st.markdown("""<div style='text-align:center;margin:20px 0'>
          <span class='badge-yes'>✅ Zakat IS Obligatory — Your wealth exceeds the Nisab</span>
        </div>""", unsafe_allow_html=True)
    else:
        shortfall = nisab_threshold - net_zakatable
        st.markdown(f"""<div style='text-align:center;margin:20px 0'>
          <span class='badge-no'>❌ Zakat Not Yet Obligatory — ₹{shortfall:,.0f} below Nisab</span>
        </div>""", unsafe_allow_html=True)

    monthly      = zakat_due / 12
    monthly_html = f'<div style="color:#94a3b8;font-size:0.9em;margin-top:8px">Monthly equivalent: ₹{monthly:,.0f}/month</div>' if zakat_due > 0 else ""
    st.markdown(f"""
    <div class='zakat-result'>
      <div style='color:#94a3b8;font-size:0.85em;text-transform:uppercase;letter-spacing:2px'>ZAKAT DUE (2.5%)</div>
      <div class='zakat-amount'>₹{zakat_due:,.0f}</div>
      {monthly_html}
    </div>""", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        cat_labels = ["Cash & Bank", "Gold & Silver", "Investments", "Business", "Other"]
        cat_values = [cash_total, metals_val, invest_total, biz_total, other_total]
        cat_colors = ["#f0d060", "#c0c0c0", "#38bdf8", "#f97316", "#a78bfa"]
        filtered   = [(l, v, c) for l, v, c in zip(cat_labels, cat_values, cat_colors) if v > 0]
        if filtered:
            fl, fv, fc = zip(*filtered)
            fig1 = go.Figure(go.Pie(labels=list(fl), values=list(fv), hole=0.55,
                marker=dict(colors=list(fc)), textinfo="label+percent", textfont=dict(size=11)))
            fig1.update_layout(
                title=dict(text="Asset Distribution", font=dict(color="#f0d060", size=14)),
                paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font=dict(color="#e2e8f0"),
                margin=dict(t=40, b=10, l=10, r=10), showlegend=False, height=320)
            fig1.add_annotation(text=f"₹{total_assets/100000:.1f}L<br>Total",
                x=0.5, y=0.5, font=dict(size=13, color="#f0d060"), showarrow=False)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Enter asset values to see the distribution chart.")

    with chart_col2:
        fig2 = go.Figure(go.Bar(
            x=["Total Assets", "Liabilities", "Net Zakatable", "Zakat Due"],
            y=[total_assets, total_liab, net_zakatable, zakat_due],
            marker_color=["#f0d060", "#ef4444", "#38bdf8", "#22c55e"],
            text=[f"₹{v:,.0f}" for v in [total_assets, total_liab, net_zakatable, zakat_due]],
            textposition="outside", textfont=dict(size=10)))
        fig2.update_layout(
            title=dict(text="Wealth Overview", font=dict(color="#f0d060", size=14)),
            paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font=dict(color="#e2e8f0"),
            yaxis=dict(gridcolor="#334155", tickformat=","),
            margin=dict(t=40, b=10), showlegend=False, height=320)
        st.plotly_chart(fig2, use_container_width=True)

    # Dark HTML breakdown table
    st.markdown("### 📋 Detailed Breakdown")
    rows_data = [
        ("💰 Cash & Bank",            cash_total,    "#e2e8f0", False),
        ("🥇 Gold & Silver",          metals_val,    "#e2e8f0", False),
        ("📈 Investments",            invest_total,  "#e2e8f0", False),
        ("🏪 Business Assets",        biz_total,     "#e2e8f0", False),
        ("🏠 Other Assets",           other_total,   "#e2e8f0", False),
        ("— TOTAL ASSETS —",          total_assets,  "#f0d060", True),
        ("📉 Liabilities",            total_liab,    "#ef4444", False),
        ("— NET ZAKATABLE WEALTH —",  net_zakatable, "#38bdf8", True),
        ("💚 Zakat Due (2.5%)",       zakat_due,     "#22c55e", True),
    ]
    rows_html = ""
    for i, (label, val, color, bold) in enumerate(rows_data):
        bg     = "#1e293b" if i % 2 == 0 else "#162032"
        fw     = "700" if bold else "400"
        prefix = "− " if label == "📉 Liabilities" and val > 0 else ""
        rows_html += f"""
        <tr style='background:{bg}'>
          <td style='padding:12px 16px;color:{color};font-weight:{fw};border-bottom:1px solid #0f172a'>{label}</td>
          <td style='padding:12px 16px;color:{color};text-align:right;font-weight:{fw};border-bottom:1px solid #0f172a'>{prefix}₹{val:,.0f}</td>
        </tr>"""

    st.markdown(f"""
    <table style='width:100%;border-collapse:collapse;border-radius:12px;
                  overflow:hidden;border:1px solid #334155;margin:10px 0'>
      <thead>
        <tr style='background:#0f172a'>
          <th style='padding:12px 16px;text-align:left;color:#94a3b8;font-size:0.85em;
                     text-transform:uppercase;letter-spacing:1px;border-bottom:2px solid #334155'>Category</th>
          <th style='padding:12px 16px;text-align:right;color:#94a3b8;font-size:0.85em;
                     text-transform:uppercase;letter-spacing:1px;border-bottom:2px solid #334155'>Amount (₹)</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    csv_data = pd.DataFrame({
        "Category": ["Cash & Bank", "Gold & Silver", "Investments", "Business Assets",
                     "Other Assets", "Total Assets", "Liabilities", "Net Zakatable Wealth", "Zakat Due (2.5%)"],
        "Amount (INR)": [cash_total, metals_val, invest_total, biz_total, other_total,
                         total_assets, total_liab, net_zakatable, zakat_due]
    }).to_csv(index=False)

    st.download_button(
        "⬇️ Download Results as CSV", csv_data,
        file_name=f"Zakat_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


# ══════════════════════════════════════════
# TAB 5 — FAQ (Pure HTML accordion)
# ══════════════════════════════════════════
with tab5:
    st.markdown("### ❓ Frequently Asked Questions")

    faqs = [
        ("Is Zakat on ALL gold, including jewelry?",
         "Scholars differ. The <strong style='color:#f0d060'>Hanafi</strong> school considers all gold/silver zakatable, including personal jewelry. <strong style='color:#f0d060'>Shafi'i, Maliki, and Hanbali</strong> schools may exempt normal personal jewelry. Enter only what your madhab considers zakatable, or consult your local imam."),
        ("Which Nisab should I use — Gold or Silver?",
         "Most contemporary scholars (including Mufti Taqi Usmani) recommend <strong style='color:#f0d060'>Silver Nisab</strong> as it is lower and ensures more Muslims fulfil the obligation. Gold Nisab is also valid. Choose in the sidebar."),
        ("What about my home loan / mortgage?",
         "Your <strong style='color:#f0d060'>primary home is NOT zakatable</strong>. For mortgage debt, most scholars say you can deduct only the installment(s) <strong style='color:#f0d060'>due within the current lunar year</strong> — not the full outstanding amount."),
        ("How do I calculate Zakat on stocks & mutual funds?",
         "<strong style='color:#f0d060'>Method 1 (Simple):</strong> Pay 2.5% on the full current market value.<br><br><strong style='color:#f0d060'>Method 2 (Detailed):</strong> Calculate only on the company's zakatable assets (cash + inventory), typically ~25–40% of market value. Method 1 is easier and more conservative."),
        ("What are the 8 categories eligible to receive Zakat?",
         "Based on the Quran (9:60):<br><br>1) The poor (Fuqara) &nbsp; 2) The needy (Masakin)<br>3) Zakat administrators &nbsp; 4) Those whose hearts are to be reconciled<br>5) Those in bondage (freeing) &nbsp; 6) The debt-ridden (Gharimin)<br>7) In the way of Allah (Fi Sabilillah) &nbsp; 8) Stranded travelers (Ibn al-Sabil)"),
        ("When should I pay Zakat?",
         "Once your wealth has been <strong style='color:#f0d060'>above Nisab for one complete lunar year</strong> (Hawl ≈ 354 days). Many Muslims pay during <strong style='color:#f0d060'>Ramadan</strong> for extra blessings, but any time of year is valid."),
        ("Where can I pay Zakat in India?",
         "• Your <strong style='color:#f0d060'>local mosque or masjid</strong> Zakat committee<br>• <strong style='color:#f0d060'>Islamic Relief India</strong> — islamicreliefindia.org<br>• <strong style='color:#f0d060'>Human Welfare Foundation (HWF)</strong><br>• <strong style='color:#f0d060'>Zakat Foundation of India</strong><br>• Directly to individuals from the 8 eligible categories"),
    ]

    faq_html = ""
    for q, a in faqs:
        faq_html += f"""
        <details style='background:#1e293b;border:1px solid #334155;border-radius:10px;
                        margin-bottom:10px;overflow:hidden'>
          <summary style='padding:14px 18px;cursor:pointer;color:#f0d060;font-weight:600;
                          font-size:1em;list-style:none;display:flex;
                          justify-content:space-between;align-items:center'>
            <span>❓ &nbsp;{q}</span>
            <span style='color:#f0d060;font-size:1.4em;font-weight:300;margin-left:12px'>＋</span>
          </summary>
          <div style='padding:14px 18px 18px 18px;color:#cbd5e1;
                      border-top:1px solid #334155;line-height:1.8;font-size:0.95em'>
            {a}
          </div>
        </details>"""

    st.markdown(faq_html, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div class='info-box' style='text-align:center'>
      ⚠️ <strong>Disclaimer:</strong> This calculator is a guide only. For authoritative Islamic rulings
      specific to your situation, please consult a <strong>qualified Islamic scholar</strong> or your local imam.
      Zakat calculations may vary by school of thought (madhab).
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:30px 0 10px 0;margin-top:40px;
            border-top:1px solid #1e293b'>
  <p style='color:#475569;font-size:0.85em'>
    Made with 🤍 &nbsp;|&nbsp;
    <strong style='color:#f0d060'>Created by Dr. Mohammad Ibrahim Badar for the love of Ummah</strong>
    &nbsp;|&nbsp; 🕌
  </p>
</div>
""", unsafe_allow_html=True)
