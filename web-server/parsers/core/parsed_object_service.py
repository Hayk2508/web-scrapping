from parsers.core import PARSED_OBJECTS_FACTORY


def create_parsed_object(obj_type, data):
    parsed_object = PARSED_OBJECTS_FACTORY.create(obj_type, **data)
    parsed_object.save()
    return parsed_object


def update_parsed_object(obj, data):
    if data.get("video_url") is not None:
        obj.video_url = data["video_url"]
    if data.get("image_url") is not None:
        obj.image_url = data["image_url"]
    obj.parser_id = data["parser_id"]
    obj.save()
