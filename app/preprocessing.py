import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """Basic cleanup for raw article text."""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-z\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_text(text: str, nlp) -> str:
    """Clean, tokenize, lemmatize, and remove stop words."""
    cleaned = clean_text(text)
    doc = nlp(cleaned)

    tokens = [
        token.lemma_
        for token in doc
        if token.text not in stop_words
        and len(token.text) > 2
        and not token.is_space
    ]

    return " ".join(tokens)
