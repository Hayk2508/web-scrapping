from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def to_data(self, obj) -> dict:
        pass
