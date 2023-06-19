from flask import Flask
from flask_login import LoginManager
from .article import article_routes
from .models import User, db
from .subscribe import subscribe_routes
from .routes import common_routes
from .user import user_routes


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(common_routes)
    app.register_blueprint(article_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(subscribe_routes)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        return db.session.get(User, int(user_id))

    return app
