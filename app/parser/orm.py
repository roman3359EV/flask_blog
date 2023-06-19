from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import Config
from app.blog.models import Article


class ParserOrm:
    def __init__(self):
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        # self.session = Session(self.engine)

    def save(self, article: Article):
        # session.add(article)
        # session.commit()
        with Session(self.engine) as session:
            session.add(article)
            session.commit()
