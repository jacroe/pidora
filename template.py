import os

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def index(songData):
	return open(current_dir + "static/html/index.html").read()

def tv(songData):
	return open(current_dir + "static/html/tv.html").read()

def mobile(songData):
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
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
</head>
<body>
<div id="header">
	<p><a href=?c=pause>Pause</a> <a href=?c=next>Next</a> <a href=?c=love>Love</a> <a href=?c=ban>Ban</a> <a href=?tired>Tired</a> <a href=# onclick="explainSong();return false">Explain</a></p>
	<p>
	<select name="stationselect">
		<option>Change Station</option>
	</select>
	</p>
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
<script type="text/javascript">
	$(document).ready(function()
	{
		getStations(0);

		$('select[name=stationselect]').change(function()
		{
			var id = $('select[name=stationselect]').val();
			$.get("api", {json:JSON.stringify({"method":"ChangeStation", "id":1, "stationID":id})}).done(function()
				{
					window.setTimeout(function(){location.reload();}, 3000);
				});
		});
	});

	function getStations(index)
	{
		$.get("api", {json:JSON.stringify({"method":"GetStationData", "id":1, "index":index})}).done(function(stationList)
		{
			stationList = stationList.stationData;
			for(var i = 0; i < stationList.stations.length; i++)
			{
				$('select[name=stationselect]')
					.append($('<option>', { value : index.toString() + i.toString() }).text(stationList.stations[i]));
			}
			if(stationList.next != null)
				getStations(index+1);
		});
	}

	function explainSong()
	{
		switch({EXPLANATION})
		{
			case 1:
				$.get("api", {json:JSON.stringify({"method":"GetExplanation", "id":1})}).done(function(explain)
				{
					alert(explain.explanation);
				});
				break;
			case 2:
				alert("How can you expect an explanation when there's nothing playing? You're being silly.");
				break;
			case 3:
				alert("There does not exist an appropriate explanation for this track. Sorry about that.");
				break;
		}
	}
</script>
</body>
</html>
"""