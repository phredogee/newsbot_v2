# 📰 NewsBot 2.0

AI-assisted news monitoring, summarization, and signal detection dashboard built with Python, NLP pipelines, and Streamlit.

---

## Overview

NewsBot 2.0 is a live news intelligence platform designed to ingest, analyze, classify, and summarize technology and AI-related news in real time.

The system combines:

- RSS news ingestion
- NLP preprocessing
- Sentiment analysis
- Topic classification
- Signal detection
- Interactive dashboard analytics
- AI-generated executive briefings
- Local fallback summarization workflows

The goal is to simulate a lightweight enterprise intelligence and monitoring platform for rapidly changing AI, cybersecurity, and technology ecosystems.

---

## Features

### ✅ Live News Ingestion
- Pulls real-time news from multiple RSS feeds
- Processes articles automatically
- Stores structured analytics data in CSV format

### ✅ NLP Processing Pipeline
- Text cleaning and preprocessing
- Sentiment analysis
- Topic extraction/classification
- Signal detection workflows

### ✅ Interactive Streamlit Dashboard
- KPI metrics
- Topic filtering
- Sentiment filtering
- Source filtering
- Downloadable datasets
- Interactive charts
- Clickable article links

### ✅ AI-Generated Executive Briefings
- OpenAI-powered executive summaries
- Local fallback summarization if API quota is unavailable
- Supports operational intelligence workflows

### ✅ Modular Architecture
- Pipeline orchestration
- Reusable NLP modules
- Extensible dashboard framework
- Future-ready for embeddings and vector search

---

# Project Structure

```text
newsbot_v2/
├── app/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   └── topics.py
│
├── newsbot/
│   ├── __init__.py
│   ├── feeds.py
│   ├── scoring.py
│   └── summarizer.py
│
├── scripts/
│   ├── live_news_pipeline.py
│   ├── test_pipeline.py
│   └── fetch_news.py
│
├── data/
│   ├── analyzed_articles.csv
│   └── live_news_analysis.csv
│
├── streamlit_app.py
├── dashboard.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/phredogee/newsbot_v2.git
cd newsbot_v2
```

---

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Pipeline

## Generate Live News Analysis

```bash
python -m scripts.live_news_pipeline
```

This will:
- fetch RSS news
- analyze sentiment
- classify topics
- save results into:

```text
data/live_news_analysis.csv
```

---

# Running the Dashboard

```bash
streamlit run streamlit_app.py
```

---

# AI Briefings

NewsBot 2.0 supports AI-generated executive briefings using the OpenAI API.

Set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

If API quota is unavailable, the system automatically falls back to a local rule-based summarization engine.

---

# Future Enhancements

- Historical trend analysis
- Semantic search using embeddings
- Vector database integration
- RAG-based querying
- Real-time alerting
- Slack/Discord notifications
- Docker deployment
- Cloud hosting

---

# Technologies Used

- Python
- Streamlit
- Pandas
- OpenAI API
- NLP workflows
- RSS ingestion
- Sentiment analysis
- Topic modeling

---

# Author

Alfredo Garza

GitHub:
https://github.com/phredogee
