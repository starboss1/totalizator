from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy
from app.database.models import *
from app.exceptions.database_exceptions import *
from app.exceptions.game_exceptions import PlaceBetException
import random


class DatabaseQueries:
    def __init__(self):
        self.db: SQLAlchemy = None
        self.user_manager: UserManager = None

    def init_db(self, db_sqlalchemy: SQLAlchemy, user_manager: UserManager):
        self.db = db_sqlalchemy
        self.user_manager = user_manager

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_username(self, username) -> User:
        return User.query.filter_by(username=username).first()

    def create_user(self, username, password, email, balance=0,  is_admin=False):
        user = User(username=username, balance=balance, email=email)
        user.set_password(password)
        if is_admin:
            user.roles.append(self._get_or_create(Role, name='admin'))
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def _get_or_create(self, model, **kwargs):
        instance = self.db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.db.session.add(instance)
            self.db.session.commit()
            return instance

    def update_user_balance(self, user, diff):
        user.balance = user.balance + diff
        self.db.session.commit()

    def get_pending_matches(self):
        datetime_now = datetime.now()
        return Match.query.filter(Match.datetime_match > datetime_now).order_by(Match.datetime_match.desc())

    def create_match(self, match_name, datetime_match):
        match = Match(name=match_name, datetime_match=datetime_match)
        self.db.session.add(match)
        self.db.session.commit()
        return match
    
    def get_all_matches(self):
        return Match.query.order_by(Match.id.desc()).all()

    def create_event(self, event_name, coefficient, match, outcome=None):
        event = Event(name=event_name, coefficient=coefficient, match=match, outcome=outcome)
        self.db.session.add(event)
        self.db.session.commit()
        return event

    def get_match_by_id(self, match_id):
        return Match.query.get(match_id)

    def get_event_by_id(self, event_id) -> Event:
        return Event.query.get(event_id)

    def get_all_possible_outcomes(self):
        return Outcome.query.order_by(Outcome.id).all()

    def get_match_by_bet(self, bet: Bet) -> Match:
        res: BetDetails = BetDetails.query.filter(BetDetails.bet_fk == bet.id).scalar()
        return res.event.match

    def place_bet(self, amount: int, events_data, user: User):

        if user.balance < float(amount):
            raise PlaceBetException(message="Not enough funds")

        bet = Bet(amount=amount, user=user)
        self.db.session.add(bet)
        self.db.session.commit()

        for parlay_info in events_data:
            self.db.session.add(
                BetDetails(bet_fk=bet.id, outcome_fk=parlay_info['value'], event_fk=parlay_info['name']))

        user.balance -= float(amount)
        self.db.session.commit()

    def update_event_outcome(self, event_id, outcome_id):
        event = self.get_event_by_id(event_id)
        event.outcome_fk = outcome_id

        # if self._check_match_waiting_for_distribution(match):

        self.db.session.commit()

    def _check_match_waiting_for_distribution(self, match):
        if match.match_status != "waiting_results":
            return False
        for event in match.events:
            if event.outcome is None:
                return False
        return True

    def distribute_pool(self, match):
        bets_of_match = match.all_bets
        match.is_finished = True
        for bet in bets_of_match:
            win_sum = bet.amount*self._get_coefficient_all_event_of_bet(bet)
            bet.win_sum = win_sum
            bet.user.balance += win_sum
        self.db.session.commit()

    def _get_coefficient_all_event_of_bet(self, bet:Bet):
        total_coeff = 0

        for bet_details in bet.bet_details:
            event = self.get_event_by_id(bet_details.event_fk)
            if int(event.outcome_fk) == bet_details.outcome_fk:
                total_coeff += event.coefficient
            else:
                total_coeff = 0
                break
        return total_coeff


db_queries = DatabaseQueries()
