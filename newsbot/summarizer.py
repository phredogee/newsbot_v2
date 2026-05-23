import os

from anthropic import Anthropic, APIError, AuthenticationError, RateLimitError


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

    lines = ["### Top Signals"]

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
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        return generate_local_briefing(df, max_articles) + "\n\n_ANTHROPIC_API_KEY is not set. Showing local fallback briefing._"

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
You are NewsBot 2.0, an AI news intelligence assistant.

Create a concise executive briefing from the following analyzed news items.

Format the response in Markdown using these sections:

### Top Signals
### Why It Matters
### Risks or Concerns
### Recommended Follow-Up

News items:
{article_text}
"""

    try:
        client = Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=700,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return message.content[0].text

    except RateLimitError:
        return generate_local_briefing(df, max_articles) + "\n\n_Claude API rate limit reached. Showing local fallback briefing._"

    except AuthenticationError:
        return generate_local_briefing(df, max_articles) + "\n\n_Claude API key issue detected. Showing local fallback briefing._"

    except APIError as error:
        return generate_local_briefing(df, max_articles) + f"\n\n_Claude API error: {error}. Showing local fallback briefing._"
