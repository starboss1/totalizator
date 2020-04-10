from flask import Flask
from config import config_object
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.controllers import index_blueprint, authentication_blueprint

app = Flask(__name__)
app.config.from_object(config_object)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.register_blueprint(index_blueprint)
app.register_blueprint(authentication_blueprint)

from app.database import models
#
# def start_app():
#     database.init_app(app)
#     migrate.init_app(app, database)
#
#
#     return app

