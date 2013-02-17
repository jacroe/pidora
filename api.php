<?php
if (!$_GET) echo getSong();
elseif ($_GET['control']) 
{
	if ($_GET['control'] == "e")
	{
		$songInfo = file_get_contents("curSong");
		$arraySong = explode("|", $songInfo);
		echo getDetails($arraySong[5]);
		die();
	}

	file_put_contents("ctl", "{$_GET['control']}\n");

	if ($_GET['control'] == "n") file_put_contents("msg", "Skipped");
}


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
	if ($coverart)
	{
		$temp = "albumart/".md5($album).".jpg";
		if (!file_exists($temp)) file_put_contents($temp, file_get_contents($coverart));
		$coverart = $temp;
	}
	else $coverart = "imgs/pandora.png";
	$love = $arraySong[4];
	
	if ($love==1) $return .= "<img src=imgs/love.png class=love width=20 />";
	$return .= "
	<img src=$coverart class=albumart alt=\"Artwork for $album\" />
	<h1>$title</h1>
	<h2>$artist</h2>
	<h2 class=album>$album</h2>
	<p class=details>EMPTY</p>";
	return $return;
}
function getDetails($url)
{
	$data = file_get_contents($url);
	preg_match("#features of this track(.*?)\<p\>These are just a#is", $data, $matches);
	$strip = array("Features of This Track</h2>", "<div style=\"display: none;\">", "</div>", "<p>These are just a");
	$data = explode("<br>", str_replace($strip, "", $matches[0]));
	unset($data[count($data)-1]);
	$data = implode(", ", array_map('trim', $data));
	return "We're playing this track because it features $data, and many other similarites as identified by the Music Genome Project.";
}
?>
