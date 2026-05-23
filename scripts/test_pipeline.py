from app.pipeline import analyze_article

sample = """
NASA announced a new AI-powered monitoring system for mission operations.
The system will improve response time and reduce manual review.
"""

result = analyze_article(sample)

print(result)
