<?php
if ($_GET['p'])
{
	file_put_contents("ctl", "{$_GET['p']}\n");
	header("Location: mobile.php");
}
$songInfo = file_get_contents("curSong");
$arraySong = explode("|", $songInfo);
$title = $arraySong[0];
$artist = $arraySong[1];
$album = $arraySong[2];
$coverart = $arraySong[3];
$love = $arraySong[4];

$heading = "&ldquo;$title&rdquo;<br /> by $artist";
if ($love) $heading .= " <3";
?>
<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora | Mobile</title>
</head>
<body style="text-align:center; width:300px; font-size:2em;">
<strong><?php echo $heading; ?></strong><br />
<br />
<a href="?p=p">Pause</a><br />
<a href="?p=n">Next</a><br />
<a href="?p=%2B">Love</a><br />
<a href="?p=-">Ban</a><br />
<a href="?p=t">Tired</a>
</body>
</html>
