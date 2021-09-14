from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wikipedia.items import Article
import scrapy
from bs4 import BeautifulSoup
import bs4
import re

class ArticleSpider(CrawlSpider):
    name='article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/COVID-19_pandemic']
    rules = (Rule(LinkExtractor(allow=r'(/wiki/)((?!:).)*$'), callback = 'parser'),)


    def parser (self,response):
        def parse_tags(tag):
            """
            Discriminates the unnecessary tags
            """
            banned_classes = ['thumbcaption','reference','infobox',['mw-empty-elt'],'shortdescription nomobile noexcerpt noprint searchaux',['toclimit-3'],['thumb', 'tright'],['thumb', 'tleft']
                                ,'toc','toctitle']
            banned_names = ['style','table','ul','sup']

            if (tag.attrs.get('class',' ') in banned_classes or tag.attrs.get('role',' ')=='note' or 'style' in tag.attrs.keys() or tag.name in banned_names):
                return False

            for parent in tag.parents:
                if (parent.attrs.get('class',' ') in banned_classes or parent.attrs.get('role',' ')=='note' or 'style' in parent.attrs.keys() or parent.name in banned_names):
                    return False

            return True

        #content = Article()
        #content['url'] = response.url
        #content['article_title'] = response.css('h1::text').get()
        data = BeautifulSoup(response.text,'html.parser')
        #retrieve the headers and text underneat
        text_body = data.select('#mw-content-text > div.mw-parser-output')[0]
        print('harren')
        text = text_body.find_all(lambda tag : parse_tags(tag))
        Fathers_retrieved = list()
        current_headers = ['From url: '+response.url+'\n'+'Article Title: '+response.css('h1::text').get()]
        key_words = ('George Floyd','United States','Trump')
        Match_paragraph = ''
        retrieve_text = False
        headers = ''
        for t in text:
            retrieve = True
            #find the headers and classify them acording to the table that is being read
            if (t.get('class',' ') == ['mw-headline']):
                #When a word match is found we have to retrieve all the text until
                #we find a header, retrieve_text sets to true so that the next time a header is found it
                #retrieves the text and continues searching
                if (retrieve_text):
                    #create printable headers from our list current_headers

                    for head in current_headers:
                        headers +=head+'\n'

                    print(headers+'\n',Match_paragraph)
                    #we repeat code because we have to break on this special case (there might be an simpler way to do this)
                    N_header = int(t.parent.name[1])
                    current_headers = current_headers[0:N_header-1]
                    current_headers.append(t.get_text())
                    Match_paragraph = ''
                    retrieve_text = False
                    headers =''
                    continue
                #repeated code for regular cases
                N_header = int(t.parent.name[1])
                current_headers = current_headers[0:N_header-1]
                current_headers.append(t.get_text())
                Match_paragraph = ''
            #since we use .get_text() it is only necessary to get text from the
            #parents, there are simpler ways to do this
            for dad in t.parents:
                if(dad in Fathers_retrieved):
                    retrieve = False
                    break

            if (retrieve):
                Fathers_retrieved.append(t)
                if (re.match('h[1-9]',t.name)):
                    continue

                Match_paragraph += t.get_text() +'\n'

                for word in key_words:
                    if (word in t.get_text()):
                        retrieve_text = True
                        headers += 'Keyword: '+word+'\n'
