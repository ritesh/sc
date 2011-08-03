from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scraper.items import MyImageItem
import urlparse
import re
class GSpider(BaseSpider):
    name = 'gspider'
    allowed_domains = ['gumtree.co.uk', 'gumtree.com']
    def start_requests(self):
        a = open('short.txt','r').readlines()
        return [Request(x.strip()) for x in a]


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        images = hxs.select('//img/@src').extract()
        for image in images:
            if re.match('(.*)/image/big/(.*)\.jpg', image, re.IGNORECASE):
                item = MyImageItem()
                item['image_urls'] = []
                if re.match('^http+', image):
                    imgurl = image
                else:
                    imgurl = urlparse.urljoin(response.url, image)
                item['image_urls'].append(imgurl)
                yield item
