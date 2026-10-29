import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Netflix Data App",
    page_icon="🎬",
    layout="wide",
)



@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()


st.title("🎬 Netflix Data Analytics Dashboard")

st.write(
    "Explore and understand Netflix's movies and TV shows "
    "catalog through interactive data visualization."
)

tab1, tab2 = st.tabs([
    "📋 Overview",
    "📊 Data Visualization & Insights"
])

with tab1:
    st.header("About the Dataset")

    st.write(
        "This dataset contains Netflix movies and TV shows, "
        "including genres, release years, countries, and ratings."
    )

    col1, col2 = st.columns(2)
    col1.metric("Total Records", len(df))
    col2.metric("Total Columns", len(df.columns))

    st.subheader("Available Columns")
    st.write(", ".join(df.columns))

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.header("Data Visualization")
    st.info("Interactive charts will be implemented in Issues #4 and #5.")

    st.divider()

    st.header("Key Insights")
    st.info("Dynamic insights will be implemented in Issue #6.")


