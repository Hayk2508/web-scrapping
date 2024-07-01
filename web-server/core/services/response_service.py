from rest_framework.response import Response




def validate_response(response_serializer, data=None, instance=None, many=False):
    if instance is not None:
        serializer = response_serializer(instance, many=many)
        return Response(serializer.data)
    serializer = response_serializer(data=data)
    serializer.is_valid(raise_exception=True)


def create_response(data=None, instance=None, serializer=None, many=False) -> Response:
    if serializer is None:
        return Response(data)
    resp = validate_response(
        response_serializer=serializer, data=data, instance=instance, many=many
    )

    if instance is not None:
        assert resp is not None
        return resp
    return Response(data)
