from textblob import TextBlob


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment polarity and subjectivity.
    """

    blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "polarity": polarity,
        "subjectivity": subjectivity
    }
