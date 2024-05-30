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
    
    def get_genres(self):
        user_songs = UserSong.objects.filter(user=self)
        genres = Genre.objects.filter(song__usersong__in=user_songs).distinct()
        return genres
    
class Genre(models.Model):
    name = models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return self.name
    
class Album(models.Model):
    name = models.CharField(max_length=200, null=False)
    artist = models.CharField(max_length=200, null=False)
    spotify_id = models.CharField(max_length=200, null=False, primary_key=True)
    cover_art_url = models.CharField(max_length=200, null=False)

class Song(models.Model):
    title = models.CharField(max_length=200, null=False)
    artist = models.CharField(max_length=200, null=False)
    album_id = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=200, null=False)
    genres = models.ManyToManyField(Genre)
    

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    std_name = models.CharField(max_length=100, null=True)
    playlist_id = models.CharField(max_length=150, null=False, primary_key=True)
    quick_add_option = models.BooleanField(default=False, null=False)
    smart_playlist = models.BooleanField(default=False, null=False)
    created_by_user = models.BooleanField(null=True)
    songs = models.ManyToManyField(Song, blank=True)
    in_folder = models.BooleanField(null=True, default=False)

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
    
class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    playlists = models.ManyToManyField(Playlist, blank=True)
    smart_folder = models.BooleanField(default=False, null=False)
    
class RuleModifierChoices(Enum):
    LESS_THAN = 'lt'
    LESS_THAN_EQUAL_TO = 'lteq'
    EQUAL_TO  = 'eq'
    GREATER_THAN_EQUAL_TO = 'gteq'
    GREATER_THAN = 'gt'
    
class RuleJoinChoices(Enum):
    AND = 'and'
    OR = 'or'

class RuleModifierContainChoices(Enum):
    CONTAINS = 'contains'
    DOES_NOT_CONTAIN = 'dncontain'

class RuleModifierOptionsChoices(Enum):
    ALL_OPTIONS = 'alloptions'
    AT_LEAST_ONE_OPTION = 'oneoption'

class SmartPlaylistRules(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    rating_modifier = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierChoices], null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    rating_energy_join = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleJoinChoices], null=True)
    energy_modifier = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierChoices], null=True)
    energy = models.IntegerField(choices=[(i, i) for i in range(0, 101)], null=True, blank=True)
    genre_join = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleJoinChoices], null=True)
    genre_contain_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    genre_options_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    genres = models.ManyToManyField(Genre)
    atmosphere_join = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleJoinChoices], null=True)
    atmosphere_contain_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    atmosphere_options_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    atmospheres = models.ManyToManyField(Atmosphere, blank=True)
    emotion_join = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleJoinChoices], null=True)
    emotion_contain_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    emotion_options_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    tags_join = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleJoinChoices], null=True)
    tags_contain_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    tags_options_choice = models.CharField(max_length=30, choices=[(modifier.name, modifier.value) for modifier in RuleModifierContainChoices], null=True)
    tags = models.ManyToManyField(Tag, blank=True)