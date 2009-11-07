#!/usr/bin/env python

import simplejson as json
import urllib
import sys

def statuses(user,cache=None):
  tweets_per_call = 200
  api_url_initial = "http://twitter.com/statuses/user_timeline.json?screen_name=%(screen_name)s&count=%(count)i"
  api_url = api_url_initial + "&max_id=%(max_id)i"

  request = urllib.urlopen(api_url_initial % {"screen_name":user, "count":tweets_per_call})
  response = json.loads(request.read())
  while len(response) != 0:
    for status in response:
      yield status
    request = urllib.urlopen(api_url % {"screen_name":user, "count":tweets_per_call,"max_id":response[-1]["id"]-1})
    response = json.loads(request.read())
  else:
    try:
      print >> sys.stderr, "HTTP Error " + str(request.getcode()) + " on URL " + request.geturl()
    except AttributeError:
      print >> sys.stderr, "HTTP Error on URL " + request.geturl()
      
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
