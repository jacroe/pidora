<?php
if (file_exists("msg"))
{
	$msg = file_get_contents("msg");
	unlink("msg");
	$return = json_encode(array("msg"=>$msg));
}
elseif (!file_exists("curSong.json"))
{
	$return = json_encode(array("album"=>"","loved"=>false,"artist"=>"Pianobar is starting up...", "title"=>"Hello There", "artURL"=>"inc/pandora.png", "startup"=>true));
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
			unlink("curSong.json");
			unlink("stationList");
			foreach (glob("albumart/*.jpg") as $delete) unlink($delete);
		}
		if ($c[0] == "s") file_put_contents("msg", "Changing stations");
		$return = json_encode(array("response"=>"ok"));
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
	
	$songInfo = json_decode(file_get_contents("curSong.json"), true);
	$coverart = $songInfo["artURL"];
	if ($coverart)
	{
		$temp = "albumart/".md5($songInfo["album"]).".jpg";
		if (!file_exists($temp)) file_put_contents($temp, file_get_contents($coverart));
		$coverart = $temp;
	}
	else $coverart = "inc/pandora.png";
	$songInfo = array_replace($songInfo, array("artURL"=>$coverart));
	return json_encode($songInfo);
}
function getDetails($url = NULL)
{
	if (!$url)
	{
		$songInfo = json_decode(file_get_contents("curSong.json"));
		$url = $songInfo->explainURL;
	}
	$data = file_get_contents($url);
	#preg_match("#features of this track(.*?)\<p\>These are just a#is", $data, $matches); // uncomment this if explanations act funny
	preg_match("#features of this track(.*?)\</div\>#is", $data, $matches);
	$strip = array("Features of This Track</h2>", "<div style=\"display: none;\">", "</div>", "<p>These are just a");
	if (!$matches[0]) return json_encode(array("explanation"=>"We were unable to get the song's explanation. Sorry about that."));
	$data = explode("<br>", str_replace($strip, "", $matches[0]));
	unset($data[count($data)-1]);
	if (trim($data[count($data)-1]) == "many other comedic similarities")
	{
		$ending = "many other comedic similarities";
		unset($data[count($data)-1]);
	}
	else $ending = "many other similarites as identified by the Music Genome Project";
	$data = implode(", ", array_map('trim', $data));
	return json_encode(array("explanation"=>"We're playing this track because it features $data, and $ending."));
}
?>
