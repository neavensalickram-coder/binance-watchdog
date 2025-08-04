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
        lp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=241&pageSize=1").json()
        airdrop = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=243&pageSize=1").json()
        launchpad = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=245&pageSize=1").json()
        return lp, airdrop, launchpad
    except:
        return None, None, None

last_titles = ["", "", ""]

def check_for_updates():
    global last_titles
    lp, airdrop, launchpad = fetch_binance_data()
    updated = False

    if lp and lp["data"]["articles"][0]["title"] != last_titles[0]:
        last_titles[0] = lp["data"]["articles"][0]["title"]
        send_telegram(f"🚀 New Launchpool: {last_titles[0]}")
        updated = True

    if airdrop and airdrop["data"]["articles"][0]["title"] != last_titles[1]:
        last_titles[1] = airdrop["data"]["articles"][0]["title"]
        send_telegram(f"🎁 New Airdrop: {last_titles[1]}")
        updated = True

    if launchpad and launchpad["data"]["articles"][0]["title"] != last_titles[2]:
        last_titles[2] = launchpad["data"]["articles"][0]["title"]
        send_telegram(f"🧪 New Launchpad: {last_titles[2]}")
        updated = True

    if not updated:
        print("No updates found.")

if __name__ == "__main__":
    send_telegram("🟢 Binance Watchdog started & checking hourly...")
    while True:
        check_for_updates()
        time.sleep(3600)  # Check every 1 hour
