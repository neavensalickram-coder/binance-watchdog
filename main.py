import requests
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

last_titles = ("", "", "")
def fetch_binance_data():
    try:
        lp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnowledgeArticle&tag=launchpool&lang=en").json()
        airdrop = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnowledgeArticle&tag=airdrop&lang=en").json()
        launchpad = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnowledgeArticle&tag=launchpad&lang=en").json()
        return lp, airdrop, launchpad
    except Exception as e:
        print("Error fetching Binance data:", e)
        return None, None, None


def check_for_updates():
    global last_titles

    lp, airdrop, launchpad = fetch_binance_data()

    lp_articles = lp.get("data", {}).get("articles", []) if lp else []
    airdrop_articles = airdrop.get("data", {}).get("articles", []) if airdrop else []
    launchpad_articles = launchpad.get("data", {}).get("articles", []) if launchpad else []

    if (
        lp_articles and lp_articles[0]["title"] != last_titles[0]
        or airdrop_articles and airdrop_articles[0]["title"] != last_titles[1]
        or launchpad_articles and launchpad_articles[0]["title"] != last_titles[2]
    ):
        last_titles = [
            lp_articles[0]["title"] if lp_articles else "",
            airdrop_articles[0]["title"] if airdrop_articles else "",
            launchpad_articles[0]["title"] if launchpad_articles else ""
        ]
        send_telegram_message()


    if not updated:
        print("✅ No updates found.")

if __name__ == "__main__":
    send_telegram("👀 Binance Watchdog started & checking every 5 minutes...")
    while True:
        check_for_updates()
        time.sleep(300)  # Check every 5 minutes


