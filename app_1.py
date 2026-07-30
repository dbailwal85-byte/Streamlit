import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="AI-Powered E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

.main{
    padding-top:20px;
}

h1,h2,h3{
    color:#0F62FE;
}

.metric{
    background:#f5f5f5;
    padding:15px;
    border-radius:12px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Module",
    (
        "🏠 Home",
        "📂 Data Upload",
        "🧹 Data Cleaning",
        "📊 Exploratory Data Analysis"
    )
)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if page=="🏠 Home":

    st.title("📊 AI-Powered E-Commerce Analytics Platform")

    st.write("""
Welcome to the AI-Powered E-Commerce Analytics Platform.

This application performs

- Data Upload
- Data Cleaning
- Exploratory Data Analysis
- Business Insights
- Sales Forecasting (Coming Soon)
- MySQL Integration (Coming Soon)
    """)

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Modules","4")
    col2.metric("Charts","15+")
    col3.metric("ML Models","Coming")
    col4.metric("Database","MySQL")

# ---------------------------------------------------
# DATA UPLOAD
# ---------------------------------------------------

elif page=="📂 Data Upload":

    st.title("📂 Upload Dataset")

    file=st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv","xlsx"]
    )

    if file:

        if file.name.endswith(".csv"):
            df=pd.read_csv(file)

        else:
            df=pd.read_excel(file)

        st.session_state["df"]=df

        st.success("Dataset Uploaded Successfully")

        st.subheader("Dataset Preview")

        st.dataframe(df)

        st.subheader("Dataset Information")

        col1,col2,col3=st.columns(3)

        col1.metric("Rows",df.shape[0])
        col2.metric("Columns",df.shape[1])
        col3.metric("Missing Values",df.isnull().sum().sum())

        st.subheader("Column Data Types")

        st.dataframe(
            pd.DataFrame({
                "Column":df.columns,
                "Datatype":df.dtypes.astype(str)
            })
        )

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

elif page=="🧹 Data Cleaning":

    st.title("🧹 Data Cleaning")

    if "df" not in st.session_state:

        st.warning("Upload Dataset First")

    else:

        df=st.session_state["df"]

        st.write("Original Shape:",df.shape)

        if st.button("Remove Duplicate Rows"):

            df=df.drop_duplicates()

            st.success("Duplicates Removed")

        if st.button("Fill Missing Numeric Values"):

            numeric=df.select_dtypes(include=np.number).columns

            df[numeric]=df[numeric].fillna(df[numeric].median())

            st.success("Missing Values Filled")

        if st.button("Drop Remaining Missing Values"):

            df=df.dropna()

            st.success("Remaining Missing Values Removed")

        st.write("Updated Shape:",df.shape)

        st.session_state["df"]=df

        st.dataframe(df)

        csv=df.to_csv(index=False)

        st.download_button(
            "Download Clean Dataset",
            csv,
            "clean_dataset.csv",
            "text/csv"
        )

# ---------------------------------------------------
# EDA
# ---------------------------------------------------

elif page=="📊 Exploratory Data Analysis":

    st.title("📊 Exploratory Data Analysis")

    if "df" not in st.session_state:

        st.warning("Upload Dataset First")

    else:

        df=st.session_state["df"]

        st.subheader("Statistical Summary")

        st.dataframe(df.describe())

        numeric=df.select_dtypes(include=np.number).columns.tolist()

        categorical=df.select_dtypes(include="object").columns.tolist()

        # Histogram

        st.subheader("Histogram")

        column=st.selectbox(
            "Select Numeric Column",
            numeric
        )

        fig=px.histogram(
            df,
            x=column,
            nbins=30
        )

        st.plotly_chart(fig,use_container_width=True)

        # Box Plot

        st.subheader("Box Plot")

        fig2=px.box(df,y=column)

        st.plotly_chart(fig2,use_container_width=True)

        # Correlation

        if len(numeric)>=2:

            st.subheader("Correlation Heatmap")

            corr=df[numeric].corr()

            fig3=px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Blues"
            )

            st.plotly_chart(fig3,use_container_width=True)

        # Scatter Plot

        if len(numeric)>=2:

            st.subheader("Scatter Plot")

            x=st.selectbox("X-axis",numeric,key=1)

            y=st.selectbox("Y-axis",numeric,key=2)

            fig4=px.scatter(
                df,
                x=x,
                y=y,
                color=categorical[0] if categorical else None
            )

            st.plotly_chart(fig4,use_container_width=True)

        # Bar Chart

        if len(categorical)>0:

            st.subheader("Category Distribution")

            cat=st.selectbox(
                "Categorical Column",
                categorical
            )

            fig5=px.bar(
                df[cat].value_counts().reset_index(),
                x="index",
                y=cat
            )

            st.plotly_chart(fig5,use_container_width=True)

        st.subheader("Dataset Preview")

        st.dataframe(df)