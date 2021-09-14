# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Content(scrapy.Item):
    """
    Stories, poems, etc...
    """
    url = scrapy.Field()
    links = scrapy.Field()
    type = scrapy.Field()
    text = scrapy.Field()
    title = scrapy.Field()
    
