import pandas as pd

from app.pipeline import analyze_article
from newsbot.feeds import fetch_rss_news


def main():
    articles = fetch_rss_news()

    analyzed_rows = []

    for article in articles:
        title = article.get("title", "")
        summary = article.get("summary", "")
        source = article.get("source", "Unknown source")
        url = article.get("url", article.get("link", ""))

        text_for_analysis = f"{title}. {summary}"

        analysis = analyze_article(text_for_analysis)

        analyzed_rows.append(
            {
                "title": title,
                "source": source,
                "summary": summary,
                "url": url,
                "sentiment": analysis.get("sentiment", {}).get("label", "Unknown"),
                "polarity": analysis.get("sentiment", {}).get("polarity", 0),
                "subjectivity": analysis.get("sentiment", {}).get("subjectivity", 0),
                "topics": ", ".join(analysis.get("topics", [])),
            }
        )

    df = pd.DataFrame(analyzed_rows)

    df.to_csv("data/live_news_analysis.csv", index=False)

    print(df[["title", "sentiment", "topics", "url"]].head(10))


if __name__ == "__main__":
    main()
