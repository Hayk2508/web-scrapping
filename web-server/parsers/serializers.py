from parsers.core import FACTORY

from rest_framework import serializers

from parsers.models import ParsedObject, ImageParsedObject, VideoParsedObject


class ParseContentReqSerializer(serializers.Serializer):
    url = serializers.URLField()
    parse_type = serializers.ChoiceField(choices=list(FACTORY.builders.keys()))


class ParseContentRespSerializer(serializers.Serializer):
    obj_type = serializers.CharField()
    data = serializers.DictField()


class ImageParsedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageParsedObject
        fields = "__all__"


class VideoParsedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoParsedObject
        fields = "__all__"
