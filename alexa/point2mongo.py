#!/usr/bin/env python
#coding: UTF-8

import config
from tornado.options import options
import pymongo
import time_utils

class Point2Mongo():
    def __init__(self):
        self.ranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.ranking
        self.pointranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.pointranking
        self.time_utils = time_utils.TimeUtils()

    def get_rank(self, domain, date, n_days_ago):
        days_ago = self.time_utils.n_day_ago(date, n_days_ago)
        try:
            query = {'date' : days_ago, 'domain' : domain}
            days_ago_data = self.ranking.find_one(query)
            return days_ago_data['rank']
        #指定された日を検索して、
        #見つからなければ更に1週間遡る
        except:
            weeks_ago = self.time_utils.n_day_ago(date, n_days_ago + 7)
            date_range = {'$lt' : days_ago, '$gte' : weeks_ago}
            query = {'date' : date_range, 'domain' : domain}
            try:
                weeks_ago_data = self.ranking.find(query).sort('date', pymongo.DESCENDING)
                return weeks_ago_data[0]['rank']
            except:
                return 0;

    def get_diff(self, rank, xdays_ago_rank, max):
        return rank - max if xdays_ago_rank == 0 else rank - xdays_ago_rank

    def calc_point(self, rank, days_ago, weeks_ago, months_ago):
        day = self.get_diff(rank, days_ago, 1000000)
        week = self.get_diff(rank, weeks_ago, 1000000)
        month = self.get_diff(rank, months_ago, 1000000)
        val = 1000*day + 1000 * week + 1 * month
        point = float(val) / rank ** 1.6
        return point

    def rank2point(self, date):
        pointranking = []
        rank_range = {'$lte' : 100000, '$gte' : 1000}
        for data in self.ranking.find({'date' : date, 'rank' : rank_range}):
            domain = data['domain']
            rank = data['rank']
            days_ago = self.get_rank(domain, date, 1)
            weeks_ago = self.get_rank(domain, date, 7)
            months_ago = self.get_rank(domain, date, 30)
            point = self.calc_point(rank, days_ago, weeks_ago, months_ago)
            pointranking.append({'domain' : domain, 'point' : point, 'rank' : rank, '1 days ago' : self.get_diff(rank, days_ago, 1000000)})
        return pointranking

    def cmp_diff(self, x, y):
        return 1 if x['point'] > y['point'] else -1

    def insert2mongo(self, pointranking, date):
        for i,d in enumerate(pointranking):
            query = {'date' : date, 'domain' : d['domain'], 'point' : d['point'], 'rank' : i+1, 'original rank' : d['rank'], '1 days ago' : d['1 days ago']}
            self.pointranking.insert(query)

    def point2mongo(self, date):
        pointranking = self.rank2point(date)
        pointranking.sort(self.cmp_diff)
        self.insert2mongo(pointranking, date)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'Usage: python %s config_file_path date' % sys.argv[0]
        sys.exit(1)
    config_file_path = sys.argv[1]
    config.setup_options(config_file_path)
    t = time_utils.TimeUtils()
    date = t.str2date(sys.argv[2])
    p2m = Point2Mongo()
    p2m.point2mongo(date)
