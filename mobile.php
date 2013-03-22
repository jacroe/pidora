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
$songlink = $arraySong[5];
$pidoraurl = "http://" . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
if ($coverart)
{
	$temp = "albumart/".md5($album).".jpg";
	if (!file_exists($temp)) file_put_contents($temp, file_get_contents($coverart));
	$coverart = $temp;
}   
else $coverart = "imgs/pandora.png";

$love = $arraySong[4];

if ($love) $heading .= " <3";
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-GB">
<head>
    <title>Pidora | Mobile</title>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <meta name="description" content="Pidora mobile site - Full web control of Pianobar" />
    <meta name="HandheldFriendly" content="true" />
    <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no" />
    <meta name="robots" content="index, follow" />
    <meta http-equiv="Refresh" content="5">
    <link rel=stylesheet href=inc/mobile.css />
</head>
<body>
<div id="header">
    <ul>
        <li><a href="<?=$pidoraurl;?>?p=p">Pause</a></li>
        <li><a href="<?=$pidoraurl;?>?p=n">Next</a></li>
        <li><a href="<?=$pidoraurl;?>?p=%2B">Love</a></li>
        <li><a href="<?=$pidoraurl;?>?p=-">Ban</a></li>
        <li><a href="<?=$pidoraurl;?>?p=t">Tired</a></li>
    </ul>
</div>
<div class="colmask fullpage">
    <div class="col1">
        <!-- Column 1 start -->
        <div class="displayed"><?=$artist;?><br />
        <a href="<?=$songlink;?>"><?=$title;?></a><br />
        <?=$album;?></div>
        <img class="displayed" src="<?=$coverart;?>" width="350", height="350", alt="<?=$title;?> by <?=$artist;?>">
        <!-- Column 1 end -->
    </div>
</div>
<div class="footer" style=display:none>
<strong><p><a href="http://github.com/jacroe/pidora">Pidora</a> by jacroe</p></strong>
</div>
</body>
</html>
