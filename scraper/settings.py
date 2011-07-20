# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scraper'
BOT_VERSION = '1.0'
LOG_LEVEL="ERROR"
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
DEFAULT_ITEM_CLASS = 'scraper.items.ScraperItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
#Fake user agent. This is a grey area! 
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline',
'scraper.pipelines.DbSqlitePipeline']
IMAGES_STORE = '/users/mscit/1006510k/images/scraper/'
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

