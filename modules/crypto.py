import requests
import json
import config
from datetime import datetime
from reportlab.pdfgen import canvas
from sklearn.ensemble import IsolationForest

# 1️⃣ **Blockchain APIs (Bitcoin, Ethereum)**
BLOCKCHAIN_API_URLS = {
    "Bitcoin": f"https://api.blockcypher.com/v1/btc/main/addrs/{{}}/full?token={config.OSINTELConfig.BLOCKCYPHER_API_KEY}",
    "Ethereum": f"https://api.blockcypher.com/v1/eth/main/addrs/{{}}/full?token={config.OSINTELConfig.BLOCKCYPHER_API_KEY}"
}

# 2️⃣ **Monitor Crypto Transactions**
def monitor_crypto_transactions(wallet_address):
    """Tracks transactions of a given crypto wallet."""
    print(f"🔍 Scanning blockchain transactions for {wallet_address}...")

    findings = {}

    for currency, api_url in BLOCKCHAIN_API_URLS.items():
        url = api_url.format(wallet_address)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                num_txs = len(data.get("txs", []))
                total_received = data.get("total_received", 0) / 10**8  # Convert Satoshis to BTC
                total_sent = data.get("total_sent", 0) / 10**8

                findings[currency] = {
                    "Total Transactions": num_txs,
                    "Total Received": f"{total_received:.4f} {currency}",
                    "Total Sent": f"{total_sent:.4f} {currency}"
                }
                print(f"✅ {currency} Wallet Detected: {num_txs} transactions found.")
            else:
                findings[currency] = "❌ No transactions detected"

        except Exception as e:
            findings[currency] = f"⚠️ Error: {str(e)}"

    return findings

# 3️⃣ **AI-Based Crypto Fraud Analysis**
def ai_crypto_fraud_analysis(findings):
    """Uses AI to assess blockchain fraud risk."""
    model = IsolationForest(n_estimators=100, contamination=0.1)
    data = [{"Fraud_Score": 1 if "Total Transactions" in v else 0} for v in findings.values()]
    df = json.dumps(data)

    model.fit([[entry["Fraud_Score"]] for entry in json.loads(df)])
    fraud_scores = model.predict([[entry["Fraud_Score"]] for entry in json.loads(df)])

    fraud_risk_level = sum(fraud_scores) / len(fraud_scores)

    if fraud_risk_level < -0.3:
        print("🚨 HIGH-RISK CRYPTO WALLET DETECTED!")
    
    return fraud_risk_level

# 4️⃣ **Generate Crypto Intelligence Report (PDF)**
def generate_crypto_report(wallet_address, findings, fraud_score):
    """Creates a detailed Blockchain Intelligence Report in PDF."""
    filename = f"Crypto_Report_{wallet_address}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    c = canvas.Canvas(filename)

    c.drawString(100, 750, "💰 Blockchain Intelligence Report")
    c.drawString(100, 730, f"Wallet Address: {wallet_address}")
    c.drawString(100, 710, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 680, "🔍 Blockchain Findings:")

    y = 660
    for currency, result in findings.items():
        c.drawString(120, y, f"- {currency}: {result}")
        y -= 20

    c.drawString(100, y - 20, "🚨 AI Crypto Fraud Score:")
    c.drawString(120, y - 40, f"- Risk Level: {fraud_score}")

    c.save()
    print(f"📄 Crypto Intelligence Report saved as {filename}")

# 5️⃣ **Real-Time Alerts Using Telegram (If Enabled)**
def send_telegram_alert(message):
    """Sends alerts via Telegram if the bot token is set in config."""
    if config.OSINTELConfig.TELEGRAM_BOT_TOKEN:
        url = f"https://api.telegram.org/bot{config.OSINTELConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": config.OSINTELConfig.TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    else:
        print("⚠️ Telegram alerts are disabled. Configure in `config.json` if needed.")

# 6️⃣ **Blockchain OSINT Execution**
def run():
    """Executes the blockchain intelligence module."""
    wallet_address = input("Enter the crypto wallet address to track: ")

    findings = monitor_crypto_transactions(wallet_address)
    fraud_score = ai_crypto_fraud_analysis(findings)
    generate_crypto_report(wallet_address, findings, fraud_score)

    # Send Telegram Alerts if high-risk wallet detected
    if fraud_score < -0.3:
        send_telegram_alert(f"🚨 HIGH-RISK CRYPTO WALLET DETECTED!\nWallet: {wallet_address}")

    print("✅ Blockchain OSINT completed.")

if __name__ == "__main__":
    run()