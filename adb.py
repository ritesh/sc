from twisted.enterprise import adbapi
from twisted.internet import reactor

def getstuff():
    """docstring for getstuff"""
    return dbpool.runQuery("SELECT COUNT(*) FROM data")

def printresult(l):
    for item in l:
        print item[0]
def errhandler(l):
    print l
dbpool = adbapi.ConnectionPool("MySQLdb", host='storo', user='ritesh', passwd='6510',db='ritesh' )
getstuff().addCallback(printresult)
reactor.callLater(1,reactor.stop)
reactor.run()
