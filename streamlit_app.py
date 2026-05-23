from pathlib import Path
from datetime import datetime
from newsbot.summarizer import generate_ai_briefing

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="NewsBot v2",
    page_icon="📰",
    layout="wide",
)


DATA_PATH = Path("data/live_news_analysis.csv")


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0rem;
    }

    table {
        width: 100%;
        table-layout: fixed;
    }

    th, td {
        white-space: normal !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
        vertical-align: top;
        padding: 10px;
    }

    td:nth-child(1) {
        width: 25%;
    }

    td:nth-child(3) {
        width: 35%;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #a0a0a0;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #374151;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.20);
    }

    .metric-label {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
    }

    .article-card {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18);
    }

    .article-title {
        font-size: 1.15rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
    }

    .article-meta {
        color: #9ca3af;
        font-size: 0.88rem;
        margin-bottom: 0.75rem;
    }

    .topic-pill {
        display: inline-block;
        background: #1e3a8a;
        color: #dbeafe;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-right: 6px;
        margin-top: 6px;
    }

    .positive {
        color: #22c55e;
        font-weight: 700;
    }

    .negative {
        color: #ef4444;
        font-weight: 700;
    }

    .neutral {
        color: #d1d5db;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df = df.fillna("")
    return df


def get_topic_list(df: pd.DataFrame) -> list[str]:
    if df.empty or "topics" not in df.columns:
        return []

    topics = set()

    for item in df["topics"].astype(str):
        for topic in item.split(","):
            clean_topic = topic.strip()
            if clean_topic:
                topics.add(clean_topic)

    return sorted(topics)


def explode_topics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "topics" not in df.columns:
        return pd.DataFrame(columns=["topic"])

    topic_rows = []

    for topics in df["topics"].astype(str):
        for topic in topics.split(","):
            clean_topic = topic.strip()
            if clean_topic:
                topic_rows.append({"topic": clean_topic})

    return pd.DataFrame(topic_rows)


def sentiment_class(sentiment: str) -> str:
    sentiment = str(sentiment).strip().lower()

    if sentiment == "positive":
        return "positive"
    if sentiment == "negative":
        return "negative"
    return "neutral"


def sentiment_label(sentiment: str) -> str:
    sentiment = str(sentiment).strip()

    if sentiment == "Positive":
        return "Positive"
    if sentiment == "Negative":
        return "Negative"
    if sentiment == "Neutral":
        return "Neutral"

    return sentiment or "Unknown"


def find_url(row: pd.Series) -> str:
    for col in ["url", "link", "article_url"]:
        if col in row and str(row[col]).strip():
            return str(row[col]).strip()
    return ""


def render_metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topic_pills(topics: str) -> str:
    pills = ""

    for topic in str(topics).split(","):
        clean_topic = topic.strip()
        if clean_topic:
            pills += f'<span class="topic-pill">{clean_topic}</span>'

    return pills


# -----------------------------
# Load Data
# -----------------------------
df = load_data(DATA_PATH)


# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">📰 NewsBot v2</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-assisted news monitoring, summarization, and signal detection dashboard.</div>',
    unsafe_allow_html=True,
)

header_col1, header_col2 = st.columns([5, 1])

with header_col2:
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()


if df.empty:
    st.warning("No live news data found yet.")
    st.info("Run this first in your terminal: `python -m scripts.live_news_pipeline`")
    st.stop()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Controls")

all_topics = get_topic_list(df)

topic_filter = st.sidebar.selectbox(
    "Topic Focus",
    ["All"] + all_topics,
)

sentiment_filter = "All"
if "sentiment" in df.columns:
    sentiment_options = sorted(df["sentiment"].astype(str).unique())
    sentiment_filter = st.sidebar.selectbox(
        "Sentiment",
        ["All"] + sentiment_options,
    )

source_filter = "All"
if "source" in df.columns:
    source_options = sorted(df["source"].astype(str).unique())
    source_filter = st.sidebar.selectbox(
        "Source",
        ["All"] + source_options,
    )

article_limit = st.sidebar.slider(
    "Articles to Display",
    min_value=5,
    max_value=50,
    value=10,
    step=5,
)


