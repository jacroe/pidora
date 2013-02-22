Pidora
======

*This is a quick and dirty README. Use at your own risk*

1.	Install pianobar, apache2, and libapache2-mod-php5 and their dependencies
2.	Configure Apache2 and PHP the way you like. I followed this [guide](https://help.ubuntu.com/community/ApacheMySQLPHP#Installing_Apache_2) and moved my `www` folder to the home directory.
3.	Create an `albumart` directory in the pidora server directory and make sure it's writeable by the server.
4.	Configure pianobar until you are able to run <tt>pianobar</tt> from the command line without any interaction. The man file is particularly helpful. If you get a "TLS Handshake failed" error, run [this command](https://gist.github.com/4200610). It will append the correct TLS fingerprint to your config file.
5.	Create a FIFO file by running `mkfifo ctl` in your pidora directory. Make this writable by the server.
6.	Edit your pianobar config file by adding the `fifo` and `event_command` variables and their location. The `event_command` should point to the Python script.
7.	Edit the directory location in the python script to point to the root of pidora.
8.	Run pianobar and open Midori to the location of pidora. You should see the song information and the album art. This should fade out with the next song. Try Loving, Banning, and Shelving a song. The appropriate message should fade in then out again.

That's it for the installation. Now let's configure our machine to automatically launch the web browser and pianobar.

1.	Enable the pi to automatically log in and start the x server.
2.	Add the following lines of code to `/etc/xdg/lxsession/LXDE/autostart`: `rm /home/user/pidoraWebLocation/curSong`, `@midori -a "http://localhost/pidora/" -e Fullscreen`, `@pianobar` perferably with pianobar being called after Midori.
	This will cause Midori to launch fullscreen with pidora as the location and will start pianobar. I added it to the `autostart` file in LXDE as I didn't want it to launch until the x server was up and running. It also removes the last played song from Pidora so we get a "Pianobar is starting" message if Midori beats out pianobar (hasn't happened for me).
3.	Follow the instructions [here](http://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank) to make the monitor not turn itself off. However, save it to the `~/.xsessionrc` instead of `~/.xinitrc`.
4.	Finally, remove all the icons on the desktop and set the statusbar to hide automatically. This isn't necessary but it gives less an impression that this is a computer.


Contact me
==========

You can shoot me an email or submit an issue at [GitHub](https://github.com/jacroe/pidora/issues/new) if you have a question or a suggestion. I welcome them with open arms.
