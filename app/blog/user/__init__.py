from flask import Blueprint

user_routes = Blueprint('users', __name__, template_folder='templates')

from . import routes
