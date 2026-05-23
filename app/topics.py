TOPIC_KEYWORDS = {
    "Artificial Intelligence": [
        "ai",
        "a.i.",
        "artificial intelligence",
        "machine learning",
        "large language model",
        "llm",
        "automation",
        "model"
    ],
    "Cybersecurity": [
        "cybersecurity",
        "hacking",
        "breach",
        "malware",
        "ransomware",
        "vulnerability",
        "security"
    ],
    "Government & Policy": [
        "executive order",
        "government",
        "federal",
        "regulation",
        "policy",
        "law",
        "department",
        "agency"
    ],
    "Operations": [
        "operations",
        "monitoring",
        "workflow",
        "response time",
        "service",
        "system outage",
        "incident"
    ],
    "Autonomous Vehicles": [
        "waymo",
        "self-driving",
        "autonomous vehicle",
        "robotaxi",
        "driverless"
    ],
    "Space & Aerospace": [
        "nasa",
        "spacecraft",
        "satellite",
        "rocket",
        "mission control",
        "astronaut"
    ],
}

def detect_topics(text: str) -> list[str]:
    text_lower = text.lower()
    matched_topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                matched_topics.append(topic)
                break

    return matched_topics
