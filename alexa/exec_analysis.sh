#!/bin/sh
source ~/.virtualenvs/alexa/bin/activate
date
for date in 03 04 05
do
    echo 2012-06-$date
    time python csv2mongo.py ../config.ini data/2012-06-$date.csv
    time python point2mongo.py ../config.ini 2012-06-$date
    date
    purge
done
