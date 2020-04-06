from flask import Flask
from config import config_object
from app.controllers import index_blueprint


def start_app():
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(index_blueprint)

    return app
