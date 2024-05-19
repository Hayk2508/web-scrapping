import os
import unittest
from unittest.mock import patch

import tempfile

from myproject.parsers.media_parser import MediaParser


class TestMediaParser(unittest.TestCase):
    @patch.multiple("parsers.media_parser.MediaParser", __abstractmethods__=set())
    def setUp(self) -> None:
        self.parser = MediaParser(
            url="https://example.com", directory="/path/to/directory"
        )

    @patch("parsers.media_parser.requests.get")
    def test_fetch(self, mock_requests):
        mock_requests.return_value.content = b"""
            <html>
                <body>
                    <h1>Example HTML Content</h1>
                    <p>This is paragraph 1.</p>
                    <p>This is paragraph 2.</p>
                    <p>This is paragraph 3.</p>
                </body>
            </html>
        """

        tag = "p"

        result = self.parser.fetch(tag)
        self.assertEqual(len(result), 3)

    @patch("parsers.media_parser.requests.get")
    def test_download(self, mock_requests):
        mock_content = b"Image content"
        mock_requests.return_value.content = mock_content
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            media_url = "https://example.com/image.jpg"
            media_name = "image.jpg"
            self.parser.directory = tmp_dir_name
            self.parser.download(media_url)

            file_path = os.path.join(tmp_dir_name, media_name)
            with open(file_path, "rb") as f:
                self.assertEqual(f.read(), mock_content)


if __name__ == "__main__":
    unittest.main()
