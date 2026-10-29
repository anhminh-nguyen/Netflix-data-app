import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Netflix Data App",
    page_icon="🎬",
    layout="wide",
)

st.title("Netflix Data Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()

st.header("Dataset Overview")

st.write("This dataset contains information about Netflic movies and TV shows")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Total Columns", len(df.columns))

# Display dataset
st.header("Netflix Dataset")
st.dataframe(df, use_container_width=True)

# Dataset information
st.header("Dataset Information")

st.subheader("Column Names")
st.write(df.columns.tolist())

st.subheader("Missing Values")
st.dataframe(
    df.isnull().sum().reset_index(
        name="Missing Values"
    ).rename(columns={"index": "Column"})
)

st.subheader("Data Types")
st.write(df.dtypes.astype(str))

