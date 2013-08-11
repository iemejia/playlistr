#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import *

import argparse
import codecs
import json
import socket
from urlparse import urlsplit, parse_qs

SPOTIFY_API_PREFIX = 'http://api.deezer.com/2.0/'
YOUTUBE_API_PREFIX = 'https://gdata.youtube.com/feeds/api/videos?'
YOUTUBE_VIDEO_PREFIX = 'https://www.youtube.com/watch?v='
M3U_HEADER = '#EXTM3U\n'
M3U_TRACK = '#EXTINF:'
EXT_MP3 = 'mp3'

def extract_filenames(m3ufile):
    """ reads the file and ignores the # and strips the .mp3 extension """
    content = []
    with codecs.open(m3ufile, encoding='utf-8') as f:
        content = f.readlines()
    filenames = [line.strip()[:-4] for line in content if not line.startswith('#')]
    return filenames

def download_with_youtubedl(m3ufile, filename):
    """ returns [filename] """
    filenames = extract_filenames(m3ufile)
    # for test purposes only
    # filenames = filenames[:10]
    # filenames = filenames[50:]
    urls = []
    for i, f in enumerate(filenames):
        url = youtube_getsong_url(f)
        video_id = get_youtube_video_id(url)
        real_url = YOUTUBE_VIDEO_PREFIX + video_id
        print('%3s / %3s - %s : %s' % (i+1, len(filenames), video_id, f))
        urls.append(real_url)
    write_youtube_playlist(urls, filename)

def write_youtube_playlist(urls, filename):
    s = '\n'.join(urls)
    write_m3u_file(filename, s)

def get_youtube_video_id(url):
    query = parse_qs(urlsplit(url).query)
    return query['v'][0]

def youtube_getsong_url(songname):
    """ searchs for the first result in youtube (via relevant criteria) """
    # example request to youtube api
    # https://gdata.youtube.com/feeds/api/videos?q=sonic%20youth%20-%20bull%20in%20the%20heather&orderby=viewCount&alt=json&max-results=1&v=2
    orderby = 'relevance'  # viewCount
    params = compat_urllib_parse.urlencode({
        'q': songname.encode('utf-8'),
        'orderby': orderby,
        'alt': 'json',
        'results': 1,
        'v': 2,
    })
    url = YOUTUBE_API_PREFIX + params
    try:
        data = compat_urllib_request.urlopen(url).read().decode('utf-8')
        o = json.loads(data)
        # print(json.dumps(o, sort_keys=True, indent=4, separators=(',', ': ')))
        if 'entry' in o['feed']:
            url = o['feed']['entry'][0]['link'][0]['href']
            return url
        else:
            print('error finding %s' % songname)
    except (compat_urllib_error.URLError, compat_http_client.HTTPException, socket.error) as err:
        print(u'unable to find song: %s' % songname)
    return ''

def write_m3u_file(filename, s):
    f = open(filename, 'wb')
    f.write(s.encode('utf-8'))
    print('writing file %s' % filename)

def write_m3u_playlist(dest, o):
    #EXTINF Track information, including runtime and title.
    #EXTINF:191,Artist Name - Track Title
    print(json.dumps(o, sort_keys=True, indent=4, separators=(',', ': ')))
    tracks = o['tracks']['data']
    s = M3U_HEADER
    for t in tracks:
        trackname = (t['artist']['name'] + ' - ' + t['title'])
        s += M3U_TRACK + str(t['duration']) + ',' + trackname + '\n' + \
            trackname + '.' + EXT_MP3 + '\n'
    write_m3u_file(dest, s)

def resolve_url(url):
    # the webpage format for urls is like this:
    # http://www.deezer.com/fr/playlist/4341978
    # the api calls is like this:
    # http://api.deezer.com/2.0/playlist/4341978
    playlist_id = url[-9:]
    api_url = SPOTIFY_API_PREFIX + 'playlist/' + playlist_id
    return api_url


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='playlistr', prog='playlistr',
                                     epilog='playlistr <URL> <DEST>')
    # general options
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('cmd', action='store',
                        help='command')
    parser.add_argument('url', action='store',
                        help='URL of the playlist')
    parser.add_argument('dest', action='store',
                        help='destination format (e.g. m3u)')

    args = parser.parse_args()
    # print args

    if args.cmd == 'export':
        api_url = resolve_url(args.url)
        data = compat_urllib_request.urlopen(api_url).read().decode('utf-8')
        o = json.loads(data)
        write_m3u_playlist(args.dest, o)
    if args.cmd == 'transform':
        m3ufile = args.url
        filename = args.dest
        download_with_youtubedl(m3ufile, filename)

