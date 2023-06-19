from datetime import datetime
from app.blog.models import Article


class ParserDto:
    AUTHOR_ID_DEFAULT = 4

    @classmethod
    def article_dto(cls, item: dict) -> Article:
        return Article(
            name=item.get('name', ''),
            text=item.get('text', ''),
            author_id=ParserDto.AUTHOR_ID_DEFAULT,
            status=Article.STATUS_DRAFT,
            created_at=f"{datetime.now():%Y-%m-%d %H:%M:%S}",
            updated_at=f"{datetime.now():%Y-%m-%d %H:%M:%S}",
            category_id=1
        )