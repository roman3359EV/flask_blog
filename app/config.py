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
    CACHE_TYPE = env.get('CACHE_TYPE', 'NullCache')
    CACHE_KEY_PREFIX = env.get('CACHE_KEY_PREFIX', 'cache')
    CACHE_REDIS_HOST = env.get('CACHE_REDIS_HOST', '')
    CACHE_REDIS_PORT = env.get('CACHE_REDIS_PORT', 6379)
    CACHE_REDIS_URL = env.get('CACHE_REDIS_URL', '')
    CACHE_DEFAULT_TIMEOUT = env.get('CACHE_DEFAULT_TIMEOUT', 3600)


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
    CACHE_TYPE = 'NullCache'


class DevelopConfig(Config):
    ENV = env.get('APP_ENV', 'develop')


class ProductionConfig(Config):
    DEBUG = env.get('APP_DEBUG', False)
    ENV = env.get('APP_ENV', 'production')
