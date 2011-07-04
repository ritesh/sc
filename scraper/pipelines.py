# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
import time
# Database storage pipeline. Adapted from Scrapy docs
# Connects to a MySQL database via a connection pool to allow
# for non blocking DB access

class DbPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', 
                db='scraper',
                user='root',
                passwd='pa55w0rd',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
                )

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.__insertdata, item)
        query.addErrback(self.handle_error)
        return item

    def __insertdata(self, tx, item):
        for img in item['images']:
            tx.execute("select * from gla where url = %s", (img['url'],))
            result = tx.fetchone()
            if result:
                log.msg("Stored already", level=log.DEBUG)
            else:
                tx.execute(\
                        "insert into gla(url, localpath, checksum, created) "
                        "values (%s, %s, %s, %s)",
                        (img['url'],
                         img['path'],
                         img['checksum'],
                         time.time())
                        )
                log.msg("Item stored in db", level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
