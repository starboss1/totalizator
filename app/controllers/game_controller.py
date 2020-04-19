from flask import Blueprint, render_template, request, jsonify
from flask_user import login_required, current_user

from app.exceptions.game_exceptions import PlaceBetException
from app.database.db_queries import db_queries

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
def basket_play():
    draws = db_queries.get_pending_draws()
    return render_template('pages/games/basketball.html', draws=draws)


@game_blueprint.route('/play/<draw_id>')
@login_required
def draw_play(draw_id):
    draw = db_queries.get_draw_by_id(draw_id)
    possible_outcomes = db_queries.get_all_possible_outcomes()
    return render_template('pages/games/basketball_placebet.html', draw=draw, possible_outcomes=possible_outcomes)


@game_blueprint.route('/play/placebet', methods=['POST'])
@login_required
def place_bet():
    json = request.get_json()
    print('json = ', json)
    amount = json['info']['amount']
    if amount == '':
        raise PlaceBetException(message="Provide bet amount data")

    events_data = json['events']
    db_queries.place_bet(amount=amount, events_data=events_data, user=current_user)
    return jsonify({"message": "Bet placed successfully"})


@game_blueprint.errorhandler(PlaceBetException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
