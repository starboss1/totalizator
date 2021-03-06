from flask_user import roles_required
from flask import Blueprint, render_template, flash, request, jsonify, redirect

from app.forms.AdminForm import *
from app.database.db_queries import db_queries
from app.exceptions.game_exceptions import PlaceBetException

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@roles_required('admin')
def main_page():
    return redirect("/admin/matches")


@admin_blueprint.route('/admin/matches', methods=['GET', 'POST'])
@roles_required('admin')
def matches():
    form = AdminCreateMatchForm()
    if form.validate_on_submit():
        try:
            match = db_queries.create_match(match_name=form.name.data, datetime_match=form.date.data)
            flash(f"Match #{match.id} created successfully", "success")
        except PlaceBetException:
            flash(f"This match is already exists", "error")
    matches_list = db_queries.get_all_matches()
    return render_template('pages/adminka/admin_bets.html', form=form, matches=matches_list)


@admin_blueprint.route('/admin/matches/<match_id>', methods=['GET', 'POST'])
@roles_required('admin')
def match_edit(match_id):
    form = AdminCreateEventForm()
    match = db_queries.get_match_by_id(match_id)
    possible_outcomes = db_queries.get_all_possible_outcomes()
    if form.validate_on_submit():
        event = db_queries.create_event(event_name=form.name.data,
                                        coefficient=form.coefficient.data,  match=match)
        flash(f"Event #{event.id} created successfully", "success")
    return render_template('pages/adminka/admin_bet_edit.html', form=form, match=match,
                           possible_outcomes=possible_outcomes)


@admin_blueprint.route('/admin/matches/<match_id>/update_outcome', methods=['POST'])
@roles_required('admin')
def update_outcome(match_id):
    outcomes = request.get_json()
    for outcome in outcomes:
        db_queries.update_event_outcome(outcome['event_id'], outcome['outcome_id'])
    match = db_queries.get_event_by_id(outcomes[0]['event_id']).match
    db_queries.calculate_results(match)
    return jsonify({"message": f"Outcome successfully updated for match #{match_id}"})

