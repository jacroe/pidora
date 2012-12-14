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
	
	
	Mousetrap.bind('p', function() { $.get("api.php",{control:"p"}); });
	Mousetrap.bind('n', function() { $.get("api.php",{control:"n"}); });
	Mousetrap.bind('l', function() { $.get("api.php",{control:"+"}); });
	Mousetrap.bind('b', function() { $.get("api.php",{control:"-"}); });
	Mousetrap.bind('t', function() { $.get("api.php",{control:"t"}); });
});
</script>
</head>
<body>
<div id=controls>
<a onclick=$.get("api.php",{control:"p"});>Play</a>
<a onclick=$.get("api.php",{control:"n"});>Next</a>
<a onclick=$.get("api.php",{control:"+"});>Love</a>
<a onclick=$.get("api.php",{control:"-"});>Ban</a>
<a onclick=$.get("api.php",{control:"t"});>Tired</a>
</div>
<div id=content>
</div>
</body>
</html>
