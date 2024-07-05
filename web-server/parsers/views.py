from rest_framework import viewsets
from rest_framework.decorators import api_view
from parsers.core import PARSERS_FACTORY, PARSED_OBJECTS_FACTORY

from core.services.response_service import create_response
from parsers.core.image_parser import ImgParserBuilder
from parsers.core.parsed_object_service import (
    create_parsed_object,
    update_parsed_object,
)
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
    ParsedObjectSerializer,
    CreateParsedObjectSerializer,
)

from parsers.core.parsed_objects_builders import (
    ImageParsedObjectBuilder,
    VideoParsedObjectBuilder,
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
        parsed_object = create_parsed_object(obj_type, serializer.validated_data)
        return create_response(
            instance=parsed_object, serializer=ParsedObjectSerializer, many=False
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CreateParsedObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_parsed_object(obj=instance, data=serializer.validated_data)
        return create_response(
            instance=instance, serializer=ParsedObjectSerializer, many=False
        )
