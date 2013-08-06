import json as libjson, os, re, urllib2, subprocess

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def process(command, new = False):
	if new:
		with open(os.devnull, "w") as fnull: result = subprocess.Popen(command, stdout = fnull, stderr = fnull)
	else:
		with open(os.devnull, "w") as fnull: result = subprocess.call(command, stdout = fnull, stderr = fnull)
	return result

def getSongData(data=dict()):
	if os.path.exists(current_dir + "curSong.json"):
		jsonObj = libjson.loads(open(current_dir + "curSong.json").read())
		if jsonObj["title"].find("NPR News") != -1:
			jsonObj["isSong"] = False
		else:
			jsonObj["isSong"] = True
		return jsonObj
	elif "pianobar" in data:
		if data["pianobar"] is not None:
			return libjson.loads('{"startup":true, "isSong":false}')
		else:
			return libjson.loads('{"startup":false, "isSong":false}')
	else:
		return False

def writeMsg(msg):
	open(current_dir + "msg", "w").write(msg)

def getExplanation():
	songData = getSongData()
	regex = re.compile("Track</h2>(.*?)</div>",re.IGNORECASE|re.DOTALL)
	response = urllib2.urlopen(songData["explainURL"])
	html = response.read()
	string = html.replace("\t", "").replace("\n", "").replace('<div style="display: none;">', "")
	r = regex.search(string)
	if r is None:
		return "We were unable to get the song's explanation. Sorry about that."
	data = r.groups()[0].split("<br>")
	traits = data[0:len(data)-1]
	if data[len(data)-2].find("many other comedic similarities") == -1:
		ending = "many other similarites as identified by the Music Genome Project"
	else:
		ending = "many other comedic similarites"
		traits = data[0:len(data)-2]
	return "We're playing this track because it features " + ", ".join(traits) + ", and " + ending +"."

def getStations(index):
	listStations = open(current_dir + "stationList").read().split("|")
	stationList = dict(index=index)
	lo = index*10
	if lo > len(listStations):
		return dict(error="No stations in that range")
	if len(listStations) < lo+10:
		hi = len(listStations)
	else:
		hi = lo+10
	
	stationList["back"] = index-1 if lo > 0 else None
	stationList["next"] = index+1 if len(listStations) > hi else None
	stations = []
	for i in range(lo,hi):
		station = listStations[i].split("=")
		stations.append(station[1])
	stationList["stations"] = stations

	return stationList

def Control(command):
	commands = dict(pause="p", next="n", love="+", ban="-", tired="t")
	try:
		open(current_dir + "ctl", "w").write(commands[command])
		if command == "next":
			writeMsg("Skipped")
		elif command == "love":
			writeMsg("Loved")
		elif command == "ban":
			writeMsg("Banned")
		elif command == "tired":
			writeMsg("Tired")
		return True
	except KeyError:
		return False
def ChangeStation(id):
	open(current_dir + "ctl", "w").write("s" + str(int(id)) + "\n")
	writeMsg("Changed station")
	return True

def CreateStation(type, meta):
	if type == "quick":
		if meta == "song":
			open(current_dir + "ctl", "w").write("vs\n")
			writeMsg("Station created")
			return True
		elif meta == "artist":
			open(current_dir + "ctl", "w").write("va\n")
			writeMsg("Station created")
			return True
		else:
			return False
	else:
		return False

def api(data, json=None):
	if json is None or json == "":
		replyJSON = libjson.dumps(dict(method="NoJSON", id=None, response="bad"), indent=2)
	json = libjson.loads(json)
	
	if json["method"] == "GetSongInfo":
		if os.path.exists(current_dir + "msg"):
			msg = open(current_dir + "msg").read()
			os.remove(current_dir + "msg")
		else:
			msg = None
		songData = getSongData(data)
		replyJSON = libjson.dumps(dict(method="GetSongInfo", msg=msg, id=json["id"], song=songData), indent=2)
	elif json["method"] == "GetExplanation":
		replyJSON = libjson.dumps(dict(method="GetExplanation", id=json["id"], explanation=getExplanation()), indent=2)
	elif json["method"] == "GetStationData":
		replyJSON = libjson.dumps(dict(method="GetStationList", id=json["id"], stationData=getStations(json["index"])), indent=2)
	elif json["method"] == "Control":
		if Control(json["command"]):
			replyJSON = libjson.dumps(dict(method="Control", id=json["id"], command=json["command"], response="ok"), indent=2)
		else:
			replyJSON = libjson.dumps(dict(method="Control", id=json["id"], command=json["command"], response="bad"), indent=2)
	elif json["method"] == "CreateStation":
		replyJSON = libjson.dumps(dict(method="CreateStation", id=json["id"], response="disabled - See issue #23"), indent=2) # see issue#23
		if json["quick"]:
			if CreateStation("quick", json["quick"]):
				replyJSON = libjson.dumps(dict(method="CreateStation", id=json["id"], quick=json["quick"], response="ok"), indent=2)
			else:
				replyJSON = libjson.dumps(dict(method="CreateStation", id=json["id"], quick=json["quick"], response="bad"), indent=2)
		else:
			replyJSON = libjson.dumps(dict(method="CreateStation", id=json["id"], response="bad"), indent=2)
	elif json["method"] == "ChangeStation":
		if json["stationID"]:
			if ChangeStation(json["stationID"]):
				replyJSON = libjson.dumps(dict(method="ChangeStation", id=json["id"], stationID=json["stationID"], response="ok"), indent=2)
			else:
				replyJSON = libjson.dumps(dict(method="ChangeStation", id=json["id"], stationID=json["stationID"], response="bad"), indent=2)
		else:
			replyJSON = libjson.dumps(dict(method="ChangeStation", id=json["id"], response="bad"), indent=2)
	elif json["method"] == "Pianobar.Start":
		if(data["pianobar"] is None):
			data["pianobar"] = process(["pianobar"], True)
			replyJSON = json=libjson.dumps(dict(method="Pianobar.Start", id=json["id"], response="ok"), indent=2)
		else:
			replyJSON = json=libjson.dumps(dict(method="Pianobar.Start", id=json["id"], response="bad"), indent=2)
	elif json["method"] == "Pianobar.Quit":
		if(data["pianobar"]):
			open(current_dir + "ctl", "w").write("q")
			writeMsg("Shutdown")
			os.remove(current_dir + "stationList")
			os.remove(current_dir + "curSong.json")
			data["pianobar"].wait()
			data["pianobar"] = None
			replyJSON = libjson.dumps(dict(method="Pianobar.Quit", id=json["id"], response="ok"), indent=2)
		else:
			replyJSON = libjson.dumps(dict(method="Pianobar.Quit", id=json["id"], response="bad"), indent=2)
	else:
		replyJSON = libjson.dumps(dict(method="NoValidMethod", id=json["id"], response="bad"), indent=2)

	return dict(data=data, json=replyJSON)