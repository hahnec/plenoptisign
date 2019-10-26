#!/bin/bash

# install additional tkinter package in ubuntu
sudo apt install python3-tk
sudo pip3 install numpy==1.16.2 # solves issue in bundling with pyinstaller

# rmeove build directories
sudo rm -rf build/
sudo rm -rf dist/

# run pyinstaller with provided options
pyinstaller3.cp plenoptisign/gui/gui_app.py \
    	--onefile \
	--noconsole \
	--name=plenoptisign \
	--icon=plenoptisign/gui/misc/circlecompass_1055093_24x24.gif \
	--add-data=./docs/build/html/:./docs/build/html/ \
	--add-data=plenoptisign/gui/misc/circlecompass_1055093_24x24.gif:./misc/

# change distribution folder ownership to user
sudo chown -R chris: ./dist

# set absolute path to icon file
gio set -t string ./dist/plenoptisign 'metadata::custom-icon' 'file:/home/chris/MyRepos/plenoptisign/gui/misc/circlecompass_1055093_24x24.gif'
