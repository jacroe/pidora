#!/usr/bin/env python

import sys, csv, os, json, requests
from time import gmtime, strftime

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
config = json.loads(open(current_dir + "config.json", "r").read())

url = "http://localhost:" + str(config["default_port"]) + "/api"

def sendSongData(title, artist, album, albumart, loved, explainURL):
	data = dict(title=title, artist=artist, album=album, albumart=albumart, extra=dict(loved=bool(loved), explainURL=explainURL))
	requests.post(url, params=dict(json=json.dumps(dict(method="Song.SetData", params=data))))
def sendStationData(stations):
	requests.post(url, params=dict(json=json.dumps(dict(method="Pianobar.SetStationData", params=dict(stations=stations)))))

event = sys.argv[1]
lines = sys.stdin.readlines()
fields = dict([line.strip().split("=", 1) for line in lines])

artist = fields["artist"]
title = fields["title"]
album = fields["album"]
coverArt = fields["coverArt"]
rating = int(fields["rating"])
detailUrl = fields["detailUrl"].split('?dc')[0]
songDuration = fields["songDuration"]
songPlayed = fields["songPlayed"]

if event in ["songstart", "songexplain"]:
	sendSongData(title, artist, album, coverArt, rating, detailUrl)
elif event == "songlove":
	sendSongData(title, artist, album, coverArt, rating, detailUrl)
elif event in ["usergetstations", "stationcreate", "stationdelete", "stationrename"]: # Code thanks to @officerNordBerg on GitHub
	stationCount = int(fields["stationCount"])
	stations = list()
	for i in range(0, stationCount):
		stations.append(fields["station%s"%i])
	sendStationData(stations)

