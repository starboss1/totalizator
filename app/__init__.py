from flask import Flask
from config import config_object
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.controllers import index_blueprint, authentication_blueprint


def start_app():
    app = Flask(__name__)
    app.config.from_object(config_object)

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(authentication_blueprint)

    return app


from app.db import models
