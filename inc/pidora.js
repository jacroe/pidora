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
					clearScreen('#content');
				}
				newSongData = newData;
				if(JSON.stringify(oldSongData) !== JSON.stringify(newSongData))
				{
					oldSongData = newSongData;
					clearScreen('#content', function()
					{
						updateSong(newSongData);
					});
					setMousetraps();
				}
			}
			else if(newData.msg)
			{
				clearScreen('#msg', function()
				{
					$('#msg h1').html(newData.msg);
				});
			}
		});
	}, 3000);
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
		clearScreen('#content', function()
		{
			setMousetraps();
		});
	});
}

function getStations(index)
{
	$.get("api.php", {station:index}).done(function(stationList)
	{
		clearScreen('#stationList', function()
		{
			$('#stationList').html(stationList);
		});
	});
}

function newStationSetup()
{
	Mousetrap.reset();
	Mousetrap.bind('s', function() { newStation('s'); });
	Mousetrap.bind('a', function() { newStation('a'); });
	Mousetrap.bind('esc', function()
	{
		clearScreen('#content', function()
		{
			setMousetraps();
		});
	});
	clearScreen('#newStation');
}

function newStation(type)
{
	sendCommand('v' + type);
	clearScreen('#content', function()
	{
		setMousetraps();
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
	Mousetrap.bind('c', function() { newStationSetup(); });
}