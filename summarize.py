import os
import json
from groq import Groq
from datetime import datetime


def summarize_news(articles: list) -> str:
  """Send articles to Groq (Llama 3) and get a clean email-ready summary."""
  if not articles:
   return "No recent AI or BI news articles were found in the last 24 hours."

  # Build article list for the model
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

 AI HIGHLIGHTS
• [2-3 bullet points covering the most important AI news. Each bullet: bold key idea, then 1-sentence explanation.]

 BI & DATA HIGHLIGHTS
• [2-3 bullet points covering the most important BI/Data news.]

 KEY TAKEAWAY
[1-2 sentences: What is the most significant trend or insight from today's news?]

 FULL ARTICLES
[List each article as: • Title — Source (Link)]

Rules:
- Be concise. Each bullet max 2 lines.
- Use plain language, no jargon.
- Do not fabricate information. Only use what is in the articles below.
- If there are no BI articles, skip that section.

Today's date: {today}

ARTICLES:
{article_text}
"""

client = Groq(api_key=os.environ["GROQ_API_KEY"])
response = client.chat.completions.create(
  model="llama3-70b-8192", # Free, fast, high quality
  messages=[{"role": "user", "content": prompt}],
  max_tokens=1024,
  temperature=0.5,
  )
return response.choices[0].message.content

if __name__ == "__main__":
 # Quick test with a dummy article
 test_articles = [
  {
  "title": "Meta releases Llama 4 with multimodal support",
  "source": "TechCrunch",
  "category": "AI News",
  "published": "2025-01-01 08:00",
  "summary": "Meta announced Llama 4 with vision and audio capabilities, available open source...",
  "link": "https://techcrunch.com/example"
  }
 ]
  print(summarize_news(test_articles))
