import spacy
from app.preprocessing import clean_text, preprocess_text
from app.sentiment import analyze_sentiment

nlp = spacy.load("en_core_web_sm")

sample = """
NASA announced a new AI-powered monitoring system for mission operations.
The system will improve response time and reduce manual review.
"""

print("CLEANED:")
print(clean_text(sample))

print("\nPROCESSED:")
print(preprocess_text(sample, nlp))

print("\nSENTIMENT:")
print(analyze_sentiment(sample))
