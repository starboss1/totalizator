from flask import Blueprint, redirect

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def index_page():
    return redirect('/play')
