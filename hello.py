import cherrypy, os, json as libjson, pidora
#from cherrypy.process.plugins import Daemonizer
#Daemonizer(cherrypy.engine).subscribe()
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
class Pidora():

	@cherrypy.expose
	def api(self, json=None):
		if json is None or json == "":
			return libjson.dumps(dict(method="NoJSON", id=None, response="bad"), indent=2)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		json = libjson.loads(json)
		
		if json["method"] == "GetSongInfo":
			if os.path.exists(current_dir + "msg"):
				msg = open(current_dir + "msg").read()
				os.remove(current_dir + "msg")
			else:
				msg = None
			songData = pidora.getSongData()
			return libjson.dumps(dict(method="GetSongInfo", msg=msg, id=json["id"], song=songData), indent=2)
		elif json["method"] == "GetExplanation":
			return libjson.dumps(dict(method="GetExplanation", id=json["id"], explanation=pidora.getExplanation()), indent=2)
		elif json["method"] == "GetStationList":
			return libjson.dumps(dict(method="GetStationList", id=json["id"], stationList=pidora.getStations(json["index"])), indent=2)
		elif json["method"] == "Control":
			if pidora.Control(json["command"]):
				return libjson.dumps(dict(method="Control", id=json["id"], command=json["command"], response="ok"), indent=2)
			else:
				return libjson.dumps(dict(method="Control", id=json["id"], command=json["command"], response="bad"), indent=2)
		elif json["method"] == "CreateStation":
			if json["quick"]:
				if pidora.CreateStation("quick", json["quick"]):
					return libjson.dumps(dict(method="CreateStation", id=json["id"], quick=json["quick"], response="ok"), indent=2)
				else:
					return libjson.dumps(dict(method="CreateStation", id=json["id"], quick=json["quick"], response="bad"), indent=2)
			else:
				return libjson.dumps(dict(method="CreateStation", id=json["id"], response="bad"), indent=2)
		elif json["method"] == "ChangeStation":
			if json["stationID"]:
				if pidora.ChangeStation(json["stationID"]):
					return libjson.dumps(dict(method="ChangeStation", id=json["id"], stationID=json["stationID"], response="ok"), indent=2)
				else:
					return libjson.dumps(dict(method="ChangeStation", id=json["id"], stationID=json["stationID"], response="bad"), indent=2)
			else:
				return libjson.dumps(dict(method="ChangeStation", id=json["id"], response="bad"), indent=2)
		elif json["method"] == "Pianobar.Start":
			pidora.process(["pianobar"], True)
			return libjson.dumps(dict(method="Pianobar.Start", id=json["id"], response="ok"), indent=2)
		elif json["method"] == "Pianobar.Quit":
			open(current_dir + "ctl", "w").write("q")
			pidora.writeMsg("Shutdown")
			os.remove(current_dir + "stationList")
			os.remove(current_dir + "curSong.json")
			return libjson.dumps(dict(method="Pianobar.Quit", id=json["id"], response="ok"), indent=2)
		else:
			return libjson.dumps(dict(method="NoValidMethod", id=json["id"], response="bad"), indent=2)

	def mobileHead(self):
		return """<!doctype html>
<html lang="en-GB">
<head>
	<title>Pidora | Mobile</title>
	<meta name="description" content="Pidora mobile site - Full web control of Pianobar" />
	<meta name="HandheldFriendly" content="true" />
	<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no" />
	<meta name="robots" content="index, follow" />
	<meta http-equiv="Refresh" content="5">
	<link rel=stylesheet href=css/mobile.css />
</head>
<body>
<div id="header">
	<p>Controls currently disabled</p>
</div>
<div class="colmask fullpage">
	<div class="col1">
	<!-- Column 1 start -->
"""
	def mobileFoot(self):
		return """\n\t<!-- Column 1 end -->
    </div>
</div>
<div class="footer" style=display:none>
<p><strong><a href="http://github.com/jacroe/pidora">Pidora</a> by jacroe</strong></p>
</div>
</body>
</html>
"""
	@cherrypy.expose
	def mobile(self):
		songData = pidora.getSongData()
		
		returnData = self.mobileHead()
		returnData += """\t<div class="displayed">""" + songData["artist"] + """<br />
	<a href=""" + songData["explainURL"]  + """>""" + songData["title"] + """</a><br />
	""" + songData["album"] + """</div>
	<img class="displayed" src=""" + songData["artURL"] + """ width="350" height="350" alt=" """ + songData["title"]  + " by " + songData["artist"] + """ ">"""
		returnData += self.mobileFoot()
		return returnData

	m = mobile

#cherrypy.tree.mount(Pidora(), config=current_dir + "cpy.conf")
#cherrypy.engine.start()
#cherrypy.engine.block()
cherrypy.quickstart(Pidora(), config=current_dir + "cpy.conf")