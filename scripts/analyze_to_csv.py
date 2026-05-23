import pandas as pd

from app.pipeline import analyze_article

articles = [
    """
    NASA announced a new AI-powered monitoring system for mission operations.
    The system will improve response time and reduce manual review.
    """,
    """
    A cybersecurity vulnerability was discovered in a major cloud platform.
    Security teams are urging users to apply patches immediately.
    """,
    """
    City officials introduced a new workflow automation system to reduce permit processing delays.
    """
]

results = []

for article in articles:
    result = analyze_article(article)

    results.append({
        "original_text": result["original_text"].strip(),
        "cleaned_text": result["cleaned_text"],
        "processed_text": result["processed_text"],
        "sentiment_label": result["sentiment"]["label"],
        "polarity": result["sentiment"]["polarity"],
        "subjectivity": result["sentiment"]["subjectivity"],
        "topics": ", ".join(result["topics"]),
    })

df = pd.DataFrame(results)

df.to_csv("data/analyzed_articles.csv", index=False)

print("Saved results to data/analyzed_articles.csv")
print(df)
