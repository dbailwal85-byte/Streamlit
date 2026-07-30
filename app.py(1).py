"""
===============================================================================
AI-Powered E-Commerce Analytics & Sales Forecasting Platform
===============================================================================
File: app.py
Description: Main entry point and orchestrator for the Streamlit application.
             Initializes global session states, injects custom dark mode & blue-accent
             CSS theme, renders the modern landing page, and configures sidebar routing.

Author: Senior Software Architect & UI/UX Engineer
Date: July 2026
===============================================================================
"""

import os
import streamlit as st

# =============================================================================
# 1. GLOBAL PAGE CONFIGURATION (Must be first Streamlit command)
# =============================================================================
st.set_page_config(
    page_title="AI E-Commerce Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/",
        "Report a bug": "https://github.com/",
        "About": "### AI-Powered E-Commerce Analytics Platform v2.0",
    },
)

# =============================================================================
# 2. GLOBAL SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state() -> None:
    """
    Initializes shared application state across all module pages.
    """
    default_states = {
        "raw_data": None,
        "cleaned_data": None,
        "engineered_data": None,
        "data_filename": None,
        "db_connection": None,
        "db_status": False,
        "forecast_model": None,
        "forecast_results": None,
        "kpi_metrics": {},
    }
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# =============================================================================
# 3. GLOBAL DARK MODE & BLUE ACCENT STYLING
# =============================================================================
def inject_custom_styling() -> None:
    """
    Injects responsive dark-mode styling with high-contrast typography,
    glassmorphism effects, blue-accent KPI containers, and polished scrollbars.
    """
    custom_css = """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Dark Theme Background Base */
        .stApp {
            background-color: #0E1117;
            color: #E0E6ED;
        }

        /* Glassmorphic KPI Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(21, 32, 43, 0.7) 0%, rgba(13, 25, 41, 0.8) 100%);
            border: 1px solid rgba(0, 119, 255, 0.25);
            border-top: 4px solid #0077FF;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(8px);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: #00D4FF;
        }
        .metric-label {
            font-size: 0.85rem;
            font-weight: 500;
            color: #8899A6;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #FFFFFF;
        }
        .metric-subtitle {
            font-size: 0.8rem;
            color: #00FF88;
            margin-top: 6px;
        }

        /* Landing Page Hero Header */
        .hero-banner {
            background: linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%);
            padding: 40px;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 82, 212, 0.3);
        }
        .hero-banner h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            color: #FFFFFF;
        }
        .hero-banner p {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0E1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #1E3A8A;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #0077FF;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


inject_custom_styling()

# =============================================================================
# 4. PAGE ROUTING & NAVIGATION MANAGEMENT
# =============================================================================
def render_landing_page() -> None:
    """
    Renders the default landing / home page overview when app.py runs directly.
    """
    st.markdown(
        """
        <div class="hero-banner">
            <h1>🛍️ AI-Powered E-Commerce Analytics Platform</h1>
            <p>An enterprise-grade analytical solution for data understanding, automated data cleaning, exploratory visual discovery, SQL database integration, customer intelligence, and AI sales forecasting.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key Platform Features Showcase
    st.markdown("### 🚀 Core Capabilities")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Data Pipeline</div>
                <div class="metric-value">Automated</div>
                <div class="metric-subtitle">Cleaning, Validation & Engineering</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Business Intelligence</div>
                <div class="metric-value">Interactive</div>
                <div class="metric-subtitle">KPI Dashboards & Customer RFM</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Machine Learning</div>
                <div class="metric-value">Forecasting</div>
                <div class="metric-subtitle">Time-Series & Machine Learning Models</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Workflow Guidance
    st.markdown("### 📋 Recommended Workflow")
    w_col1, w_col2, w_col3, w_col4 = st.columns(4)

    with w_col1:
        st.info("**1. Data Upload**\nUpload raw CSV or Excel datasets.")
    with w_col2:
        st.info("**2. Cleaning & EDA**\nProcess missing values & explore trends.")
    with w_col3:
        st.info("**3. Analytics**\nView Customer, Product & Sales Dashboards.")
    with w_col4:
        st.info("**4. Forecasting**\nTrain models and generate future predictions.")


def main() -> None:
    """
    Main entry point configuring page navigation and sidebar dataset status.
    """
    # Sidebar Header Branding
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 10px 0;">
            <h2 style="margin:0; color:#0077FF;">🛍️ E-Com AI</h2>
            <p style="margin:0; font-size: 0.8rem; color:#8899A6;">v2.0 Enterprise Analytics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Native Streamlit Multi-Page Definition
    pages = {
        "Main": [
            st.Page(render_landing_page, title="Home Page", icon="🏠"),
            st.Page("pages/01_Data_Upload.py", title="Data Upload", icon="📤"),
        ],
        "Pipeline": [
            st.Page("pages/02_Data_Understanding.py", title="Data Understanding", icon="🔍"),
            st.Page("pages/03_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
            st.Page("pages/04_Exploratory_Data_Analysis.py", title="Exploratory Data Analysis", icon="📊"),
        ],
        "Analytics": [
            st.Page("pages/05_Business_Dashboard.py", title="Business Dashboard", icon="📈"),
            st.Page("pages/06_Customer_Analytics.py", title="Customer Analytics", icon="👥"),
            st.Page("pages/07_Product_Analytics.py", title="Product Analytics", icon="📦"),
            st.Page("pages/08_Sales_Analytics.py", title="Sales Analytics", icon="💰"),
        ],
        "Advanced Tools": [
            st.Page("pages/09_SQL_Database.py", title="SQL Database", icon="🗄️"),
            st.Page("pages/10_Sales_Forecasting.py", title="Sales Forecasting", icon="🤖"),
            st.Page("pages/11_Reports.py", title="Reports Generator", icon="📄"),
        ],
    }

    # Navigation runner
    pg = st.navigation(pages)

    # Dataset Status Indicator in Sidebar
    st.sidebar.markdown("### 📌 Data State")
    if st.session_state["raw_data"] is not None:
        st.sidebar.success(f"Raw: Loaded ({st.session_state['raw_data'].shape[0]} rows)")
    else:
        st.sidebar.warning("Raw: No Dataset Uploaded")

    if st.session_state["cleaned_data"] is not None:
        st.sidebar.success(f"Cleaned: Ready ({st.session_state['cleaned_data'].shape[0]} rows)")
    else:
        st.sidebar.info("Cleaned: Pending")

    try:
        pg.run()
    except Exception as e:
        st.error(f"An unexpected error occurred during page execution: {str(e)}")


if __name__ == "__main__":
    main()