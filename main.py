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
            print("❌ Binance API response code failure")
            return None, None, None

    except Exception as e:
        print(f"❌ Binance fetch failed: {e}")
        return None, None, None

last_titles = ("", "", "")

def check_for_updates():
    global last_titles
    lp, airdrop, launchpad = fetch_binance_data()

    if not lp or not airdrop or not launchpad:
        return

    updated = False

    # Launchpool block
    if lp.get("data") and lp["data"].get("article") and lp["data"]["article"]:
        title = lp["data"]["article"][0]["title"]
        if title != last_titles[0]:
            last_titles = (title, last_titles[1], last_titles[2])
            send_telegram(f"🚀 New Launchpool: {title}")
            updated = True

    # Airdrop block
    if airdrop.get("data", {}).get("articles") and airdrop["data"]["articles"]:
        title = airdrop["data"]["articles"][0]["title"]
        if title != last_titles[1]:
            last_titles = (last_titles[0], title, last_titles[2])
            send_telegram(f"🎁 New Airdrop: {title}")
            updated = True

    # Launchpad block
    if launchpad.get("data", {}).get("articles") and launchpad["data"]["articles"]:
        title = launchpad["data"]["articles"][0]["title"]
        if title != last_titles[2]:
            last_titles = (last_titles[0], last_titles[1], title)
            send_telegram(f"📢 New Launchpad: {title}")
            updated = True

    if not updated:
        print("✅ No updates found.")

# === Start monitoring loop ===
if __name__ == "__main__":
    print("🟢 Binance watcher running...")
    while True:
        check_for_updates()
        time.sleep(3600)  # Check every hour


