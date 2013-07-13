<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora</title>
<link rel=stylesheet href=inc/styles.css />
<link rel="icon" type="image/png" href="favicon.ico">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
<script src="http://cdn.craig.is/js/mousetrap/mousetrap.min.js?88c23"></script>
<script>
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
					$('#content .details').html("EMPTY")
					if(newDataObj.loved) {$('#content .love').show()} else {$('#content .love').hide()}
					$('#content .albumart').attr("src", newDataObj.artURL)
					$('#content').fadeIn('slow')
				});
				setMousetraps();
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
</script>
</head>
<body>

<div id="controls">
<a onclick="control('p');">Pause</a>
<a onclick="control('n');">Next</a>
<a onclick="control('+');">Love</a>
<a onclick="control('-');">Ban</a>
<a onclick="control('t');">Tired</a>
<a onclick="explain();">Explain</a>
<a onclick="stationSetup();">Station</a>
</div>

<div id="content">
<img src=inc/love.png class=love style="display:none" />
<img src=inc/pandora.png class=albumart alt="Pandora logo" />
<h1>Hello There</h1>
<h2>Pianobar is starting up...</h2>
<h2 class=album></h2>
<p class=details>EMPTY</p>
</div>

<div id="stationList" style="display:none">
</div>

<div id="msg" style="display:none">
<h1></h1>
</div>

</body>
</html>
