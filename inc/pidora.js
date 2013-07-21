$(document).ready(function()
{
	var newDataPlain, oldSongData, newSongData;
	window.setInterval(function()
	{
		$.get("api.php", function(newDataPlain)
		{
			newData = JSON.parse(newDataPlain);
			if(newData.title)
			{
				if($('#msg').is(':visible'))
				{
					clearScreen(function()
					{
						$('#content').fadeIn('slow');
					});
				}
				newSongData = newData;
				if(JSON.stringify(oldSongData) !== JSON.stringify(newSongData))
				{
					oldSongData = newSongData;
					clearScreen(function()
					{
						updateSong(newSongData);
						$('#content').fadeIn('slow');
					});
					setMousetraps();
				}
			}
			else if(newData.msg)
			{
				clearScreen(function()
				{
					$('#msg h1').html(newData.msg);
					$('#msg').fadeIn('slow');
				});
			}
		});
	}, 3000);
});

function clearScreen(doNext)
{
	$('#content, #msg, #stationList').fadeOut('slow').promise().done(function()
	{
		doNext();
	});
}

function updateSong(data)
{
	$('#content h1').html(data.title);
	$('#content h2').html(data.artist);
	$('#content .album').html(data.album);
	$('#content .details').html("EMPTY").hide();
	if(data.loved)
		$('#content .love').show();
	else
		$('#content .love').hide();
	$('#content .albumart').attr("src", data.artURL).attr("alt", data.album + " by " + data.artist);
};

function explainSong()
{
	details = $('p.details').html();
	if (details == "EMPTY")
	{
		$('p.details').html("Grabbing explanation...").fadeToggle('slow');
		$.get("api.php", {command:'e'}).done(function(explainPlain)
		{
			explain = JSON.parse(explainPlain);
			$('p.details').fadeOut('slow', function()
			{
				$(this).html(explain.explanation).fadeIn('slow');
			});
		});
	}
	else
		$('p.details').fadeToggle('slow');
}

function stationSetup()
{
	var index = 0;
	getStations(index);
	Mousetrap.reset();
	Mousetrap.bind('0', function() { sendCommand('s'.concat(index,'0')); });
	Mousetrap.bind('1', function() { sendCommand('s'.concat(index,'1')); });
	Mousetrap.bind('2', function() { sendCommand('s'.concat(index,'2')); });
	Mousetrap.bind('3', function() { sendCommand('s'.concat(index,'3')); });
	Mousetrap.bind('4', function() { sendCommand('s'.concat(index,'4')); });
	Mousetrap.bind('5', function() { sendCommand('s'.concat(index,'5')); });
	Mousetrap.bind('6', function() { sendCommand('s'.concat(index,'6')); });
	Mousetrap.bind('7', function() { sendCommand('s'.concat(index,'7')); });
	Mousetrap.bind('8', function() { sendCommand('s'.concat(index,'8')); });
	Mousetrap.bind('9', function() { sendCommand('s'.concat(index,'9')); });
	Mousetrap.bind('n', function() { getStations(++index); });
	Mousetrap.bind('b', function() { getStations(--index); });
	Mousetrap.bind('esc', function()
	{
		clearScreen(function()
		{
			$('#content').fadeIn('slow');
			setMousetraps();
		});
	});
}

function getStations(index)
{
	$.get("api.php", {station:index}).done(function(stationList)
	{
		clearScreen(function()
		{
			$('#stationList').html(stationList).fadeIn('slow');
		});
	});
}

function sendCommand(action)
{
	$.get("api.php", {command:action});
};

function setMousetraps()
{
	Mousetrap.reset();
	Mousetrap.bind(['p', 'space'], function() { sendCommand('p'); });
	Mousetrap.bind('n', function() { sendCommand('n'); });
	Mousetrap.bind('l', function() { sendCommand('+'); });
	Mousetrap.bind('b', function() { sendCommand('-'); });
	Mousetrap.bind('t', function() { sendCommand('t'); });
	Mousetrap.bind('q', function() { sendCommand('q'); });
	Mousetrap.bind('e', function() { explainSong(); });
	Mousetrap.bind('s', function() { stationSetup(); });
}