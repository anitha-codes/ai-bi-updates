import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def load_subscribers(path="subscribers.json") -> list:
    """Load subscriber list from JSON file."""
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("subscribers", [])


def build_html_email(plain_text: str, date_str: str) -> str:
    """Wrap the plain text summary in a clean HTML email template."""
    # Convert markdown-style bullets to HTML
    lines = plain_text.split('\n')
    html_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append('<br>')
        elif line.startswith('•'):
            html_lines.append(f'<li style="margin-bottom:8px;">{line[1:].strip()}</li>')
        elif line.startswith('🤖') or line.startswith('📊') or line.startswith('💡') or line.startswith('📰'):
            html_lines.append(f'<h3 style="color:#2d2d2d;margin-top:20px;margin-bottom:8px;">{line}</h3>')
        else:
            html_lines.append(f'<p style="margin:4px 0;">{line}</p>')

    body_html = '\n'.join(html_lines)

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;max-width:650px;margin:auto;padding:20px;color:#333;">

  <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:24px;border-radius:12px;margin-bottom:24px;">
    <h1 style="color:white;margin:0;font-size:22px;">🧠 Daily AI & BI News Digest</h1>
    <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;">{date_str}</p>
  </div>

  <div style="background:#f9f9f9;border-radius:8px;padding:20px;line-height:1.7;">
    {body_html}
  </div>

  <hr style="border:none;border-top:1px solid #eee;margin:24px 0;">
  <p style="font-size:12px;color:#999;text-align:center;">
    You're receiving this because you subscribed to the AI & BI Daily Digest.<br>
    Powered by Claude AI · Automated via GitHub Actions
  </p>

</body>
</html>
"""


def send_digest(summary: str):
    """Send the digest to all subscribers."""

    # Load config from environment variables (set as GitHub Secrets)
    gmail_user = os.environ["GMAIL_USER"]          # your Gmail address
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]  # Gmail App Password (not your real password)

    subscribers = load_subscribers()
    if not subscribers:
        print("[send_email] No subscribers found.")
        return

    date_str = datetime.now().strftime("%A, %B %d %Y")
    subject = f"🧠 AI & BI Daily Digest — {date_str}"
    html_body = build_html_email(summary, date_str)

    # Connect to Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)

        sent_count = 0
        for email in subscribers:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"AI & BI Digest <{gmail_user}>"
                msg["To"] = email

                # Attach both plain text and HTML
                msg.attach(MIMEText(summary, "plain"))
                msg.attach(MIMEText(html_body, "html"))

                server.sendmail(gmail_user, email, msg.as_string())
                sent_count += 1
                print(f"[send_email] ✅ Sent to {email}")

            except Exception as e:
                print(f"[send_email] ❌ Failed for {email}: {e}")

    print(f"[send_email] Done. Sent to {sent_count}/{len(subscribers)} subscribers.")


if __name__ == "__main__":
    # Test send
    test_summary = "This is a test digest.\n• AI news item 1\n• BI news item 2"
    send_digest(test_summary)
