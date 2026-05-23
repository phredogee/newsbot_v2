import pandas as pd
import feedparser

from app.pipeline import analyze_article

rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

feed = feedparser.parse(rss_url)

results = []

for entry in feed.entries[:10]:

    text = f"""
    {entry.title}

    {entry.summary}
    """

    analysis = analyze_article(text)

    results.append({
        "title": entry.title,
        "link": entry.link,
        "summary": entry.summary,
        "sentiment": analysis["sentiment"]["label"],
        "polarity": analysis["sentiment"]["polarity"],
        "topics": ", ".join(analysis["topics"]),
    })

df = pd.DataFrame(results)

df.to_csv("data/live_news_analysis.csv", index=False)

print(df[["title", "sentiment", "topics"]])
