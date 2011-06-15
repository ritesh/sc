from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import re
from scraper.items import MyImageItem

class GlaSpider(BaseSpider):
    """A simple spider for gla.ac.uk"""
    name = "gla.ac.uk"
    allowed_domains = ["gla.ac.uk"]
    start_urls = ["http://www.gla.ac.uk"]
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        images = hxs.select('//img/@src').extract()
        for image in images:
            item = MyImageItem()
            item['image_urls']=[]
            if re.match('^http+', image):
                imgurl = image
            #If we have a relative url, append the site name to make it
            #absolute
            else:
                imgurl = response.url + image
            item['image_urls'].append(imgurl)
            yield item

