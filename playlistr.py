#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 2/3 compatibility imports
from __future__ import print_function
from __future__ import unicode_literals

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import argparse
import json

SPOTIFY_API_PREFIX = 'http://api.deezer.com/2.0/'
M3U_HEADER = '#EXTM3U\n'
M3U_TRACK = '#EXTINF:'
EXT_MP3 = 'mp3'


def write_m3u_playlist(dest, data):
    tracks = data['tracks']['data']
    s = M3U_HEADER
    for t in tracks:
        trackname = (t['artist']['name'] + ' - ' + t['title'])
        s += M3U_TRACK + str(t['duration']) + ',' + trackname + '\n' + \
            trackname + '.' + EXT_MP3 + '\n'

    f = open(dest, 'wb')
    f.write(s.encode('utf-8'))
    print('writing playlist %s' % dest)

    #EXTINF Track information, including runtime and title.
    #EXTINF:191,Artist Name - Track Title


def resolve_url(url):
    # the webpage format for urls is like this:
    # http://www.deezer.com/fr/playlist/4341978
    # the api calls is like this:
    # http://api.deezer.com/2.0/playlist/4341978
    # TODO implement teh validation of url and the conversion to the api one
    api_url = url
    return api_url


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='playlistr', prog='playlistr',
                                     epilog='playlistr <URL> <DEST>')
    # general options
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('url', action='store',
                        help='URL of the playlist')
    parser.add_argument('dest', action='store',
                        help='destination format (e.g. m3u)')

    args = parser.parse_args()
    # print args

    api_url = resolve_url(args.url)
    response = urlopen(api_url)
    data = json.loads(response.read().decode('utf-8'))
    # data = json.load(response, encoding='utf-8')

    write_m3u_playlist(args.dest, data)
