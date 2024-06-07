from abc import ABC, abstractmethod

from parsers.models import Url


class Parser(ABC):

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def to_data(self, obj) -> dict:
        pass

    def create_url(self):

        if not Url.objects.filter(url=self.url).exists():
            Url.objects.create(url=self.url)
