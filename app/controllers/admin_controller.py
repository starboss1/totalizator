from flask_user import roles_required
from flask import Blueprint, render_template, flash, request, jsonify, redirect

from app.forms.AdminForm import *
from app.database.db_queries import db_queries

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
        match = db_queries.create_match(match_name=form.name.data, datetime_match=form.date.data)
        flash(f"Match #{match.id} created successfully", "success")

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


# @admin_blueprint.route('/admin/event/<event_id>/update_outcome', methods=['POST'])
# @roles_required('admin')
# def update_outcome(event_id):
#     print(request.get_json())
#     print(event_id)
#     # outcome_id = request.get_json()['outcome_id']
#     # db_queries.update_event_outcome(outcome_id=outcome_id, event_id=event_id)
#     return jsonify({"message": f"Outcome successfully updated for event #{event_id}"})
@admin_blueprint.route('/admin/matches/<match_id>/update_outcome', methods=['POST'])
@roles_required('admin')
def update_outcome(match_id):
    print('request = '+str(request.get_json()))
    print('match_id = '+str(match_id))
    outcomes = request.get_json()
    for outcome in outcomes:
        db_queries.update_event_outcome(outcome['event_id'], outcome['outcome_id'])
    match = db_queries.get_event_by_id(outcomes[0]['event_id']).match
    db_queries.distribute_pool(match)
    return jsonify({"message": f"Outcome successfully updated for match #{match_id}"})

@admin_blueprint.route('/admin/matches/<match_id>/distribute', methods=['GET'])
@roles_required('admin')
def test_distribute(match_id):
    db_queries._distribute_pool(db_queries.get_match_by_id(match_id))
    return "test_distribute"