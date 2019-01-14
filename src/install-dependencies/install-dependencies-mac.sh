#!/bin/sh
brew update
brew install python || true
brew install brew-cask || true
brew cask install google-chrome chromedriver || true
brew install flex bison || true
pip install selenium pysocks urllib3 requests
