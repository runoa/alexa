#!/bin/sh
source $HOME/.bash_profile
workon alexa
python $HOME/alexa/alexa/view.py $HOME/alexa/config.ini
