#!/bin/env python3 

import urllib.request
import json
import numbers
import sys
from pprint import pprint

if __name__ == '__main__': 
	request_result = urllib.request.urlopen("https://api.spotify.com/v1/search?q=tania%20bowra&type=artist" -H "Authorization: Bearer {your access token}").read()
	data = json.loads(request_result)