import time
import requests
import csv
from datetime import datetime
from config import PRODUCT_URL, TARGET_PRICE, WEBHOOK_URL, CHECK_INTERVAL
from utils import scrape_price

old_price = None

# function to log alerts to a CSV file
def log_alert(title, old_price, new_price, url):
    with open("alerts.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            title,
            f"₹{old_price}" if old_price else "N/A",
            f"₹{new_price}",
            url
        ])

if __name__ == "__main__":
    while True:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking price...")

        title, current_price = scrape_price()

        if current_price is None:
            print("Could not fetch the price.")
        else:
            print(f"Product: {title}")
            print(f"Current Price: ₹{current_price}")
            print(f"Target Price: ₹{TARGET_PRICE}")

            if current_price < TARGET_PRICE:
                if old_price is None or current_price != old_price:
                    log_alert(title, old_price, current_price, PRODUCT_URL)

                    # send webhook notification
                    try:
                        payload = {
                            "title": title,
                            "old_price": f"₹{old_price}" if old_price else "N/A",
                            "new_price": f"₹{current_price}",
                            "url": PRODUCT_URL
                        }
                        r = requests.post(WEBHOOK_URL, json=payload)
                        if r.status_code == 200:
                            print("Webhook alert sent.")
                        else:
                            print("Webhook failed:", r.status_code)
                    except Exception as e:
                        print("Failed to send webhook:", e)

                    old_price = current_price
                else:
                    print("Price is low, but alert already sent.")
            else:
                print(f"Price is still above target (₹{TARGET_PRICE})")

        time.sleep(CHECK_INTERVAL)
