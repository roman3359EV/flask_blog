def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_login_post_fail(client, auth, roles):
    # roles.create_roles()
    # auth.create_user()
    fail = client.post('/login', data={'login': 'test2', 'password': 'password'}, follow_redirects=True)
    assert fail.request.path == '/login'


def test_login_post_success(client, auth, roles):
    success = client.post('/login', data={'login': 'test1', 'password': 'password'}, follow_redirects=True)
    assert success.request.path == '/profile'
    # auth.delete_user()
    # roles.delete_roles()


def test_logout_post(client, auth, roles):
    response = client.get('/logout', follow_redirects=True)
    assert response.request.path == '/login'

