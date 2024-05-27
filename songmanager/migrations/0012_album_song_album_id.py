# Generated by Django 4.2.13 on 2024-05-26 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songmanager', '0011_playlist_std_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('spotify_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('cover_art_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='album_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='songmanager.album'),
        ),
    ]