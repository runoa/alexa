#!/bin/sh
home=$HOME/alexa
month=2012-07-
source $HOME/.bash_profile
workon alexa
date
for date in 19
do
    echo $month$date
    time python $home/alexa/csv2mongo.py $home/config.ini $home/alexa/data/$month$date.csv
    time python $home/alexa/point2mongo.py $home/config.ini $month$date
    date
done
