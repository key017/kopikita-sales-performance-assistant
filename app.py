from pathlib import Path

import base64

import html

import os



import pandas as pd

import streamlit as st

import plotly.express as px

from dotenv import load_dotenv

from google import genai



from src.business_context import BUSINESS_CONTEXT



# ============================================================

# PAGE CONFIG

# ============================================================

st.set_page_config(

    page_title="KopiKita Sales Performance",

    page_icon="☕",

    layout="wide",

    initial_sidebar_state="expanded",

)

# ============================================================
# CUSTOM SIDEBAR STATE
# ============================================================
# Initialize before any reference to session_state.
if "kopikita_sidebar_open" not in st.session_state:
    st.session_state.kopikita_sidebar_open = True

if "kopikita_page" not in st.session_state:
    st.session_state.kopikita_page = "Overview"



# ============================================================

# PATH & ENVIRONMENT

# ============================================================

ROOT_DIR = Path(__file__).resolve().parent

DATA_PATH = ROOT_DIR / "data" / "sales_data.csv"

COFFEE_LOGO = ROOT_DIR / "assets/KopiKita_Coffee_Shop_Logo.png"

AI_LOGO = ROOT_DIR / "assets/KopiKita_AI_Logo.png"



load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")



# ============================================================

# COLOR PALETTE

# ============================================================

BG = "#F8F4EE"

WHITE = "#FFFFFF"

CREAM = "#F1E4D0"

CREAM_LIGHT = "#FBF8F3"

SIDEBAR = "#4A2818"

BROWN_DARK = "#4A2818"

BROWN_MID = "#70452E"

BROWN = "#70452E"

BROWN_LIGHT = "#A97855"

GOLD = "#C49A5A"

TEXT = "#2F241F"

TEXT_MUTED = "#776B64"

BORDER = "#E5D7C7"

GREEN = "#547A5C"

RED = "#A85245"



# ============================================================

# HELPERS

# ============================================================

def money(value):

    return f"Rp {value:,.0f}"





def pct(value):

    return f"{value:.2f}%"





def load_logo_base64(path: Path) -> str:

    if not path.exists():

        return ""

    return base64.b64encode(path.read_bytes()).decode("utf-8")





def render_html(body: str):

    st.html(body)





def chart_layout(fig, height=390):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor=WHITE,

        height=height,

        margin=dict(l=42, r=24, t=24, b=48),

        font=dict(color=TEXT, family="Arial, sans-serif", size=12),

        hoverlabel=dict(bgcolor=WHITE, font_color=TEXT),

        legend=dict(font=dict(color=TEXT)),

    )

    return fig





def section_title(title):

    render_html(

        f"""

        <div class="section-title-custom">{html.escape(title)}</div>

        """

    )





def card_html(label, value, note="", icon=""):

    icon_html = f'<span class="card-icon">{icon}</span>' if icon else ""

    return f"""

    <div class="dashboard-card">

        <div class="card-label">{icon_html}{html.escape(label)}</div>

        <div class="card-value">{html.escape(str(value))}</div>

        {f'<div class="card-note">{html.escape(note)}</div>' if note else ''}

    </div>

    """





def insight_html(label, name, value, note="", icon=""):

    return f"""

    <div class="insight-card">

        <div class="insight-label">{icon} {html.escape(label)}</div>

        <div class="insight-name">{html.escape(str(name))}</div>

        <div class="insight-value">{html.escape(str(value))}</div>

        {f'<div class="insight-note">{html.escape(note)}</div>' if note else ''}

    </div>

    """





# ============================================================

# GLOBAL CSS

# ============================================================

ai_logo_base64 = load_logo_base64(AI_LOGO)

coffee_logo_base64 = load_logo_base64(COFFEE_LOGO)



