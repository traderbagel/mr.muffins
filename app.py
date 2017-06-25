from flask import Flask, request, abort
import json
import requests
import os 

from linebot import (
    LineBotApi, WebhookHandler
)

import linebot.exceptions

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage
)

app = Flask(__name__)

# Some python config method :
# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b


API_CONFIG = {
	'channel_id':'1521764494',
    'channel_secret':'74c0cf68a0fd5fd6f1f68ca12c83c2f6',
	'channel_access_token':'Z6kGvct04yThOXOacWqg72dqExNO39KmKGmibbAQ2wN2yCbtnR6vx0Qq9MbCdUusC3CAsQSDcqRBEFDmO3qIImfdit5jsFV4CmcqmVViR0kSyR5ZugOB56Rhm1JKUOOkSkgPVncMfwJxBlB9up8qkwdB04t89/1O/w1cDnyilFU='
}


line_bot_api = LineBotApi(API_CONFIG['channel_access_token'])
handler = WebhookHandler(API_CONFIG['channel_secret'])


@app.route('/')
def index():
    return "<p>Hello World!</p>"

# https://github.com/line/line-bot-sdk-python
@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except linebot.exceptions.InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        reply = "love princess~" + str(event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply[::-1])) 
    except linebot.exceptions.LineBotApiError as e:
        abort(400)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    try:
        reply = str(event.message.latitude) + "." + str(event.message.longitude)
        app.logger.info("Location event: " + reply)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
    except linebot.exceptions.LineBotApiError as e:
        abort(400)

if __name__ == '__main__':
    # http://kennmyers.github.io/tutorial/2016/03/11/getting-flask-on-heroku.html
    app.debug=True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
