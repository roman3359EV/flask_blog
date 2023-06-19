from bs4 import BeautifulSoup
import threading
import requests


class Parser:
    def __init__(self, domain: str, slug: str):
        self.domain = domain
        self.slug = slug
        self.result = dict()
        self.threading = []

    def parse_news(self) -> None:
        response = requests.get(f"{self.domain}{self.slug}")
        parser = BeautifulSoup(response.text, 'html.parser')
        captions = parser.findAll('a', 'news-section__item-name')

        self.result = {caption['href']: {'name': caption.text.strip(), 'text': ''} for caption in captions}

    def iterate_news(self):
        for key, item in self.result.items():
            self.threading.append(threading.Thread(target=self.parse_new, args=(key, )))
            self.threading[-1].start()

        for item in self.threading:
            item.join()

    def parse_new(self, link: str) -> None:
        response_item = requests.get(f"{self.domain}{link}")
        parser_item = BeautifulSoup(response_item.text, 'html.parser')
        new_item = parser_item.find('div', 'news-detail__text')

        self.result[link]['text'] = ' '.join(list(new_item.stripped_strings)[3:])

    def get_result(self) -> dict:
        return self.result
