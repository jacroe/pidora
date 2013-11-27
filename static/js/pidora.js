$(document).ready(function()
{
	var newDataPlain, oldSongData, newSongData;
	window.setInterval(function()
	{
		$.get("api", {json:JSON.stringify({"method":"GetSongInfo", "id":1})}).done(function(newData)
		{
			if(!newData.msg)
			{
				if($('#msg').is(':visible'))
				{
					clearScreen('#content');
				}
				newSongData = newData.song;
				if(JSON.stringify(oldSongData) !== JSON.stringify(newSongData))
				{
					oldSongData = newSongData;
					clearScreen('#content', function()
					{
						updateSong(newSongData);
					});
					if(newSongData.isSong)
					{
						setMousetraps();
						$('#controls').fadeIn('slow');
					}
					else
					{
						Mousetrap.reset();
						$('#controls').fadeOut('slow');
						if(newSongData.startup == false)
							Mousetrap.bind(['s', 'enter', 'space'], function() { pianobarStart(); });
					}
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
	if(data.startup == false)
	{
		document.title = "Pidora";
		$('#content h1').html("Want Music?");
		$('#content h2').html("Scan the QR Code");
		$('#content .album').html("");
		$('#content .love').hide();
		$('#content .details').html("EMPTY").hide();
		$('#content .albumart').attr("src", "https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl=http%3A//" + location.host + "/start&chld=H|0");
	}
	else if(data.startup == true)
	{
		document.title = "Starting up | Pidora";
		$('#content h1').html("Hello There");
		$('#content h2').html("Pianobar is starting up...");
		$('#content .album').html("");
		$('#content .love').hide();
		$('#content .albumart').attr("src", "imgs/pandora.png");
	}
	else
	{
		document.title = data.title + ", " + data.artist + " | Pidora";
		$('#content h1').html(data.title);
		$('#content h2').html(data.artist);
		$('#content .album').html(data.album);
		$('#content .details').html("EMPTY").hide();
		if(data.loved)
			$('#content .love').show();
		else
			$('#content .love').hide();
		$('#content .albumart').attr("alt", data.album + " by " + data.artist);
		if(data.artURL)
			$('#content .albumart').attr("src", data.artURL);
		else
			$('#content .albumart').attr("src", "imgs/pandora.png");
	}
};

function explainSong()
{
	details = $('p.details').html();
	if (details == "EMPTY")
	{
		$('p.details').html("Grabbing explanation...").fadeToggle('slow');
		$.get("api", {json:JSON.stringify({"method":"GetExplanation", "id":1})}).done(function(explain)
		{
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
	Mousetrap.bind('0', function() { changeStation(index + '0'); });
	Mousetrap.bind('1', function() { changeStation(index + '1'); });
	Mousetrap.bind('2', function() { changeStation(index + '2'); });
	Mousetrap.bind('3', function() { changeStation(index + '3'); });
	Mousetrap.bind('4', function() { changeStation(index + '4'); });
	Mousetrap.bind('5', function() { changeStation(index + '5'); });
	Mousetrap.bind('6', function() { changeStation(index + '6'); });
	Mousetrap.bind('7', function() { changeStation(index + '7'); });
	Mousetrap.bind('8', function() { changeStation(index + '8'); });
	Mousetrap.bind('9', function() { changeStation(index + '9'); });
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
	$.get("api", {json:JSON.stringify({"method":"GetStationData", "id":1, "index":index})}).done(function(stationList)
	{
		stationList = stationList.stationData
		clearScreen('#stationList', function()
		{
			var htmlStationList = ""
			if(stationList.back != null)
				htmlStationList = "<a onclick=getStations(" + stationList.back + ");>B - Back</a><br />\n";
			for(var i = 0; i < stationList.stations.length; i++)
			{
				htmlStationList += "<a onclick=changeStation('" + index + i + "');>" + i + " - " + stationList.stations[i] + "</a><br />\n"
			}
			if(stationList.next != null)
				htmlStationList += "<a onclick=getStations(" + stationList.next + ");>N - Next</a><br />\n";
			$('#stationList').html(htmlStationList);
		});
	});
}

function changeStation(id)
{
	$.get("api", {json:JSON.stringify({"method":"ChangeStation", "id":1, "stationID":id})})
}

function newStationSetup()
{
	Mousetrap.reset();
	Mousetrap.bind('s', function() { newStation('song'); });
	Mousetrap.bind('a', function() { newStation('artist'); });
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
	$.get("api", {json:JSON.stringify({"method":"CreateStation", "id":1, "quick":type})});
	clearScreen('#content', function()
	{
		setMousetraps();
	});
}

function sendCommand(action)
{
	$.get("api", {json:JSON.stringify({"method":"Control", "id":1, "command":action})});
};

function pianobarStart()
{
	$.get("api", {json:JSON.stringify({"method":"Pianobar.Start", "id":1})});
};
function pianobarQuit()
{
	$.get("api", {json:JSON.stringify({"method":"Pianobar.Quit", "id":1})});
};

function setMousetraps()
{
	Mousetrap.reset();
	Mousetrap.bind(['p', 'space'], function() { sendCommand('pause'); });
	Mousetrap.bind('n', function() { sendCommand('next'); });
	Mousetrap.bind('l', function() { sendCommand('love'); });
	Mousetrap.bind('b', function() { sendCommand('ban'); });
	Mousetrap.bind('t', function() { sendCommand('tired'); });
	Mousetrap.bind('q', function() { pianobarQuit(); });
	Mousetrap.bind('e', function() { explainSong(); });
	Mousetrap.bind('s', function() { stationSetup(); });
	Mousetrap.bind(['(', '-', '_'], function() { sendCommand('volumedown'); });
	Mousetrap.bind([')', '=', '+'], function() { sendCommand('volumeup'); });
	//Mousetrap.bind('c', function() { newStationSetup(); }); See issue#23
}