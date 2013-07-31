import json as libjson, os, re, urllib2, subprocess

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def process(command, new = False):
	if new:
		with open(os.devnull, "w") as fnull: result = subprocess.Popen(command, stdout = fnull, stderr = fnull)
	else:
		with open(os.devnull, "w") as fnull: result = subprocess.call(command, stdout = fnull, stderr = fnull)

def getSongData():
	if os.path.exists(current_dir + "curSong.json"):
		jsonObj = libjson.loads(open(current_dir + "curSong.json").read())
		if jsonObj["title"].find("NPR News") != -1:
			jsonObj["isSong"] = False
		else:
			jsonObj["isSong"] = True
		return jsonObj
	else:
		return libjson.loads('{"album":"","loved":false,"artist":"Pianobar is starting up...","title":"Hello There","artURL":"","startup":true, "isSong":false}')

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
	lo = index*10
	if lo > len(listStations):
		return ""
	if len(listStations) < lo+10:
		hi = len(listStations)
	else:
		hi = lo+10
	returnData = ""

	if lo > 0:
		returnData += "<a onclick=getStations(" + str(index-1) + ");>B - Back</a><br />\n"
	for i in range(lo,hi):
		station = listStations[i].split("=")
		returnData += "<a onclick=changeStation('" + str(station[0]) + "');>" + str(station[0][-1:]) + " - " + str(station[1]) + "</a><br />\n"

	if len(listStations) > hi:
		returnData += "<a onclick=getStations(" + str(index+1) + ");>N - Next</a><br />"

	return returnData

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
	open(current_dir + "ctl", "w").write("s" + str(id) + "\n")
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