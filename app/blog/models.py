from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    accesses = db.relationship('Access', backref='access', lazy=True)
    articles = db.relationship('Article', backref='articles', lazy=True)
    payments = db.relationship('Payment', backref='payments', lazy=True)
    subscribe = db.relationship('Subscribe', uselist=False, backref='subscribe', lazy=True)

    def __repr__(self):
        return f"User {self.name}"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_balance(cls, user) -> str:
        if not isinstance(user, User):
            return f"0 р."

        if not user.subscribe:
            return f"0 р."

        return f"{user.subscribe.balance} р."


class Role(db.Model):
    ROLE_ADMIN = 1
    ROLE_USER = 2

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    alias = db.Column(db.String(255), unique=True, nullable=False)
    users = db.relationship('User', backref='users', lazy=False)

    def __repr__(self):
        return f"Role {self.name}"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category_articles', lazy=False)

    def __repr__(self):
        return f"Category {self.name}"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    alias = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag {self.name}"


tags = db.Table('tag_article',
                db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                db.Column('article_id', db.Integer, db.ForeignKey('articles.id'))
                )


class Article(db.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_PRIVATE = 3

    PER_PAGE = 10

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    accesses = db.relationship('Access', backref='article_access', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return f"Article {self.name}"


class Access(db.Model):
    __tablename__ = 'access'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)

    @classmethod
    def is_access(cls, article: Article, user: User) -> bool:
        if article.status == Article.STATUS_PUBLIC:
            return True

        if not isinstance(user, User):
            return False

        if article.author_id == user.id:
            return True

        access = Access.query.filter(and_(Access.article_id == Article.id, Access.user_id == user.id)).first()
        if access is not None:
            return True

        return False


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class Subscribe(db.Model):
    __tablename__ = 'subscribes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
