<?php
if (!$_GET) echo getSong();
if ($_GET['control'])
	file_put_contents("ctl", $_GET['control']);


function getSong() {
	$return = "";
	if (!file_exists("curSong")) 
	{
		$return = "
	<img src=pandora.png class=albumart alt=\"Pandora logo\" />
	<h1>Hello There</h1>
	<h2>Pianobar is starting up...</h2>";
		die($return);
	}

	if (file_exists("msg"))
	{
		$msg = file_get_contents("msg");
		unlink("msg");
		die("<h1 class=msg>$msg</h1>");
	
	}

	$songInfo = file_get_contents("curSong");
	$arraySong = explode("|", $songInfo);
	$title = $arraySong[0];
	$artist = $arraySong[1];
	$album = $arraySong[2];
	$love = $arraySong[3];
	$albumart = str_replace(" ","-","{$artist}_{$album}.jpg");
	$albumart = str_replace("/","-",$albumart);
	$albumart = str_replace("#","",$albumart);
	if (!file_exists("artwork/".$albumart))
	{
		$arrayRemove = array("(Explicit)", "(Single)", "(Radio Edit)", "(US Bonus Track Version)", "(Radio Single)");
		$albumCleaned = str_replace($arrayRemove, "", $album);
		$lastfm = new SimpleXMLElement(file_get_contents("http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=72dde5529328e4f5da9eb6e3139876f4&artist=".urlencode($artist)."&album=".urlencode($albumCleaned)));
		$image = $lastfm->album[0]->image[3];
		if ($image == "") $image = "pandora.png";	
		file_put_contents("artwork/".$albumart, file_get_contents($image));
	}


	if ($love==1) $return .= "<img src=love.png class=love width=20 />\n";
	$return .= "
	<img src=artwork/$albumart class=albumart alt=\"Artwork for $album\" />
	<h1>$title</h1>
	<h2>$artist</h2>
	<h2 class=album>$album</h2>";
	return $return;
}
?>
