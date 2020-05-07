from flask import Blueprint, render_template, request, jsonify
from flask_user import login_required, current_user

from app.exceptions.game_exceptions import PlaceBetException
from app.database.db_queries import db_queries

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
def basket_play():
    matches = db_queries.get_pending_matches()
    return render_template('pages/games/games.html', matches=matches)


@game_blueprint.route('/play/<match_id>')
@login_required
def match_play(match_id):
    match = db_queries.get_match_by_id(match_id)
    possible_outcomes = db_queries.get_all_possible_outcomes()
    return render_template('pages/games/game_placebet.html', match=match, possible_outcomes=possible_outcomes)


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
    response = jsonify({"message": "Bet placed successfully"})
    return response


@game_blueprint.errorhandler(PlaceBetException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
