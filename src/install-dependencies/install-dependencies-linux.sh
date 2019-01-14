#!/bin/sh
sudo apt-get update
sudo apt-get install python3-pip python3-dev build-essential imagemagick apt-transport-https
sudo pip3 install selenium pysocks requests urllib3 --upgrade

# Add the repositories for google-chrome-stable
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable

# Download the chromedriver and put it in a common place
wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip
unzip chromedriver_linux64.zip && sudo cp chromedriver /usr/local/bin
export PATH=/usr/local/bin/chromedriver:$PATH