st.markdown(

    f"""

    <style>

    .stApp {{

        background: {BG};

        color: {TEXT};

    }}



    [data-testid="stHeader"] {{

        background: transparent;

    }}



    #MainMenu, footer, [data-testid="stToolbar"] {{

        visibility: hidden;

    }}



    section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {{

        max-width: 1500px;

        padding-top: 2.2rem;

        padding-bottom: 5rem;

        padding-left: 2.8rem;

        padding-right: 2.8rem;

    }}



    h1, h2, h3, h4 {{

        color: {BROWN_DARK} !important;

    }}



    /* ========================================================
       CUSTOM KOPIKITA SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }}

    .st-key-kopikita_custom_sidebar {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 320px !important;
        height: 100vh !important;
        z-index: 999998 !important;
        box-sizing: border-box !important;
        padding: 24px 22px 22px 22px !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        background: {SIDEBAR} !important;
        color: {WHITE} !important;
        box-shadow: 8px 0 28px rgba(47,36,31,.16) !important;
    }}
    .st-key-kopikita_custom_sidebar > div {{ width: 100% !important; }}
    .st-key-kopikita_custom_sidebar * {{ color: {WHITE}; }}
    .st-key-kopikita_sidebar_close {{ position: absolute !important; top: 16px !important; right: 16px !important; width: 38px !important; height: 38px !important; z-index: 10 !important; }}
    .st-key-kopikita_sidebar_close button {{ width: 38px !important; height: 38px !important; min-width: 38px !important; padding: 0 !important; border-radius: 50% !important; border: 1px solid rgba(255,255,255,.22) !important; background: rgba(255,255,255,.08) !important; color: #FFFFFF !important; font-size: 20px !important; }}
    .st-key-kopikita_sidebar_reopen {{ position: fixed !important; top: 12px !important; left: 12px !important; width: 58px !important; height: 58px !important; z-index: 2147483647 !important; }}
    .st-key-kopikita_sidebar_reopen button {{ width: 58px !important; height: 58px !important; min-width: 58px !important; min-height: 58px !important; padding: 0 !important; border-radius: 50% !important; border: 3px solid #FFFFFF !important; background-color: #4A2818 !important; background-image: url("data:image/png;base64,{coffee_logo_base64}") !important; background-repeat: no-repeat !important; background-position: center !important; background-size: 44px 44px !important; box-shadow: 0 4px 14px rgba(74,40,24,.25) !important; color: transparent !important; cursor: pointer !important; }}
    .st-key-kopikita_sidebar_reopen button p, .st-key-kopikita_sidebar_reopen button span {{ color: transparent !important; }}
    .sidebar-logo-wrap {{ width: 88px; height: 88px; border-radius: 50%; background: {WHITE}; display: flex; align-items: center; justify-content: center; margin: 24px auto 18px auto; box-shadow: 0 8px 20px rgba(0,0,0,.16); overflow: hidden; }}
    .sidebar-logo-wrap img {{ width: 72px; height: 72px; object-fit: contain; }}
    .sidebar-brand {{ font-size: 25px; font-weight: 800; text-align: left; color: {WHITE}; margin: 0 0 4px 0; }}
    .sidebar-subtitle {{ font-size: 13px; color: rgba(255,255,255,.72); margin-bottom: 28px; }}
    .sidebar-divider {{ height: 1px; background: rgba(255,255,255,.18); margin: 0 0 26px 0; }}
    .sidebar-menu-title {{ color: rgba(255,255,255,.68); font-size: 11px; font-weight: 800; letter-spacing: 1px; margin: 0 0 8px 0; text-transform: uppercase; }}
    .st-key-kopikita_custom_sidebar [data-testid="stRadio"] > div {{ gap: 2px !important; }}
    .st-key-kopikita_custom_sidebar [data-testid="stRadio"] label {{ border-radius: 9px !important; padding: 7px 8px !important; margin: 1px 0 !important; }}
    .st-key-kopikita_custom_sidebar [data-testid="stRadio"] label:hover {{ background: rgba(255,255,255,.08) !important; }}
    .st-key-kopikita_custom_sidebar [data-testid="stRadio"] label p {{ font-size: 14px !important; font-weight: 500 !important; }}
    .st-key-kopikita_custom_sidebar [data-testid="stRadio"] [role="radio"] {{ width: 17px !important; height: 17px !important; }}
    .sidebar-info {{ display: block !important; visibility: visible !important; margin-top: 20px; border: 1px solid rgba(255,255,255,.22); border-radius: 13px; padding: 16px; background: rgba(255,255,255,.06); }}
    .sidebar-info-title {{ font-size: 12px; font-weight: 800; margin-bottom: 12px; }}
    .sidebar-info-text {{ font-size: 12px; line-height: 1.65; color: rgba(255,255,255,.86); }}

    /* ========================================================

       MAIN HEADER

       ======================================================== */

    .main-page-title {{

        font-size: 31px;

        line-height: 1.15;

        font-weight: 800;

        color: {BROWN_DARK};

        margin-top: 12px;

    }}



    .main-page-subtitle {{

        color: {TEXT_MUTED};

        font-size: 14px;

        margin-top: 8px;

        margin-bottom: 44px;

    }}



    .section-title-custom {{

        font-size: 20px;

        font-weight: 800;

        color: {BROWN_DARK};

        margin-top: 30px;

        margin-bottom: 16px;

    }}



    /* ========================================================

       CARDS

       ======================================================== */

    .dashboard-card, .insight-card {{

        background: {WHITE};

        border: 1px solid {BORDER};

        border-radius: 16px;

        box-shadow: 0 5px 18px rgba(74,40,24,.055);

    }}



    .dashboard-card {{

        padding: 21px;

        min-height: 125px;

    }}



    .card-label {{

        font-size: 11px;

        font-weight: 800;

        letter-spacing: .8px;

        text-transform: uppercase;

        color: {TEXT_MUTED};

    }}



    .card-icon {{

        margin-right: 5px;

    }}



    .card-value {{

        font-size: 27px;

        font-weight: 800;

        color: {BROWN_DARK};

        margin-top: 12px;

    }}



    .card-note {{

        font-size: 12px;

        color: {TEXT_MUTED};

        margin-top: 7px;

    }}



    .insight-card {{

        padding: 20px;

        min-height: 160px;

    }}



    .insight-label {{

        font-size: 11px;

        font-weight: 800;

        letter-spacing: .7px;

        text-transform: uppercase;

        color: {TEXT_MUTED};

    }}



    .insight-name {{

        font-size: 18px;

        font-weight: 800;

        color: {BROWN_DARK};

        margin-top: 12px;

    }}



    .insight-value {{

        font-size: 20px;

        font-weight: 800;

        color: {BROWN};

        margin-top: 8px;

    }}



    .insight-note {{

        font-size: 12px;

        color: {TEXT_MUTED};

        margin-top: 6px;

    }}



    /* ========================================================

       CHART BOX

       ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {{

        background: {WHITE} !important;

        border: 1px solid {BORDER} !important;

        border-radius: 16px !important;

        box-shadow: 0 5px 18px rgba(74,40,24,.045) !important;

    }}



    /* ========================================================

       AI FLOATING BUTTON

       ======================================================== */

    [class*="st-key-ai_open"] {{

        position: fixed !important;

        right: 25px !important;

        bottom: 25px !important;

        z-index: 1000000 !important;

    }}



    [class*="st-key-ai_open"] button {{

        width: 64px !important;

        height: 64px !important;

        min-width: 64px !important;

        padding: 0 !important;

        border-radius: 50% !important;

        border: 3px solid {WHITE} !important;

        background-color: {BROWN_DARK} !important;

        background-image: url("data:image/png;base64,{ai_logo_base64}") !important;

        background-size: 76% !important;

        background-position: center !important;

        background-repeat: no-repeat !important;

        box-shadow: 0 8px 24px rgba(47,36,31,.25) !important;

        color: transparent !important;

        transition: transform .18s ease, box-shadow .18s ease !important;

    }}



    [class*="st-key-ai_open"] button:hover {{

        transform: scale(1.07);

        box-shadow: 0 11px 30px rgba(47,36,31,.32) !important;

    }}



    [class*="st-key-ai_open"] button p,

    [class*="st-key-ai_open"] button span {{

        color: transparent !important;

    }}









    /* ========================================================

    AI DIALOG, THEME-INDEPENDENT

    ======================================================== */



    div[data-testid="stDialog"]:has(.kopikita-ai-marker) {{

        align-items: flex-start !important;

        justify-content: flex-end !important;

        padding: 0 !important;

    }}



    /* Main dialog */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker) div[role="dialog"] {{

        width: 27vw !important;

        max-width: 430px !important;

        min-width: 370px !important;

        height: 76vh !important;

        max-height: 760px !important;

        min-height: 560px !important;

        margin: 12vh 18px 0 0 !important;



        background: #FFFFFF !important;

        background-color: #FFFFFF !important;



        color: #2F241F !important;



        border: 1px solid #E5D7C7 !important;

        border-radius: 18px !important;



        box-shadow: -10px 12px 36px rgba(47,36,31,.18) !important;

        overflow: hidden !important;



        color-scheme: light !important;

    }}



    /* Force light color scheme for everything inside AI dialog */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker) div[role="dialog"] * {{

        color-scheme: light !important;

    }}



    /* Dialog content wrapper */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker) div[role="dialog"] > div {{

        height: 100% !important;

        overflow: hidden !important;

        background: #FFFFFF !important;

    }}



    /* Dialog header */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stDialogHeader"] {{

        background: #FFFFFF !important;

        color: #4A2818 !important;

    }}



    /* Dialog title */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stDialogHeader"] * {{

        color: #4A2818 !important;

    }}



    /* Close button */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stDialogHeader"] button {{

        color: #4A2818 !important;

        background: transparent !important;

    }}



    /* Remove Streamlit default container styling */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stVerticalBlockBorderWrapper"] {{

        border: none !important;

        box-shadow: none !important;

        background: transparent !important;

    }}



    /* Chat message cards */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] {{

        background: #FBF8F3 !important;

        background-color: #FBF8F3 !important;



        border: 1px solid #E5D7C7 !important;

        border-radius: 12px !important;



        padding: 10px 12px !important;

        margin-bottom: 9px !important;



        color: #2F241F !important;

    }}



    /* Chat message text */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] p,

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] li,

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] strong,

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] em {{

        color: #2F241F !important;

    }}



    /* Chat message markdown container */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{

        color: #2F241F !important;

    }}



    /* Chat input container */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatInput"] {{

        position: sticky !important;

        bottom: 0 !important;

        z-index: 30 !important;



        background: #FFFFFF !important;

        background-color: #FFFFFF !important;



        border-color: #E5D7C7 !important;



        padding-top: 8px !important;

        padding-bottom: 4px !important;

    }}



    /* Chat input field */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatInput"] textarea {{

        background: #FBF8F3 !important;

        background-color: #FBF8F3 !important;



        color: #2F241F !important;



        border: 1px solid #E5D7C7 !important;

    }}



    /* Placeholder text */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatInput"] textarea::placeholder {{

        color: #776B64 !important;

        opacity: 1 !important;

    }}



    /* Input send button */

    div[data-testid="stDialog"]:has(.kopikita-ai-marker)

    [data-testid="stChatInput"] button {{

        color: #4A2818 !important;

        background: transparent !important;

    }}



    /* Custom AI header */

    .ai-mini-header {{

        display: flex;

        align-items: center;

        gap: 10px;

        padding: 1px 0 12px 0;

        border-bottom: 1px solid #E5D7C7;

        margin-bottom: 10px;

        background: #FFFFFF !important;

    }}



    .ai-mini-logo {{

        width: 38px;

        height: 38px;

        border-radius: 50%;

        background: #4A2818 !important;

        border: 2px solid #FFFFFF;

        box-shadow: 0 3px 10px rgba(47,36,31,.14);



        display: flex;

        align-items: center;

        justify-content: center;



        overflow: hidden;

        flex: 0 0 auto;

    }}



    .ai-mini-logo img {{

        width: 76%;

        height: 76%;

        object-fit: contain;

    }}



    .ai-mini-title {{

        font-size: 16px;

        font-weight: 800;

        color: #4A2818 !important;

    }}



    .ai-mini-subtitle {{

        font-size: 11px;

        color: #776B64 !important;

        margin-top: 2px;

    }}



    @media (max-width: 800px) {{

        section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {{

            padding-left: *1rem*;

            padding-right: *1rem*;

        }}





        div[data-testid="stDialog"]:has(.kopikita-ai-marker) div[role="dialog"] {{

            width: calc(100vw - 20px) !important;

            max-width: calc(100vw - 20px) !important;

            min-width: 0 !important;

            height: 82vh !important;

            max-height: 82vh !important;

            min-height: 0 !important;

            margin: 9vh 10px 0 0 !important;

        }}



        [class*="st-key-ai_open"] {{

            right: 16px !important;

            bottom: 16px !important;

        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,

)



# ============================================================

if st.session_state.kopikita_sidebar_open:
    st.markdown("""
    <style>
    section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
        padding-left: 350px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# LOAD DATA

# ============================================================

@st.cache_data

def load_data():

    if not DATA_PATH.exists():

        raise FileNotFoundError(

            f"File data tidak ditemukan: {DATA_PATH}. "

            "Pastikan sales_data.csv berada di folder data."

        )



    df = pd.read_csv(DATA_PATH)

    required_columns = {

        "transaction_id", "date", "time", "outlet", "product",

        "category", "quantity", "total_sales"

    }

    missing = required_columns.difference(df.columns)

    if missing:

        raise ValueError(

            "Kolom berikut tidak ditemukan pada sales_data.csv: "

            + ", ".join(sorted(missing))

        )



    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce").fillna(0)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)

    df["time"] = df["time"].astype(str)

    df["hour"] = pd.to_datetime(df["time"], errors="coerce", format="%H:%M:%S").dt.hour



    missing_hour = df["hour"].isna()

    if missing_hour.any():

        df.loc[missing_hour, "hour"] = pd.to_datetime(

            df.loc[missing_hour, "time"], errors="coerce"

        ).dt.hour



    df = df.dropna(subset=["date"]).copy()

    df["hour"] = df["hour"].fillna(0).astype(int)

    df["month_period"] = df["date"].dt.to_period("M")

    df["weekday"] = df["date"].dt.day_name()

    return df





try:

    df = load_data()

except Exception as exc:

    st.error(str(exc))

    st.stop()



# ============================================================

# BUSINESS CALCULATIONS

# ============================================================

total_sales = df["total_sales"].sum()

transactions = df["transaction_id"].nunique()

total_quantity = df["quantity"].sum()

aov = total_sales / transactions if transactions else 0

asp = total_sales / total_quantity if total_quantity else 0



product_sales = df.groupby("product")["total_sales"].sum().sort_values(ascending=False)

outlet_sales = df.groupby("outlet")["total_sales"].sum().sort_values(ascending=False)

category_sales = df.groupby("category")["total_sales"].sum().sort_values(ascending=False)

monthly_sales = df.groupby("month_period")["total_sales"].sum().sort_index()

hourly_sales = df.groupby("hour")["total_sales"].sum().sort_index()

daily_sales = df.groupby("weekday")["total_sales"].sum()



# Ensure chronological weekday order.

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

daily_sales = daily_sales.reindex([d for d in weekday_order if d in daily_sales.index])



# Common metrics.

top_product = product_sales.index[0]

top_product_sales = product_sales.iloc[0]

top_product_contribution = top_product_sales / total_sales * 100 if total_sales else 0

top_outlet = outlet_sales.index[0]

top_outlet_sales = outlet_sales.iloc[0]

peak_hour = int(hourly_sales.idxmax())

peak_hour_sales = hourly_sales.max()

average_monthly_sales = monthly_sales.mean()

lowest_month_period = monthly_sales.idxmin()

lowest_month_sales = monthly_sales.min()

lowest_month_gap = (

    (average_monthly_sales - lowest_month_sales) / average_monthly_sales * 100

    if average_monthly_sales else 0

)



month_id = {

    "January": "Januari", "February": "Februari", "March": "Maret",

    "April": "April", "May": "Mei", "June": "Juni",

    "July": "Juli", "August": "Agustus", "September": "September",

    "October": "Oktober", "November": "November", "December": "Desember",

}

weekday_id = {

    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",

    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu",

}



# ============================================================
# CUSTOM SIDEBAR NAVIGATION
# ============================================================
if st.session_state.kopikita_sidebar_open:
    with st.container(key="kopikita_custom_sidebar"):
        if st.button("×", key="kopikita_sidebar_close", help="Tutup sidebar"):
            st.session_state.kopikita_sidebar_open = False
            st.rerun()

        if coffee_logo_base64:
            st.markdown(f'<div class="sidebar-logo-wrap"><img src="data:image/png;base64,{coffee_logo_base64}"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sidebar-logo-wrap">☕</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-brand">KopiKita</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subtitle">Sales Performance</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-menu-title">Main Menu</div>', unsafe_allow_html=True)

        page = st.radio(
            "Navigasi",
            ["Overview", "Product Performance", "Outlet Performance", "Time Analysis", "Business Alerts"],
            index=0,
            label_visibility="collapsed",
            key="kopikita_page_radio",
        )

        previous_page = st.session_state.get("previous_page")
        if previous_page is not None and page != previous_page:
            st.session_state.ai_dialog_open = False
        st.session_state.previous_page = page

        st.markdown(
            """
            <div class="sidebar-info">
                <div class="sidebar-info-title">Business Intelligence</div>
                <div class="sidebar-info-text">
                    Dashboard analisis performa penjualan untuk membantu manajemen KopiKita
                    mengambil keputusan berbasis data.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    with st.container(key="kopikita_sidebar_reopen"):
        if st.button(" ", key="kopikita_sidebar_reopen_button", help="Buka sidebar"):
            st.session_state.kopikita_sidebar_open = True
            st.rerun()
    page = st.session_state.get("kopikita_page", "Overview")

st.session_state.kopikita_page = page

# ============================================================
# PAGE HEADER
# ============================================================


# PAGE HEADER

# ============================================================

page_titles = {

    "Overview": ("Overview Penjualan", "Ringkasan performa bisnis KopiKita berdasarkan data transaksi."),

    "Product Performance": ("Product Performance", "Analisis performa penjualan berdasarkan produk KopiKita."),

    "Outlet Performance": ("Outlet Performance", "Perbandingan performa penjualan setiap outlet KopiKita."),

    "Time Analysis": ("Time Analysis", "Analisis pola penjualan berdasarkan waktu dan hari."),

    "Business Alerts": ("Business Alerts", "Kondisi bisnis yang perlu diperhatikan berdasarkan data penjualan."),

}

page_title, page_subtitle = page_titles[page]



render_html(

    f"""

    <div class="main-page-title">{html.escape(page_title)}</div>

    <div class="main-page-subtitle">{html.escape(page_subtitle)}</div>

    """

)



# ============================================================

# OVERVIEW

# ============================================================

if page == "Overview":

    section_title("Business Overview")

    k1, k2, k3, k4 = st.columns(4)

    kpis = [

        (k1, "Total Sales", money(total_sales), "Total penjualan"),

        (k2, "Transactions", f"{transactions:,.0f}", "Total transaksi"),

        (k3, "Quantity", f"{total_quantity:,.0f}", "Total quantity terjual"),

        (k4, "Average Order Value", money(aov), "Rata-rata nilai transaksi"),

    ]

    for col, label, value, note in kpis:

        with col:

            render_html(card_html(label, value, note))



    section_title("Performance Snapshot")

    s1, s2, s3 = st.columns(3)

    snapshots = [

        (s1, "Top Product", top_product, money(top_product_sales), f"Kontribusi {pct(top_product_contribution)} dari total sales", "🏆"),

        (s2, "Top Outlet", top_outlet, money(top_outlet_sales), "Outlet dengan sales tertinggi", "🏪"),

        (s3, "Peak Hour", f"{peak_hour:02d}:00", money(peak_hour_sales), "Jam dengan sales tertinggi", "⏰"),

    ]

    for col, label, name, value, note, icon in snapshots:

        with col:

            render_html(insight_html(label, name, value, note, icon))



    section_title("Monthly Sales")

    monthly_df = monthly_sales.reset_index(name="Sales")

    monthly_df["Bulan"] = monthly_df["month_period"].apply(

        lambda x: month_id.get(x.strftime("%B"), x.strftime("%Y-%m"))

    )

    fig_month = px.line(monthly_df, x="Bulan", y="Sales", markers=True)

    fig_month.update_traces(

        line=dict(color=BROWN, width=3),

        marker=dict(color=BROWN, size=8),

        hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

    )

    chart_layout(fig_month, 390)

    fig_month.update_layout(

        xaxis=dict(title="Bulan", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_month, width="stretch", config={"displayModeBar": False})



    p_col, o_col = st.columns(2)

    with p_col:

        section_title("Product Performance")

        product_df = product_sales.head(10).sort_values().reset_index()

        product_df.columns = ["Product", "Sales"]

        fig_product = px.bar(product_df, x="Sales", y="Product", orientation="h")

        fig_product.update_traces(

            marker_color=BROWN,

            hovertemplate="%{y}<br>Sales: Rp %{x:,.0f}<extra></extra>",

        )

        chart_layout(fig_product, 430)

        fig_product.update_layout(

            xaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

            yaxis=dict(title="Produk", categoryorder="total ascending"),

        )

        with st.container(border=True):

            st.plotly_chart(fig_product, width="stretch", config={"displayModeBar": False})



    with o_col:

        section_title("Outlet Performance")

        outlet_df = outlet_sales.sort_values().reset_index()

        outlet_df.columns = ["Outlet", "Sales"]

        fig_outlet = px.bar(outlet_df, x="Outlet", y="Sales")

        fig_outlet.update_traces(

            marker_color=BROWN_LIGHT,

            hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

        )

        chart_layout(fig_outlet, 430)

        fig_outlet.update_layout(

            xaxis=dict(title="Outlet", tickangle=-20, showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_outlet, width="stretch", config={"displayModeBar": False})



# ============================================================

# PRODUCT PERFORMANCE

# ============================================================

elif page == "Product Performance":

    section_title("Product Sales")

    p_col, c_col = st.columns([1.7, 1])



    with p_col:

        product_df = product_sales.head(10).sort_values().reset_index()

        product_df.columns = ["Product", "Sales"]

        fig_product = px.bar(product_df, x="Sales", y="Product", orientation="h")

        fig_product.update_traces(

            marker_color=BROWN,

            hovertemplate="%{y}<br>Sales: Rp %{x:,.0f}<extra></extra>",

        )

        chart_layout(fig_product, 520)

        fig_product.update_layout(

            xaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

            yaxis=dict(title="Produk", categoryorder="total ascending"),

        )

        with st.container(border=True):

            st.plotly_chart(fig_product, width="stretch", config={"displayModeBar": False})



    with c_col:

        section_title("Top Product")

        render_html(card_html("Top Product", top_product, f"{money(top_product_sales)} | kontribusi {pct(top_product_contribution)}"))

        section_title("Top 5 Products")

        top5 = product_sales.head(5)

        rows = "".join(

            f"<tr><td>{html.escape(str(name))}</td><td>{money(value)}</td><td>{pct(value/total_sales*100)}</td></tr>"

            for name, value in top5.items()

        )

        render_html(

            f"""

            <div class="dashboard-card" style="padding:0;overflow:hidden;">

                <table style="width:100%;border-collapse:collapse;font-size:12px;">

                    <thead><tr style="background:{CREAM_LIGHT};">

                        <th style="text-align:left;padding:10px;">Product</th>

                        <th style="text-align:right;padding:10px;">Sales</th>

                        <th style="text-align:right;padding:10px;">Contribution</th>

                    </tr></thead>

                    <tbody>{rows}</tbody>

                </table>

            </div>

            """

        )



# ============================================================

# OUTLET PERFORMANCE

# ============================================================

elif page == "Outlet Performance":

    section_title("Outlet Sales")

    o_col, d_col = st.columns([1.6, 1])



    with o_col:

        outlet_df = outlet_sales.sort_values().reset_index()

        outlet_df.columns = ["Outlet", "Sales"]

        fig_outlet = px.bar(outlet_df, x="Outlet", y="Sales")

        fig_outlet.update_traces(

            marker_color=BROWN,

            hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

        )

        chart_layout(fig_outlet, 470)

        fig_outlet.update_layout(

            xaxis=dict(title="Outlet", tickangle=-20, showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_outlet, width="stretch", config={"displayModeBar": False})



    with d_col:

        section_title("Outlet Ranking")

        rows = "".join(

            f"<tr><td>{i}</td><td>{html.escape(str(name))}</td><td style='text-align:right'>{money(value)}</td></tr>"

            for i, (name, value) in enumerate(outlet_sales.items(), start=1)

        )

        render_html(

            f"""

            <div class="dashboard-card" style="padding:0;overflow:hidden;">

                <table style="width:100%;border-collapse:collapse;font-size:12px;">

                    <thead><tr style="background:{CREAM_LIGHT};">

                        <th style="padding:10px;text-align:left;">#</th>

                        <th style="padding:10px;text-align:left;">Outlet</th>

                        <th style="padding:10px;text-align:right;">Sales</th>

                    </tr></thead>

                    <tbody>{rows}</tbody>

                </table>

            </div>

            """

        )



    section_title("Category Performance")

    category_df = category_sales.sort_values().reset_index()

    category_df.columns = ["Category", "Sales"]

    fig_category = px.bar(category_df, x="Sales", y="Category", orientation="h")

    fig_category.update_traces(

        marker_color=GOLD,

        hovertemplate="%{y}<br>Sales: Rp %{x:,.0f}<extra></extra>",

    )

    chart_layout(fig_category, 370)

    fig_category.update_layout(

        xaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        yaxis=dict(title="Kategori"),

    )

    with st.container(border=True):

        st.plotly_chart(fig_category, width="stretch", config={"displayModeBar": False})



# ============================================================

# TIME ANALYSIS

# ============================================================

elif page == "Time Analysis":

    # Outlet filter khusus untuk analisis waktu.

    # Default = seluruh outlet, sehingga angka tetap konsisten dengan

    # analisis waktu agregat sebelumnya.

    outlet_options = ["All Outlets"] + sorted(df["outlet"].dropna().unique().tolist())

    selected_outlet = st.selectbox(

        "Outlet",

        outlet_options,

        index=0,

        key="time_analysis_outlet",

    )



    if selected_outlet == "All Outlets":

        time_df = df.copy()

        outlet_label = "All Outlets"

    else:

        time_df = df[df["outlet"] == selected_outlet].copy()

        outlet_label = selected_outlet



    # Recalculate every time-based metric from the selected outlet.

    time_df["hour"] = pd.to_datetime(time_df["time"], errors="coerce").dt.hour

    hourly_time = time_df.groupby("hour")["total_sales"].sum().sort_index()

    daily_time = time_df.groupby("weekday")["total_sales"].sum().reindex(

        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    ).fillna(0)

    period_time = (

        time_df.assign(

            period_type=time_df["weekday"].isin(["Saturday", "Sunday"]).map(

                {True: "Weekend", False: "Weekday"}

            )

        )

        .groupby("period_type")["total_sales"]

        .sum()

        .reindex(["Weekday", "Weekend"])

        .fillna(0)

    )

    monthly_time = (

        time_df.groupby(time_df["date"].dt.to_period("M"))["total_sales"]

        .sum()

        .sort_index()

    )



    section_title(f"Sales by Hour | {outlet_label}")

    st.caption("Total sales berdasarkan jam transaksi untuk outlet yang dipilih.")

    hourly_df = hourly_time.reset_index()

    hourly_df.columns = ["Hour", "Sales"]

    hourly_df["Jam"] = hourly_df["Hour"].apply(lambda x: f"{int(x):02d}:00")



    fig_hour = px.bar(hourly_df, x="Jam", y="Sales")

    fig_hour.update_traces(

        marker_color=BROWN,

        hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

    )

    chart_layout(fig_hour, 430)

    fig_hour.update_layout(

        xaxis=dict(title="Jam", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_hour, width="stretch", config={"displayModeBar": False})



    d_col, w_col = st.columns(2)

    with d_col:

        section_title(f"Sales by Day | {outlet_label}")

        day_df = daily_time.reset_index()

        day_df.columns = ["Day", "Sales"]

        day_df["Hari"] = day_df["Day"].map(weekday_id)

        fig_day = px.bar(day_df, x="Hari", y="Sales")

        fig_day.update_traces(

            marker_color=BROWN_LIGHT,

            hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

        )

        chart_layout(fig_day, 370)

        fig_day.update_layout(

            xaxis=dict(title="Hari", showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_day, width="stretch", config={"displayModeBar": False})



    with w_col:

        section_title(f"Weekday vs Weekend | {outlet_label}")

        period_df = period_time.reset_index()

        period_df.columns = ["Period", "Sales"]

        fig_period = px.bar(period_df, x="Period", y="Sales")

        fig_period.update_traces(

            marker_color=GOLD,

            hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

        )

        chart_layout(fig_period, 370)

        fig_period.update_layout(

            xaxis=dict(title="Periode", showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_period, width="stretch", config={"displayModeBar": False})



    section_title(f"Monthly Sales | {outlet_label}")

    monthly_df = monthly_time.reset_index(name="Sales")

    monthly_df["Bulan"] = monthly_df["date"].apply(

        lambda x: month_id.get(x.strftime("%B"), x.strftime("%Y-%m"))

    )

    fig_month = px.line(monthly_df, x="Bulan", y="Sales", markers=True)

    fig_month.update_traces(

        line=dict(color=BROWN, width=3),

        marker=dict(color=BROWN, size=8),

        hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

    )

    chart_layout(fig_month, 390)

    fig_month.update_layout(

        xaxis=dict(title="Bulan", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_month, width="stretch", config={"displayModeBar": False})



# ============================================================

elif page == "Time Analysis":

    section_title("Sales by Hour")

    hourly_df = hourly_sales.reset_index()

    hourly_df.columns = ["Hour", "Sales"]

    hourly_df["Jam"] = hourly_df["Hour"].apply(lambda x: f"{int(x):02d}:00")



    fig_hour = px.bar(hourly_df, x="Jam", y="Sales")

    fig_hour.update_traces(

        marker_color=BROWN,

        hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>",

    )

    chart_layout(fig_hour, 430)

    fig_hour.update_layout(

        xaxis=dict(title="Jam", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_hour, width="stretch", config={"displayModeBar": False})



    d_col, w_col = st.columns(2)

    with d_col:

        section_title("Sales by Day")

        day_df = daily_sales.reset_index()

        day_df.columns = ["Day", "Sales"]

        day_df["Hari"] = day_df["Day"].map(weekday_id)

        fig_day = px.bar(day_df, x="Hari", y="Sales")

        fig_day.update_traces(marker_color=BROWN_LIGHT, hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>")

        chart_layout(fig_day, 370)

        fig_day.update_layout(

            xaxis=dict(title="Hari", showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_day, width="stretch", config={"displayModeBar": False})



    with w_col:

        section_title("Weekday vs Weekend")

        df_time = df.copy()

        df_time["period_type"] = df_time["weekday"].isin(["Saturday", "Sunday"]).map({True: "Weekend", False: "Weekday"})

        period_sales = df_time.groupby("period_type")["total_sales"].sum().reindex(["Weekday", "Weekend"])

        period_df = period_sales.reset_index()

        period_df.columns = ["Period", "Sales"]

        fig_period = px.bar(period_df, x="Period", y="Sales")

        fig_period.update_traces(marker_color=GOLD, hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>")

        chart_layout(fig_period, 370)

        fig_period.update_layout(

            xaxis=dict(title="Periode", showgrid=False),

            yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

        )

        with st.container(border=True):

            st.plotly_chart(fig_period, width="stretch", config={"displayModeBar": False})



    section_title("Monthly Sales")

    monthly_df = monthly_sales.reset_index(name="Sales")

    monthly_df["Bulan"] = monthly_df["month_period"].apply(lambda x: month_id.get(x.strftime("%B"), x.strftime("%Y-%m")))

    fig_month = px.line(monthly_df, x="Bulan", y="Sales", markers=True)

    fig_month.update_traces(line=dict(color=BROWN, width=3), marker=dict(color=BROWN, size=8), hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>")

    chart_layout(fig_month, 390)

    fig_month.update_layout(

        xaxis=dict(title="Bulan", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_month, width="stretch", config={"displayModeBar": False})



# ============================================================

# BUSINESS ALERTS

# ============================================================

else:

    section_title("Business Alerts")

    a1, a2, a3 = st.columns(3)

    with a1:

        render_html(card_html("Lowest Month", month_id.get(lowest_month_period.strftime("%B"), str(lowest_month_period)), f"{money(lowest_month_sales)} | {pct(lowest_month_gap)} di bawah rata-rata", "⚠️"))

    with a2:

        render_html(card_html("Top Product", top_product, f"Kontribusi {pct(top_product_contribution)} dari total sales", "⚠️"))

    with a3:

        render_html(card_html("Peak Hour", f"{peak_hour:02d}:00", f"Sales {money(peak_hour_sales)}", "💡"))



    section_title("Alert Details")

    alert_rows = [

        ("⚠️", f"{month_id.get(lowest_month_period.strftime('%B'), str(lowest_month_period))} berada {lowest_month_gap:.2f}% di bawah rata-rata sales bulanan."),

        ("⚠️", f"{top_product} menyumbang {top_product_contribution:.2f}% dari total sales."),

        ("💡", "Peak period berada pada 18:00-20:00 berdasarkan tiga jam dengan sales tertinggi."),

    ]

    for icon, message in alert_rows:

        render_html(

            f"""

            <div style="background:{WHITE};border:1px solid {BORDER};border-radius:14px;padding:16px 18px;margin-bottom:12px;box-shadow:0 4px 14px rgba(74,40,24,.04);">

                <span style="font-size:17px;margin-right:8px;">{icon}</span>

                <span style="font-size:13px;color:{TEXT};">{html.escape(message)}</span>

            </div>

            """

        )



    section_title("Monthly Context")

    monthly_df = monthly_sales.reset_index(name="Sales")

    monthly_df["Bulan"] = monthly_df["month_period"].apply(lambda x: month_id.get(x.strftime("%B"), x.strftime("%Y-%m")))

    fig_month = px.bar(monthly_df, x="Bulan", y="Sales")

    fig_month.update_traces(marker_color=BROWN, hovertemplate="%{x}<br>Sales: Rp %{y:,.0f}<extra></extra>")

    chart_layout(fig_month, 390)

    fig_month.update_layout(

        xaxis=dict(title="Bulan", showgrid=False),

        yaxis=dict(title="Sales (Rp)", gridcolor=BORDER, tickprefix="Rp "),

    )

    with st.container(border=True):

        st.plotly_chart(fig_month, width="stretch", config={"displayModeBar": False})



# ============================================================

# AI CHAT

# ============================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

if "ai_dialog_open" not in st.session_state:

    st.session_state.ai_dialog_open = False



SYSTEM_PROMPT = """

Anda adalah KopiKita AI Sales Performance Assistant.



PERAN:

Anda membantu manajemen KopiKita memahami performa penjualan berdasarkan data bisnis yang tersedia.



ATURAN UTAMA:

1. Gunakan hanya data yang tersedia dalam BUSINESS CONTEXT.

2. Jangan mengarang angka, produk, outlet, tanggal, atau fakta bisnis yang tidak tersedia.

3. Jika data yang diperlukan tidak tersedia, katakan bahwa data tersebut belum tersedia.

4. Bedakan antara FAKTA dan INTERPRETASI.

5. Jika memberikan rekomendasi, jelaskan alasan berdasarkan data.

6. Jangan menyatakan hubungan sebab-akibat jika data tidak cukup untuk membuktikannya.

7. Gunakan bahasa Indonesia yang profesional, ringkas, dan mudah dipahami oleh manajemen.

8. Fokus pada konteks bisnis KopiKita.

9. Jika pertanyaan membutuhkan perhitungan, gunakan angka yang tersedia dalam BUSINESS CONTEXT.

10. Jangan menyimpulkan tren, seasonality, hubungan sebab-akibat, atau perubahan performa jika data belum cukup.

11. Jika membandingkan kondisi, tampilkan perbandingan yang relevan sebelum kesimpulan.

12. Untuk pertanyaan analitis, jelaskan konteks angka yang mendukung kesimpulan.

13. Jangan menyebut trafik, jumlah pelanggan, atau kunjungan jika data tersebut tidak tersedia.

14. Tandai rekomendasi umum yang membutuhkan data di luar BUSINESS CONTEXT.



FORMAT:

Jika membutuhkan analisis:

1. Temuan

2. Analisis

3. Rekomendasi



Jika hanya membutuhkan fakta, jawab langsung dan ringkas.

"""





def ask_gemini(question: str) -> str:

    USER_FRIENDLY_ERROR = (

        "🤖 **KopiKita AI sedang mengalami gangguan sementara.**\n\n"

        "Sistem belum dapat memproses pertanyaan Anda saat ini. "

        "Silakan coba kembali beberapa saat lagi.\n\n"

        "*Fitur dashboard dan analisis data tetap dapat digunakan seperti biasa.*"

    )



    if not API_KEY:

        print("[KopiKita AI] GEMINI_API_KEY tidak ditemukan.")

        return USER_FRIENDLY_ERROR



    try:

        client = genai.Client(api_key=API_KEY)



        prompt = f"""

{SYSTEM_PROMPT}



========================================

BUSINESS CONTEXT

========================================

{BUSINESS_CONTEXT}



========================================

USER QUESTION

========================================

{question}



Berikan jawaban berdasarkan BUSINESS CONTEXT di atas.

"""



        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt,

        )



        return response.text or "Maaf, KopiKita AI belum dapat memberikan jawaban saat ini."



    except Exception as exc:

        # Error teknis hanya ditampilkan di terminal/log,

        # bukan kepada pengguna.

        print(

            f"[KopiKita AI] API Error: "

            f"{type(exc).__name__}: {exc}"

        )



        return USER_FRIENDLY_ERROR





@st.dialog(

    "KopiKita AI",

    width="small",

    dismissible=True,

    icon=":material/smart_toy:",

)

def ai_chat():

    st.html('<span class="kopikita-ai-marker"></span>')



    if ai_logo_base64:

        render_html(

            f"""

            <div class="ai-mini-header">

                <div class="ai-mini-logo">

                    <img src="data:image/png;base64,{ai_logo_base64}">

                </div>

                <div>

                    <div class="ai-mini-title">KopiKita AI</div>

                    <div class="ai-mini-subtitle">Sales Performance Assistant</div>

                </div>

            </div>

            """

        )

    else:

        render_html(

            f"""

            <div class="ai-mini-header">

                <div>

                    <div class="ai-mini-title">KopiKita AI</div>

                    <div class="ai-mini-subtitle">Sales Performance Assistant</div>

                </div>

            </div>

            """

        )



    # Only this region scrolls. The chat input remains visible below it.

    chat_container = st.container(height=430, border=False)

    history_placeholder = chat_container.empty()



    def render_chat_history(target):

        with target.container():

            if not st.session_state.chat_history:

                render_html(

                    f"""

                    <div style="background:{CREAM_LIGHT};border:1px solid {BORDER};border-radius:12px;padding:13px;color:{TEXT_MUTED};font-size:12px;line-height:1.55;">

                        <b style="color:{BROWN_DARK};">Selamat datang.</b><br>

                        Tanyakan mengenai sales, produk, outlet, jam penjualan, kategori, atau kondisi bulanan KopiKita.

                    </div>

                    """

                )

            else:

                for message in st.session_state.chat_history:

                    with st.chat_message(message["role"]):

                        st.markdown(message["content"])



    render_chat_history(history_placeholder)



    question = st.chat_input(

        "Tanyakan sesuatu tentang performa KopiKita...",

        key="kopikita_chat_input",

    )



    if question and question.strip():

        question = question.strip()

        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.spinner("KopiKita AI sedang menganalisis..."):

            answer = ask_gemini(question)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})



        # Refresh only the scrollable conversation area.

        # No st.rerun() here, so the dialog stays open without closing/reopening.

        render_chat_history(history_placeholder)





# ============================================================

# FLOATING AI BUTTON

# ============================================================

if st.button("", key="ai_open", help="Tanya KopiKita AI"):

    st.session_state.ai_dialog_open = True

    st.rerun()



if st.session_state.ai_dialog_open:

    ai_chat()