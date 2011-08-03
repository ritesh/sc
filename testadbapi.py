from twisted.enterprise import adbapi
from twisted.internet import reactor
import MySQLdb.cursors
dbpool = adbapi.ConnectionPool("MySQLdb", 
       host = "storo",
       db = "ritesh",
       user = "ritesh",
       passwd = "6510",
       cursorclass = MySQLdb.cursors.DictCursor,
       charset = "UTF8",
       use_unicode=True)
def _getstuff(txn, spidername):
    txn.execute("SELECT COUNT(*) FROM data WHERE spidername = ?", spidername)
    result = txn.fetchall()
    if result:
        return result[0][0]
    else:
        return None
def getstuff(spidername):
    return dbpool.runInteraction(_getstuff, spidername)
def printresult(count):
    if count != None:
        print count, "is the count"
    else:
        print "Nothing!"
def handlerror():
    print "Whoops"
getstuff("gspider").addCallback(printresult).addErrback(handlerror)
reactor.run()
