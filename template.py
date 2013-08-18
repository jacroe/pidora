import os

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def index(songData):
	return open(current_dir + "static/html/index.html").read()

def mobile(songData):
	returnData = mobileHead()
	try:
		if not songData["artURL"]:
			songData["artURL"] = "imgs/pandora.png"
		returnData += """\t<div class="displayed">""" + songData["title"] + """ """
		if songData["loved"]:
			returnData += "<3"
		returnData += """ <br />
		""" + songData["artist"] + """<br />
		""" + songData["album"] + """</div>
		<img class="displayed" src=""" + songData["artURL"] + """ width="350" height="350" alt=" """ + songData["title"]  + " by " + songData["artist"] + """ ">"""
	except KeyError:
		returnData += """\t<div class="displayed">We're Starting up<br />
		Sit Tight<br />
		And Hang On</div>
		<img class="displayed" src=imgs/pandora.png alt="Pandora logo">"""
	returnData += mobileFoot()
	return returnData

def mobileHead():
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
	<p><a href=?c=pause>Pause</a> <a href=?c=next>Next</a> <a href=?c=love>Love</a> <a href=?c=ban>Ban</a> <a href=?tired>Tired</a></p>
</div>
<div class="colmask fullpage">
	<div class="col1">
	<!-- Column 1 start -->
"""
def mobileFoot():
	return """\n\t<!-- Column 1 end -->
    </div>
</div>
<div class="footer" style=display:none>
<p><strong><a href="http://github.com/jacroe/pidora">Pidora</a> by jacroe</strong></p>
</div>
</body>
</html>
"""
