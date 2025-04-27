import requests
import os
import time

# Load from environment variables (Railway will automatically handle this)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Constants for the P2P tracking
ASSET = "USDT"
FIAT = "UZS"
TRADE_TYPE = "SELL"
PAY_TYPE = "Uzcard"
LIMIT = 10
THRESHOLD_PRICE = 13200  # Price alert threshold
INTERVAL_SECONDS = 1200  # 20 minutes

def send_alert(price: float):
    """
    Send a Telegram alert when the price is above the threshold.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    text = (
        f"🚨 High Sell Price Alert!\n"
        f"Top USDT sell price via Uzcard: {price} UZS\n"
        f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Check it fast!"
    )
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def get_highest_price() -> float | None:
    """
    Fetch the highest selling USDT price from CryptoBot P2P marketplace.
    """
    try:
        url = "https://p2p.cryptobot.biz/api/merchant/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36"
        }
        params = {
            "asset": ASSET,
            "fiat": FIAT,
            "trade_type": TRADE_TYPE,
            "limit": LIMIT,
            "pay_type": PAY_TYPE
        }
        response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        offers = data.get("data", [])
        if not offers:
            return None
        return float(offers[0]['price'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def main():
    """
    Main loop to continuously fetch the highest price and check against the threshold.
    """
    while True:
        price = get_highest_price()
        if price and price >= THRESHOLD_PRICE:
            send_alert(price)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
