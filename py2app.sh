#!/bin/bash

# remove build and dist folder
sudo rm -rf build dist

# generate MacOSX app
sudo python ./setup.py py2app || sudo python3 ./setup.py py2app

# grant write privileges to config file
sudo chmod -R 666 ./dist/plenoptisign.app/Contents/Resources/cfg/cfg.json

# copy docs folder to app bundle
cp -r ./docs/build/html ./dist/plenoptisign.app/Contents/Resources/docs/build/html