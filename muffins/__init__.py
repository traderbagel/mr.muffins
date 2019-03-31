from flask import Flask, current_app

from muffins import logger
from muffins.converters import JsonEncoder

from linebot import (
    LineBotApi, WebhookHandler
)

logger = logger

def create_app():
    app = Flask(__name__)
    app.config.from_object('muffins.settings.default')

    with app.app_context():
        app.LINE_BOT_API = LineBotApi(app.config.get('CHANNEL_ACCESS_TOKEN'))
        app.LINE_HANDLER = WebhookHandler(app.config.get('CHANNEL_ACCESS_TOKEN'))

    app.json_encoder = JsonEncoder
    _register_blueprints(app)
    
    return app


def _register_blueprints(app):
    from muffins.endpoints import BP as root

    app.register_blueprint(root)