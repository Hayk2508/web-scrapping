from django.db import migrations
from django.contrib.contenttypes.models import ContentType


def populate_content_type_and_object_id(apps, schema_editor):
    ImageParser = apps.get_model("parsers", "ImageParser")
    VideoParser = apps.get_model("parsers", "VideoParser")

    image_content_type = ContentType.objects.get_for_model(ImageParser)
    video_content_type = ContentType.objects.get_for_model(VideoParser)

    for image_parser in ImageParser.objects.all():
        image_parser.content_type = image_content_type
        image_parser.object_id = image_parser.id
        image_parser.save()

    for video_parser in VideoParser.objects.all():
        video_parser.content_type = video_content_type
        video_parser.object_id = video_parser.id
        video_parser.save()


class Migration(migrations.Migration):

    dependencies = [
        (
            "parsers",
            "0003_imageparsedobject_polymorphic_ctype_and_more",
        ),  # Replace with the actual previous migration name
    ]

    operations = [
        migrations.RunPython(populate_content_type_and_object_id),
    ]
