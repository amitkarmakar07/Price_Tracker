import time
import smtplib
import requests
import csv
from email.mime.text import MIMEText
from datetime import datetime
from config import PRODUCT_URL, TARGET_PRICE, WEBHOOK_URL, CHECK_INTERVAL
from utils import scrape_price

# Email credentials
EMAIL_FROM = "amit@gmail.com"
EMAIL_TO = "user@gmail.com"
EMAIL_SUBJECT = "Flipkart Price Drop Alert"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "abcc@gmail.com"
EMAIL_PASSWORD = "your_app_password"

old_price = None

def send_email(title, old_price, new_price, url):
    body = f"""Flipkart Price Alert

Product: {title}
Old Price: ₹{old_price if old_price else 'N/A'}
New Price: ₹{new_price}
Link: {url}
"""
    msg = MIMEText(body)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print("Failed to send email:", e)

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

            #  checking price update

            if current_price < TARGET_PRICE:
                if old_price is None or current_price != old_price:
                    send_email(title, old_price, current_price, PRODUCT_URL)
                    log_alert(title, old_price, current_price, PRODUCT_URL)

            # sending the webhook
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
                    except Exception as e:
                        print("Failed to send webhook:", e)

                    old_price = current_price
                else:
                    print("Price is low, but alert already sent.")
            else:
                print(f"Still above target (₹{TARGET_PRICE})")

        time.sleep(CHECK_INTERVAL)
