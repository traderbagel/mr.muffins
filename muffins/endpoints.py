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

BP = Blueprint('root', __name__)


@BP.route("/", method=["GET"])
def index():
    # img = urllib.request.urlretrieve("http://opendata.cwb.gov.tw/opendata/MFC/F-C0035-015.jpg", "weather.jpg")
    return current_app.config.get('PAGE_TITLE')

@BP.route("/origin_weather", method=["GET"])
def get_origin_weather():
    img = urllib.request.urlretrieve("http://opendata.cwb.gov.tw/opendata/MFC/F-C0035-015.jpg", "origin_weather.jpg")
    return send_file('origin_weather.jpg', mimetype='image/jpg')

# document: https://github.com/line/line-bot-sdk-python
@BP.route("/callback", method=["POST"])
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
@current_app.LINE_HANDLER.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        receive_text = str(event.message.text)        
        if "雨" in receive_text or "天氣" in receive_text:
            reply = "http://opendata.cwb.gov.tw/opendata/MFC/F-C0035-015.jpg"
        elif "吃" in receive_text or "食" in receive_text:
            reply = "最近想吃酸酸辣辣的泰式料理"
        elif "幹" in receive_text:
            reply = "妹子妹子不收泣"
        else:
            reply = "愛妹子!對不起！妹子不要生氣氣惹"
        
        current_app.LINE_BOT_API.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except LineBotApiError as e:
        abort(400)

@current_app.LINE_HANDLER.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    try:
        reply = f"(lat,lng): ({event.message.latitude},{event.message.longitude})"

        current_app.LINE_BOT_API.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except LineBotApiError as e:
        abort(400)
