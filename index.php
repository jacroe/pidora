<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora</title>
<link rel=stylesheet href=styles.css />
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
<script src="mousetrap.js"></script>
<script>
$(document).ready(function(){
	
	oldData = $('#content').html();
	window.setInterval(function(){
	   $.get("api.php", function(newData)
	   {
	      if (!(oldData == newData))
	      {
		 oldData = newData;
		 $('#content').fadeOut('slow', function(){$(this).html(newData).fadeIn('slow')});
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
	Mousetrap.bind('n', function() { getStations(++index); })
	Mousetrap.bind('b', function() { getStations(--index); })
	Mousetrap.bind('esc', function()
	{
	    $('#content').fadeOut('slow', function(){$(this).html(oldData).fadeIn('slow')});
	    setMousetraps();
	});
}
function getStations(index)
{
	$.get("api.php", {station:index})
	   .done(function(stationList) {$('#content').fadeOut('slow', function(){$(this).html(stationList).fadeIn('slow')}); });
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
	      $.get("api.php",{control:"e"})
	         .done(function(data) { $('p.details').fadeOut('slow', function(){$(this).html(data).fadeIn('slow')}); });
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
	Mousetrap.bind('e', function() { explain(); });
	Mousetrap.bind('s', function() { stationSetup(); });
}
</script>
</head>
<body>
<div id=controls>
<a onclick=control('p');>Play</a>
<a onclick=control('n');>Next</a>
<a onclick=control('+');>Love</a>
<a onclick=control('-');>Ban</a>
<a onclick=control('t');>Tired</a>
<a onclick=explain();>Explain</a>
<a onclick=stationSetup();>Station</a>
</div>
<div id=content>
</div>
</body>
</html>
