from app.controllers.index_controller import index_blueprint
from app.controllers.authentication_controller import authentication_blueprint
from app.controllers.game_controller import game_blueprint
from app.controllers.admin_controller import admin_blueprint

__all__ = ['index_blueprint', 'admin_blueprint', 'authentication_blueprint', 'game_blueprint']
