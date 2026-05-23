import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NewsBot 2.0",
    page_icon="📰",
    layout="wide"
)

st.title("NewsBot 2.0")
st.subheader("AI-Powered News Analysis Dashboard")

DATA_PATH = "data/live_news_analysis.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.write("Latest analyzed articles from the live news pipeline.")

col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(df))
col2.metric("Positive Articles", len(df[df["sentiment"] == "Positive"]))
col3.metric("Negative Articles", len(df[df["sentiment"] == "Negative"]))

st.divider()

st.subheader("Sentiment Breakdown")
sentiment_counts = df["sentiment"].value_counts()
st.bar_chart(sentiment_counts)

st.subheader("Topic Breakdown")
topic_series = (
    df["topics"]
    .fillna("")
    .str.split(", ")
    .explode()
)

topic_counts = topic_series[topic_series != ""].value_counts()
st.bar_chart(topic_counts)

st.divider()

st.subheader("Analyzed Articles")

topic_filter = st.selectbox(
    "Filter by topic",
    ["All"] + sorted(topic_counts.index.tolist())
)

filtered_df = df.copy()

if topic_filter != "All":
    filtered_df = filtered_df[
        filtered_df["topics"].fillna("").str.contains(topic_filter, case=False)
    ]

st.dataframe(
    filtered_df[["title", "sentiment", "topics", "link"]],
    use_container_width=True
)
