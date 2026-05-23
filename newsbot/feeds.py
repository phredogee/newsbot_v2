import feedparser


RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Wired AI": "https://www.wired.com/feed/tag/ai/latest/rss",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
}


def fetch_rss_news(limit_per_source=5):
    articles = []

    for source, feed_url in RSS_FEEDS.items():
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit_per_source]:
            articles.append(
                {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "source": source,
                    "url": entry.get("link", ""),
                }
            )

    return articles
