from flask import Flask, current_app

from muffins import logger
from muffins.converters import JsonEncoder

logger = logger

def create_app():
    app = Flask(__name__)
    app.config.from_object('muffins.settings.default')

    app.json_encoder = JsonEncoder
    _register_blueprints(app)
    
    return app


def _register_blueprints(app):
    from muffins.endpoints import BP as root

    app.register_blueprint(root)