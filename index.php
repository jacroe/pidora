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
	      }
	   });
	}, 3000);


	Mousetrap.bind(['p', 'space'], function() { control('p'); });
	Mousetrap.bind('n', function() { control('n'); });
	Mousetrap.bind('l', function() { control('+'); });
	Mousetrap.bind('b', function() { control('-'); });
	Mousetrap.bind('t', function() { control('t'); });
	Mousetrap.bind('e', function() { explain(); });
});
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
</div>
<div id=content>
</div>
</body>
</html>
