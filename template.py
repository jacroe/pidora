import os

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def index(songData, songExplanation=False):
	return open(current_dir + "static/html/index.html").read()

def tv(songData, songExplanation=False):
	return open(current_dir + "static/html/tv.html").read()

def mobile(songData, songExplanation=False):
	returnData = mobileTemplate()
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
		if songExplanation is not False:
			returnData = returnData.replace("{EXPLANATION}", songExplanation.replace("'", "\\\'"))
		else:
			returnData = returnData.replace("{EXPLANATION}", "There does not exist an appropriate explanation for this track. Sorry about that.")
	elif songData["startup"]:
		returnData = returnData.replace("{SONGTITLE}", "We're starting up")
		returnData = returnData.replace("{SONGARTIST}", "Sit Tight")
		returnData = returnData.replace("{SONGALBUM}", "And Hang On")
		returnData = returnData.replace("{SONGARTURL}", "imgs/pandora.png")
		returnData = returnData.replace("{ALBUMARTALT}", "Pandora logo")
		returnData = returnData.replace("{LOVED}", "")
		returnData = returnData.replace("{EXPLANATION}", "How can you expect an explanation when there\\\'s nothing playing? You\\\'re being silly.")
	else:
		returnData = returnData.replace("{SONGTITLE}", "We're Shutdown")
		returnData = returnData.replace("{SONGARTIST}", "Just Chillin'")
		returnData = returnData.replace("{SONGALBUM}", "And Taking It Easy")
		returnData = returnData.replace("{SONGARTURL}", "imgs/pandora.png")
		returnData = returnData.replace("{ALBUMARTALT}", "Pandora logo")
		returnData = returnData.replace("{LOVED}", "")
		returnData = returnData.replace("{EXPLANATION}", "How can you expect an explanation when there\\\'s nothing playing? You\\\'re being silly.")
	return returnData

def mobileTemplate():
	return """<!doctype html>
<html lang="en-GB">
<head>
	<title>Pidora | Mobile</title>
	<meta name="description" content="Pidora mobile site - Full web control of Pianobar" />
	<meta name="HandheldFriendly" content="true" />
	<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no" />
	<meta name="robots" content="index, follow" />
	<link rel=stylesheet href=css/mobile.css />
</head>
<body>
<div id="header">
	<p><a href=?c=pause>Pause</a> <a href=?c=next>Next</a> <a href=?c=love>Love</a> <a href=?c=ban>Ban</a> <a href=?tired>Tired</a> <a href=# onclick="alert('{EXPLANATION}');return false">Explain</a></p>
</div>
<div class="colmask fullpage">
	<div class="col1">
	<!-- Column 1 start -->
	<div class="displayed">{SONGTITLE} {LOVED} <br />
	{SONGARTIST}<br />
	{SONGALBUM}</div>
	<img class="displayed" src="{SONGARTURL}" width="350" height="350" alt="{ALBUMARTALT}" />
	<!-- Column 1 end -->
    </div>
</div>
<div class="footer" style=display:none>
<p><strong><a href="http://github.com/jacroe/pidora">Pidora</a> by jacroe</strong></p>
</div>
</body>
</html>
"""