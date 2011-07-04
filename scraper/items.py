# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
# Default class to handle scraped items


class ScrapedItem(Item):
    title = Field()
    link = Field()
    desc = Field()
#Class to store image data
#image_urls contains urls of images to be downloaded
#images stores the location of the downloaded images
class MyImageItem(Item):
    image_urls = Field()
    images = Field()

