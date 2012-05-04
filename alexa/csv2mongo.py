#!/usr/bin/env python
#coding: UTF-8

import config
from tornado.options import options
import pymongo
import csv
import time_utils
import zipfile
import StringIO

class CSV2Mongo():
    def __init__(self):
        self.datelist = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.datelist
        self.ranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.ranking
        self.time_utils = time_utils.TimeUtils()

#ZipFile instance has no attribute '__exit__'
#↑のエラーが出てwith が使えない..
    def zcat_with(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            return '\n'.join([zip_file.read(filename) for filename in zip_file.namelist()])

    def zcat(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            return '\n'.join([zip_file.read(filename) for filename in zip_file.namelist()])

    def get_csv(self, file_path):
        if (file_path.find(".zip") > 0):
            return StringIO.StringIO(self.zcat(file_path))
        else:
            return open(file_path)

    def get_last_rank(self, domain, today, back_date):
        end = self.time_utils.n_day_ago(today, back_date)
        try:
            query = {"domain" : domain, "date" : end}
            last_data = self.ranking.find_one(query)
            return last_data["rank"]
        except:
            start = self.time_utils.n_day_ago(today, back_date - 7)
            date_range = {"date" : {"$lt" : end, "$gt" : start}}
            query = {"domain" : domain, "date" : date_range}
            try:
                last_data = self.ranking.find(query).sort("date", pymongo.DESCENDING)
                return last_data[0]["rank"]
            except:
                return ""

    def get_some_last_rank(self, domain, rank, today):
        data = {}
        for i in [1, 30]:
            key = "%d days ago" % i
            last_rank = self.get_last_rank(domain, today, i)
            try:
                difference = rank - last_rank
            except:
                difference = "new"
            #値が小さいほどアクセス数が増えている
            data.update({key : difference})
        return data

    def array2mongo(self, array, date):
        self.time_utils.start()
        self.datelist.insert({"date" : date})
        for data in array:
            rank = int(data[0])
            domain = data[1]
            insert_data = {"date" : date, "rank" : rank, "domain" : domain}
            insert_data.update(self.get_some_last_rank(domain, rank, date))
            self.ranking.insert(insert_data)
        self.time_utils.end()

    def csv2mongo(self, data_file_path):
        csvfile = self.get_csv(data_file_path)
        array = csv.reader(csvfile)
        date = self.time_utils.str2date(data_file_path)
        self.array2mongo(array, date)
        return date

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "Usage: python %s config_file_path read_csv_file" % sys.argv[0]
        sys.exit(1)
    config_file_path = sys.argv[1]
    config.setup_options(config_file_path)
    data_file_path= sys.argv[2]
    c = CSV2Mongo()
    c.csv2mongo(data_file_path)
