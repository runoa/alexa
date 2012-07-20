#!/usr/bin/env python
#coding: utf-8

import tornado.ioloop
import tornado.web
import pymongo
import os.path
import urllib
import datetime
import time_utils
import config
from tornado.options import options

NAV_RANGES = [
    (1, 20),
    (21, 50),
    (51, 100),
    (101, 200),
    (201, 300),
    (301, 400),
    (401, 500),
]

def get_lastday(col):
    datelist = col.find().sort("date", pymongo.DESCENDING)
    lastday = datelist[0]["date"]
    return lastday

#newには1daysagoがないから気をつけてね
#最初はdaily_data["1 days ago"]も計算してたんだけどやめた
def _get_ranking(daily_data, point_data):
    alexa_url = "http://www.alexa.com/siteinfo/"
    return {
        "daily_rank"    : daily_data["rank"],
        "daily_diff"    : "---",
        "daily_domain"  : daily_data["domain"],
        "daily_link"    : alexa_url + daily_data["domain"],

        "point_rank"    : point_data["original rank"],
        "point_diff"    : point_data["1 days ago"],
        "point_domain"  : point_data["domain"],
        "point_link"    : alexa_url + point_data["domain"]
    }

def get_ranking(ranking, pointranking, newrank, rank_range, date):
    daily_ranking = ranking.find({"date" : date, "rank" : rank_range})
    point_ranking = pointranking.find({"date" : date, "rank" : rank_range})
    new_ranking = newrank.find({"date" : date, "rank" : rank_range})
    rank_list = []
    #newも一緒にzipしたら、要素が少なくてダメになっちゃった
    for (daily_data, point_data) in zip(daily_ranking, point_ranking):
        rank_list.append(_get_ranking(daily_data, point_data))
    return rank_list

def _create_nav(start, end, date):
    return {u'link': u'/?%s' % urllib.urlencode({'date': date, 'start_rank':str(start), 'end_rank':str(end)}), u'name':u'%d-%d 位'%(start, end)}

def create_nav_list(ranges, date):
    return [_create_nav(start, end, date) for (start, end) in ranges]

def _create_day(date):
    return {u'link': u'/?%s' % urllib.urlencode({'date': date, 'start_rank':str(1), 'end_rank':str(20)}), u'name':date.strftime('%m/%d')}

def last_ndays(date=datetime.date.today()):
    return [date - datetime.timedelta(days=days) for days in range(-4, 4)]

def create_days(date):
    return [_create_day(d) for d in last_ndays(date)]

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.datelist = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.datelist
        self.ranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.ranking
        self.pointranking = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.pointranking
        self.newrank = pymongo.Connection(options.mongodb_host, options.mongodb_port).alexa.newrank
        self.time_utils = time_utils.TimeUtils()

    def get(self):
        try:
            date = self.time_utils.str2date(self.get_argument("date"))
            start_rank = int(self.get_argument("start_rank"))
            end_rank = int(self.get_argument("end_rank"))
        except:
            date = get_lastday(self.datelist)
            start_rank = 1
            end_rank = 20
        rank_range = {"$gte" : start_rank, "$lte" : end_rank}

        ranking = get_ranking(self.ranking, self.pointranking, self.newrank, rank_range, date)
        nav_list = create_nav_list(NAV_RANGES, date)
        last_seven_days = create_days(date)
        last_seven_days.reverse()
        self.render("template.html", date=date, ranking=ranking, nav_list=nav_list, days=last_seven_days)

def main(config_file_name='config.ini'):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': static_dir}),
    ])
    config.setup_options(config_file_name)
    application.listen(options.tornado_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: python %s config_file_path" % sys.argv[0]
        sys.exit(0)
    main(sys.argv[1])
