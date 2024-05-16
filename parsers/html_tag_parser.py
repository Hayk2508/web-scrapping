from datetime import datetime
import os

from parsers import register_builder
from parsers.parser_abc import Parser


class HtmlTagParser(Parser):
    def __init__(self, url: str, directory: str, tag: str):
        super().__init__(url=url)
        self.html_tag = tag
        self.directory = directory

    def parse(self):
        tags = self.fetch(self.html_tag)
        abs_path = os.path.join(self.directory, f'{self.html_tag}_{datetime.now().strftime('%d/%m/%Y')}.txt')
        with open(abs_path, 'w') as file:
            for tag in tags:
                if tag.text:
                    file.write(tag.text)
                    file.write('\n==================\n')


@register_builder("HtmlTag")
class HtmlTagBuilder:
    def __call__(self, url: str, directory: str, tag: str, **_ignored):
        return HtmlTagParser(url=url, directory=directory, tag=tag)
