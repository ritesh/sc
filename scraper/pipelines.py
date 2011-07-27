# Define your item pipelines here
#
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
import time
import sqlite3

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

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.__insertdata, item, spider.name)
        query.addErrback(self.handle_error)
        return item

    def __insertdata(self, tx, item, spidername):
        for img in item['images']:
            log.msg(type(img['url']))
            tx.execute("select * from data where url = %s", (img['url']))
            result = tx.fetchone()
            if result:
                log.msg("Item has been stored previously", level=log.DEBUG)
            else:
                tx.execute(\
                        "insert into data(url, localpath, checksum, created, spidername)"
                        "values (%s, %s, %s, %s, %s)",
                        (img['url'],
                         img['path'],
                         img['checksum'],
                         time.time(),
                         spidername)
                        )
                log.msg("Item stored in db", level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
class DbSqlitePipeline(object):
    def __init__(self):
        """Initialize"""
        self.__dbpool = adbapi.ConnectionPool('sqlite3',
                database='/users/mscit/1006510k/scraper/db/sqlite.db',
                check_same_thread=False)
    def shutdown(self):
        """Shutdown the connection pool"""
        self.__dbpool.close()
    def process_item(self,item,spider):
        """Process each item process_item"""
        query = self.__dbpool.runInteraction(self.__insertdata, item, spider)
        query.addErrback(self.handle_error)
        return item
    def __insertdata(self,tx,item,spider):
        """Insert data into the sqlite3 database"""
        spidername=spider.name
        for img in item['images']:
            tx.execute("select * from data where url = ?", (img['url'],))
            result = tx.fetchone()
            if result:
                log.msg("Already exists in database", level=log.DEBUG)
            else:
                tx.execute(\
                        "insert into data(url, localpath, checksum, created, spidername) values (?,?,?,?,?)",(
                            img['url'],
                            img['path'],
                            img['checksum'],
                            time.time(),
                            spidername)
                        )
                log.msg("Item stored in db", level=log.DEBUG)
    def handle_error(self,e):
        log.err(e)
