# Generated by Django 4.1.7 on 2023-07-06 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mood_tracker", "0005_mood_descriptionn"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mood", old_name="descriptionn", new_name="description",
        ),
    ]