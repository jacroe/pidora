import requests, os, re, subprocess, json
from base import Base

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"

config = json.loads(open(current_dir + "config.json", "r").read())["pianobar"]

class Pianobar(Base):

	def start(self):
		self.songdata = dict(
			title="",
			artist="",
			album="",
			albumart="",
			loved="",
			explanation="",
			explainURL="",
			)
		self.stationdata = []
		self.process = None
		with open(os.devnull, "w") as fnull: self.process = subprocess.Popen(["pianobar"], stdout = fnull, stderr = fnull)
	def quit(self):
		open(config["ctl"], "w").write("q")
		self.process.wait()

	def control(self, command):
		commands = dict(pause="p", next="n", love="+", ban="-", tired="t", volumedown="(", volumeup=")")
		if command == "start":
			self.start()
			return True
		elif command == "quit":
			self.quit()
			return True
		else:
			try:
				open(config["ctl"], "w").write(commands[command])
				return True
			except KeyError:
				return False

	def change_station_by_id(self, stationId):
		open(config["ctl"], "w").write("s" + str(int(stationId)) + "\n")
		return True
	def change_station_by_name(self, station):
		for i in range(0, len(self.stationdata)):
			if self.stationdata[i].find(station) != -1:
				return self.change_station_by_id(i)
				break
		return False

	def get_explanation(self, explainURL):
		regex = re.compile("Track</h2>(.*?)</div>",re.IGNORECASE|re.DOTALL)
		html = requests.get(explainURL).text
		string = html.replace("\t", "").replace("\n", "").replace('<div style="display: none;">', "")
		r = regex.search(string)
		if r is None:
			return "We were unable to get the song's explanation. Sorry about that."
		data = r.groups()[0].split("<br>")
		traits = data[0:len(data)-1]
		if data[len(data)-2].find("many other comedic similarities") == -1:
			ending = "many other similarities as identified by the Music Genome Project"
		else:
			ending = "many other comedic similarities"
			traits = data[0:len(data)-2]
		return "We're playing this track because it features " + ", ".join(traits) + ", and " + ending +"."

	def get_songdata(self):
		return self.songdata
	def set_songdata(self, title, artist, album, albumart, extra=dict(loved=False, explainURL=False)):
		self.songdata = dict(
			title=title,
			artist=artist,
			album=album,
			albumart=albumart,
			loved=extra["loved"],
			explanation=False,
			explainURL=extra["explainURL"],
			)
		if extra["explainURL"] is not False:
			self.songdata["explanation"] = str(self.get_explanation(extra["explainURL"]))

	def get_stationdata(self):
		return self.stationdata
	def set_stationdata(self, stations):
		self.stationdata = stations

	def api(self, data):

		validMethods = ["Pianobar.GetStationData", "Pianobar.SetStationData", "Pianobar.ChangeStation"]
		notValidMethodJSON = json.dumps(dict(response="bad", error="NotValidMethod"), indent=2)
		notValidParameterJSON = json.dumps(dict(response="bad", error="NotValidParameter"), indent=2)
		missingParamaterJSON = json.dumps(dict(response="bad", error="MissingParameters"), indent=2)
		validCall = dict(response="good")

		method = data["method"]
		if "params" in data:
			if type(data["params"]) is type(dict()):
				params = data["params"]
			else:
				return notValidParameterJSON
		else:
			params = None

		if method not in validMethods:
			return notValidMethodJSON

		if method == "Pianobar.GetStationData":
			validCall["stationData"] = self.get_stationdata()
			return json.dumps(validCall, indent=2)
		elif method == "Pianobar.SetStationData":
			if params is None or "stations" not in params:
				return missingParamaterJSON
			elif type(params["stations"]) is not type(list()):
				return notValidParameterJSON
			else:
				self.set_stationdata(params["stations"])
				return json.dumps(validCall, indent=2)
		elif method == "Pianobar.ChangeStation":
			if params is None or "stationId" not in params:
				return missingParamaterJSON
			else:
				self.change_station_by_id(params["stationId"])
				return json.dumps(validCall)
				