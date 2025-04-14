import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()  # 讀取 .env 檔案

app = Flask(__name__)

# YOUR_API_URL = os.getenv("YOUR_API_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")


@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Slack URL 驗證
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # 處理訊息事件
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "message" and not event.get("bot_id"):
            user = event.get("user")
            text = event.get("text")
            channel = event.get("channel")

            # # 發送到你的後端 API
            # response = requests.post(YOUR_API_URL, json={"user": user, "text": text})
            result_text = "成功了"

            # 回傳到 Slack
            # 回覆訊息到 Slack 頻道
            try:
                headers = {
                    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                    "Content-Type": "application/json",
                }
                payload = {"channel": channel, "text": f"🔍 結果：{user}, {text}"}
                slack_response = requests.post(
                    "https://slack.com/api/chat.postMessage",
                    headers=headers,
                    json=payload,
                    timeout=5,
                )
                slack_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"無法傳送訊息到 Slack：{e}")

    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
