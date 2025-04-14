import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()  # 讀取 .env 檔案

app = Flask(__name__)

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Slack URL 驗證
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # 處理訊息事件
    if data.get("type") == "event_callback":
        event = data.get("event", {})

        # 檢查事件類型是否為 app_mention
        if event.get("type") == "app_mention":
            channel = event.get("channel")
            text = "@igris Hello world!"

            try:
                # 傳送回應到 Slack 頻道
                result = client.chat_postMessage(
                    channel=channel, text=text, parse="full", link_names=True
                )
                logger.info("Message posted: %s", result)
                return (
                    jsonify(
                        {
                            "status": "success",
                            "slack_response": result.data,
                            "orginal_data": data,
                        }
                    ),
                    200,
                )
            except SlackApiError as e:
                logger.error("Error posting message: %s", e)
                return jsonify({"status": "error", "error": e}), 500
        return (
            jsonify(
                {"status": "ignored", "message": "No action taken for this request"}
            ),
            200,
        )


if __name__ == "__main__":
    app.run(debug=True)
