#!/bin/sh
home=$HOME/alexa
month=2012-07-
source $HOME/.bash_profile
workon alexa
date
for date in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
do
    echo $month$date
    time python $home/alexa/csv2mongo.py $home/config.ini $home/alexa/data/$month$date.csv
    time python $home/alexa/point2mongo.py $home/config.ini $month$date
    date
done
