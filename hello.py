import cherrypy, os, json as libjson
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
cherrypy.engine.autoreload.unsubscribe()

from pidora.pianobar import Pianobar as pianobar
from pidora.npr import Npr as npr
from pidora.somafm import Somafm as somafm
from pidora.bbc import Bbc as bbc

config = libjson.loads(open(current_dir + "config.json", "r").read())

class Pidora():

	service, serviceName = None, None

	if "startup" in config:
		service = globals()[config["startup"]]()
		serviceName = config["startup"]
		service.start()

	@cherrypy.expose
	def index(self):
		return open("static/html/index.html", "r").read()

	@cherrypy.expose
	def status(self):
		return "We're jolly good"

	@cherrypy.expose
	def mobile(self, c=None):
		if c is not None:
			self.service.control(c)
			raise cherrypy.HTTPRedirect('/mobile')
		songdata = self.service.get_songdata()
		mobile_page = open("static/html/mobile.html", "r").read()

		replacement_dict = {
			"{SONGTITLE}":songdata["title"],
			"{SONGARTIST}":songdata["artist"],
			"{SONGALBUM}":songdata["album"],
			"{SONGARTURL}":songdata["albumart"],
			"{ALBUMARTALT}":songdata["album"],
			"{LOVED}":"",
			"{SERVICE}":self.serviceName
		}

		if "loved" in songdata:
			if songdata["loved"]: replacement_dict["{LOVED}"] = "&hearts;"
		if songdata["albumart"] == "":
			replacement_dict["{SONGARTURL}"] = "static/imgs/pandora.png"

		for k,v in replacement_dict.items():
			mobile_page = mobile_page.replace(k,v)

		return mobile_page
	m = mobile

	@cherrypy.expose
	def api(self, json=None):
		cherrypy.response.headers['Content-Type'] = 'application/json'

		validMethods = ["Song.GetData", "Song.SetData", "Player.Control", "Player.Service"]
		notValidMethodJSON = libjson.dumps(dict(response="bad", error="NotValidMethod"), indent=2)
		notValidParameterJSON = libjson.dumps(dict(response="bad", error="NotValidParameter"), indent=2)
		missingParamaterJSON = libjson.dumps(dict(response="bad", error="MissingParameters"), indent=2)
		validCall = dict(response="good")

		if not json:
			return notValidMethodJSON
		data = libjson.loads(json)

		if "method" not in data:
			return notValidMethodJSON
		else:
			method = data["method"]

		if "params" in data:
			if type(data["params"]) is type(dict()):
				params = data["params"]
			else:
				return notValidParameterJSON
		else:
			params = None

		if method not in validMethods:
			return self.service.api(data)

		if method == "Song.GetData":
			validCall["data"] = self.service.get_songdata()
			validCall["service"] = self.serviceName
			return libjson.dumps(validCall, indent=2)
		elif method == "Song.SetData":
			if params is None:
				return missingParamaterJSON
			if "extra" in params:
				self.service.set_songdata(
					params["title"],
					params["artist"],
					params["album"],
					params["albumart"],
					params["extra"])
			else:
				self.service.set_songdata(
					params["title"],
					params["artist"],
					params["album"],
					params["albumart"])
			return libjson.dumps(validCall, indent=2)
		elif method == "Player.Control":
			if params is None or "command" not in params:
				return missingParamaterJSON
			else:
				if self.service.control(params["command"]):
					if params["command"] == "quit":
						self.service = None
					return libjson.dumps(validCall, indent=2)
				else:
					return notValidParameterJSON
		elif method == "Player.Service":
			if params is None or "service" not in params:
				return missingParamaterJSON
			else:
				if self.service is not None:
					self.service.quit()
				self.service = globals()[params["service"]]()
				self.serviceName = params["service"]
				self.service.start()
				return libjson.dumps(validCall, indent=2)

cherrypy.config.update({
	'server.socket_host': "0.0.0.0",
	'server.socket_port': config["default_port"],
})

cherrypy_config = {
	'/': {"tools.staticdir.root": os.path.dirname(os.path.abspath(__file__))},
	'/static': {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': 'static'
	}
}
cherrypy.quickstart(Pidora(), config=cherrypy_config)
# @TODO
# If the service has quit or hasn't started, we should let the people know instead of returning old/null data
