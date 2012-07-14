#!/usr/bin/env python
#coding: UTF-8

import config
from tornado.options import options
import pymongo
import time_utils

class Point2Mongo():
    def __init__(self):
        self.ranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.ranking
        self.pointrank = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.pointrank
        self.time_utils = time_utils.TimeUtils()

    def calc_point(self, rank, days_ago, weeks_ago, months_ago):
        day = days_ago if days_ago != "new" else (rank - 1000000) / 10
        week = weeks_ago if weeks_ago != "new" else (rank - 1000000) / 10
        month = months_ago if months_ago != "new" else (rank - 1000000) / 10
        val = 1000*day + 1000 * week + 1 * month
        point = float(val) / rank ** 1.6
        return point

    def rank2point(self):
        pointrank = []
        rank_range = {"$lte" : 100000, "$gte" : 1000}
        for data in self.ranking.find({"date" : date, "rank" : rank_range}):
            domain = data["domain"]
            rank = data["rank"]
            days_ago = data["1 days ago"]
            try:
                weeks_ago = data["7 days ago"]
            except:
                weeks_ago = 0
            months_ago = data["30 days ago"]
            point = self.calc_point(rank, days_ago, weeks_ago, months_ago)
            pointrank.append({"domain" : domain, "point" : point, "rank" : rank, "1 days ago" : days_ago})
        return pointrank

    def cmp_diff(self, x, y):
        if x["point"] == "new":
            return 1
        elif y["point"] == "new":
            return -1
        else:
            return 1 if x["point"] > y["point"] else -1

    def insert2mongo(self, pointrank, date):
        for i,d in enumerate(pointrank):
            query = {"date" : date, "domain" : d["domain"], "point" : d["point"], "rank" : i+1, "original rank" : d["rank"], "1 days ago" : d["1 days ago"]}
            self.pointrank.insert(query)

    def point2mongo(self, date):
        pointrank = self.rank2point()
        pointrank.sort(self.cmp_diff)
        self.insert2mongo(pointrank, date)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "Usage: python %s config_file_path date" % sys.argv[0]
        sys.exit(1)
    config_file_path = sys.argv[1]
    config.setup_options(config_file_path)
    t = time_utils.TimeUtils()
    date = t.str2date(sys.argv[2])
    p2m = Point2Mongo()
    p2m.point2mongo(date)
