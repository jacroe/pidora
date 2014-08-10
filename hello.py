import cherrypy, os, json as libjson, re
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
cherrypy.engine.autoreload.unsubscribe()

from pidora.pianobar import Pianobar as pianobar
from pidora.npr import Npr as npr
from pidora.somafm import Somafm as somafm
from pidora.bbc import Bbc as bbc
from pidora.googlemusic import Googlemusic as googlemusic

config = libjson.loads(open(current_dir + "config.json", "r").read())

class Pidora():

	def __init__(self):
		self.service, self.serviceName = None, None

		if "startup" in config:
			self.service = globals()[config["startup"]]()
			self.serviceName = config["startup"]
			self.service.start()

	@cherrypy.expose
	def index(self):
		if self.is_mobile(cherrypy.request.headers["User-Agent"]):
			raise cherrypy.HTTPRedirect('/mobile')
		return open(current_dir + "static/html/index.html", "r").read()

	@cherrypy.expose
	def status(self):
		return "We're jolly good"

	@cherrypy.expose
	def mobile(self, c=None):
		if c is not None:
			self.service.control(c)
			raise cherrypy.HTTPRedirect('/mobile')
		songdata = self.service.get_songdata()
		mobile_page = open(current_dir + "static/html/mobile.html", "r").read()

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
			if self.serviceName is None:
				validCall["data"] = None
			else:
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
						self.service, self.serviceName = None, None
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

	def is_mobile(self, user_agent):
		reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
		reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)
		b = reg_b.search(user_agent)
		v = reg_v.search(user_agent)

		if b or v:
			return True
		else:
			return False

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
