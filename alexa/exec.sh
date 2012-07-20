#!/bin/sh
source $HOME/.bash_profile
workon alexa

date
date=`date +"%Y-%m-%d"`
home=$HOME/alexa
file=`python $home/alexa/getCSV.py $home/config.ini`
python $home/alexa/csv2mongo.py $home/config.ini $file
python $home/alexa/point2mongo.py $home/config.ini $date
date
