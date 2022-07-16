from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi("VYkCP0EWI35XWo/TMhYx9grz4OGqaTu/8hHalp4i4jdQV7Rdeb3OTOAYx3Xl6j4idsLNAhcH+pFfzsqkwS4BYY0CmbO2mEPnD+BBpjcArUgbWmsugUiXullqm/qGPmqQ1t+ioB+/CsCbnPaVTHpI5QdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("54ae860fc81c283e6401748493be167d")

@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)