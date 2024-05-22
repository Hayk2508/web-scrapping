from parsers.core import FACTORY

from rest_framework import serializers


class ParseContentReqSerializer(serializers.Serializer):
    url = serializers.URLField()
    parse_type = serializers.ChoiceField(choices=list(FACTORY.builders.keys()))


class ParseContentRespSerializer(serializers.Serializer):
    obj_type = serializers.CharField()
    data = serializers.CharField()

