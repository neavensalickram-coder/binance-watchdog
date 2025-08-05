import requests
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def fetch_binance_data():
    try:
        lp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48b4995e1e04473b6ef3c7010c0598c&pageSize=1")
        airdrop = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=2&catalogId=48b4995e1e04473b6ef3c7010c0598c&pageSize=1")
        launchpad = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=3&catalogId=48b4995e1e04473b6ef3c7010c0598c&pageSize=1")

        if lp.status_code == 200 and airdrop.status_code == 200 and launchpad.status_code == 200:
            return lp.json(), airdrop.json(), launchpad.json()
        else:
            print("❌ Binance API status code error")
            return None, None, None
    except Exception as e:
        print(f"❌ Binance API fetch error: {e}")
        return None, None, None

last_titles = ("", "", "")

def check_for_updates():
    global last_titles
    lp, airdrop, launchpad = fetch_binance_data()

    if not lp or not airdrop or not launchpad:
        return

    updated = False

    # Launchpool block
    try:
        articles = lp.get("data", {}).get("articles", []) if lp else []
if articles and articles[0]["title"] != last_titles[0]:
                last_titles = (title, last_titles[1], last_titles[2])
                send_telegram(f"🚀 New Launchpool: {title}")
                updated = True
    except Exception as e:
        print(f"Launchpool error: {e}")

    # Airdrop block
    try:
        if airdrop.get("data", {}).get("articles"):
            title = airdrop["data"]["articles"][0]["title"]
            if title != last_titles[1]:
                last_titles = (last_titles[0], title, last_titles[2])
                send_telegram(f"🎁 New Airdrop: {title}")
                updated = True
    except Exception as e:
        print(f"Airdrop error: {e}")

    # Launchpad block
    try:
        if launchpad.get("data", {}).get("articles"):
            title = launchpad["data"]["articles"][0]["title"]
            if title != last_titles[2]:
                last_titles = (last_titles[0], last_titles[1], title)
                send_telegram(f"📢 New Launchpad: {title}")
                updated = True
    except Exception as e:
        print(f"Launchpad error: {e}")

    if not updated:
        print("✅ No updates found.")

if __name__ == "__main__":
    print("🔄 Binance monitor starting...")
    while True:
        check_for_updates()
        time.sleep(3600)  # Check every hour



