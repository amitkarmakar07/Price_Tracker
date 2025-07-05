# webhook_server.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("\n Price Drop Alert!")
    print("Product:", data.get("title"))
    print("Old Price:", data.get("old_price"))
    print("New Price:", data.get("new_price"))
    print("Link:", data.get("url"))
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(port=5000)
