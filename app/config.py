from dotenv import load_dotenv
from os import environ as env

load_dotenv('.env')


class Config(object):
    DEBUG = env.get('APP_DEBUG', True)
    ENV = env.get('APP_ENV', 'local')
    FLASK_APP = env.get('APP_NAME', '')
    SECRET_KEY = env.get('APP_SECRET_KEY', '')
    SESSION_TYPE = env.get('SESSION_TYPE', 'filesystem')
    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI', '')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@postgresql/flask_blog'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/flask_blog'
    SQLALCHEMY_DATABASE_URI_ASYNC = env.get('SQLALCHEMY_DATABASE_URI_ASYNC', '')
    # SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@postgresql/flask_blog'
    # SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@localhost/flask_blog'
    SCHEDULER_API_ENABLED = True


class TestingConfig(Config):
    DEBUG = True
    FLASK_APP = 'blog'
    SECRET_KEY = 'TvFm9Ana'
    SESSION_TYPE = 'filesystem'
    ENV = 'testing'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@postgresql_testing/flask_blog_testing'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost:5433/flask_blog_testing'
    # SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@postgresql_testing/flask_blog_testing'
    SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@localhost:5433/flask_blog_testing'
    SCHEDULER_API_ENABLED = False


class DevelopConfig(Config):
    ENV = env.get('APP_ENV', 'develop')


class ProductionConfig(Config):
    DEBUG = env.get('APP_DEBUG', False)
    ENV = env.get('APP_ENV', 'production')
