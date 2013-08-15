import os

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def index(songData):
	return open(current_dir + "static/html/index.html").read()

def mobile(songData):
	returnData = mobileHead()
	returnData += """\t<div class="displayed">""" + songData["artist"] + """<br />
	""" + songData["title"] + """</a><br />
	""" + songData["album"] + """</div>
	<img class="displayed" src=""" + songData["artURL"] + """ width="350" height="350" alt=" """ + songData["title"]  + " by " + songData["artist"] + """ ">"""
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
	<meta http-equiv="Refresh" content="5">
	<link rel=stylesheet href=css/mobile.css />
</head>
<body>
<div id="header">
	<p>Controls currently disabled</p>
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
