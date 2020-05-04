from flask_user import roles_required
from flask import Blueprint, render_template, flash, request, jsonify, redirect

from app.exceptions.database_exceptions import DrawEventsOverflowException
from app.forms.AdminForm import *
from app.database.db_queries import db_queries

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@roles_required('admin')
def main_page():
    return redirect("/admin/draws")


@admin_blueprint.route('/admin/draws', methods=['GET', 'POST'])
@roles_required('admin')
def draws():
    form = AdminCreateDrawForm()
    if form.validate_on_submit():
        match = db_queries.create_match(match_name=form.name.data)
        if form.add_random_events.data:
            db_queries.add_random_events_to_match(match=match, date=form.date.data)
            flash(f"Random events added to draw", "success")
        flash(f"Draw #{match.id} created successfully", "success")

    matches_list = db_queries.get_all_matches()
    return render_template('pages/adminka/admin_draws.html', form=form, matches=matches_list)


@admin_blueprint.route('/admin/matches/<match_id>', methods=['GET', 'POST'])
@roles_required('admin')
def match_edit(match_id):
    form = AdminCreateEventForm()
    match = db_queries.get_match_by_id(match_id)
    possible_outcomes = db_queries.get_all_possible_outcomes()
    if form.validate_on_submit():
        try:
            event = db_queries.create_event(event_name=form.name.data, event_datetime=form.date.data, match=match)
            flash(f"Event #{event.id} created successfully", "success")
        except DrawEventsOverflowException:
            flash(f"You are trying to add to many events: maximum {match.events_amount}", "error")
    return render_template('pages/adminka/admin_draw_edit.html', form=form, match=match,
                           possible_outcomes=possible_outcomes)


@admin_blueprint.route('/admin/event/<event_id>/update_outcome', methods=['POST'])
@roles_required('admin')
def update_outcome(event_id):
    outcome_id = request.get_json()['outcome_id']
    db_queries.update_event_outcome(outcome_id=outcome_id, event_id=event_id)
    return jsonify({"message": f"Outcome successfully updated for event #{event_id}"})


@admin_blueprint.route('/admin/matches/<draw_id>/distribute', methods=['GET'])
@roles_required('admin')
def test_distribute(draw_id):
    db_queries._distribute_pool(db_queries.get_match_by_id(draw_id))
    return "test_distribute"