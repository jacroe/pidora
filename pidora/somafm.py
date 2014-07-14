import requests, os, subprocess, json, time, re
from bs4 import BeautifulSoup as bsoup
from base import Base

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"

config = json.loads(open(current_dir + "config.json", "r").read())["somafm"]

class Somafm(Base):

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
		self.last_checked_epoch = 0
		self.process = None
		with open(os.devnull, "w") as fnull: self.process = subprocess.Popen(["mpg123", "http://mp1.somafm.com:8800"], stdout = fnull, stderr = fnull)
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
		if int(time.time()) - 10 > self.last_checked_epoch:
			regex = re.compile("<td>(.*)\(Now\) <\/td>(.*)<!-- line 2 -->", re.IGNORECASE|re.DOTALL)
			lush_html = requests.get("http://somafm.com/lush/played").text
			lush_html_regexed = regex.search(lush_html)
			parsed_lush_html = bsoup(lush_html_regexed.groups()[1])

			title = parsed_lush_html.findAll("td")[1].text
			artist = parsed_lush_html.findAll("td")[0].text
			album = parsed_lush_html.findAll("td")[2].text

			if parsed_lush_html.findAll("td")[1].text != self.songdata["title"]:
				self.songdata = {"title": title,
								 "artist": artist,
								 "album": album,
								 "albumart": self.get_albumart(artist, album),
								}
			self.last_checked_epoch = time.time()
		return self.songdata
	def set_songdata(self, title, artist, album, albumart, extra=dict()):
		pass

	def get_albumart(self, artist, album):
		albumart_url = None
		
		if "lastfm_api" in config:
			lastfm_json = requests.get("http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s&format=json" % (config["lastfm_api"], artist, album)).json()
			if "error" not in lastfm_json:
				lastfm_images = lastfm_json["album"]["image"]
				for i in range(0, len(lastfm_images)):
					if lastfm_images[i]["size"] == "mega":
						albumart_url = lastfm_images[i]["#text"]
				albumart_url = str(albumart_url)

		if albumart_url is None or albumart_url is "":
			albumart_url = "http://i.img.co/radio/16/85/8516_290.png"

		return albumart_url

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
