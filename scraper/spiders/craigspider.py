from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
import urlparse
from scraper.items import MyImageItem
from scrapy.log import log

class CraigSpider(CrawlSpider):
    """docstring for CraigSpider"""
    name = "craigslist"
    allowed_domains = ["london.craigslist.co.uk", "images.craigslist.com"]
    start_urls = ["http://london.craigslist.co.uk/"]
    rules = (Rule(SgmlLinkExtractor(allow=("/", )), callback='parse_data'),)
    categories = re.compile('^http(.*)\/[A-Za-z]{3}/[A-Za-z]+')
    htmlpages = re.compile('^http(.*)html$')
    searchpage = re.compile('^http(.*)\/search\/(.*)')

    def parse_data(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        images = hxs.select('//img/@src').extract()
        for image in images:
            if re.match('(.*)craigslist(.*)\.jpg', image):
                item = MyImageItem()
                item['image_urls']=[]
                if re.match('^http+', image):
                    imgurl = image
                else:
                    imgurl = urlparse(response.url, image)
                item['image_urls'].append(imgurl)
                yield item
        for url in hxs.select('//a/@href').extract():
            if self.categories.match(url) or self.htmlpages.match(url) or self.searchpage.match(url):
                yield Request(url, callback=self.parse_data)


