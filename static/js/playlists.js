document.addEventListener("DOMContentLoaded", () => {

    // Clicking on the 'play' button for a playlist
    const playButtons = document.querySelectorAll('.play-playlist-btn');
    playButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            console.log('clicked');
            const playlistHolder = event.target.closest('.playlist-main-holder-2');
            if (playlistHolder) {
                const playlistId = playlistHolder.getAttribute('data-playlist-id');
                console.log('Playlist ID:', playlistId);
                play_playlist(playlistId);
            }
        });
    });
    
    const queueButtons = document.querySelectorAll('.queue-button');
    queueButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            console.log('clicked');
            const playlistHolder = event.target.closest('.playlist-main-holder-2');
            if (playlistHolder) {
                const playlistId = playlistHolder.getAttribute('data-playlist-id');
                console.log('Playlist ID:', playlistId);
                add_playlist_to_queue(playlistId);
            }
        });
    });

})


