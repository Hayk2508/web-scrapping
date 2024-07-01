from rest_framework import viewsets
from rest_framework.decorators import api_view
from parsers.core import PARSERS_FACTORY, PARSED_OBJECTS_FACTORY

from core.services.response_service import create_response
from parsers.core.image_parser import ImgParserBuilder
from parsers.core.video_parser import VideoParserBuilder
from parsers.models import (
    ImageParser,
    VideoParser,
    ParsedObject,
    ImageParsedObject,
    VideoParsedObject,
    ImageParsedObjectBuilder,
    VideoParsedObjectBuilder,
)
from parsers.serializers import (
    ParseContentReqSerializer,
    ParsedObjectSerializer,
    CreateParsedObjectSerializer,
)


@api_view(["GET"])
def parse_content(request):
    serializer_req = ParseContentReqSerializer(data=request.query_params)
    serializer_req.is_valid(raise_exception=True)
    url = serializer_req.validated_data["url"]
    parse_type = serializer_req.validated_data["parse_type"]
    max_videos = serializer_req.validated_data["max_videos"]
    parsed_args = {"url": url, "max_videos": max_videos}

    parser = PARSERS_FACTORY.create(parse_type, **parsed_args)
    parsed_objects = parser.parse()
    return create_response(
        instance=parsed_objects, serializer=ParsedObjectSerializer, many=True
    )


class ParsedObjectViewSet(viewsets.ModelViewSet):
    queryset = ParsedObject.objects.all()
    serializer_class = ParsedObjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateParsedObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj_type = serializer.validated_data["obj_type"]
        parsed_object = PARSED_OBJECTS_FACTORY.create(
            obj_type, **serializer.validated_data
        )
        parsed_object.save()
        return create_response(
            instance=parsed_object, serializer=ParsedObjectSerializer, many=False
        )
