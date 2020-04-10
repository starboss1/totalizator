from app import db
from datetime import datetime
from functools import reduce

from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), server_default='')
    balance = db.Column(db.Float, nullable=False, default=0)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    parlays = db.relationship('Parlay', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class Outcome(db.Model):
    __tablename__ = 'possible_outcomes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f'<Outcome {self.name}'


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    draw_fk = db.Column(db.Integer, db.ForeignKey('draws.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='CASCADE', onupdate='CASCADE'))

    outcome = db.relationship('Outcome')
    draw = db.relationship('Draw', back_populates="events")
    parlays = db.relationship('Parlay', secondary='parlay_details')


class Draw(db.Model):
    __tablename__ = 'draws'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    datetime_first_match = db.Column(db.DateTime, nullable=True)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)
    events = db.relationship('Event', back_populates='draw', order_by='Event.id')

    @hybrid_property
    def draw_status(self):
        if self.is_finished:
            return "finished"
        if self.datetime_first_match < datetime.now():
                return "waiting_results"
        else:
            return "pending"

    @hybrid_property
    def all_parlays(self):
        parlays = set()
        if len(self.events) > 0:
            for p in self.events[0].parlays:
                parlays.add(p)
        return parlays

    @hybrid_property
    def pool_amount(self):
        return reduce(lambda x, y: x+y.amount, self.all_parlays, 0)

    @hybrid_property
    def all_players(self):
        players = set()
        for p in self.all_parlays:
            players.add(p.user)
        return players


class Parlay(db.Model):
    __tablename__ = 'parlays'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    win_sum = db.Column(db.Float, nullable=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates="parlays")
    parlay_details = db.relationship('ParlayDetails')


class ParlayDetails(db.Model):
    __tablename__ = 'parlay_details'

    parlay_fk = db.Column(db.Integer, db.ForeignKey('parlays.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False, primary_key=True)
    event_fk = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, primary_key=True)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False, primary_key=True)

    outcome = db.relationship('Outcome')
    event = db.relationship('Event')


@event.listens_for(Role.__table__, 'after_create')
def init_roles(*args, **kwargs):
    db.session.add(Role(name="admin"))
    db.session.commit()


@event.listens_for(Outcome.__table__, 'after_create')
def init_outcomes(*args, **kwargs):
    db.session.add(Outcome(name="W1"))
    db.session.add(Outcome(name="X"))
    db.session.add(Outcome(name="W2"))
    db.session.commit()


# @event.listens_for(UserRoles.__tablename__, 'after_create')
# def init_users(*args, **kwargs):
# TODO: users

