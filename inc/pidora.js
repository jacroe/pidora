$(document).ready(function()
{
	var msgShown = false;
	oldData = $('#content h1').html();
	window.setInterval(function()
	{
		if(msgShown)
		$('#msg').fadeOut('slow', function()
		{
			$('#content').fadeIn('slow');
		});
		$.get("api.php", function(newData)
		{
			var newDataObj = JSON.parse(newData)
			if(newDataObj.msg)
			{
				$('#content').fadeOut('slow', function()
				{
					$('#msg h1').html(newDataObj.msg);
					$('#msg').fadeIn('slow');
					msgShown = true;
				});
			}
			else if (!(oldData == newDataObj.title) && newDataObj.title)
			{
				oldData = newDataObj.title;
				$('#content').fadeOut('slow', function()
				{
					$('#content h1').html(newDataObj.title)
					$('#content h2').html(newDataObj.artist)
					$('#content .album').html(newDataObj.album)
					$('#content .details').html("EMPTY").hide()
					if(newDataObj.loved) {$('#content .love').show()} else {$('#content .love').hide()}
					$('#content .albumart').attr("src", newDataObj.artURL)
					$('#content').fadeIn('slow')
				});
				setMousetraps();
			}
			else if(newDataObj.loved && !($('#content .love').is(':visible')))
			{
				$('#content .love').show();
			}
		});
	}, 3000);
});
function stationSetup()
{
	index = 0;
	getStations(index);
	Mousetrap.reset();
	Mousetrap.bind('0', function() { control('s'.concat(index,'0')); });
	Mousetrap.bind('1', function() { control('s'.concat(index,'1')); });
	Mousetrap.bind('2', function() { control('s'.concat(index,'2')); });
	Mousetrap.bind('3', function() { control('s'.concat(index,'3')); });
	Mousetrap.bind('4', function() { control('s'.concat(index,'4')); });
	Mousetrap.bind('5', function() { control('s'.concat(index,'5')); });
	Mousetrap.bind('6', function() { control('s'.concat(index,'6')); });
	Mousetrap.bind('7', function() { control('s'.concat(index,'7')); });
	Mousetrap.bind('8', function() { control('s'.concat(index,'8')); });
	Mousetrap.bind('9', function() { control('s'.concat(index,'9')); });
	Mousetrap.bind('n', function() { getStations(++index, true); })
	Mousetrap.bind('b', function() { getStations(--index, true); })
	Mousetrap.bind('esc', function()
	{
	    $('#stationList').fadeOut('slow', function(){$('#content').fadeIn('slow')});
	    setMousetraps();
	});
}
function getStations(index, shown)
{
	$.get("api.php", {station:index}).done(function(stationList)
	{
		if(shown)
		{
			$('#stationList').fadeOut('slow', function()
			{
				$('#stationList').html(stationList).fadeIn('slow');
			});
		}
		else
		{
			$('#content').fadeOut('slow', function()
			{
				$('#stationList').html(stationList).fadeIn('slow');
			});
		}
	});
}
function control(action)
{
	$.get("api.php", {control:action});
};
function explain()
{
	details = $('p.details').html();
	if (details == "EMPTY")
	{
		$('p.details').html("Grabbing explanation...").fadeToggle("slow");
		$.get("api.php",{control:"e"}).done(function(data)
		{
			dataObj = JSON.parse(data);
			$('p.details').fadeOut('slow', function()
			{
				$(this).html(dataObj.explanation).fadeIn('slow')
			});
		});
	}
	else {$('p.details').fadeToggle("slow");}
};
function setMousetraps()
{
	Mousetrap.reset();
	Mousetrap.bind(['p', 'space'], function() { control('p'); });
	Mousetrap.bind('n', function() { control('n'); });
	Mousetrap.bind('l', function() { control('+'); });
	Mousetrap.bind('b', function() { control('-'); });
	Mousetrap.bind('t', function() { control('t'); });
	Mousetrap.bind('q', function() { control('q'); });
	Mousetrap.bind('e', function() { explain(); });
	Mousetrap.bind('s', function() { stationSetup(); });
}