from rest_framework import viewsets
from rest_framework.decorators import api_view
from parsers.core import FACTORY

from core.services.response_service import create_response
from parsers.core.image_parser import ImgParserBuilder
from parsers.core.video_parser import VideoParserBuilder
from parsers.models import (
    ImageParser,
    VideoParser,
    ParsedObject,
    ImageParsedObject,
    VideoParsedObject,
)
from parsers.serializers import (
    ParseContentReqSerializer,
    ParseContentRespSerializer,
    ParsedObjectSerializer,
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
        data = parsed_object.to_data()
        response_data.append({"obj_type": parsed_object.to_type(), "data": data})

    return create_response(
        data=response_data, serializer_class=ParseContentRespSerializer, many=True
    )


class ParsedObjectViewSet(viewsets.ModelViewSet):
    queryset = ParsedObject.objects.all()
    serializer_class = ParsedObjectSerializer
