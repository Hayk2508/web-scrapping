import unittest
from unittest.mock import patch, MagicMock

from parsers.video_parser import VideoParser


class TestVideoParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = VideoParser(
            url="https://example.com", directory="/path/to/directory", max_videos=3
        )

    @patch("parsers.media_parser.MediaParser.download")
    @patch("parsers.media_parser.MediaParser.fetch")
    def test_parse(self, mock_fetch, mock_download):
        mock_fetch.return_value = [
            MagicMock(
                find=lambda tag: MagicMock(
                    get=lambda attr: "https://example.com/video1.mp4"
                )
            ),
            MagicMock(
                find=lambda tag: MagicMock(
                    get=lambda attr: "https://example.com/video2.mp4"
                )
            ),
            MagicMock(
                find=lambda tag: MagicMock(
                    get=lambda attr: "https://example.com/video3.mp4"
                )
            ),
            MagicMock(
                find=lambda tag: MagicMock(
                    get=lambda attr: "https://example.com/video4.mp4"
                )
            ),
        ]
        self.parser.parse()
        self.assertEqual(mock_fetch.call_count, 1)
        self.assertEqual(mock_download.call_count, 3)


if __name__ == "__main__":
    unittest.main()
