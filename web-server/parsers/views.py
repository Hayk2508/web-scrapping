from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from parsers.core import FACTORY
from parsers.core.video_parser import VideoParserBuilder
from parsers.core.image_parser import ImgParserBuilder
from parsers.serializers import ParseContentReqSerializer, ParseContentRespSerializer


@api_view(['GET'])
def parse_content(request):
    serializer_req = ParseContentReqSerializer(data=request.query_params)
    if not serializer_req.is_valid():
        raise APIException(serializer_req.errors, code=status.HTTP_400_BAD_REQUEST)
    url = serializer_req.validated_data["url"]
    parse_type = serializer_req.validated_data["parse_type"]

    parsed_args = {
        "url": url,
        "directory": "",
        "max_videos": 0,
    }

    parser = FACTORY.create(parse_type, **parsed_args)
    parsed_objects = parser.parse()
    response_data = [{"obj_type": parse_type, "data": obj} for obj in parsed_objects]
    serializer_resp = ParseContentRespSerializer(data=response_data,  many=True)

    if not serializer_resp.is_valid():
        raise APIException(serializer_resp.errors, code=status.HTTP_400_BAD_REQUEST)
    return Response(serializer_resp.validated_data)

