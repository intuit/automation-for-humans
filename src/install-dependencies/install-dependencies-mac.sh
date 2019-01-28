#!/bin/sh
brew update
brew install python || true
brew install brew-cask || true
brew cask install google-chrome || true
brew cask install chromedriver || true
brew install flex bison || true
pip install selenium pysocks urllib3 requests pyperclip
wget https://github.com/appium/appium-for-mac/releases/download/v0.3.0/AppiumForMac.zip
unzip AppiumForMac.zip
sudo cp -r AppiumForMac.app /Applications
