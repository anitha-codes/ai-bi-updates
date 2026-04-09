#!/usr/bin/env python3
"""
main.py — Entry point for the AI & BI Daily News Digest
Run by GitHub Actions on a daily schedule.
"""

import sys
from fetch_news import fetch_recent_articles
from summarize import summarize_news
from send_email import send_digest


def main():
    print("=" * 50)
    print("🚀 Starting AI & BI Daily Digest Pipeline")
    print("=" * 50)

    # Step 1: Fetch news
    print("\n[1/3] Fetching latest AI & BI news...")
    articles = fetch_recent_articles()

    if not articles:
        print("⚠️  No articles found. Sending fallback message.")
        summary = (
            "No new AI or BI articles were found in the last 24 hours. "
            "Check back tomorrow for the latest updates!"
        )
    else:
        print(f"      Found {len(articles)} articles.")

        # Step 2: Summarize with Claude
        print("\n[2/3] Summarizing with Claude AI...")
        summary = summarize_news(articles)
        print("      Summary generated successfully.")

    # Step 3: Send emails
    print("\n[3/3] Sending digest emails...")
    send_digest(summary)

    print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)
