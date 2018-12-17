sudo apt-get update
sudo apt-get install python3-pip python3-dev build-essential
sudo pip3 install selenium
wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip
unzip chromedriver_linux64.zip && sudo cp chromedriver /usr/local/bin
sudo apt-get install imagemagick
export PATH=/usr/local/bin/chromedriver:$PATH
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install google-chrome-stable
sudo pip3 install pysocks
sudo pip3 install urllib3 --upgrade
