from parsers.core import PARSERS_FACTORY, PARSED_OBJECTS_FACTORY
from rest_framework import serializers

from parsers.models import ParsedObject, ImageParsedObject, VideoParsedObject


class ParseContentReqSerializer(serializers.Serializer):
    url = serializers.URLField()
    parse_type = serializers.ChoiceField(choices=list(PARSERS_FACTORY.builders.keys()))
    max_videos = serializers.IntegerField(default=None)


class ParsedObjectSerializer(serializers.ModelSerializer):
    obj_type = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = ParsedObject
        fields = ("id", "created_at", "updated_at", "obj_type", "data", "parser_id")

    def get_obj_type(self, obj):
        return obj.to_type()

    def get_data(self, obj):
        return obj.to_data()


class CreateParsedObjectSerializer(serializers.Serializer):
    obj_type = serializers.ChoiceField(
        choices=list(PARSED_OBJECTS_FACTORY.builders.keys())
    )
    image_url = serializers.CharField(required=False)
    video_url = serializers.CharField(required=False)
    parser_id = serializers.IntegerField()
