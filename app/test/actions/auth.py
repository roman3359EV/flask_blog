from app.blog.models import User, Role, db
from werkzeug.security import generate_password_hash


class Auth:
    def __init__(self, client, name='TestName1', login='test1', password='password'):
        self.client = client
        self.name = name
        self.login = login
        self.password = password

    def create_user(self):
        with self.client.app_context():
            test_user = User(
                name=self.name,
                login=self.login,
                password=generate_password_hash(self.password),
                role_id=Role.ROLE_USER,
                active=True
            )
            db.session.add(test_user)
            db.session.commit()

    def get_id(self) -> int:
        with self.client.app_context():
            user = db.session.query(User).filter_by(login=self.login).first()

        return user.id

    def get(self) -> int:
        with self.client.app_context():
            user = db.session.query(User).filter_by(login=self.login).first()

        return user

    def delete_user(self):
        with self.client.app_context():
            db.session.query(User).filter_by(login=self.login).delete()
            db.session.commit()