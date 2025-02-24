import requests
import time
import json
import threading
import config
from bs4 import BeautifulSoup
from datetime import datetime
from reportlab.pdfgen import canvas
from sklearn.ensemble import IsolationForest

# 1️⃣ **Darknet Configuration**
TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

DARKNET_SITES = {
    "Hacker Forums": "http://dark.fail/search?q=hacking",
    "Black Markets": "http://ahmia.fi/search?q=stolen+credentials",
    "Carding Shops": "http://onionlandsearchengine.com/search?q=credit+cards",
    "Ransomware Networks": "http://hss3uro2hsxfogfq.onion/search?q=ransomware",
    "Weapons Market": "http://dark.fail/search?q=illegal+weapons"
}

# 2️⃣ **Darknet Monitoring**
def monitor_darknet():
    """Scans darknet forums and marketplaces for criminal activity."""
    print("🔍 Scanning darknet forums and markets...")

    findings = {}

    for name, url in DARKNET_SITES.items():
        try:
            response = requests.get(url, proxies=TOR_PROXY, timeout=20)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.find_all("a")
                if results:
                    findings[name] = f"🚨 Threat Detected! ({len(results)} mentions found)"
                    print(f"⚠️ ALERT: Possible {name} activity detected at {url}")
                else:
                    findings[name] = "No activity detected"
        except Exception as e:
            findings[name] = f"Error accessing site: {str(e)}"

    return findings

# 3️⃣ **AI-Based Cybercrime Risk Analysis**
def ai_cybercrime_risk_analysis(findings):
    """Uses AI to assess darknet threat levels."""
    model = IsolationForest(n_estimators=100, contamination=0.1)
    data = [{"Threat_Level": len(value.split())} for key, value in findings.items()]
    df = json.dumps(data)

    model.fit([[entry["Threat_Level"]] for entry in json.loads(df)])
    risk_scores = model.predict([[entry["Threat_Level"]] for entry in json.loads(df)])

    risk_level = sum(risk_scores) / len(risk_scores)

    if risk_level < -0.5:
        print("🚨 HIGH-RISK CYBERCRIME ACTIVITY DETECTED!")
    
    return risk_level

# 4️⃣ **Generate Darknet Intelligence Report (PDF)**
def generate_darknet_report(findings, risk_score):
    """Creates a detailed Darknet Cybercrime Intelligence Report in PDF."""
    filename = f"Darknet_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    c = canvas.Canvas(filename)

    c.drawString(100, 750, "🚨 Darknet Cybercrime Intelligence Report")
    c.drawString(100, 730, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 700, "🔍 Darknet Findings:")

    y = 680
    for site, result in findings.items():
        c.drawString(120, y, f"- {site}: {result}")
        y -= 20

    c.drawString(100, y - 20, "🚨 AI Cybercrime Risk Score:")
    c.drawString(120, y - 40, f"- Threat Level: {risk_score}")

    c.save()
    print(f"📄 Intelligence Report saved as {filename}")

# 5️⃣ **Real-Time Alerts Using Telegram (If Enabled)**
def send_telegram_alert(message):
    """Sends alerts via Telegram if the bot token is set in config."""
    if config.OSINTELConfig.TELEGRAM_BOT_TOKEN:
        url = f"https://api.telegram.org/bot{config.OSINTELConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": config.OSINTELConfig.TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    else:
        print("⚠️ Telegram alerts are disabled. Configure in `config.json` if needed.")

# 6️⃣ **Darknet OSINT Execution**
def run():
    """Executes the darknet intelligence module."""
    findings = monitor_darknet()
    risk_score = ai_cybercrime_risk_analysis(findings)
    generate_darknet_report(findings, risk_score)

    # Send Telegram Alerts if high-risk activity detected
    if risk_score < -0.5:
        send_telegram_alert(f"🚨 HIGH-RISK DARKNET ACTIVITY DETECTED!\nThreat Level: {risk_score}")

    print("✅ Darknet OSINT completed.")

if __name__ == "__main__":
    run()