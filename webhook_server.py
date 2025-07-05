from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# email config
EMAIL_FROM = "karamit819@gmail.com"
EMAIL_TO = "amittkarmakar@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "karamit819@gmail.com"
EMAIL_PASSWORD = "####"

def send_email(title, old_price, new_price, url):
    body = f"""Flipkart Price Drop Alert

Product: {title}
Old Price: {old_price}
New Price: {new_price}
Link: {url}
"""
    msg = MIMEText(body)
    msg["Subject"] = "Flipkart Price Alert"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent from webhook.")
    except Exception as e:
        print("Failed to send email:", e)

# webhook endpoint

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    title = data.get("title")
    old_price = data.get("old_price")
    new_price = data.get("new_price")
    url = data.get("url")

    print("Webhook received:")
    print("Title:", title)
    print("Old Price:", old_price)
    print("New Price:", new_price)
    print("URL:", url)

    send_email(title, old_price, new_price, url)

    return jsonify({"status": "email sent"}), 200

if __name__ == "__main__":
    app.run(port=5000)
