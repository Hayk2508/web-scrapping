from parsers.core import FACTORY
from rest_framework import serializers

from parsers.models import ParsedObject, ImageParsedObject, VideoParsedObject, Parser


class ParseContentReqSerializer(serializers.Serializer):
    url = serializers.URLField()
    parse_type = serializers.ChoiceField(choices=list(FACTORY.builders.keys()))


class ParseContentRespSerializer(serializers.Serializer):
    obj_type = serializers.CharField()
    data = serializers.DictField()


class ParsedObjectSerializer(serializers.ModelSerializer):
    obj_type = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = ParsedObject
        fields = ("id", "created_at", "updated_at", "obj_type", "data")

    def get_obj_type(self, obj):
        return obj.to_type()

    def get_data(self, obj):
        return obj.to_data()
