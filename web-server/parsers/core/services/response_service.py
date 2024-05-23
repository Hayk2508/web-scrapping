from rest_framework.response import Response


def create_response(data, serializer_class) -> Response:
    serializer_resp = serializer_class(data=data, many=True)
    if not serializer_resp.is_valid():
        raise ValueError("Internal Server Error")
    return Response(serializer_resp.validated_data)
