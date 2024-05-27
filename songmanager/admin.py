from django.contrib import admin

# Register your models here.
from .models import User, UserSong, Song, Playlist, Atmosphere, Emotion, Tag, Genre, Album, Folder

admin.site.register(User)
admin.site.register(Song)
admin.site.register(UserSong)
admin.site.register(Playlist)
admin.site.register(Atmosphere)
admin.site.register(Emotion)
admin.site.register(Tag)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Folder)