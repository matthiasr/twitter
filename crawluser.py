#!/usr/bin/env python

import json
import urllib
import sys

user = "plomlompom"
tweets_per_call = 200
api_url_initial = "http://twitter.com/statuses/user_timeline.json?screen_name={screen_name}&count={count}"
api_url = api_url_initial + "&max_id={max_id}"

statuses = []

request = urllib.urlopen(str.format(api_url_initial,screen_name=user,count=tweets_per_call))

while request.getcode() == 200:
  response = json.loads(request.read())
  for status in response:
    print status["created_at"], status["text"].encode('utf-8')
  statuses.append(response)
  request = urllib.urlopen(str.format(api_url,screen_name=user,count=tweets_per_call,max_id=response[-1]["id"]-1))
else:
  print >> sys.stderr, "HTTP Error " + str(request.getcode()) + " on URL " + request.geturl()
  exit(1)

f = open(user + ".json")
f.write(json.dumps(statuses))
f.close()
