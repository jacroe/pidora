<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora</title>
<link rel=stylesheet href=styles.css />
<script src="jquery.js"></script>
<script>
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
</script>
</head>
<body>
<div id=content>
</div>
</body>
</html>

