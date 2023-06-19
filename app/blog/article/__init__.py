from flask import Blueprint

article_routes = Blueprint('articles', __name__, template_folder='templates')

from . import routes
