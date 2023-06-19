from flask import render_template
from flask import Blueprint

common_routes = Blueprint('common', __name__)


@common_routes.route('/')
def index() -> str:
    return render_template('index.html')