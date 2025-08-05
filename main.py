import requests
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

def fetch_binance_data():
    try:
        lp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnoledgeArticle&tag=launchpool&lang=en").json()
        airdrop = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnoledgeArticle&tag=airdrop&lang=en").json()
        launchpad = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=KnoledgeArticle&tag=launchpad&lang=en").json()
        return lp, airdrop, launchpad
    except:
        return None, None, None

last_titles = ("", "", "")

def check_for_updates():
    global last_titles
    updated = False
    lp, airdrop, launchpad = fetch_binance_data()

    if lp and lp["data"] and lp["data"]["articles"]:
        new_title = lp["data"]["articles"][0]["title"]
        if new_title != last_titles[0]:
            send_telegram(f"🚀 New Launchpool: {new_title}")
            last_titles = (new_title, last_titles[1], last_titles[2])
            updated = True

    if airdrop and airdrop["data"] and airdrop["data"]["articles"]:
        new_title = airdrop["data"]["articles"][0]["title"]
        if new_title != last_titles[1]:
            send_telegram(f"🎁 New Airdrop: {new_title}")
            last_titles = (last_titles[0], new_title, last_titles[2])
            updated = True

    if launchpad and launchpad["data"] and launchpad["data"]["articles"]:
        new_title = launchpad["data"]["articles"][0]["title"]
        if new_title != last_titles[2]:
            send_telegram(f"📢 New Launchpad: {new_title}")
            last_titles = (last_titles[0], last_titles[1], new_title)
            updated = True

    if not updated:
        print("✅ No updates found.")

if __name__ == "__main__":
    send_telegram("👀 Binance Watchdog started & checking every 5 minutes...")
    while True:
        check_for_updates()
        time.sleep(300)  # Check every 5 minutes


