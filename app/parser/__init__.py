# from parser_requests import Parser
# from parser_theading import Parser
from parser_multiprocessing import ParserWithPool
from parser_async import ParserAsync
import asyncio
from orm import ParserOrm
from orm_async import ParserOrmAsync
from dto import ParserDto
from time import time


def parse():
    parser_obj = ParserWithPool('https://www.onlinetambov.ru', '/news/')

    # start
    start = time()

    parser_obj.parse_news()

    # time 1
    time1 = time() - start
    print(time1)

    parser_obj.iterate_news()

    # time 2
    time2 = time() - start - time1
    print(time2)

    result = parser_obj.get_result()

    parser_orm = ParserOrm()

    for item in result.values():
        article = ParserDto.article_dto(item)
        parser_orm.save(article)

    return


async def async_parse():
    parser_obj = ParserAsync('https://www.onlinetambov.ru', '/news/')

    # start
    start = time()

    await parser_obj.parse_news()

    # time 1
    time1 = time() - start
    print(time1)

    await parser_obj.iterate_news()

    # time 2
    time2 = time() - start - time1
    print(time2)

    result = parser_obj.get_result()

    parser_orm = ParserOrmAsync()

    articles = []
    for article in result.values():
        articles.append(ParserDto.article_dto(article))

    await parser_orm.save(articles)

    return


if __name__ == '__main__':
    # parse()
    asyncio.run(async_parse())
