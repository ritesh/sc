# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
import time
class ScraperPipeline(object):
    def process_item(self, item, spider):
        print "Entered scraperpipeline"
        return item
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
        tx.execute("select * from sites where url = %s", (item['url'][0],))
        result = tx.fetchone()
        if result:
            log.msg("Stored already in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute(\
                    "insert into sites(name, url, description, created) "
                    "values (%s, %s, %s, %s)",
                    (item['name'][0],
                     item['url'][0],
                     item['description'][0],
                     time.time())
                    )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
    def handle_error(self, e):
        log.err(e)
