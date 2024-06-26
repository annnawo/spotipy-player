from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('player/', views.player_view, name='player'),
    path('playlists/', views.playlists_view, name='playlists'),
    path('check_library/<str:track_id>/', views.check_library, name='check_library'),
    path('check_listen_again/<str:track_id>/', views.check_listen_again, name='check_listen_again'),
    path('add_to_library/', views.add_to_library, name='add_to_library'),
    path('add_to_listen_again/', views.add_to_listen_again, name='add_to_listen_again'),
    path('add_album_to_found_sounds/', views.add_album_to_found_sounds, name='add_album_to_found_sounds'),
    path('add_rating/', views.add_rating, name='add_rating'),
    path('get_rating/<str:track_id>/', views.get_rating, name='get_rating'),
    path('add_atmosphere_option/', views.add_atmosphere_option, name='add_atmosphere_option'),
    path('get_atmospheres/<str:track_id>/', views.get_atmospheres, name='get_atmospheres'),
    path('remove_atmosphere_option/', views.remove_atmosphere_option, name='remove_atmosphere_option'),
    path('add_emotion_option/', views.add_emotion_option, name='add_emotion_option'),
    path('remove_emotion_option/', views.remove_emotion_option, name='remove_emotion_option'),
    path('get_emotions/<str:track_id>/', views.get_emotions, name='get_emotions'),
    path('add_energy_level/', views.add_energy_level, name='add_energy_level'),
    path('pause_playback/', views.pause_playback, name='pause_playback'),
    path('resume_playback/', views.resume_playback, name='resume_playback'),
    path('skip_song/<str:track_id>/', views.skip_song, name='skip_song'),
    path('play_previous_song/', views.play_previous_song, name='play_previous_song'),
    path('add_tag_option/', views.add_tag_option, name='add_tag_option'),
    path('add_song_tag/', views.add_song_tag, name='add_song_tag'),
    path('remove_song_tag/', views.remove_song_tag, name='remove_song_tag'),
    path('get_tags/<str:track_id>/', views.get_tags, name='get_tags'),
    path('get_all_user_tags/', views.get_all_user_tags, name='get_all_user_tags'),
    path('clear_song_form_selections/', views.clear_song_form_selections, name='clear_song_form_selections'),
    path('get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),
    path('get_quick_select_playlists/<str:track_id>/', views.get_quick_select_playlists, name='get_quick_select_playlists'),
    
    
    path('play_playlist/', views.play_playlist, name='play_playlist'),
    path('queue_playlist/', views.queue_playlist, name='queue_playlist'),
    
    path('add-smart-playlist/', views.add_smart_playlist, name='add_smart_playlist'),
    
    
    
]
