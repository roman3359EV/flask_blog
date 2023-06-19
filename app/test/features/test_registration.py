from app.blog.models import User, db


def test_registration_get(client, roles):
    # roles.create_roles()
    response = client.get('/registration')
    assert response.status_code == 200


def test_registration_post(client):
    registration = client.post(
        '/registration',
        data={'name': 'my_name', 'login': 'my_login', 'password': '123456'},
        follow_redirects=True
    )
    new_user = User.query.filter_by(login='my_login').first()
    assert registration.request.path == '/login'
    assert isinstance(new_user, User)
    assert new_user.name == 'my_name'
    assert new_user.active


def test_login_after_registration(client, roles):
    success = client.post('/login', data={'login': 'my_login', 'password': '123456'}, follow_redirects=True)
    assert success.request.path == '/profile'
    new_user = User.query.filter_by(login='my_login').first()
    db.session.delete(new_user)
    db.session.commit()
    # roles.delete_roles()
