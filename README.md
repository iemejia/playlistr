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

You can then download and convert the audio version of each song from your playlist:
    
    youtube-dl -x -a playlist-youtube.m3u

Anothyer alternative to preserve the audio quality and avoid transcoding:

	youtube-dl -a playlist-youtube.m3u

    # then in the folder when all the videos are:
	for input in * 
	do 
	ffmpeg -i "$input" -vn -acodec copy "$input".m4a
	done 

notes
-----

For the moment only works with URLs from the deezer API.