# -----------------------------
# Filters
# -----------------------------
filtered_df = df.copy()

if topic_filter != "All" and "topics" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["topics"].astype(str).str.contains(topic_filter, case=False, na=False)
    ]

if sentiment_filter != "All" and "sentiment" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["sentiment"].astype(str) == sentiment_filter]

if source_filter != "All" and "source" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["source"].astype(str) == source_filter]


# -----------------------------
# KPI Cards
# -----------------------------
articles_scanned = len(df)
articles_displayed = len(filtered_df)

high_signal_items = 0
if "sentiment" in df.columns:
    high_signal_items = len(df[df["sentiment"].isin(["Positive", "Negative"])])

sources_active = 0
if "source" in df.columns:
    sources_active = df["source"].nunique()

last_updated = datetime.fromtimestamp(DATA_PATH.stat().st_mtime).strftime("%b %d, %Y %I:%M %p")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    render_metric_card("Articles Scanned", str(articles_scanned))

with metric_col2:
    render_metric_card("Displayed", str(articles_displayed))

with metric_col3:
    render_metric_card("High-Signal Items", str(high_signal_items))

with metric_col4:
    render_metric_card("Sources Active", str(sources_active))

st.caption(f"Last updated: {last_updated}")

st.divider()


# -----------------------------
# Charts
# -----------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sentiment Breakdown")

    if "sentiment" in filtered_df.columns and not filtered_df.empty:
        sentiment_counts = filtered_df["sentiment"].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.write("No sentiment data available.")

with chart_col2:
    st.subheader("Topic Frequency")

    topic_df = explode_topics(filtered_df)

    if not topic_df.empty:
        topic_counts = topic_df["topic"].value_counts().head(10)
        st.bar_chart(topic_counts)
    else:
        st.write("No topic data available.")

st.divider()


# -----------------------------
# AI Briefing
# -----------------------------
st.subheader("AI-Generated Briefing")

if st.button("Generate AI Briefing"):
    with st.spinner("Generating briefing..."):
        briefing = generate_ai_briefing(filtered_df)
        st.markdown(briefing)

st.divider()


# -----------------------------
# Article Cards
# -----------------------------
st.subheader("Top News Signals")

if filtered_df.empty:
    st.warning("No articles match the selected filters.")
else:
    for _, row in filtered_df.head(article_limit).iterrows():
        title = row.get("title", "Untitled article")
        source = row.get("source", "Unknown source")
        summary = row.get("summary", "")
        sentiment = sentiment_label(row.get("sentiment", "Unknown"))
        topics = row.get("topics", "")
        url = find_url(row)

        sentiment_css = sentiment_class(sentiment)
        topic_pills = render_topic_pills(topics)

        if url:
            title_html = f'<a href="{url}" target="_blank" style="color:#93c5fd; text-decoration:none;">{title}</a>'
        else:
            title_html = title

        st.markdown(
            f"""
            <div class="article-card">
                <div class="article-title">{title_html}</div>
                <div class="article-meta">{source} · <span class="{sentiment_css}">{sentiment}</span></div>
                <div>{summary}</div>
                <div style="margin-top: 10px;">{topic_pills}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Data Table + Export
# -----------------------------
st.divider()
st.subheader("Live News Analysis Table")

table_df = filtered_df.copy()

# Make title clickable if URL exists
if "url" in table_df.columns and "title" in table_df.columns:
    table_df["article"] = table_df.apply(
        lambda row: f'<a href="{row["url"]}" target="_blank">{row["title"]}</a>'
        if str(row["url"]).strip()
        else row["title"],
        axis=1,
    )

    display_columns = ["article", "source", "summary", "sentiment", "topics"]

    existing_columns = [col for col in display_columns if col in table_df.columns]

    st.markdown(
        table_df[existing_columns].to_html(
            escape=False,
            index=False,
        ),
        unsafe_allow_html=True,
    )
else:
    st.dataframe(table_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered CSV",
    data=csv,
    file_name="newsbot_filtered_live_news.csv",
    mime="text/csv",
)


# -----------------------------
# Footer
# -----------------------------
st.caption(
    f"Designed for quick review, signal detection, and AI-assisted summarization. "
    f"Data source: {DATA_PATH}"
)
