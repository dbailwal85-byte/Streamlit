import streamlit as st

# ------------------------------
# PAGE CONFIGURATION
# ------------------------------
st.set_page_config(
    page_title="AI-Powered E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# CUSTOM CSS
# ------------------------------
st.markdown("""
<style>
.main{
    padding-top:1rem;
}

.big-font{
    font-size:42px;
    font-weight:bold;
    color:#2E86C1;
}

.sub-font{
    font-size:20px;
    color:gray;
}

.metric-box{
    background-color:#F8F9F9;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "🏠 Home",
        "📂 Data Upload",
        "🧹 Data Cleaning",
        "📊 Exploratory Data Analysis",
        "📈 Business Dashboard",
        "🗄 MySQL Database",
        "🤖 Sales Forecasting",
        "📑 Reports"
    ]
)

# ------------------------------
# HOME PAGE
# ------------------------------
if page == "🏠 Home":

    st.markdown(
        '<p class="big-font">AI-Powered E-Commerce Analytics Platform</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-font">Complete Data Analytics & Sales Forecasting Solution</p>',
        unsafe_allow_html=True
    )

    st.divider()

    col1,col2,col3,col4=st.columns(4)

    with col1:
        st.metric("Orders","15,420","+12%")

    with col2:
        st.metric("Revenue","$245K","+18%")

    with col3:
        st.metric("Customers","4,821","+7%")

    with col4:
        st.metric("Profit","$58K","+14%")

    st.divider()

    st.subheader("Project Overview")

    st.write("""
This application provides a complete E-Commerce Analytics solution.

### Features

- Data Upload
- Data Cleaning
- Exploratory Data Analysis
- Business KPI Dashboard
- Customer Analytics
- Product Analytics
- Sales Forecasting
- MySQL Integration
- Report Generation
""")

    st.info("Select a module from the sidebar to begin.")

# ------------------------------
# DATA UPLOAD
# ------------------------------
elif page == "📂 Data Upload":

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv","xlsx"]
    )

    if uploaded_file:
        st.success("Dataset Uploaded Successfully")

# ------------------------------
# DATA CLEANING
# ------------------------------
elif page == "🧹 Data Cleaning":

    st.title("🧹 Data Cleaning")

    st.write("Cleaning module will be implemented here.")

# ------------------------------
# EDA
# ------------------------------
elif page == "📊 Exploratory Data Analysis":

    st.title("📊 Exploratory Data Analysis")

    st.write("EDA Visualizations")

# ------------------------------
# DASHBOARD
# ------------------------------
elif page == "📈 Business Dashboard":

    st.title("📈 Business Dashboard")

    st.write("Interactive KPI Dashboard")

# ------------------------------
# MYSQL
# ------------------------------
elif page == "🗄 MySQL Database":

    st.title("🗄 MySQL Database")

    st.write("Database Connectivity")

# ------------------------------
# FORECASTING
# ------------------------------
elif page == "🤖 Sales Forecasting":

    st.title("🤖 Sales Forecasting")

    st.write("Machine Learning Predictions")

# ------------------------------
# REPORTS
# ------------------------------
elif page == "📑 Reports":

    st.title("📑 Reports")

    st.write("Generate PDF / Excel Reports")

# ------------------------------
# FOOTER
# ------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Developed by Deepak")