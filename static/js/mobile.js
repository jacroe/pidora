$(document).ready(function()
{
	getStations();

	$('select[name=stationselect]').change(function()
	{
		var id = $('select[name=stationselect]').val();
		$.get("api", {json:JSON.stringify({"method":"Pianobar.ChangeStation", "params":{"stationId":id}})}).done(function()
			{
				window.setTimeout(function(){location.reload();}, 3000);
			});
	});
});

function getStations()
{
	$.get("api", {json:JSON.stringify({"method":"Pianobar.GetStationData"})}).done(function(stationList)
	{
		stationList = stationList.stationData;
		for(var i = 0; i < stationList.length; i++)
		{
			$('select[name=stationselect]')
				.append($('<option>', { value : i.toString() }).text(stationList[i]));
		}
	});
}

function explainSong()
{
	$.get("api", {json:JSON.stringify({"method":"Song.GetData"})}).done(function(songData)
	{
		alert(songData.data.explanation);
		return false;
	});
}