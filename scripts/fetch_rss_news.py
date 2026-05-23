import feedparser

rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

feed = feedparser.parse(rss_url)

for entry in feed.entries[:5]:
    print("\nTITLE:")
    print(entry.title)

    print("\nLINK:")
    print(entry.link)

    print("\nSUMMARY:")
    print(entry.summary[:200])
