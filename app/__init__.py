from flask import Flask
from config import config_object
from flask_migrate import Migrate
from flask_user import UserManager
from app.database.models import User
from logging import StreamHandler, INFO, Formatter
from logging.handlers import RotatingFileHandler
import os
from app.controllers import index_blueprint, authentication_blueprint, game_blueprint, admin_blueprint


def create_app():
    # init flask app
    app = Flask(__name__)
    app.config.from_object(config_object)

    # init database and migrations
    from app.database import db
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)
    user_manager = UserManager(app, db, UserClass=User)
    from app.database.db_queries import db_queries
    db_queries.init_db(db, user_manager)

    # register blueprints
    app.register_blueprint(index_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(admin_blueprint)

    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = StreamHandler()
            stream_handler.setLevel(INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/totalizator.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(INFO)
        app.logger.info('Totalizator startup')

    return app

from app.database import models


