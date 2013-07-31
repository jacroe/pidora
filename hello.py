import cherrypy, os, json as libjson, pidora, template
#from cherrypy.process.plugins import Daemonizer
#Daemonizer(cherrypy.engine).subscribe()
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
class Pidora():


	@cherrypy.expose
	def index(self):
		songData = pidora.getSongData()
		return template.index(songData)

	@cherrypy.expose
	def api(self, json=None):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return pidora.api(json)

	@cherrypy.expose
	def mobile(self):
		songData = pidora.getSongData()
		return template.mobile(songData)
	m = mobile

#cherrypy.tree.mount(Pidora(), config=current_dir + "cpy.conf")
#cherrypy.engine.start()
#cherrypy.engine.block()
cherrypy.quickstart(Pidora(), config=current_dir + "cpy.conf")