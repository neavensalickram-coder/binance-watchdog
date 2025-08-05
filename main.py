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
        lp_resp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48b499e5e1e04d73b6ef3c7010c0598c&pageSize=1")
        ad_resp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=2&catalogId=48b499e5e1e04d73b6ef3c7010c0598c&pageSize=1")
        launchpad_resp = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=3&catalogId=48b499e5e1e04d73b6ef3c7010c0598c&pageSize=1")

        # Validate status codes
        if lp_resp.status_code != 200 or ad_resp.status_code != 200 or launchpad_resp.status_code != 200:
            print("❌ API request failed — check response codes")
            return None, None, None

        lp = lp_resp.json()
        airdrop = ad_resp.json()
        launchpad = launchpad_resp.json()

        return lp, airdrop, launchpad
    except Exception as e:
        print(f"❌ Fetch Error: {e}")
        return None, None, None

last_titles = ("", "", "")

def check_for_updates():
    global last_titles
    lp, airdrop, launchpad = fetch_binance_data()
    updated = False

    if lp and lp.get("data", {}).get("articles"):
        title = lp["data"]["articles"][0]["title"]
        if title != last_titles[0]:
            send_telegram(f"🚀 New Launchpool: {title}")
            last_titles = (title, last_titles[1], last_titles[2])
            updated = True

    if airdrop and airdrop.get("data", {}).get("articles"):
        title = airdrop["data"]["articles"][0]["title"]
        if title != last_titles[1]:
            send_telegram(f"🎁 New Airdrop: {title}")
            last_titles = (last_titles[0], title, last_titles[2])
            updated = True

    if launchpad and launchpad.get("data", {}).get("articles"):
        title = launchpad["data"]["articles"][0]["title"]
        if title != last_titles[2]:
            send_telegram(f"🚀 New Launchpad: {title}")
            last_titles = (last_titles[0], last_titles[1], title)
            updated = True

    if not updated:
        print("No updates found.")

if __name__ == "__main__":
    send_telegram("✅ Binance Watchdog started & checking hourly...")
    while True:
        check_for_updates()
        time.sleep(300)  # Check every 1 hour

