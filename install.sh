cd $HOME
echo "Installing packages. This may take a while..."
sudo apt-get install pianobar git mpg123 python-feedparser -y
echo "All packages installed"
sleep 5
clear
echo "Starting to set up pianobar"
read -p "What is your Pandora email address? " username
read -p "What is your Pandora pasword? " password
mkdir -p ~/.config/pianobar
echo "user = $username
password = $password" > ~/.config/pianobar/config
fingerprint=`openssl s_client -connect tuner.pandora.com:443 < /dev/null 2> /dev/null | openssl x509 -noout -fingerprint | tr -d ':' | cut -d'=' -f2` && echo tls_fingerprint = $fingerprint >> ~/.config/pianobar/config
echo
echo "We think we set up pianobar. We'll test it now. It should log in and ask you to select a station."
echo "After selecting the station, pianobar will print the station's name and a long ID number. Copy that number to the clipboard."
echo "Press q to quit at any time."
read -n1 -r -p "Press any key to continue..."
echo
pianobar
echo "If for whatever reason it didn't work, you'll need to troubleshoot it yourself."
echo "Once you've done so, we'll start setting up the rest of it."
read -n1 -r -p "Press any key to continue..."
echo
read -p "What was the station's ID number? " stationID
echo "autostart_station = $stationID" >> ~/.config/pianobar/config
cd $HOME
clear
echo "Thanks. We'll now start cloning into Pidora"
git clone https://github.com/jacroe/pidora.git -q
echo "Downloading finished."
echo
echo "We'll begin setting up Pidora for use."
echo "Creating FIFO queue"
mkfifo pidora/ctl
echo "Adding new variables to pianobar's config"
echo "event_command = $HOME/pidora/bar-update.py
fifo = $HOME/pidora/ctl" >> ~/.config/pianobar/config
echo "We think we're done. Let's test it, shall we?"
read -n1 -r -p "Press any key to continue..."
clear
echo "Start pianobar in another terminal."
echo "I'll wait."
read -n1 -r -p "Press any key to continue..."
echo 
echo "We're going to start the Pidora webserver now. You can access it by going to http://127.0.0.1:8080 in a browser."
echo "You should have full control pianobar. Experiment with it to be sure."
echo "You can stop the server at any time by pressing Ctrl+C."
python pidora/hello.py
clear
echo "Configuring the startup script."
echo "rm /home/user/pidoraLocation/curSong
@midori -a \"http://localhost:8080/\" -e Fullscreen
@python pidora/hello.py
@pianobar" | sudo tee -a /etc/xdg/lxsession/LXDE/autostart
echo
echo "Done!"
echo "Reboot your Pi and enjoy!"