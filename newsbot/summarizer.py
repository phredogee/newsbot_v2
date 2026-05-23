import os
from openai import OpenAI
from openai import RateLimitError, APIError, AuthenticationError


def generate_local_briefing(df, max_articles=8):
    articles = df.head(max_articles)

    top_topics = []
    if "topics" in df.columns:
        for topics in df["topics"].astype(str):
            for topic in topics.split(","):
                topic = topic.strip()
                if topic:
                    top_topics.append(topic)

    top_topic_text = ", ".join(sorted(set(top_topics))[:5]) or "No major topics detected"

    lines = [
        "### Top Signals",
    ]

    for _, row in articles.iterrows():
        title = row.get("title", "Untitled article")
        sentiment = row.get("sentiment", "Unknown")
        topics = row.get("topics", "")
        lines.append(f"- **{title}** — {sentiment}; Topics: {topics}")

    lines.extend(
        [
            "",
            "### Why It Matters",
            f"The current news set is concentrated around: **{top_topic_text}**.",
            "",
            "### Recommended Follow-Up",
            "- Review negative and high-signal items first.",
            "- Track repeated topics across future pipeline runs.",
            "- Compare topic frequency over time once historical storage is added.",
        ]
    )

    return "\n".join(lines)


def generate_ai_briefing(df, max_articles=8):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return generate_local_briefing(df, max_articles)

    try:
        client = OpenAI(api_key=api_key)

        articles = df.head(max_articles)

        article_text = ""

        for _, row in articles.iterrows():
            article_text += f"""
Title: {row.get("title", "")}
Source: {row.get("source", "")}
Summary: {row.get("summary", "")}
Sentiment: {row.get("sentiment", "")}
Topics: {row.get("topics", "")}
"""

        prompt = f"""
Create a concise executive briefing from these analyzed news items.

Format:
1. Top Signals
2. Why It Matters
3. Risks or Concerns
4. Recommended Follow-Up

News items:
{article_text}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text

    except RateLimitError:
        return generate_local_briefing(df, max_articles) + "\n\n_API quota unavailable, showing local fallback briefing._"

    except AuthenticationError:
        return generate_local_briefing(df, max_articles) + "\n\n_API key issue detected, showing local fallback briefing._"

    except APIError as error:
        return generate_local_briefing(df, max_articles) + f"\n\n_OpenAI API error: {error}. Showing local fallback briefing._"
