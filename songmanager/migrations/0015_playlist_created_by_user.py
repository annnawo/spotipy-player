# Generated by Django 4.2.13 on 2024-05-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songmanager', '0014_playlist_smart_playlist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='created_by_user',
            field=models.BooleanField(null=True),
        ),
    ]