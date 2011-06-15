from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class GlaSpider(BaseSpider):
    """A simple spider for craigslist"""
    name = "craigslist.org"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://www.craigslist.org"]
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        filename = response.url.split("/")[-2]
        open('temp.txt','wb').write(response.body)
