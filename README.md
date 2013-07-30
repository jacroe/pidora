Pidora
======

*This is a quick and dirty README. Use at your own risk*

1.	Install pianobar, mpg123, and python-feedparser and their dependencies.
2.	Configure pianobar until you are able to run <tt>pianobar</tt> from the command line without any interaction. The man file is particularly helpful. If you get a "TLS Handshake failed" error, run [this command](https://gist.github.com/4200610). It will append the correct TLS fingerprint to your config file.
3.	Create a FIFO file by running `mkfifo ctl` in your pidora directory. 
4.	Edit your pianobar config file by adding the `fifo` and `event_command` variables and their location. The `event_command` should point to the `bar-update.py` Python script. You can use this [sample config file](https://gist.github.com/jacroe/cd1850ad6a1fcf4a72e3) as a guide.
5.  Run `python hello.py`. Pidora will begin running. 
6.	Run pianobar and open Midori to the location of pidora. By default, this is http://localhost:8080. You should see the song information and the album art. This should fade out with the next song. Try Loving, Banning, and Shelving a song. The appropriate message should fade in then out again.

That's it for the installation. Now let's configure our machine to automatically launch the web browser and pianobar.

1.	Enable the pi to automatically log in and start the x server.
2.	Add the following lines of code to `/etc/xdg/lxsession/LXDE/autostart`: `rm /home/user/pidoraLocation/curSong`, `@midori -a "http://localhost:8080/" -e Fullscreen`, `@pianobar` perferably with pianobar being called after Midori.
	This will cause Midori to launch fullscreen with pidora as the location and will start pianobar. I added it to the `autostart` file in LXDE as I didn't want it to launch until the x server was up and running. It also removes the last played song from Pidora so we get a "Pianobar is starting" message if Midori beats out pianobar (hasn't happened for me).
3.	Follow the instructions [here](http://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank) to make the monitor not turn itself off. However, save it to the `~/.xsessionrc` instead of `~/.xinitrc`.
4.	Finally, remove all the icons on the desktop and set the statusbar to hide automatically. This isn't necessary but it gives less an impression that this is a computer.


Contact me
==========

You can shoot me an email or submit an issue at [GitHub](https://github.com/jacroe/pidora/issues/new) if you have a question or a suggestion. I welcome them with open arms.

If you found this useful, I also welcome tips with open arms! You can tip me via [Gittip](http://gittip.com/jacroe), [Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XC7VG35XEHN8W), or [Bitcoin](http://jacroe.com/bitcoin.html). I'll use these to pay for bills and/or Mountain Dew and pizza. Thank you, and best wishes!