from flask import Flask
from config import config_object
from flask_migrate import Migrate
from flask_user import UserManager
from app.database.models import User
from app.controllers import index_blueprint, authentication_blueprint, game_blueprint

app = Flask(__name__)
app.config.from_object(config_object)

from app.database import db
db.init_app(app)
db.app = app
migrate = Migrate(app, db)
user_manager = UserManager(app, db, UserClass=User)

from app.database.db_queries import db_queries
db_queries.init_db(db, user_manager)

app.register_blueprint(index_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(game_blueprint)

from app.database import models
#
# def start_app():
#     database.init_app(app)
#     migrate.init_app(app, database)
#
#
#     return app

