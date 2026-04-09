import feedparser
import json
from datetime import datetime, timedelta
import re

RSS_FEEDS = {
    "AI News": [
        "https://feeds.feedburner.com/venturebeat/SZYF",  # VentureBeat AI
        "https://www.artificialintelligence-news.com/feed/",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    ],
    "BI & Data": [
        "https://feeds.feedburner.com/kdnuggets-data-mining-analytics",
        "https://towardsdatascience.com/feed",
        "https://www.businessinsider.com/rss",
        "https://feeds.harvardbusiness.org/harvardbusiness/",
    ]
}

MAX_ARTICLES_PER_FEED = 3
MAX_AGE_HOURS = 24


def clean_html(text):
    """Strip HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text or '').strip()


def fetch_recent_articles():
    """Fetch articles from the last 24 hours across all feeds."""
    cutoff = datetime.utcnow() - timedelta(hours=MAX_AGE_HOURS)
    all_articles = []

    for category, feeds in RSS_FEEDS.items():
        category_articles = []

        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
                    # Parse published date
                    published = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    
                    # Skip if too old
                    if published and published < cutoff:
                        continue

                    # Get summary/description
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = clean_html(entry.summary)[:300]
                    elif hasattr(entry, 'description'):
                        summary = clean_html(entry.description)[:300]

                    article = {
                        "title": clean_html(entry.get("title", "No title")),
                        "link": entry.get("link", ""),
                        "summary": summary,
                        "source": feed.feed.get("title", feed_url),
                        "category": category,
                        "published": published.strftime("%Y-%m-%d %H:%M") if published else "Unknown"
                    }
                    category_articles.append(article)

            except Exception as e:
                print(f"[Warning] Could not fetch {feed_url}: {e}")
                continue

        all_articles.extend(category_articles[:5])  # cap per category

    print(f"[fetch_news] Fetched {len(all_articles)} articles total.")
    return all_articles


if __name__ == "__main__":
    articles = fetch_recent_articles()
    print(json.dumps(articles, indent=2))
