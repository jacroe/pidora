cd $HOME
echo "Installing packages. This may take a while..."
sudo apt-get install apache2 libapache2-mod-php5 pianobar git mpg123 python-feedparser -y
echo "All packages installed"
echo "Restarting Apache just for kicks"
sudo /etc/init.d/apache2 restart
mkdir ~/www
sudo cp /etc/apache2/sites-available/default /etc/apache2/sites-available/pidora
echo "We're about to open a config file with nano. Please change each instance of '/var/www/' to '$HOME/www/'"
read -n1 -r -p "Press any key to continue..."
sudo nano /etc/apache2/sites-available/pidora
echo "Thanks. Enabling the new profile..."
sudo a2dissite default && sudo a2ensite pidora
echo "...and restarting Apache again"
sudo /etc/init.d/apache2 restart
echo "Testing Apache configuration"
echo "pidora" > /home/pi/www/index.html
if [[ $(wget -qO- http://localhost/) ]]
   then echo "Apache is up and running!"
else (
   echo "Ugh... Could not setup Apache"
   echo "Exiting..."
   return
)
fi
echo "Making sure PHP is enabled"
sudo a2enmod php5
sudo /etc/init.d/apache2 restart
echo "Finished installing Apache and PHP"
echo
echo "Starting to set up pianobar"
read -p "What is your Pandora email address? " username
read -p "What is your Pandora pasword? " password
mkdir -p ~/.config/pianobar
echo "user = $username
password = $password" > ~/.config/pianobar/config
fingerprint=`openssl s_client -connect tuner.pandora.com:443 < /dev/null 2> /dev/null | openssl x509 -noout -fingerprint | tr -d ':' | cut -d'=' -f2` && echo tls_fingerprint = $fingerprint >> ~/.config/pianobar/config
echo "We think we set up pianobar. We'll test it now. It should log in and ask you to select a station."
pianobar
echo "If it didn't work, you'll need to troubleshoot it yourself."
echo "Once you've done so, we'll start setting up the rest of it."
read -n1 -r -p "Press any key to continue..."
echo
rm -rf ~/www/
echo "We'll now start cloning into Pidora"
git clone https://github.com/jacroe/pidora.git -q
echo "Downloading finished. Setting up now"
mv pidora/* www/
sudo chgrp www-data www/
chmod g+w www/
mkdir www/albumart/
sudo chgrp www-data www/albumart/
chmod g+w www/albumart/
echo "Creating FIFO queue"
mkfifo www/ctl
chmod g+w www/ctl
sudo chgrp www-data www/ctl
echo "Adding new variables to pianobar's config"
echo "event_command = ~/www/pianobar-eventcmd/update.py
fifo = ~/www/ctl" >> ~/.config/pianobar/config
echo "We're going to open a python script with nano. Please set the variable 'www' to '$HOME/www/'"
read -n1 -r -p "Press any key to continue..."
nano www/pianobar-eventcmd/update.py
