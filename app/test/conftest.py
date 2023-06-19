import pytest
from flask_migrate import Migrate, upgrade as flask_migrate_upgrade
from flask_wtf.csrf import CSRFProtect
from app.blog import create_app
from app.config import TestingConfig
from app.blog.models import db
from app.test.actions.auth import Auth
from app.test.actions.role import RoleTesting


@pytest.fixture()
def auth(app):
    return Auth(app)


@pytest.fixture()
def roles(app):
    return RoleTesting(app)


@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    # other setup can go here
    with app.app_context():
        CSRFProtect(app)
        db.init_app(app)
        Migrate(app, db, directory='app/migrations')
        flask_migrate_upgrade(directory="app/migrations")

        RoleTesting(app).create_roles()
        Auth(app).create_user()

        yield app

        Auth(app).delete_user()
        RoleTesting(app).delete_roles()
    # clean up / reset resources here


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()
