import spacy

from app.preprocessing import clean_text, preprocess_text
from app.sentiment import analyze_sentiment
from app.topics import detect_topics

nlp = spacy.load("en_core_web_sm")


def analyze_article(text: str) -> dict:
    cleaned = clean_text(text)
    processed = preprocess_text(text, nlp)
    sentiment = analyze_sentiment(text)
    topics = detect_topics(text)

    return {
        "original_text": text,
        "cleaned_text": cleaned,
        "processed_text": processed,
        "sentiment": sentiment,
        "topics": topics,
    }
