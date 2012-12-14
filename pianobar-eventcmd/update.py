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

if event == "songstart":
	open(www + "curSong", "w").write(title + "|" + artist + "|" + album + "|" + coverArt + "|" + rating)
elif event == "songlove":
	song = open(www + "curSong", "a").write(str(1))
	open(www + "msg", "w").write("Loved")
elif event == "songban":
	open(www + "msg", "w").write("Banned")
elif event == "songshelf":
	open(www + "msg", "w").write("Tired")
