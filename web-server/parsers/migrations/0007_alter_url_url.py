# Generated by Django 5.0.6 on 2024-06-07 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parsers", "0006_alter_imageparser_content_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="url",
            field=models.URLField(unique=True),
        ),
    ]