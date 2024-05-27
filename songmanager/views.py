from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.

def home(request):
    return render(request, 'songmanager/player.html')

# views.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy.util as util
from django.shortcuts import render
from django.core import serializers
import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone, timedelta
from django.db.models import Q, Count
import numpy as np
load_dotenv()

def lastfm_get(payload, LASTFM_API_KEY):
    # define headers and URL
    headers = {'user-agent': 'anna-woodward'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = LASTFM_API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def player_view(request):
    current_user = User.objects.get(pk=1)
    # Initialize Spotipy with appropriate credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    current_user_id = sp.current_user()['id']
    # Make a call to the Spotify API to get the currently playing song
    current_track = sp.current_user_playing_track()
    user_details = sp.current_user()
    display_name = user_details['display_name']
    # prev_track = sp.previous_track()

    # Extract relevant information from the response
    if current_track is not None and 'item' in current_track and current_track['item']['name'] != "":
        song_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        album_art = current_track['item']['album']['images'][0]['url']
        album_id = current_track['item']['album']['id']
        album_name = current_track['item']['album']['name']
        track_id = current_track['item']['id']
        energy_level = get_energy_level(track_id=track_id)
        playback = sp.current_playback()
        if playback['item']['id'] == track_id and playback['device']['is_active']:
            now_playing = True    
        else:
            now_playing = False
        if (check_library_bool(track_id=track_id)):
            user_song = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
            user_song.last_played = datetime.now(timezone.utc)
            user_song.save()
            
        return render(request, 'songmanager/player.html', {'song_name': song_name, 'artist_name': artist_name, 'album_art': album_art, 'track_id': track_id, 'album_id': album_id, 'energy_level': energy_level, 'now_playing': now_playing, 'display_name': display_name, 'album_name': album_name})
    else: 
        # If there is no currently playing track, retrieve the most recently played track instead
        recent_tracks = sp.current_user_recently_played(limit=1)['items']
        if recent_tracks:
            # Extract information about the most recently played track
            recent_track = recent_tracks[0]['track']
            song_name = recent_track['name']
            artist_name = recent_track['artists'][0]['name']
            album_art = recent_track['album']['images'][0]['url']
            album_id = recent_track['album']['id']
            album_name = recent_track['album']['name']
            track_id = recent_track['id']
            energy_level = get_energy_level(track_id=track_id)
            # Pass the information about the most recently played track to the template
            return render(request, 'songmanager/player.html', {'song_name': song_name, 'artist_name': artist_name, 'album_art': album_art, 'track_id': track_id, 'album_id': album_id, 'energy_level': energy_level, 'now_playing': False, 'display_name': display_name, 'album_name': album_name})
        else:
            # If there are no recent tracks, return an error message to the template
            return render(request, 'songmanager/player.html', {'error_message': 'No song currently playing'})
    

def check_library(request, track_id):
    current_user = User.objects.get(pk=1)
    try:
        user_song = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        in_library = user_song.in_library
    except UserSong.DoesNotExist:
        in_library = False
    
    return JsonResponse({'in_library': in_library})


def check_library_bool(track_id):
    current_user = User.objects.get(pk=1)
    try:
        user_song = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        in_library = user_song.in_library
    except UserSong.DoesNotExist:
        in_library = False
    
    return in_library


def check_listen_again(request, track_id):
    current_user = User.objects.get(pk=1)
    listen_again_playlist = Playlist.objects.get(user=current_user, name="Listen Again")
    listen_again_playlist = listen_again_playlist.playlist_id
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    in_listen_again = False
    playlist_tracks = sp.playlist_tracks(listen_again_playlist)
    for item in playlist_tracks['items']:
        if item['track']['id'] == track_id:
            in_listen_again = True
            break
    return JsonResponse({'in_listen_again': in_listen_again})


def check_listen_again_bool(track_id, playlist_id):
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    in_listen_again = False
    playlist_tracks = sp.playlist_tracks(playlist_id)
    for item in playlist_tracks['items']:
        if item['track']['id'] == track_id:
            in_listen_again = True
            break
    return in_listen_again


def get_rating(request, track_id):
    current_user = User.objects.get(pk=1)
    try:
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        if usersong.rating:
            return JsonResponse({'star_ct': usersong.rating})
        else:
            return JsonResponse({'star_ct': 0})
    except UserSong.DoesNotExist:
        return JsonResponse({'star_ct': 0})
  
    

def get_genres(song_name, artist_name):
    LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
    r = lastfm_get({
        'track': song_name,
        'artist': artist_name,
        'method': 'track.getInfo'
    }, LASTFM_API_KEY)

    if r.status_code == 200:
        response_data = r.json()
        # Extract genres from the Last.fm API response
        toptags = response_data['track']['toptags']['tag']
        genres = [tag['name'] for tag in toptags]
        return genres


def add_to_library(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        # Parse JSON data from the request body
        data = json.loads(request.body)
        # Extract relevant data
        track_id = data.get('track_id')
        song_name = data.get('song_name')
        artist_name = data.get('artist_name')
        album_id = data.get('album_id')
        album_name = data.get('album_name')
        album_art = data.get('album_art')
        
        in_lib = check_library_bool(track_id=track_id)
        if (not in_lib):
            # Get genres for the song
            genres = get_genres(song_name=song_name, artist_name=artist_name)
            print(genres)
            
            # Create the album object
            album, _ = Album.objects.get_or_create(
                name=album_name,
                artist=artist_name,
                spotify_id=album_id,
                cover_art_url=album_art
            )
            
            # Create the song object
            song, _ = Song.objects.get_or_create(
                title=song_name,
                artist=artist_name,
                album_id=album,
                spotify_id=track_id
            )
            
            # Associate genres with the song
            for genre_name in genres:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                song.genres.add(genre)
            
            # Create the UserSong object and link it with the song
            user_song = UserSong.objects.create(
                user=current_user,
                song=song,
                in_library=True
            )
        else:
            song = get_object_or_404(Song, spotify_id=track_id)
            user_song = get_object_or_404(UserSong, user=current_user, song=song)
            user_song.delete()
        
        return redirect('/player/')


def add_to_listen_again(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        playlist_id = Playlist.objects.get(user=current_user, name="Listen Again")
        playlist_id = playlist_id.playlist_id
        # Parse JSON data from the request body
        data = json.loads(request.body)
        track_id = data.get('track_id')
        
        SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
        SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
        SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
        username = "ye6bq7h7l9wnphebox5b1jgqu"
        scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
        sp = spotipy.Spotify(auth=token)
        
        in_la = check_listen_again_bool(track_id=track_id, playlist_id=playlist_id)
        if (not in_la):
            sp.playlist_add_items(playlist_id=playlist_id, items=[track_id], position=0)
        else:
            sp.user_playlist_remove_all_occurrences_of_tracks(user=username, playlist_id=playlist_id, tracks=[track_id])
        return redirect('/player/')
    

def add_album_to_found_sounds(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        playlist_id = Playlist.objects.get(user=current_user, name="Future (Songs of Intrigue)")
        playlist_id = playlist_id.playlist_id
        
         # Parse JSON data from the request body
        data = json.loads(request.body)
        album_id = data.get('album_id')
        
        SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
        SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
        SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
        username = "ye6bq7h7l9wnphebox5b1jgqu"
        scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
        sp = spotipy.Spotify(auth=token)
        
        album_tracks = sp.album_tracks(album_id=album_id)
        track_ids = [track['id'] for track in album_tracks['items']]
        playlist_tracks = sp.playlist_tracks(playlist_id)
        for item in playlist_tracks['items']:
            item_id = item['track']['id']
            if item_id in track_ids:
                track_ids.remove(item_id)
        for track in track_ids:
            if check_library_bool(track):
                track_ids.remove(track)
        if len(track_ids) > 0:
            sp.playlist_add_items(playlist_id=playlist_id, items=track_ids, position=0)
        
        return redirect('/player/')

def add_rating(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        rating = data.get('rating')
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.rating = rating
        usersong.save()
            
        return redirect('/player/')
    
    
def add_atmosphere_option(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        atmosphere_option = data.get('atmosphere_option')
        try:
            atmosphere = Atmosphere.objects.get(atmosphere=atmosphere_option)
        except Atmosphere.DoesNotExist:
            return HttpResponse("Atmosphere does not exist", status=404)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.atmospheres.add(atmosphere)
        usersong.save()
        return HttpResponse(status=200)
    
    
def get_atmospheres(request, track_id):
    current_user = User.objects.get(pk=1)
    try:
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        atmospheres = list(usersong.atmospheres.values_list('atmosphere', flat=True))
        return JsonResponse({'atmospheres': atmospheres})
    except UserSong.DoesNotExist:
        return JsonResponse({'atmospheres': []})
    

def remove_atmosphere_option(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        atmosphere_option = data.get('atmosphere_option')
        try:
            atmosphere = Atmosphere.objects.get(atmosphere=atmosphere_option)
        except Atmosphere.DoesNotExist:
            return HttpResponse("Atmosphere does not exist", status=404)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.atmospheres.remove(atmosphere)
        usersong.save()
        return HttpResponse(status=200)
    
    
def add_emotion_option(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        emotion_option = data.get('emotion_option')
        try:
            emotion = Emotion.objects.get(emotion=emotion_option)
        except Emotion.DoesNotExist:
            return HttpResponse("Emotion does not exist", status=404)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.emotions.add(emotion)
        usersong.save()
        return HttpResponse(status=200)
    

def remove_emotion_option(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        emotion_option = data.get('emotion_option')
        try:
            emotion = Emotion.objects.get(atmosphere=emotion_option)
        except Emotion.DoesNotExist:
            return HttpResponse("Emotion does not exist", status=404)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.emotions.remove(emotion)
        usersong.save()
        return HttpResponse(status=200)
    

def get_emotions(request, track_id):
    current_user = User.objects.get(pk=1)
    try:
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        emotions = list(usersong.emotions.values_list('emotion', flat=True))
        return JsonResponse({'emotions': emotions})
    except UserSong.DoesNotExist:
        return JsonResponse({'emotions': []})
    
    
def add_energy_level(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        energy_level = data.get('energy_level')
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.energy = energy_level
        usersong.save()
        return HttpResponse(status=200)
        

def get_energy_level(track_id):
    current_user = User.objects.get(pk=1)
    try:
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        energy_level = usersong.energy
        if energy_level == None:
            return 0
        else:
            return energy_level
    except UserSong.DoesNotExist:
        return 0
    

def pause_playback(request):
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    sp.pause_playback()
    return HttpResponse(status=200)

    
def resume_playback(request):
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    sp.start_playback()
    return HttpResponse(status=200)


def skip_song(request, track_id):
    current_user = User.objects.get(pk=1)
    if (UserSong.objects.filter(user=current_user, song__spotify_id=track_id).exists()):
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        usersong.last_skipped = datetime.now(timezone.utc)
        usersong.save()
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    sp.next_track()
    return redirect('/player/')


def play_previous_song(request):
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    sp.previous_track()
    return redirect('/player/')


def add_tag_option(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        tag_option = data.get('tag_option')
        tag, _ = Tag.objects.get_or_create(author=current_user, tag=tag_option)
        add_song_tag(request)
        return redirect('/player/')


def add_song_tag(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        tag_option = data.get('tag_option')
        tag = Tag.objects.get(author=current_user, tag=tag_option)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.tags.add(tag)
        usersong.save()
    return HttpResponse(status=200)
        
    
def remove_song_tag(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        tag_option = data.get('tag_option')
        tag = Tag.objects.get(author=current_user, tag=tag_option)
        if (not check_library_bool(track_id)):
            add_to_library(request=request)
        song = get_object_or_404(Song, spotify_id=track_id)
        usersong = UserSong.objects.get(user=current_user, song=song)
        usersong.tags.remove(tag)
        usersong.save()
    return HttpResponse(status=200)


def get_tags(request, track_id):
    current_user = User.objects.get(pk=1)
    try:
        usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
        tags = list(usersong.tags.values_list('tag', flat=True))
        return JsonResponse({'tags': tags})
    except UserSong.DoesNotExist:
        return JsonResponse({'tags': []})
    
    
def get_all_user_tags(request):
    current_user = User.objects.get(pk=1)
    tags = list(Tag.objects.filter(author=current_user).values_list('tag', flat=True))
    return JsonResponse({'tags': tags})


def clear_song_form_selections(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=1)
        data = json.loads(request.body)
        track_id = data.get('track_id')
        if (check_library_bool(track_id)):
            usersong = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
            usersong.atmospheres.clear()
            usersong.emotions.clear()
            usersong.tags.clear()
            usersong.energy = None
            usersong.rating = None
            usersong.save()
    return redirect('/player/')


def get_quick_select_playlists(request, track_id):
    current_user = User.objects.get(pk=1) 
    playlists = Playlist.objects.filter(user=current_user, quick_add_option=True)
    
    # List to store playlist objects
    qs_playlists = []
    
    # Iterate over playlists
    for playlist in playlists:
        # Check if the track exists in the playlist
        track_in_playlist = playlist.songs.filter(spotify_id=track_id).exists()
        
        # Create a dictionary to store playlist information
        playlist_info = {
            'name': playlist.name,
            'id': playlist.playlist_id,
            'track_in_playlist': track_in_playlist
        }
        
        # Append playlist information to the list
        qs_playlists.append(playlist_info)
    
    # Convert the list to JSON response
    qsp_response = json.dumps(qs_playlists, indent=4)
    
    # Return JSON response
    return JsonResponse(qsp_response, safe=False)



# PLAYLIST MANAGEMENT FUNCTIONS


def get_playlists():
    current_user = User.objects.get(pk=1)
    playlists = []
    playlists_filtered = Playlist.objects.filter(user=current_user, created_by_user=True)
    
    class PlaylistObj:
        def __init__(self, name, id):
            self.name = name
            self.id = id
            self.images = []  # Initialize images list
        
        def add_image_url(self, url):
            self.images.append(url)  # Append image URL to images list
    
    for playlist in playlists_filtered:
        playlist_obj = PlaylistObj(playlist.name, playlist.playlist_id)
        songs = playlist.songs.all()  # Retrieve queryset of related songs
        counter = 0
        albums = set()  # Use a set to store unique album IDs
        for song in songs:
            if song.album_id_id not in albums:  # Access album ID directly
                album = Album.objects.get(spotify_id=song.album_id.spotify_id)
                url = album.cover_art_url
                playlist_obj.add_image_url(url=url)
                albums.add(song.album_id_id)  # Add album ID to set
                counter += 1
                if counter == 7:
                    break
        playlists.append(playlist_obj)  # Append playlist object to playlists list
    return playlists
            


def playlists_view(request):
    current_user = User.objects.get(pk=1)
    # Initialize Spotipy with appropriate credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    current_user_id = sp.current_user()['id']
    # Make a call to the Spotify API to get the currently playing song
    current_track = sp.current_user_playing_track()
    user_details = sp.current_user()
    display_name = user_details['display_name']
    # prev_track = sp.previous_track()
    playlists = get_playlists()
        
    

    # Extract relevant information from the response
    if current_track is not None and 'item' in current_track and current_track['item']['name'] != "":
        song_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        album_art = current_track['item']['album']['images'][0]['url']
        album_id = current_track['item']['album']['id']
        album_name = current_track['item']['album']['name']
        track_id = current_track['item']['id']
        energy_level = get_energy_level(track_id=track_id)
        playback = sp.current_playback()
        if playback['item']['id'] == track_id and playback['device']['is_active']:
            now_playing = True    
        else:
            now_playing = False
        if (check_library_bool(track_id=track_id)):
            user_song = UserSong.objects.get(user=current_user, song__spotify_id=track_id)
            user_song.last_played = datetime.now(timezone.utc)
            user_song.save()
            
        return render(request, 'songmanager/playlists.html', {'song_name': song_name, 'artist_name': artist_name, 'album_art': album_art, 'track_id': track_id, 'album_id': album_id, 'energy_level': energy_level, 'now_playing': now_playing, 'display_name': display_name, 'album_name': album_name, 'playlists':playlists})
    else: 
        # If there is no currently playing track, retrieve the most recently played track instead
        recent_tracks = sp.current_user_recently_played(limit=1)['items']
        if recent_tracks:
            # Extract information about the most recently played track
            recent_track = recent_tracks[0]['track']
            song_name = recent_track['name']
            artist_name = recent_track['artists'][0]['name']
            album_art = recent_track['album']['images'][0]['url']
            album_id = recent_track['album']['id']
            album_name = recent_track['album']['name']
            track_id = recent_track['id']
            energy_level = get_energy_level(track_id=track_id)
            # Pass the information about the most recently played track to the template
            return render(request, 'songmanager/playlists.html', {'song_name': song_name, 'artist_name': artist_name, 'album_art': album_art, 'track_id': track_id, 'album_id': album_id, 'energy_level': energy_level, 'now_playing': False, 'display_name': display_name, 'album_name': album_name, 'playlists':playlists})
        else:
            # If there are no recent tracks, return an error message to the template
            return render(request, 'songmanager/playlists.html', {'error_message': 'No song currently playing'})
    

def update_personal_radio(request):
    current_user = User.objects.get(pk=1) 
    personal_radio_playlist = Playlist.objects.get(user=current_user, std_name="personal_radio")
    radio_playlist_id = personal_radio_playlist.playlist_id
    previously_added_song_ids = personal_radio_playlist.songs.values_list('spotify_id', flat=True)
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)
    songs_filtered = UserSong.objects.filter(user=current_user, in_library=True, rating__gte=3)
    songs_filtered = songs_filtered.filter(Q(last_played__lt=one_week_ago) | Q(last_played__isnull=True))
    songs_filtered = songs_filtered.filter(Q(last_skipped__lt=two_weeks_ago) | Q(last_skipped__isnull=True))
    song_ids_filtered = songs_filtered.values_list('song__spotify_id', flat=True) 
    song_ids_filtered = np.array(song_ids_filtered)
    previously_added_song_ids = np.array(previously_added_song_ids)
    songs_to_remove = np.setdiff1d(previously_added_song_ids, song_ids_filtered)
    songs_to_add = np.setdiff1d(song_ids_filtered, previously_added_song_ids)

    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    username = "ye6bq7h7l9wnphebox5b1jgqu"
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    current_user_id = sp.current_user()['id']

    if len(songs_to_remove) > 0:
        sp.user_playlist_remove_all_occurrences_of_tracks(user=current_user_id, playlist_id=radio_playlist_id, tracks=songs_to_remove)
        songs_to_remove_s = Song.objects.filter(spotify_id__in=list(songs_to_remove))
        personal_radio_playlist.songs.remove(*songs_to_remove_s)

    if len(songs_to_add) > 0:
        sp.playlist_add_items(playlist_id=radio_playlist_id, items=songs_to_add)
        songs_to_add_s = Song.objects.filter(spotify_id__in=list(songs_to_add))
        personal_radio_playlist.songs.add(*songs_to_add_s)
    
    return HttpResponse(status=200)



# TEST VIEW TEST VIEW TEST VIEW
def get_user_playlists(request):    
#     SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
#     SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
#     SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
#     username = "ye6bq7h7l9wnphebox5b1jgqu"
#     scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
#     client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#     token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
#     sp = spotipy.Spotify(auth=token)
#     user_playlists = sp.current_user_playlists()
# # Iterate over playlists and check ownership
#     for playlist in user_playlists['items']:
#         playlist_name = playlist['name']
#         playlist_id = playlist['id']
#         playlist_owner_id = playlist['owner']['id']
        
#         if playlist_owner_id == sp.me()['id']:
#             print(f"Playlist '{playlist_name}' is created by the user.")
#         else:
#             print(f"Playlist '{playlist_name}' is saved or followed by the user.")
    
    # current_user_id = sp.current_user()['id']
#     userplaylists = sp.current_user_playlists(offset=0)
#     userplaylists = userplaylists['items']
#     listofusertitles = []

#     for playlist in userplaylists:
#         usertitles = playlist['name']
#         playlistid = playlist['id']
#         print(usertitles, ": ", playlistid)
    return HttpResponse(status=200)