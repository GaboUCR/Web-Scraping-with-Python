import scrapy
from items import Content
from bs4 import BeautifulSoup
from TextLib import extract_text,clean_string,rank_text
import re
from urllib.request import urlopen
import time
from InternetLib import get_internal_links
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# class AmericanLiterature(scrapy.Spider):
#     """
#
#     """
#     name = 'AmericanLiterature'
#     def start_requests(self):
#         return [scrapy.Request(url='https://americanliterature.com/author/robert-browning/poem/youll-love-me-yet',callback=self.parse)]


class AmericanLiterature(CrawlSpider):
    name = 'AmericanLiterature'
    allowed_domains = ['americanliterature.com']
    start_urls = ['https://americanliterature.com/author/nathaniel-hawthorne/short-story/david-swan']
    rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse',follow=True)]

    def parse(self,response):
        content = Content()
        base_url = 'https://americanliterature.com'
        data = BeautifulSoup(response.text,'html.parser')
        print('getting : ',response.url)
        time.sleep(5)
        content_keys = ('/short-story/','/poem/','/book/')
        #determine if it is a Content or a Transition
        type = ""
        print('banano')
        for key in content_keys:
            if (key in response.url):
                if (key =='/short-story/'):
                    type = 'ShortStory'
                if (key == '/poem/'):
                    type = 'Poem'
                if (key == '/book/'):
                    type = 'Book'
        #Getting raw data from stories and poems
        if (type in ['ShortStory','Poem']):
            body = data.find('div',attrs={'class':['jumbotron'],'itemtype':'https://schema.org/'+type})
            content['url'] = response.url
            content['links'] = get_internal_links(data,base_url)
            content['type'] = type
            content['title'] = body.find('h1',itemprop = 'name').get_text() +" by "+ body.find('a',itemprop = 'author').get_text()
            #Remove every tag a tag and every father of an a tag.
            content['text'] = extract_text(body,('a',))
        #getting raw data from books
        elif (type == 'Book' and response.url.endswith('summary')):
            body = data.find('div',attrs={'class':['jumbotron'],'itemtype':'https://schema.org/'+type})
            content['url'] = response.url
            content['links'] = get_internal_links(data,base_url)
            content['type'] = type
            content['title'] = body.find('h1',itemprop = 'name').get_text() +" by "+ body.find('a',href = re.compile('^/author/.+')).get_text()
            #Selects the links to every chapter and creates a dictionary linking their names to the text
            author = clean_string(body.find('a',href = re.compile('^/author/.+')).get_text())
            name = clean_string(body.find('h1',itemprop = 'name').get_text())
            chapters_links = [base_url+anchor.attrs.get('href',"") for anchor in body.find_all('a',href = re.compile('^/author/'+author+'/book/'+name))]
            #we have to make a request for every chapter get the text and save it as a dictionary
            text_dict = dict()
            for chapter in chapters_links:
                response = BeautifulSoup(urlopen(chapter),'html.parser')
                time.sleep(3)
                body = response.find('div',class_ = 'jumbotron')
                title = body.find(re.compile('h[3-9]')).get_text()
                text_dict.update({title:extract_text(body,('a',))})
                content['text'] = text_dict
        else:
            #This is a Transition page
            content['url'] = response.url
            content['links'] = get_internal_links(data,base_url)
            content['type'] = 'Transition'


        return content
