import streamlit as st
import pandas as pd
import plotly.express as px

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

        # Interactive Plotly charts
    st.divider()
    st.subheader("Interactive Data Visualization")

    analysis_type = st.selectbox(
        "Select Analysis",
        [
            "Content Distribution",
            "Release Year Trends",
            "Top 10 Genres"
        ]
    )

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")

    elif analysis_type == "Content Distribution":
        chart_data = (
            filtered_df["type"]
            .value_counts()
            .rename_axis("Content Type")
            .reset_index(name="Number of Titles")
        )

        chart_type = st.radio(
            "Chart Type",
            ["Bar", "Pie"],
            horizontal=True
        )

        if chart_type == "Bar":
            fig = px.bar(
                chart_data,
                x="Content Type",
                y="Number of Titles",
                color="Content Type",
                title="Netflix Content Distribution"
            )
        else:
            fig = px.pie(
                chart_data,
                names="Content Type",
                values="Number of Titles",
                color="Content Type",
                title="Netflix Content Distribution"
            )

        st.plotly_chart(fig, width="stretch")

    elif analysis_type == "Release Year Trends":
        chart_data = (
            filtered_df.groupby("release_year")
            .size()
            .reset_index(name="Number of Titles")
            .sort_values("release_year")
        )

        chart_type = st.radio(
            "Chart Type",
            ["Line", "Bar"],
            horizontal=True
        )

        if chart_type == "Line":
            fig = px.line(
                chart_data,
                x="release_year",
                y="Number of Titles",
                markers=True,
                title="Netflix Titles by Release Year"
            )
            fig.update_traces(name="Titles", showlegend=True)
        else:
            fig = px.bar(
                chart_data,
                x="release_year",
                y="Number of Titles",
                title="Netflix Titles by Release Year"
            )
            fig.update_traces(name="Titles", showlegend=True)

        fig.update_xaxes(title_text="Release Year")
        fig.update_yaxes(title_text="Number of Titles")

        st.plotly_chart(fig, width="stretch")

    elif analysis_type == "Top 10 Genres":
        genres = (
            filtered_df["listed_in"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
        )

        chart_data = (
            genres.value_counts()
            .head(10)
            .rename_axis("Genre")
            .reset_index(name="Number of Titles")
            .sort_values("Number of Titles")
        )

        fig = px.bar(
            chart_data,
            x="Number of Titles",
            y="Genre",
            color="Genre",
            orientation="h",
            title="Top 10 Netflix Genres"
        )

        st.plotly_chart(fig, width="stretch")


    st.divider()

    st.header("Key Insights")
    st.info("Dynamic insights will be implemented in Issue #6.")


