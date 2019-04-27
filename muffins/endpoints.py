import os 
import urllib

from flask import (
    Blueprint,
    current_app,
    request,
    send_file,
    abort,
)

from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError,
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, ImageSendMessage
)

from muffins.line import LINE_BOT_API, LINE_HANDLER
from muffins.solitaire import solitaire

# Deploy Note
'''
https://dashboard.heroku.com/apps/mrmuffins/deploy/heroku-git

heroku git:remote -a mrmuffins
git push heroku master

# https://yaoandy107.github.io/line-bot-tutorial/
'''
BP = Blueprint('root', __name__)


@BP.route("/", methods=["GET"])
def index():
    # img = urllib.request.urlretrieve("http://opendata.cwb.gov.tw/opendata/MFC/F-C0035-015.jpg", "weather.jpg")
    return current_app.config.get('PAGE_TITLE')

# document: https://github.com/line/line-bot-sdk-python
@BP.route("/callback", methods=["POST"])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # current_app.logger.info(f"Request body {body}")
    try:
        current_app.LINE_HANDLER.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



# Line handler
@LINE_HANDLER.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        receive_text = str(event.message.text)        
        if "雨" in receive_text or "天氣" in receive_text:
            reply = "http://opendata.cwb.gov.tw/opendata/MFC/F-C0035-015.jpg"
        elif "玩" in receive_text:
            reply = "玩成語接龍，開始：" + solitaire.start()
        elif len(receive_text) == 4:
            reply = solitaire.get_next(receive_text)
        else:
            reply = "可以跟我玩成語接龍或是問我天氣"
        
        current_app.LINE_BOT_API.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except LineBotApiError as e:
        abort(400)

@LINE_HANDLER.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    try:
        reply = f"(lat,lng): ({event.message.latitude},{event.message.longitude})"

        current_app.LINE_BOT_API.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except LineBotApiError as e:
        abort(400)
