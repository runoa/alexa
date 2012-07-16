#!/bin/sh
source $HOME/.bash_profile
workon alexa
python $HOME/alexa/alexa/getCSV.py $HOME/alexa/config.ini
