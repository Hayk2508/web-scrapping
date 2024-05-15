import os
import unittest
from unittest.mock import patch, mock_open

from parsers.media_parser import MediaParser


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
        abs_path = os.path.join("/path/to/directory", "image.jpg")
        with patch("builtins.open", mock_open()) as mock_file_open:
            media_url = "https://example.com/image.jpg"
            self.parser.download(media_url)

            mock_file_open.assert_called_once_with(abs_path, "wb")


if __name__ == "__main__":
    unittest.main()
