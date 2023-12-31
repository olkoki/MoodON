# Generated by Django 4.1.7 on 2023-02-19 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0010_alter_mood_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "tod",
                    models.CharField(
                        choices=[
                            ("M", "Morning"),
                            ("A", "Afternoon"),
                            ("E", "Evening"),
                            ("N", "Night"),
                        ],
                        max_length=1,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "happiness_level",
                    models.IntegerField(
                        choices=[
                            (-4, -4),
                            (-3, -3),
                            (-2, -2),
                            (-1, -1),
                            (0, 0),
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                        ],
                        default=0,
                    ),
                ),
                (
                    "anger_level",
                    models.IntegerField(
                        choices=[
                            (-4, -4),
                            (-3, -3),
                            (-2, -2),
                            (-1, -1),
                            (0, 0),
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                        ],
                        default=0,
                    ),
                ),
                (
                    "anxiety_level",
                    models.IntegerField(
                        choices=[
                            (-4, -4),
                            (-3, -3),
                            (-2, -2),
                            (-1, -1),
                            (0, 0),
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                        ],
                        default=0,
                    ),
                ),
                (
                    "energy_level",
                    models.IntegerField(
                        choices=[
                            (-4, -4),
                            (-3, -3),
                            (-2, -2),
                            (-1, -1),
                            (0, 0),
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                        ],
                        default=0,
                    ),
                ),
                (
                    "motivation_level",
                    models.IntegerField(
                        choices=[
                            (-4, -4),
                            (-3, -3),
                            (-2, -2),
                            (-1, -1),
                            (0, 0),
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                        ],
                        default=0,
                    ),
                ),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.day"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("date", models.DateField()),
                ("title", models.CharField(max_length=50)),
                ("content", models.TextField()),
                ("show", models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(name="Mood",),
    ]
