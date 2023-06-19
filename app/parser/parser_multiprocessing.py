from multiprocessing import Process, Queue, Pool
from bs4 import BeautifulSoup
from abc import abstractmethod
import requests, pickle, queue


class Parser:
    COUNT_PROCESS = 5

    def __init__(self, domain: str, slug: str):
        self.domain = domain
        self.slug = slug
        self.result = dict()
        self.processes = []

    def parse_news(self) -> None:
        response = requests.get(f"{self.domain}{self.slug}")
        parser = BeautifulSoup(response.text, 'html.parser')
        captions = parser.findAll('a', 'news-section__item-name')

        self.result = {caption['href']: {'name': caption.text.strip(), 'text': ''} for caption in captions}

    @abstractmethod
    def iterate_news(self) -> None:
        pass

    def parse_new(self, link: str) -> dict:
        response_item = requests.get(f"{self.domain}{link}")
        parser_item = BeautifulSoup(response_item.text, 'html.parser')
        new_item = parser_item.find('div', 'news-detail__text')

        return {
            'key': link,
            'text': ' '.join(list(new_item.stripped_strings)[3:])
        }

    def get_result(self) -> dict:
        return self.result


class ParserWithQueue(Parser):
    def __init__(self, domain: str, slug: str):
        super().__init__(domain, slug)
        self.queue_tasks = Queue()
        self.queue_results = Queue()

    def iterate_news(self) -> None:
        for key, item in self.result.items():
            self.queue_tasks.put(key)

        for i in range(Parser.COUNT_PROCESS):
            process = Process(target=self.queue_handler)
            self.processes.append(process)
            process.start()

        for process_item in self.processes:
            process_item.join()

        while not self.queue_results.empty():
            message = pickle.loads(self.queue_results.get())
            self.result[message.get('key')]['text'] = message.get('text')

    def queue_handler(self) -> bool:
        while True:
            try:
                task = self.queue_tasks.get_nowait()
            except queue.Empty:
                break
            else:
                new = self.parse_new(task)
                self.put_result(new)

        return True

    def put_result(self, new: dict) -> None:
        self.queue_results.put(pickle.dumps(new))


class ParserWithPool(Parser):
    def __init__(self, domain: str, slug: str):
        super().__init__(domain, slug)

    def iterate_news(self) -> None:
        with Pool(Parser.COUNT_PROCESS) as pool:
            result = pool.map(self.parse_new, [i for i in self.result.keys()])
            for item in result:
                self.result[item.get('key')]['text'] = item.get('text')
