import requests, os, subprocess, json, time
from base import Base

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"

config = json.loads(open(current_dir + "config.json", "r").read())["npr"]

class Npr(Base):

	def start(self):
		self.songdata = dict(
			title="90.9 WBUR-FM",
			artist="90.9 WBUR-FM",
			album="90.9 WBUR-FM",
			albumart="http://cloudfront.assets.stitcher.com/feedimagesplain328/13726.jpg",
			)
		self.process = None
		self.last_checked_epoch = 0
		with open(os.devnull, "w") as fnull: self.process = subprocess.Popen(["mpg123", "http://wbur-sc.streamguys.com/wbur.mp3"], stdout = fnull, stderr = fnull)
		self.get_songdata()
	def quit(self):
		self.process.terminate()

	def control(self, command):
		if command == "quit":
			self.quit()
			return True
		else:
			return False

	def get_songdata(self):
		if int(time.time()) - 60 > self.last_checked_epoch:
			npr_schedule = requests.get("http://www.wbur.org/wp-content/published/json/schedule/playingNow.json")
			if npr_schedule.status_code is 200:
				now_playing = npr_schedule.json()
				self.songdata["title"] = str(now_playing["Title"])
				self.last_checked_epoch = int(time.time())

		return self.songdata
	def set_songdata(self, title, artist, album, albumart, extra=dict()):
		pass

	def api(self, data):

		validMethods = []
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
