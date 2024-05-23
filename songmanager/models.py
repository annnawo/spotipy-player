from django.db import models
from django.contrib.auth.models import User
import uuid
from enum import Enum

# Create your models here.

class User(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, unique=True, null=False)
    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=200, null=False)
    
class Song(models.Model):
    title = models.CharField(max_length=200, null=False)
    artist = models.CharField(max_length=200, null=False)
    album = models.CharField(max_length=200, null=False)
    spotify_id = models.CharField(max_length=200, null=False)
    genres = models.ManyToManyField(Genre)

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    playlist_id = models.CharField(max_length=150, null=False, primary_key=True)
    quick_add_option = models.BooleanField(default=False, null=True)
    songs = models.ManyToManyField(Song, blank=True)

class Emotion(models.Model):
    emotion = models.CharField(max_length=100)  
    
class Atmosphere(models.Model):
    atmosphere = models.CharField(max_length=100)
    
class Tag(models.Model):
    tag = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    atmospheres = models.ManyToManyField(Atmosphere, blank=True)
    energy = models.IntegerField(choices=[(i, i) for i in range(0, 101)], null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    in_library = models.BooleanField(default=False, null=True)
    last_skipped = models.DateTimeField(null=True)
    last_played = models.DateTimeField(null=True)
    playlists = models.ManyToManyField(Playlist, blank=True)
    


# later, might need to add album table with description and genres and stuff, and image