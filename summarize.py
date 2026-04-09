import anthropic
import json
from datetime import datetime


def summarize_news(articles: list) -> str:
    """Send articles to Claude and get a clean email-ready summary."""

    if not articles:
        return "No recent AI or BI news articles were found in the last 24 hours."

    # Build article list for Claude
    article_text = ""
    for i, a in enumerate(articles, 1):
        article_text += f"""
{i}. [{a['category']}] {a['title']}
   Source: {a['source']} | Published: {a['published']}
   Summary: {a['summary']}
   Link: {a['link']}
"""

    today = datetime.now().strftime("%A, %B %d %Y")

    prompt = f"""You are an expert technology news curator. Below are the latest AI and Business Intelligence (BI) news articles from the past 24 hours.

Your task: Write a concise, engaging daily digest email body for a professional audience.

Format your response EXACTLY like this:

🤖 AI HIGHLIGHTS
• [2-3 bullet points covering the most important AI news. Each bullet: bold key idea, then 1-sentence explanation.]

📊 BI & DATA HIGHLIGHTS  
• [2-3 bullet points covering the most important BI/Data news.]

💡 KEY TAKEAWAY
[1-2 sentences: What's the most significant trend or insight from today's news?]

📰 FULL ARTICLES
[List each article as: • Title — Source (Link)]

Rules:
- Be concise. Each bullet max 2 lines.
- Use plain language, no jargon.
- Do not fabricate information. Only use what's in the articles below.
- If there are no BI articles, skip that section.

Today's date: {today}

ARTICLES:
{article_text}
"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


if __name__ == "__main__":
    # Test with dummy articles
    test_articles = [
        {
            "title": "OpenAI releases GPT-5 with multimodal reasoning",
            "source": "TechCrunch",
            "category": "AI News",
            "published": "2025-01-01 08:00",
            "summary": "OpenAI announced GPT-5 today, featuring enhanced multimodal capabilities...",
            "link": "https://techcrunch.com/example"
        }
    ]
    result = summarize_news(test_articles)
    print(result)
