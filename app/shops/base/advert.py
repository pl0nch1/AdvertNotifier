import sys
from dataclasses import dataclass
from hashlib import md5


@dataclass
class Advert:
    title: str = 'Udefined'
    url: str = 'Udefined'
    time_ago: str = 'Udefined'
    cost: str = 'Udefined'

    @staticmethod
    def make_url(text, link):
        return f'[{text}]({link})'

    def __str__(self):
        return f'{Advert.make_url(self.title, self.url)} ({self.cost}) - {self.time_ago}'

    def __hash__(self):
        return int.from_bytes(md5(bytes(self.url, 'UTF-8')).digest(), sys.byteorder)
