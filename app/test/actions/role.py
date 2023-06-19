from app.blog.models import Role, db


class RoleTesting:
    def __init__(self, client):
        self.client = client

    def create_roles(self):
        with self.client.app_context():
            role_admin = Role(
                id=1,
                name='Admin',
                alias='admin'
            )
            db.session.add(role_admin)

            role_user = Role(
                id=2,
                name='User',
                alias='user'
            )
            db.session.add(role_user)

            db.session.commit()

    def delete_roles(self):
        with self.client.app_context():
            db.session.query(Role).delete()
            db.session.commit()