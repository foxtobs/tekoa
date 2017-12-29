#!/bin/env python3 

import urllib.request
import json
import numbers
import sys
import spotipy 
import spotipy.util as util
from collections import Counter
from pprint import pprint
from credentials.spotify import spotify_client_id
from credentials.spotify import spotify_client_secret
from credentials.songkick import songkick_key

from songkickapi import SongkickApiHandler

from IPython import embed


def get_upcoming_concerts(spotify=None, songkick=None):
	if spotify is None or songkick is None: 
		return None

	spotify.trace = False
	ranges = ['short_term', 'medium_term'] # + 'long_term'?

	counter = Counter()
	for time_range in ranges: 
			results = spotify.current_user_top_artists(time_range=time_range, limit=50)
			counter.update([el['name'] for el in results['items']])

	upcoming_events = []
	for name in counter: 
		events = songkick.getEvents(name)
		if events: 
			for event in events:
				upcoming_events.append((name, event.venue, event.start))

	return upcoming_events


if __name__ == '__main__': 
	spotify_redirect_uri = 'http://localhost'
	scope = 'user-top-read'

	username = input('Enter your spotify-username: ')

	token = util.prompt_for_user_token(username, scope, client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri)

	if not token: 
		sys.exit()

	sp = spotipy.Spotify(auth=token)
	s = SongkickApiHandler(songkick_key)

	upcoming = get_upcoming_concerts(sp, s)
	pprint(upcoming)
