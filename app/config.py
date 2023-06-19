class Config(object):
    DEBUG = True
    ENV = 'local'
    FLASK_APP = 'blog'
    SECRET_KEY = 'TvFm9Ana'
    SESSION_TYPE = 'filesystem'
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@postgresql/flask_blog'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/flask_blog'
    SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@postgresql/flask_blog'
    # SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@localhost/flask_blog'


class TestingConfig(Config):
    ENV = 'test'
    SCHEDULER_API_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@postgresql_testing/flask_blog_testing'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost:5433/flask_blog_testing'
    # SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@postgresql_testing/flask_blog_testing'
    SQLALCHEMY_DATABASE_URI_ASYNC = 'postgresql+asyncpg://user:pass@localhost:5433/flask_blog_testing'


class DevelopConfig(Config):
    ENV = 'develop'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
