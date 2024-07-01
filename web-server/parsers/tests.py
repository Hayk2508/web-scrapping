from unittest.mock import MagicMock, patch
from django.test import TestCase
from parsers.core.image_parser import ImgParser
from parsers.core.media_parser import MediaParser
from parsers.core.video_parser import VideoParser
from parsers.models import ImageParsedObject, ImageParser, VideoParsedObject


class TestImageParser(TestCase):
    def setUp(self) -> None:
        self.parser = ImgParser(url="https://example.com")

    @patch("parsers.core.media_parser.MediaParser.fetch")
    def test_parse(self, mock_fetch):
        mock_fetch.return_value = [
            MagicMock(get=lambda attr: "image1.jpg"),
            MagicMock(get=lambda attr: "image2.jpg"),
        ]

        self.parser.parse()

        self.assertEqual(mock_fetch.call_count, 1)

        image_parsed_objects = ImageParsedObject.objects.all()

        self.assertEqual(len(image_parsed_objects), 2)


class TestMediaParser(TestCase):
    @patch.multiple("parsers.core.media_parser.MediaParser", __abstractmethods__=set())
    def setUp(self) -> None:
        self.parser = MediaParser(url="https://example.com")

    @patch("parsers.core.media_parser.requests.get")
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


class TestVideoParser(TestCase):
    def setUp(self) -> None:
        self.parser = VideoParser(url="https://example.com", max_videos=3)

    @patch("parsers.core.media_parser.MediaParser.fetch")
    @patch.object(VideoParsedObject.objects, "filter")
    @patch.object(VideoParsedObject.objects, "create")
    def test_parse(self, mock_create, mock_filter, mock_fetch):
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
        ]

        mock_filter.return_value.exists.return_value = False

        mock_create.side_effect = lambda **kwargs: VideoParsedObject(**kwargs)

        vide_parsed_objects = self.parser.parse()
        self.assertEqual(mock_fetch.call_count, 1)
        self.assertEqual(len(vide_parsed_objects), 3)
