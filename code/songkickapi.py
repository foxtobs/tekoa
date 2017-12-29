#!/bin/env python

import urllib.request
import json
import numbers
import sys
from pprint import pprint


class SongkickApiHandler: 
    class Artist: 
        def __init__(self, json_artist): 
            self.name = json_artist["displayName"]
            self.id = json_artist["id"]
            self.on_tour_until = json_artist["onTourUntil"]
            self.uri = json_artist["uri"]
            #self.identifier = json.loads(json_artist["identifier"])

    class Event: 
        def __init__(self, json_event): 
            self.id = json_event["id"]
            self.type = json_event["type"]
            self.uri = json_event["uri"]
            self.name = json_event["displayName"]
            self.start = json_event["start"]["datetime"]
            self.location = json_event["location"]["city"]
            self.venue = json_event["venue"]["displayName"]


    def __init__(self, key): 
        self.key = key
    
    def getArtist(self, artist): 
        request_artist = artist.replace(" ", "%20", 10)
        request_result = urllib.request.urlopen("http://api.songkick.com/api/3.0/search/artists.json?query=" + request_artist + "&apikey=" + self.key).read()
        data = json.loads(request_result)
        try: 
            return [SongkickApiHandler.Artist(x) for x in data["resultsPage"]["results"]["artist"] if x["displayName"] == artist]
        except: 
            return None

    def getEvents(self, artist_id): 
        try: 
            if not isinstance(artist_id, numbers.Number): 
                artist_id = self.getArtist(artist_id)[0].id
        except: 
            return None

        request_result = urllib.request.urlopen("http://api.songkick.com/api/3.0/artists/" + str(artist_id) + "/calendar.json?apikey=" + self.key).read()
        data = json.loads(request_result)

        try: 
            return [SongkickApiHandler.Event(x) for x in data["resultsPage"]["results"]["event"]]
        except: 
            return None
    

if __name__ == "__main__": 
    key = "9zi29VLYNibBY6WS"
    s = SongkickApiHandler(key)
    band = "Kalmah"
    if len(sys.argv) > 1: 
        band = sys.argv[1]
    events = s.getEvents(band)

    if events: 
        for event in events: 
            pprint(event.venue + " - " + str(event.start))
        

    
