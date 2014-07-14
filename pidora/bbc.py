import requests, os, subprocess, json, time
from bs4 import BeautifulSoup as bsoup
from base import Base

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"

config = json.loads(open(current_dir + "config.json", "r").read())["bbc"]

class Bbc(Base):

	def start(self):
		self.songdata = dict(
			title="BBC World Service",
			artist="BBC World Service",
			album="BBC World Service",
			albumart="http://swling.com/blog/wp-content/uploads/2013/12/BBC-World-Service.jpg",
			)
		self.process = None
		self.last_checked_epoch = 0
		with open(os.devnull, "w") as fnull: self.process = subprocess.Popen(["mpg123", "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk_backup"], stdout = fnull, stderr = fnull)
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
			bbc_html = requests.get("http://www.bbc.co.uk/worldserviceradio/programmes/schedules")
			parsed_bbc_html = bsoup(bbc_html.text)
			on_now = parsed_bbc_html.find("li", {"id":"on-now"}).find("span", {"property":"name"}).text

			self.songdata["title"] = on_now
			self.last_checked_epoch = time.time()
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
