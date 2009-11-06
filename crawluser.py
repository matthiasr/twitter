#!/usr/bin/env python

import json
import urllib

user = "plomlompom"
tweets_per_call = 200
api_url_initial = "http://twitter.com/statuses/user_timeline.json?screen_name={screen_name}&count={count}"
api_url = api_url_initial + "&max_id={max_id}"

statuses = []

request = urllib.urlopen(str.format(api_url_initial,screen_name=user,count=tweets_per_call))

while request.getcode() == 200:
  response = json.decode(request.read())
  for status in response.statuses:
    print status.created_at, status.text
  statuses.append(response.statuses)
  request = urllib.urlopen(str.format(api_url,screen_name=user,count=tweets_per_call,max_id=response.statuses[-1].id-1))
else:
  printf(stderr, "HTTP Error " + request.getcode() + " on URL " + request.geturl())
  exit(1)

