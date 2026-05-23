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

for i, article in enumerate(articles, start=1):
    print(f"\nARTICLE {i}")
    result = analyze_article(article)
    print(result)
