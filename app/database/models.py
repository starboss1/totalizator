from app.database import db
from datetime import datetime
from functools import reduce
from passlib.hash import sha256_crypt

from sqlalchemy.ext.hybrid import hybrid_property
from flask_user import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), server_default='')
    active = True

    balance = db.Column(db.Float, nullable=False, default=0)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    bets = db.relationship('Bet', back_populates='user')

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt .verify(password, self.password)

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
    coefficient = db.Column(db.Float, nullable=False)

    match_fk = db.Column(db.Integer, db.ForeignKey('matches.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='CASCADE', onupdate='CASCADE'))

    outcome = db.relationship('Outcome')
    match = db.relationship('Match', back_populates="events")
    bets = db.relationship('Bet', secondary='bet_details')


class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    datetime_match = db.Column(db.DateTime, nullable=True)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)
    events = db.relationship('Event', back_populates='match', order_by='Event.id')

    @hybrid_property
    def match_status(self):
        if self.is_finished:
            return "finished"

        if self.datetime_match < datetime.now():
                return "waiting_results"
        else:
            return "pending"

    @hybrid_property
    def all_bets(self):
        bets = set()
        if len(self.events) > 0:
            for p in self.events[0].bets:
                bets.add(p)
        return bets

    @hybrid_property
    def pool_amount(self):
        return reduce(lambda x, y: x+y.amount, self.all_bets, 0)

    @hybrid_property
    def all_players(self):
        players = set()
        for p in self.all_bets:
            players.add(p.user)
        return players


class Bet(db.Model):
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    win_sum = db.Column(db.Float, nullable=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates="bets")
    bet_details = db.relationship('BetDetails')

    @hybrid_property
    def all_events(self):
        events = set()
        for bd in self.bet_details:
            events.add(bd.event)
        return events


class BetDetails(db.Model):
    __tablename__ = 'bet_details'

    bet_fk = db.Column(db.Integer, db.ForeignKey('bets.id', ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False, primary_key=True)
    event_fk = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, primary_key=True)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False, primary_key=True)

    outcome = db.relationship('Outcome')
    event = db.relationship('Event')
