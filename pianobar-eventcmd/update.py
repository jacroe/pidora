#!/usr/bin/env python

import sys, csv

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
elif event == "songlove":
	open(www + "curSong", "w").write(title + "|" + artist + "|" + album + "|" + coverArt + "|1|" + detailUrl)
	open(www + "msg", "w").write("Loved")
elif event == "songban":
	open(www + "msg", "w").write("Banned")
elif event == "songshelf":
	open(www + "msg", "w").write("Tired")
