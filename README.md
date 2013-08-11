playlistr
=========

playlistr is an utility to import/export playlists from/to streaming services

use
---

    python playlistr.py export URL file.m3u
    e.g.
    python playlistr.py export http://www.deezer.com/en/playlist/4341978 playlist.m3u

    python playlistr.py transform PLAYLIST PLAYLIST_YOUTUBE
    e.g.
    python playlistr.py transform playlist.m3u playlist-youtube.m3u

You can then download the audio version of each song from your playlist:
    
    youtube-dl -x -a playlist-youtube.m3u

notes
-----

For the moment only works with URLs from the deezer API.

