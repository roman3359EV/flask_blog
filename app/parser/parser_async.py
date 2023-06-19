from bs4 import BeautifulSoup
import aiohttp, asyncio


class ParserAsync:
    def __init__(self, domain: str, slug: str):
        self.domain = domain
        self.slug = slug
        self.result = dict()

    async def parse_news(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.domain}{self.slug}") as response:
                text = await response.text()
                parser = BeautifulSoup(text, 'html.parser')
                captions = parser.findAll('a', 'news-section__item-name')

                self.result = {caption['href']: {'name': caption.text.strip(), 'text': ''} for caption in captions}

    async def iterate_news(self):
        tasks = []
        for key, item in self.result.items():
            task = asyncio.create_task(self.parse_new(key))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def parse_new(self, link: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.domain}{link}") as response:
                response_text = await response.text()
                parser_item = BeautifulSoup(response_text, 'html.parser')
                new_item = parser_item.find('div', 'news-detail__text')

                self.result[link]['text'] = ' '.join(list(new_item.stripped_strings)[3:])

    def get_result(self) -> dict:
        return self.result
