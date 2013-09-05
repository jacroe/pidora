import os

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def index(songData):
	return open(current_dir + "static/html/index.html").read()

def tv(songData):
	return open(current_dir + "static/html/tv.html").read()

def mobile(songData):
	returnData = open(current_dir + "static/html/mobile.html").read()
	if "startup" not in songData:
		if not songData["artURL"]:
			songData["artURL"] = "imgs/pandora.png"
		returnData = returnData.replace("{SONGTITLE}", songData["title"])
		returnData = returnData.replace("{SONGARTIST}", songData["artist"])
		returnData = returnData.replace("{SONGALBUM}", songData["album"])
		returnData = returnData.replace("{SONGARTURL}", songData["artURL"])
		returnData = returnData.replace("{ALBUMARTALT}", songData["title"] + " by " + songData["artist"])
		if songData["loved"]:
			returnData = returnData.replace("{LOVED}", "<3")
		else:
			returnData = returnData.replace("{LOVED}", "")
		if songData["isSong"] is True:
			returnData = returnData.replace("{EXPLANATION}", "1")
		else:
			returnData = returnData.replace("{EXPLANATION}", "3")
	elif songData["startup"]:
		returnData = returnData.replace("{SONGTITLE}", "We're starting up")
		returnData = returnData.replace("{SONGARTIST}", "Sit Tight")
		returnData = returnData.replace("{SONGALBUM}", "And Hang On")
		returnData = returnData.replace("{SONGARTURL}", "imgs/pandora.png")
		returnData = returnData.replace("{ALBUMARTALT}", "Pandora logo")
		returnData = returnData.replace("{LOVED}", "")
		returnData = returnData.replace("{EXPLANATION}", "2")
	else:
		returnData = returnData.replace("{SONGTITLE}", "We're Shutdown")
		returnData = returnData.replace("{SONGARTIST}", "Just Chillin'")
		returnData = returnData.replace("{SONGALBUM}", "And Taking It Easy")
		returnData = returnData.replace("{SONGARTURL}", "imgs/pandora.png")
		returnData = returnData.replace("{ALBUMARTALT}", "Pandora logo")
		returnData = returnData.replace("{LOVED}", "")
		returnData = returnData.replace("{EXPLANATION}", "2")
	return returnData