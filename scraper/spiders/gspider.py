from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
import urlparse
from scraper.items import MyImageItem
from scrapy.log import log

class GSpider(CrawlSpider):
    """A simple spider for gumtree"""
    name = "gspider"
    allowed_domains = ["gumtree.com", "thegumtree.com","glasgow.gumtree.com"]
    start_urls = ["http://www.gumtree.com/cgi-bin/list_postings.pl?search_terms=&search_location=Glasgow&ubercat=1"]
    rules = (
            Rule(SgmlLinkExtractor(allow=("/", )),callback='parse_data'),
            )


    def parse_data(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        images = hxs.select('//img/@src').extract()
        for image in images:
            if re.match('(.*)/image/big/(.*)\.jpg', image):
                item = MyImageItem()
                item['image_urls']=[]
                if re.match('^http+', image):
                    imgurl = image
                #If we have a relative url, append the site name to make it
                #absolute
                else:
                    imgurl = urlparse.urljoin(response.url,image)
                print imgurl 
                item['image_urls'].append(imgurl)
                yield item
        for url in hxs.select('//a/@href').extract():
            if re.match('^http+', url):
               yield Request(url, callback=self.parse_data)
            else:
               yield Request(urlparse.urljoin(url, response.url), callback=self.parse_data)


