from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wikipedia.items import Article
from string import whitespace

class ArticleSpider(CrawlSpider):
    """docstring for ."""

    name = 'articles'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/COVID-19_pandemic']
    rules = (Rule(LinkExtractor(allow=r'(/wiki/)((?!:).)*$'), callback = 'parse'),)

    def parse (self,response):

        #content = Article()
        #content['url'] = response.url
        #content['article_title'] = response.css('h1::text').get()
        table = response.css('#mw-content-text > div.mw-parser-output')
        link_file = open('Links.txt','a')
        link_file.write('from url: '+response.url+'\n')
        table = table.xpath('descendant')

        for desc in table:
            #Cut every element that we don't want to retrieve
            if (desc.attrib['class'] in ['thumbcaption','reference','infobox'] or desc.attrib['role'] == 'note'):
                continue

            text = desc.xpath('./text()').get()
            if (text == None):
                 continue
            try:
                link_file.write(text)
            except:
                continue
