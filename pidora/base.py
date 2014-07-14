class Base():
	def start(self):
		raise NotImplementedError("Should have implemented this")
	def quit(self):
		raise NotImplementedError("Should have implemented this")
	def control(self, command):
		raise NotImplementedError("Should have implemented this")

	def get_songdata(self):
		raise NotImplementedError("Should have implemented this")
	def set_songdata(self, title, artist, album, albumart, other=dict()):
		raise NotImplementedError("Should have implemented this")