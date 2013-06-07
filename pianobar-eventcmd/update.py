#!/usr/bin/env python

import sys, csv, subprocess, os

def process(command, new = False):
	if new:
		with open(os.devnull, "w") as fnull: result = subprocess.Popen(command, stdout = fnull, stderr = fnull)
	else:
		with open(os.devnull, "w") as fnull: result = subprocess.call(command, stdout = fnull, stderr = fnull)
www = "/home/jacob/www/pianobar/"

event = sys.argv[1]
lines = sys.stdin.readlines()
fields = dict([line.strip().split("=", 1) for line in lines])

artist = fields["artist"]
title = fields["title"]
album = fields["album"]
coverArt = fields["coverArt"]
rating = str(int(fields["rating"]))
detailUrl = fields["detailUrl"]

if event == "songstart":
	open(www + "curSong", "w").write(title + "|" + artist + "|" + album + "|" + coverArt + "|" + rating + "|" + detailUrl)
elif event == "songfinis":
	import feedparser, urllib
	feed = feedparser.parse("http://www.npr.org/rss/podcast.php?id=500005")
	if not os.path.lexists(www + "lastNews"): open(www + "lastNews", "w").write("-1")
	time = int(open(www + "lastNews", "r").read())
	if feed.entries[0].updated_parsed.tm_hour != time:
		open(www + "ctl", "w").write("p")
		urllib.urlretrieve(feed.entries[0].id, www + "newscast.mp3")
		open(www + "lastNews", "w").write(str(feed.entries[0].updated_parsed.tm_hour))
		open(www + "curSong", "w").write(feed.entries[0].title + "|" + feed.feed.title + "|" + feed.feed.title + "|http://media.npr.org/images/podcasts/2013/primary/hourly_news_summary.png|0|null")
		process(["mpg123", www + "newscast.mp3"])
		open(www + "ctl", "w").write("p")
elif event == "songlove":
	open(www + "curSong", "w").write(title + "|" + artist + "|" + album + "|" + coverArt + "|1|" + detailUrl)
	open(www + "msg", "w").write("Loved")
elif event == "songban":
	open(www + "msg", "w").write("Banned")
elif event == "songshelf":
	open(www + "msg", "w").write("Tired")
elif event == "usergetstations":				# Code thanks to @officerNordBerg on GitHub
        stationCount = int(fields["stationCount"])
	stations = ""
	for i in range(0, stationCount):
		stations += "%s="%i + fields["station%s"%i] + "|" 
	stations = stations[0:len(stations) - 1]
	open(www + "stationList", "w").write(stations)
