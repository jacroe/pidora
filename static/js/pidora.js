$(document).ready(function()
{
	var newDataPlain, oldSongData, newSongData;
	window.setInterval(function()
	{
		$.get("api", {json:JSON.stringify({"method":"Song.GetData"})}).done(function(newData)
		{
			newSongData = newData.data;
			if(JSON.stringify(oldSongData) !== JSON.stringify(newSongData))
			{
				oldSongData = newSongData;
				clearScreen('#content', function()
				{
					updateSong(newSongData);
				});
			}
		});
	}, 3000);
	setMousetraps();
});
function clearScreen(showNext, doNext)
{
	$('#content, #msg, #newStation, #stationList').fadeOut('slow').promise().done(function()
	{
		if(doNext)
			doNext();
		$(showNext).fadeIn('slow');
	});
}
function updateSong(data)
{
	document.title = data.title + ", " + data.artist + " | Pidora";
	$('#content h1').html(data.title);
	$('#content h2').html(data.artist);
	$('#content .album').html(data.album);
	$('#content .details').html(data.explanation).hide();
	if(data.loved)
		$('#content .love').show();
	else
		$('#content .love').hide();
	$('#content .albumart').attr("alt", data.album + " by " + data.artist);
	if(data.albumart)
		$('#content .albumart').attr("src", data.albumart);
	else
		$('#content .albumart').attr("src", "static/imgs/pandora.png");
}
function sendCommand(action)
{
	$.get("api", {json:JSON.stringify({"method":"Player.Control", "params":{"command":action}})});
};
function setMousetraps()
{
	Mousetrap.reset();
	Mousetrap.bind(['p', 'space'], function() { sendCommand('pause'); });
	Mousetrap.bind('n', function() { sendCommand('next'); });
	Mousetrap.bind('l', function() { sendCommand('love'); });
	Mousetrap.bind('b', function() { sendCommand('ban'); });
	Mousetrap.bind('t', function() { sendCommand('tired'); });
	Mousetrap.bind('e', function() { $('#content .details').fadeToggle('slow'); });
	Mousetrap.bind(['(', '-', '_'], function() { sendCommand('volumedown'); });
	Mousetrap.bind([')', '=', '+'], function() { sendCommand('volumeup'); });
}