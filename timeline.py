#!/usr/bin/env python

import json
import urllib
import sys

def statuses(user,cache=None):
  tweets_per_call = 200
  api_url_initial = "http://twitter.com/statuses/user_timeline.json?screen_name={screen_name}&count={count}"
  api_url = api_url_initial + "&max_id={max_id}"

  response = urllib.urlopen(str.format(api_url_initial,screen_name=user,count=tweets_per_call))
  while response.getcode() == 200:
    statuses = json.loads(response.read())
    if len(statuses) == 0:
      break
    else:
      for status in statuses:
        yield status
      response = urllib.urlopen(str.format(api_url,screen_name=user,count=tweets_per_call,max_id=statuses[-1]["id"]-1))
  else:
    print >> sys.stderr, "HTTP Error " + str(response.getcode()) + " on URL " + response.geturl()
    exit(1)

if len(sys.argv) < 2:
  print "Usage: " + sys.argv[0] + " <username>"
  exit(0)
else:
  user = sys.argv[1]

all_statuses = []
for status in statuses(user):
  print status["created_at"], status["text"].encode("utf-8")
  all_statuses.append(status)

all_statuses = sorted(all_statuses,key=lambda s:s["id"])

f = open(user + ".json","w")
f.write(json.dumps(all_statuses))
f.close()
