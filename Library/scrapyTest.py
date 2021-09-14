import scrapy

class test(scrapy.Spider):
    """docstring for test."""
    name = 'test'
    def start_requests(self):
        return [scrapy.Request(url="",callback=self.parse)]

    def parse(self,response):
        print(response.text)

#______________________________________________________________________________#

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = ''
    allowed_domains = ['']
    start_urls = ['']
    rules = [Rule(LinkExtractor(),callback='', follow=True)]
