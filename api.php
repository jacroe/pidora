<?php
if (file_exists("msg"))
{
	$msg = file_get_contents("msg");
	unlink("msg");
	$return = "<h1 class=msg>$msg</h1>";
}
elseif (!file_exists("curSong"))
{
	$return = "<img src=inc/pandora.png class=albumart alt=\"Pandora logo\" />
<h1>Hello There</h1>
<h2>Pianobar is starting up...</h2>";
}
elseif ($_GET['control']) 
{
	$c = $_GET['control'];
	if ($c == "e")
	{
		$return = getDetails();
	}
	else
	{
		file_put_contents("ctl", "$c\n");
		
		if ($c == "n") file_put_contents("msg", "Skipped");
		if ($c == "q")
		{
			file_put_contents("msg", "Shutdown");
			unlink("curSong");
			unlink("stationList");
		}
		if ($c[0] == "s") file_put_contents("msg", "Changing stations");
		$return = "ok";
	}
}
elseif ($_GET['station'] != null)
{
	$i = $_GET['station']*10;
	$max = $i+10;
	$arrayStations = explode("|", file_get_contents("stationList"));
	
	if ($i > 0) $return = "<a onclick=getStations(--index);>B - Back</a><br />\n";
	for($i; ($i < $max) && ($i < count($arrayStations) ); $i++)
	{
		$stationRaw = $arrayStations[$i];
		$station = explode("=", $stationRaw);
		$return .= "<a onclick=control('s".$station[0]."');>".substr($station[0], -1)." - ".$station[1]."</a><br />\n";
	}
	if (count($arrayStations) > $max) $return .= "<a onclick=getStations(++index);>N - Next</a><br />";
}
else $return = getSong();

echo $return;

function getSong() {
	$return = "";
	
	$songInfo = file_get_contents("curSong");
	$arraySong = explode("|", $songInfo);
	$title = $arraySong[0];
	$artist = $arraySong[1];
	$album = $arraySong[2];
	$coverart = $arraySong[3];
	if ($coverart)
	{
		$temp = "albumart/".md5($album).".jpg";
		if (!file_exists($temp)) file_put_contents($temp, file_get_contents($coverart));
		$coverart = $temp;
	}
	else $coverart = "inc/pandora.png";
	$love = $arraySong[4];
	
	if ($love==1) $return .= "<img src=inc/love.png class=love width=20 />";
	$return .= "
	<img src=$coverart class=albumart alt=\"Artwork for $album\" />
	<h1>$title</h1>
	<h2>$artist</h2>
	<h2 class=album>$album</h2>
	<p class=details>EMPTY</p>";
	return $return;
}
function getDetails($url = NULL)
{
	if (!$url)
	{
		$arraySong = explode("|", file_get_contents("curSong"));
		$url = $arraySong[5];
	}
	$data = file_get_contents($url);
	#preg_match("#features of this track(.*?)\<p\>These are just a#is", $data, $matches); // uncomment this if explanations act funny
	preg_match("#features of this track(.*?)\</div\>#is", $data, $matches);
	$strip = array("Features of This Track</h2>", "<div style=\"display: none;\">", "</div>", "<p>These are just a");
	if (!$matches[0]) return "We were unable to get the song's explanation. Sorry about that.";
	$data = explode("<br>", str_replace($strip, "", $matches[0]));
	unset($data[count($data)-1]);
	if (trim($data[count($data)-1]) == "many other comedic similarities")
	{
		$ending = "many other comedic similarities";
		unset($data[count($data)-1]);
	}
	else $ending = "many other similarites as identified by the Music Genome Project";
	$data = implode(", ", array_map('trim', $data));
	return "We're playing this track because it features $data, and $ending.";
}
?>
