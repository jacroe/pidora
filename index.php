<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora</title>
<link rel=stylesheet href=styles.css />
<script src="jquery.js"></script>
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
	$("#controls").hover(
	   function(){
	      $("#controls .c").fadeOut("fast", function(){$("a").fadeIn("slow");});
	   },
	   function(){
	      $("a").fadeOut("slow", function(){$("#controls .c").fadeIn("slow");});
	});
	$("a").css("display", "none");
});
</script>
</head>
<body>
<div id=controls>
<span class=c>C</span>
<a onclick=$.get("api.php",{control:"p"});>Play</a>
<a onclick=$.get("api.php",{control:"n"});>Next</a>
<a onclick=$.get("api.php",{control:"+"});>Love</a>
<a onclick=$.get("api.php",{control:"-"});>Ban</a>
<a onclick=$.get("api.php",{control:"t"});>Shelve</a>
</div>
<div id=content>
</div>
</body>
</html>
