from scrapy import log
from scrapy.spider import BaseSpider

class ESpider(BaseSpider):
    name = 'espider'
    allowed_domains = ['ebay.co.uk']
    
    def parse(self, response):
        self.log('blah')

    

