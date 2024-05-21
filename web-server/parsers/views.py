from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from parsers.core import FACTORY


class ParsersApiView(APIView):
    def get(self, request):
        url = request.GET.get("url")
        parse_type = request.GET.get("parse-type")

        if not url or not parse_type:
            return Response(
                {"error": "Both url and parse-type parameters are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        parsed_args = {
            "url": url,
            "directory": "",
            "max_videos": 0,
        }

        parser = FACTORY.create(parse_type, **parsed_args)
        parsed_objects = parser.parse(download_content=False)
        parsed_objects_list = []
        for obj in parsed_objects:
            obj_type = "url" if parse_type in ["images", "videos"] else "text"

            parsed_objects_list.append(
                {
                    "obj-type": parse_type,
                    "data": {
                        obj_type: obj
                    }
                }
            )

        return Response(parsed_objects_list, status=status.HTTP_200_OK)


@require_GET
def parse_content(request):
    url = request.GET.get("url")
    parse_type = request.GET.get("parse-type")

    if not url or not parse_type:
        return JsonResponse(
            {"error": "Both url and parse-type parameters are required"}, status=400
        )

    parsed_args = {
        "url": url,
        "directory": "",
        "max_videos": 0,
    }

    parser = FACTORY.create(parse_type, **parsed_args)
    parsed_objects = parser.parse(download_content=False)
    parsed_objects_list = []
    for obj in parsed_objects:
        if parse_type in ["images", "videos"]:
            parsed_objects_list.append({"obj-type": parse_type, "data": {"url": obj}})
        else:
            parsed_objects_list.append({"obj-type": parse_type, "data": {"text": obj}})

    return JsonResponse(parsed_objects_list, safe=False)
