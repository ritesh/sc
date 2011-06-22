from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
import urlparse
from scraper.items import MyImageItem
from scrapy.log import log

class GlaSpider(CrawlSpider):
    """A simple spider for gla.ac.uk"""
    name = "anonspider"
    allowed_domains = ["gla.ac.uk"]
    start_urls = ["http://www.dcs.gla.ac.uk/~tws/"]
    rules = (
            Rule(SgmlLinkExtractor(allow=("/", ))),
            Rule(SgmlLinkExtractor(allow=('(.*)\.html$', )), callback='parse_data'),
            )


    def parse_data(self, response):
        self.log('Entering the data parser!')
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
                imgurl = urlparse.urljoin(response.url,image)
            print imgurl 
            item['image_urls'].append(imgurl)
            yield item

