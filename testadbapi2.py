# Define your item pipelines here
#
from twisted.enterprise import adbapi
import MySQLdb.cursors

# Database storage pipeline. Adapted from Scrapy docs
# Connects to a MySQL database via a connection pool to allow
# for non blocking DB access

class DbPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                host='storo',
                db='ritesh',
                user='ritesh',
                passwd='6510',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
                )

    def process_item(self,spider):
        return self.dbpool.runInteraction(self.__insertdata, spider).addErrback(self.handle_error)

    def __insertdata(self, tx, spidername):
        tx.execute("select count(*) from data")
        result = tx.fetchall()
        if result:
            print "Found something!"
        else:
            print "Nothing!"

    def handle_error(self, e):
        print str(e)
if __name__== '__main__':
    a = DbPipeline()
    a.process_item("gspider")
