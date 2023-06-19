from flask import session
import re
from app.blog.models import User, db


def test_profile_get(app, client, auth, roles):
    with app.test_request_context():
        session['_user_id'] = auth.get_id()
        app.login_manager._load_user()

    profile = client.get('/profile')
    pattern = re.compile('TestName1')

    assert profile.status_code == 200
    assert True if pattern.search(profile.get_data().decode('utf-8')) is not None else False


def test_profile_set(app, client, auth, roles):
    with app.test_request_context():
        session['_user_id'] = auth.get_id()
        app.login_manager._load_user()

    profile = client.post(
        '/profile',
        data={'name': 'TestName1Update', 'login': 'test1', 'password': '', 'confirm_password': ''}
    )
    pattern = re.compile('TestName1Update')

    assert profile.status_code == 200
    assert True if pattern.search(profile.get_data().decode('utf-8')) is not None else False


def test_delete(app, client, auth, roles):
    with app.test_request_context():
        session['_user_id'] = auth.get_id()
        app.login_manager._load_user()

    profile = client.post('/delete', follow_redirects=True)
    delete_user = db.session.query(User).filter_by(login='test1').first()

    assert profile.request.path == '/login'
    assert delete_user.active is False

