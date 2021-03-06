#!/usr/bin/env python

try:
  import simplejson as json
except ImportError:
  import json
import urllib
import sys
import re
from datetime import datetime

# 4:53 PM May 19th, 2008
# Sat Apr 25 09:54:24 +0000 2009

def parsedate(line):
    try:
        return datetime.strptime(re.sub(r"(st|nd|rd|th),", ",", line),"%I:%M %p %b %d, %Y")
    except ValueError:# try:
        return datetime.strptime(line,"%a %b %d %H:%M:%S +0000 %Y")


def statuses(user,cache=None):
  tweets_per_call = 200
  api_url_initial = "http://twitter.com/statuses/user_timeline.json?screen_name=%(screen_name)s&count=%(count)i"
  api_url = api_url_initial + "&max_id=%(max_id)i"

  response = urllib.urlopen(api_url_initial % {"screen_name":user, "count":tweets_per_call})
  statuses = json.loads(response.read())
  while len(statuses) != 0:
    for status in statuses:
      yield status
    response = urllib.urlopen(api_url % {"screen_name":user, "count":tweets_per_call,"max_id":statuses[-1]["id"]-1})
    try:
      statuses = json.loads(response.read())
    except ValueError:    # JSON decoding failed
      statuses = []
  else:
    try:
      if response.getcode() >= 400:
        print >> sys.stderr, "HTTP Error " + str(response.getcode()) + " on URL " + response.geturl()
        exit(1)
    except AttributeError:
      pass        # we don't know whether an actual error happened, so we press on

if len(sys.argv) < 2:
  print "Usage: " + sys.argv[0] + " <username>"
  exit(0)
else:
  user = sys.argv[1]

all_statuses = []
for status in statuses(user):
  print parsedate(status["created_at"]), status["text"].encode("utf-8")
  all_statuses.append(status)

all_statuses = sorted(all_statuses,key=lambda s:s["id"])

f = open(user + ".json","w")
f.write(json.dumps(all_statuses))
f.close()
