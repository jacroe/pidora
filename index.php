<!DOCTYPE html>
<html lang="en">
<head>
<title>Pidora</title>
<link rel=stylesheet href=inc/styles.css />
<link rel="icon" type="image/png" href="favicon.ico">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
<script src="http://cdn.craig.is/js/mousetrap/mousetrap.min.js?88c23"></script>
<script src="./inc/pidora.js"></script>
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

<div id="content" style="display:none">
<img src=inc/love.png class=love style="display:none" />
<img src="" class=albumart alt="Pandora logo" />
<h1></h1>
<h2></h2>
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
