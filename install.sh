cd $HOME
clear
echo "Hello There!"
echo "We're starting the Pidora Installation. Grab your helmets and hang on. This is going to be quick."
echo "Note: This won't set it up to autostart when your Pi comes on. You'll need to do that yourself (for now)"
echo
echo "Installing packages..."
sudo apt-get install git mpg123 libao-dev libfaad-dev libmad0-dev python-feedparser pkg-config python-setuptools -y
echo
echo "Now configuring python environment..."
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
sudo pip install requests
sudo pip install beautifulsoup4
echo "All packages installed"
sleep 5
clear
echo "Downloading pianobar and moving it to the bin/"
wget https://dl.dropboxusercontent.com/u/170196/pianobar
sudo mv pianobar /usr/local/bin
sudo chown root:root /usr/local/bin/pianobar
sudo chmod 755 /usr/local/bin/pianobar 
echo "pianobar installed."
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
echo "After selecting the station, pianobar will print the station's name and a long ID number. This will be the default station. Copy that number to the clipboard."
echo "You can quit pianobar at any time by pressing 'q'."
read -n1 -r -p "Press any key to continue..."
echo
pianobar
echo
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
cd pidora
git checkout develop
cd $HOME
echo "Cloning Pidora complete."
echo
echo "We'll begin setting up Pidora for use."
echo "Creating FIFO queue"
mkfifo $HOME/.config/pianobar/ctl
echo "Adding new variables to pianobar's config"
echo "event_command = $HOME/pidora/ext/pianobar-update.py
fifo = $HOME/.config/pianobar/ctl" >> ~/.config/pianobar/config
echo "We think we're done. Let's test it, shall we?"
read -n1 -r -p "Press any key to continue..."
clear
LANip=`ip addr show | awk '$1=="inet" {print $2}' | cut -f1 -d'/'`
echo "We're going to start the Pidora webserver now."
echo "You can access it by going to http://127.0.0.1:8008 in the RPi's browser or"
echo "http://"$LANip":8008 on a device on the same Local Area Network."
echo "You should have full control of pianobar. Experiment with it to be sure."
echo "You can stop the server at any time by pressing Ctrl+C."
python pidora/hello.py
clear
echo "Done!"
echo "Reboot your Pi and enjoy!"