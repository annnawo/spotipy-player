# Generated by Django 4.2.13 on 2024-05-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songmanager', '0008_playlist_songs_usersong_playlists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersong',
            name='last_skipped',
            field=models.DateTimeField(null=True),
        ),
    ]
