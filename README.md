# 🧠 AI & BI Daily News Digest

A fully automated, **free** daily email digest of the latest AI and Business Intelligence news — powered by Claude AI and GitHub Actions.

**No server. No database. No cost.**

---

## 📬 What It Does

Every day at **8:30 AM IST** (configurable), it:
1. Fetches the latest AI & BI news from RSS feeds
2. Sends the articles to Claude AI for summarization
3. Emails a clean, formatted digest to all subscribers

---

## 🗂️ Project Structure

```
ai-bi-news-digest/
├── main.py               # Pipeline runner (fetch → summarize → send)
├── fetch_news.py         # RSS feed fetcher
├── summarize.py          # Claude AI summarizer
├── send_email.py         # Gmail SMTP email sender
├── subscribers.json      # List of subscriber emails
└── .github/
    └── workflows/
        └── daily_digest.yml   # GitHub Actions scheduler
```

---

## 🚀 Setup Guide (Step by Step)

### Step 1 — Fork this repository

Click **Fork** at the top right of this GitHub page. This creates your own copy.

---

### Step 2 — Get your API keys

#### 🔑 Anthropic API Key (Claude)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Go to **API Keys** → **Create Key**
4. Copy the key (starts with `sk-ant-...`)

#### 📧 Gmail App Password
> **Important:** This is NOT your regular Gmail password. It's a special password for apps.

1. Go to your Google Account → [Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (required)
3. Search for **"App passwords"** in the search bar
4. Select **Mail** + **Other (Custom name)** → type "News Digest"
5. Click **Generate** → copy the 16-character password

---

### Step 3 — Add GitHub Secrets

In your forked repo:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these three:

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Claude API key |
| `GMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_APP_PASSWORD` | The 16-char app password from Step 2 |

---

### Step 4 — Add subscribers

Edit `subscribers.json` in the repo:

```json
{
  "subscribers": [
    "you@gmail.com",
    "friend@example.com",
    "colleague@work.com"
  ]
}
```

Commit and push the change.

---

### Step 5 — Test it manually

1. Go to the **Actions** tab in your repo
2. Click **Daily AI & BI News Digest**
3. Click **Run workflow** → **Run workflow**
4. Watch the logs — you should receive an email within ~1 minute!

---

## ⏰ Changing the Schedule

Edit `.github/workflows/daily_digest.yml`:

```yaml
- cron: '0 3 * * *'   # 8:30 AM IST (UTC+5:30 = subtract 5.5 hrs from IST)
```

Use [crontab.guru](https://crontab.guru) to generate your preferred time.

Common examples:
| Time (IST) | Cron (UTC) |
|---|---|
| 7:00 AM | `30 1 * * *` |
| 8:30 AM | `0 3 * * *` |
| 6:00 PM | `30 12 * * *` |
| Twice daily (8:30 AM + 6 PM) | `0 3,30 12 * * *` |

---

## 📤 Sharing With Others

To let others subscribe:
- Share your forked repo link and ask them to open a PR adding their email to `subscribers.json`
- **Or** create a [Google Form](https://forms.google.com) asking for their email, then periodically update `subscribers.json`

---

## 💰 Cost Estimate

| Service | Free Limit | Typical Usage |
|---|---|---|
| GitHub Actions | 2,000 min/month | ~2 min/day = 60 min/month ✅ |
| Anthropic API | Pay-per-use | ~$0.01–0.03/day |
| Gmail SMTP | Free | Free ✅ |
| RSS Feeds | Free | Free ✅ |

**Estimated cost: ~$0.30–1.00/month** (only Claude API calls)

---

## 🛠️ Customization

### Add more news sources
Edit the `RSS_FEEDS` dict in `fetch_news.py`:
```python
RSS_FEEDS = {
    "AI News": [
        "https://your-favorite-feed.com/rss",
        ...
    ],
}
```

### Change summary style
Edit the prompt in `summarize.py` to change tone, length, or format.

### Add categories
Add new keys to `RSS_FEEDS` — Claude will automatically group them.

---

## ❓ Troubleshooting

**Email not received?**
- Check GitHub Actions logs (Actions tab → latest run)
- Verify Gmail App Password is correct (not your regular password)
- Check spam folder

**Claude API error?**
- Verify `ANTHROPIC_API_KEY` secret is set correctly
- Check [console.anthropic.com](https://console.anthropic.com) for usage/billing

**No articles found?**
- Some RSS feeds may be temporarily down — the script will still send a fallback message

---

## 📄 License

MIT — free to use, modify, and share.
