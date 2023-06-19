from app.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class ParserOrmAsync:
    def __init__(self):
        self.engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI_ASYNC)

    async def save(self, articles: list):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)

        async with async_session() as session:
            async with session.begin():
                session.add_all(articles)

        await self.engine.dispose()
