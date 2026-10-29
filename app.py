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

    st.subheader("Interactive Filters")

    # Create filter controls
    col1, col2 = st.columns(2)

    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["All"] + sorted(df["type"].dropna().unique().tolist())
        )

    # Extract countries, including multiple countries in one row
    countries = sorted({
        country.strip()
        for value in df["country"].dropna()
        for country in value.split(",")
        if country.strip()
    })

    with col2:
        country = st.selectbox(
            "Country",
            ["All"] + countries
        )

    # Release year range
    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())

    year_range = st.slider(
        "Release Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Apply filters
    filtered_df = df.copy()

    if content_type != "All":
        filtered_df = filtered_df[
            filtered_df["type"] == content_type
        ]

    if country != "All":
        filtered_df = filtered_df[
            filtered_df["country"].fillna("").apply(
                lambda value: country in [
                    item.strip() for item in value.split(",")
                ]
            )
        ]

    filtered_df = filtered_df[
        filtered_df["release_year"].between(
            year_range[0],
            year_range[1]
        )
    ]

    # Display filtered results
    st.subheader("Filtered Results")

    st.metric("Matching Records", len(filtered_df))

    if filtered_df.empty:
        st.warning("No titles match the selected filters.")
    else:
        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    st.divider()

    st.header("Key Insights")
    st.info("Dynamic insights will be implemented in Issue #6.")


