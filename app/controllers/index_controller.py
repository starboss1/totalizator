from flask import Blueprint, render_template

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def index_page():
    return render_template('pages/index.html')
