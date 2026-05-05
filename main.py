#!/usr/bin/env python3
import sys, json, os
from datetime import datetime
from fetch_news import fetch_recent_articles
from summarize import summarize_news
from send_email import send_digest


def parse_summary_sections(summary: str) -> list:
    sections, current = [], None
    for line in summary.split("\n"):
        line = line.strip()
        if not line:
            continue
        if any(line.startswith(e) for e in ["🤖", "📊", "💡", "📰"]):
            if current:
                sections.append(current)
            current = {"heading": line, "bullets": []}
        elif line.startswith("•") and current:
            current["bullets"].append(line[1:].strip())
        elif current and current["heading"].startswith("💡"):
            current["bullets"].append(line)
    if current:
        sections.append(current)
    return sections


def save_dashboard_data(articles, summary):
    grouped = {}
    for a in articles:
        cat = a.get("category", "General")
        grouped.setdefault(cat, []).append(a)

    data = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "display_date": datetime.now().strftime("%A, %B %d %Y"),
        "summary_sections": parse_summary_sections(summary),
        "raw_summary": summary,
        "article_groups": [{"category": c, "articles": a} for c, a in grouped.items()],
        "total_articles": len(articles)
    }
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"[main] Saved docs/data.json")


def main():
    print("🚀 Starting AI & BI Daily Digest Pipeline")

    print("\n[1/4] Fetching news...")
    articles = fetch_recent_articles()

    if not articles:
        summary = "No new AI or BI articles found in the last 24 hours. Check back tomorrow!"
    else:
        print(f"      {len(articles)} articles found.")
        print("\n[2/4] Summarising with AI...")
        summary = summarize_news(articles)

    print("\n[3/4] Saving dashboard data...")
    save_dashboard_data(articles, summary)

    print("\n[4/4] Sending emails...")
    send_digest(summary)

    print("\n✅ Done!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)
