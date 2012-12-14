<?php
if (!$_GET) echo getSong();
if ($_GET['control']) file_put_contents("ctl", "{$_GET['control']}\n");


function getSong() {
	$return = "";
	if (!file_exists("curSong")) 
	{
		$return = "
	<img src=imgs/pandora.png class=albumart alt=\"Pandora logo\" />
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
	$coverart = $arraySong[3];
	$love = $arraySong[4];
	
	if ($love==1) $return .= "<img src=imgs/love.png class=love width=20 />";
	$return .= "
	<img src=$coverart class=albumart alt=\"Artwork for $album\" />
	<h1>$title</h1>
	<h2>$artist</h2>
	<h2 class=album>$album</h2>";
	return $return;
}
?>
