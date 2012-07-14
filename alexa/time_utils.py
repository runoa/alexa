#!/usr/bin/env python
#coding: UTF-8

import datetime
import re

class TimeUtils():
    def __init__(self):
        self.file = open("log.txt", "w")
    def start(self):
        self.start = datetime.datetime.today()
        self.bef = self.start
        return self.start
    def diff(self):
        d = datetime.datetime.today() - self.bef
        self.bef = datetime.datetime.today()
        return d
    def log(self, key):
        d = datetime.datetime.today() - self.bef
        self.bef = datetime.datetime.today()
        self.file.writelines("%s : %s\n" % (key, d))
    def end(self):
        time = datetime.datetime.today() - self.start
        return time
    def str2date(self, str):
        p = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
        m = p.search(str)
        return datetime.datetime.strptime(m.group(), "%Y-%m-%d")
    def n_day_ago(self, date, n):
        return date - datetime.timedelta(0, n * 24 * 3600)

if __name__ == "__main__":
    t = TimeUtils()
    test = {"aaa" : 10}
    print t.start()
    for i in range(100):
        t.log("%d : %s" % (i, test))
    print t.end()
