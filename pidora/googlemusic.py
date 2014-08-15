from gmusicapi import Mobileclient, Webclient
import os, json, requests, random, threading
from base import Base
from pygame import mixer
from Queue import Queue

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
config = json.loads(open(current_dir + "config.json", "r").read())["googlemusic"]

class Googlemusic(Base):

	def __init__(self):
		self.device_id, self.gmusic_api, self.library = None, None, None
		self.playing = False
		self.thread = None

	def start(self):
		username, password = config["username"], config["password"]
		mixer.init()

		self.gmusic_api = Mobileclient()
		self._get_device_id(username, password)
		self.gmusic_api.login(username, password)
		self.library = self.gmusic_api.get_all_songs()
		self.songdata = dict(
			title="",
			artist="",
			album="",
			albumart="",
			loved=False,
			)

		#self.play_shuffled_library()
		#self.play_playlist("Soft, Quiet, Sleep")
		#self.play_album("Shatter Me")
	def quit(self):
		if self.thread is not None:
			self.thread_stop.set()
			mixer.music.stop()

	def control(self, command):
		if command == "start":
			self.play_shuffled_library()
			return True
		elif command == "quit":
			self.quit()
			return True
		elif command == "pause":
			if self.playing:
				mixer.music.pause()
				self.playing = False
			else:
				mixer.music.unpause()
				self.playing = True
		elif command == "next":
			mixer.music.stop()
			return True
		else:
			return False

	def get_songdata(self):
		return self.songdata
	def set_songdata(self, title, artist, album, albumart, extra=dict(loved=False)):
		self.songdata = dict(
			title=title,
			artist=artist,
			album=album,
			albumart=albumart,
			loved=extra["loved"]
			)

	def play_shuffled_library(self):
		library = self.library;
		random.shuffle(library)

		self.start_thread(library)

		return True


	def play_album(self, album_name):
		album_songs = list()
		for song in self.library:
			if song["album"] == album_name:
				album_songs.append(song)
		album_songs.sort(key=lambda song: song["trackNumber"])

		if album_songs == list():
			return False

		self.start_thread(album_songs)

		return True

	def play_playlist(self, playlist_name):
		playlists = self.gmusic_api.get_all_user_playlist_contents()

		playlist = None
		for i in playlists:
			if i["name"] == playlist_name:
				playlist = i
		if playlist is None:
			return False

		songlist = list()
		for song in playlist["tracks"]:
			for j in self.library:
				if j["id"] == song["trackId"]:
					songlist.append(j)
					break

		self.start_thread(songlist)
		return True

	def start_thread(self, songlist):
		if self.thread is not None:
			if self.thread.is_alive():
				self.quit()
				self.thread.join()

		self.thread = threading.Thread(target=self.queue_songlist, args=(songlist,))
		self.thread_stop = threading.Event()
		self.thread.start()

	def queue_songlist(self, songs):
		q = Queue()

		for song in songs:
			q.put(song)
		while not q.empty():
			while mixer.music.get_busy():
				pass
			if self.thread_stop.is_set():
				quit()
			cur_song = q.get()
			self._play_song(cur_song["id"])
			if "rating" in cur_song:
				rating = cur_song["rating"]=="5"
			else:
				rating = False
			if "albumArtRef" in cur_song:
				self.set_songdata(cur_song["title"], cur_song["artist"], cur_song["album"], cur_song["albumArtRef"][0]["url"], dict(loved=rating))
			else:
				self.set_songdata(cur_song["title"], cur_song["artist"], cur_song["album"], "", dict(loved=rating))
			self.playing = True

	def _play_song(self, song_id):
		stream_url = self.gmusic_api.get_stream_url(song_id, self._get_device_id()).replace("https://", "http://")

		r = requests.get(stream_url, stream=True)
		if r.status_code == 200:
			with open("/tmp/song.mp3", "wb") as f:
				for chunk in r.iter_content(1024):
					f.write(chunk)

		mixer.music.load("/tmp/song.mp3")
		mixer.music.play()

	def _get_device_id(self, username=None, password=None):
		if self.device_id is None:
			web_api = Webclient()
			web_api.login(username, password)
			devices = web_api.get_registered_devices()
			for device in devices:
				if device["type"] == "PHONE":
					self.device_id = device["id"].replace("0x", "")
					break
			web_api.logout()

		return self.device_id

	def api(self, data):
		validMethods = ["Googlemusic.PlayAlbum", "Googlemusic.PlayPlaylist", "Googlemusic.PlayShuffledLibrary"]
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

		if method == "Googlemusic.PlayAlbum":
			if params is None or "albumName" not in params:
				return missingParamaterJSON
			else:
				if self.play_album(params["albumName"]):
					return json.dumps(validCall, indent=2)
				else:
					return notValidParameterJSON
		elif method == "Googlemusic.PlayPlaylist":
			if params is None or "playlistName" not in params:
				return missingParamaterJSON
			else:
				if self.play_playlist(params["playlistName"]):
					return json.dumps(validCall, indent=2)
				else:
					return notValidParameterJSON
		elif method == "Googlemusic.PlayShuffledLibrary":
			self.play_shuffled_library()
			return json.dumps(validCall, indent=2)