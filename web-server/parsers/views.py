from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.decorators import api_view
from parsers.core import FACTORY

from core.services.response_service import create_response
from parsers.core.image_parser import ImgParserBuilder
from parsers.core.video_parser import VideoParserBuilder
from parsers.models import (
    Url,
    ImageParser,
    VideoParser,
    ParsedObject,
    ImageParsedObject,
    VideoParsedObject,
)
from parsers.serializers import (
    ParseContentReqSerializer,
    ParseContentRespSerializer,
    ImageParsedObjectSerializer,
    VideoParsedObjectSerializer,
)


@api_view(["GET"])
def parse_content(request):
    serializer_req = ParseContentReqSerializer(data=request.query_params)
    serializer_req.is_valid(raise_exception=True)

    url = serializer_req.validated_data["url"]
    parse_type = serializer_req.validated_data["parse_type"]
    parsed_args = {"url": url}

    parser = FACTORY.create(parse_type, **parsed_args)
    parsed_objects = parser.parse()

    response_data = []

    for parsed_object in parsed_objects:
        data = parser.to_data(parsed_object)
        content_type = ContentType.objects.get_for_model(parsed_object)
        response_data.append({"obj_type": content_type.name, "data": data})

    return create_response(
        data=response_data, serializer_class=ParseContentRespSerializer, many=True
    )


class ImageParsedObjectViewSet(viewsets.ModelViewSet):
    queryset = ImageParsedObject.objects.all()
    serializer_class = ImageParsedObjectSerializer


class VideoParsedObjectViewSet(viewsets.ModelViewSet):
    queryset = VideoParsedObject.objects.all()
    serializer_class = VideoParsedObjectSerializer
