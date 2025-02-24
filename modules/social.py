import requests
import time
import json
import threading
import config
from datetime import datetime
from reportlab.pdfgen import canvas
from sklearn.ensemble import IsolationForest

# 1️⃣ **Social Media Platforms to Track**
SOCIAL_MEDIA_PLATFORMS = {
    "Twitter/X": "https://nitter.net/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}",
    "OnlyFans": "https://onlyfinder.com/search?q={}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Facebook": "https://www.facebook.com/{}"
}

# 2️⃣ **Monitor Social Media Presence**
def monitor_social_media(username):
    """Tracks user activity across social media platforms."""
    print(f"🔍 Scanning social media for {username}...")

    findings = {}

    for platform, url in SOCIAL_MEDIA_PLATFORMS.items():
        formatted_url = url.format(username)
        try:
            response = requests.get(formatted_url, timeout=10)
            if response.status_code == 200:
                findings[platform] = f"✅ Profile Found: {formatted_url}"
                print(f"✅ {platform}: Profile detected!")
            else:
                findings[platform] = "❌ No profile detected"
        except Exception as e:
            findings[platform] = f"⚠️ Error: {str(e)}"

    return findings

# 3️⃣ **AI-Based Social Behavior Analysis**
def ai_social_behavior_analysis(findings):
    """Uses AI to assess user influence & engagement trends."""
    model = IsolationForest(n_estimators=100, contamination=0.1)
    data = [{"Influence_Score": 1 if "✅" in value else 0} for key, value in findings.items()]
    df = json.dumps(data)

    model.fit([[entry["Influence_Score"]] for entry in json.loads(df)])
    influence_scores = model.predict([[entry["Influence_Score"]] for entry in json.loads(df)])

    influence_level = sum(influence_scores) / len(influence_scores)

    if influence_level < -0.3:
        print("🚨 HIGH-INFLUENCE SOCIAL MEDIA PRESENCE DETECTED!")
    
    return influence_level

# 4️⃣ **Generate Social Media OSINT Report (PDF)**
def generate_social_media_report(username, findings, influence_score):
    """Creates a detailed Social Media Intelligence Report in PDF."""
    filename = f"Social_Media_Report_{username}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    c = canvas.Canvas(filename)

    c.drawString(100, 750, "📡 Social Media Intelligence Report")
    c.drawString(100, 730, f"Generated for: {username}")
    c.drawString(100, 710, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 680, "🔍 Social Media Findings:")

    y = 660
    for platform, result in findings.items():
        c.drawString(120, y, f"- {platform}: {result}")
        y -= 20

    c.drawString(100, y - 20, "📊 AI Influence Score:")
    c.drawString(120, y - 40, f"- Score: {influence_score}")

    c.save()
    print(f"📄 Social Media Intelligence Report saved as {filename}")

# 5️⃣ **Real-Time Alerts Using Telegram (If Enabled)**
def send_telegram_alert(message):
    """Sends alerts via Telegram if the bot token is set in config."""
    if config.OSINTELConfig.TELEGRAM_BOT_TOKEN:
        url = f"https://api.telegram.org/bot{config.OSINTELConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": config.OSINTELConfig.TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    else:
        print("⚠️ Telegram alerts are disabled. Configure in `config.json` if needed.")

# 6️⃣ **Social Media OSINT Execution**
def run():
    """Executes the social media intelligence module."""
    username = input("Enter the username to track: ")
    
    findings = monitor_social_media(username)
    influence_score = ai_social_behavior_analysis(findings)
    generate_social_media_report(username, findings, influence_score)

    # Send Telegram Alerts if high-influence user detected
    if influence_score < -0.3:
        send_telegram_alert(f"🚨 HIGH-INFLUENCE SOCIAL MEDIA PROFILE DETECTED!\nUser: {username}")

    print("✅ Social Media OSINT completed.")

if __name__ == "__main__":
    run()