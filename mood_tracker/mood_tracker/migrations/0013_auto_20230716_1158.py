# Generated by Django 3.2.19 on 2023-07-16 09:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mood_tracker', '0012_auto_20230716_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('reminder_date', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='reminder',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reminder',
            name='task_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
    ]