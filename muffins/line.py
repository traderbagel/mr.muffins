from flask import current_app
from linebot import (
    LineBotApi, WebhookHandler
)


CHANNEL_ACCESS_TOKEN = '1aliDJdFBoUAdsyt0ZSpJ1j3sHglbo4HAUC+De5r5tmMNK2Omwd/h3x98YJmA5Gd3lK/3z3EdAXwbLOtchyG0DOOw6cfn23QT8SRkS3ENYSk/Nnycd///bCC4XYcHn9vBmX4bIC7XH9ev77rMJHxmQdB04t89/1O/w1cDnyilFU=/1O/w1cDnyilFU=' # line_bot_api
LINE_BOT_API = LineBotApi(CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(CHANNEL_ACCESS_TOKEN)
