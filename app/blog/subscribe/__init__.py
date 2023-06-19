from flask import Blueprint

subscribe_routes = Blueprint('subscribes', __name__, template_folder='templates')

from . import routes
