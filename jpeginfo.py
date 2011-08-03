# A script that gets JPEG infor about previous images
from twisted.enterprise import adbapi
import MySQLdb.cursors
import time

# Database storage pipeline. Adapted from Scrapy docs
# Connects to a MySQL database via a connection pool to allow
# for non blocking DB access
class JpegInfo(object):
    """A class that gets jpeginfo and adds it to the database"""
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
        host = 'storo',
        db = 'ritesh',
        user = 'ritesh',
        passwd = '6510',
        cursorclass = MySQLdb.cursors.DictCursor,
        charset = 'utf8',
        use_unicode = True
        )
        self.getListFromDb()


    def getListFromDb(self):
        """get list of images from the database"""
        f = open('lastaccessed.dat', 'r')
        self.processList(f.read()).addCallback(self.printResult)
        f.close()

    def processList(self, lastread):
        return self.dbpool.runInteraction(self.__runDbQuery, lastread)
    def __runDbQuery(self, tx, lastread):
        tx.execute("SELECT COUNT(*) FROM data")
        result = tx.fetchall()
        if result:
            return result
        else:
            return None
    def printResult(results):
        if results != None:
            print results
        else:
            print "Nothing here!"

    def __handle_error(self, e):
        print e

if __name__ == '__main__':
    JpegInfo()


