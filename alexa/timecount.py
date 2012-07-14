import datetime

class Timecount():
    def start(self):
        self.start = datetime.datetime.today()
        self.bef = self.start
        return self.start
    def diff(self):
        d = datetime.datetime.today() - self.bef
        self.bef = datetime.datetime.today()
        return d
    def end(self):
        time = datetime.datetime.today() - self.start
        return time

if __name__ == "__main__":
    t = Timecount()
    print t.start()
    for i in range(100):
        print t.diff()
    print t.end()
