from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse,urljoin
from urllib.request import urlretrieve
import re
from urllib.robotparser import RobotFileParser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("http://www.musi-cal.com/robots.txt")
rp.read()
______________________________________________________________________________#

class WebSite(object):
    """Contains the information needed to scrape a webSite"""
    def __init__(self,url,body_tag,absolute_url,target_pattern):
        self.url = url
        self.absolute_url = absolute_url
        self.body_tag = body_tag
        self.target_pattern = target_pattern

______________________________________________________________________________#

class Crawler(object):
    """Crawl and scrap information from a WebSite"""
    def get_soup_data (self,url):
        try:
            request = urlopen(url)
        except HTTPError as e:
            print('Unable to establish a connection to the server. Error : ',e)
            return None
        except URLError as e:
            print('Unable to find the url. Error: ',e)
            return None
        try:
            data = bs(request.read(),'html.parser')
        except AttributeError as e:
            print('Unable to get a html. Error: ',e)
            return None

        return data
#______________________________________________________________________________#

    def get_href_links(self,data):
        """
        returns every href value from url, without duplicates
        """
        anchor_tags = data.find_all('a')
        links = list()

        for href in anchor_tags:
            link = href.get('href')

            if (link != None):
                if (link not in links):
                    links.append(link)

        return links
#______________________________________________________________________________#
________________________________________________#

    def get_external_links(self,data,base_url):
        """
        Returns every link that doesn't belongs to the same domain, does return img links
        and other kinds of crap
        """
        domain = urlparse(base_url).scheme +'://'+ urlparse(base_url).netloc
        anchor_tags = data.find_all('a')
        external_links = list()

        if anchor_tags == None:
            return None

        for href in anchor_tags:
            link = href.get('href')
            count +=1
            if (link != None):
                link = urljoin(domain,link)
                if (link not in external_links):
                    if (domain not in link):
                        external_links.append(link)

        return external_links
#______________________________________________________________________________#




# def get_internal_links(data,base_url):
#     """
#     Returns every link that belongs to the same domain, does not return img links
#     and other kinds of crap
#     """
#     domain = urlparse(base_url).scheme +'://'+ urlparse(base_url).netloc
#     anchor_tags = data.find_all('a')
#     internal_links = list()
#
#     if anchor_tags == None:
#         return None
#
#     for href in anchor_tags:
#         link = href.get('href')
#         if (link != None):
#             link = urljoin(domain,link)
#             if (link not in internal_links):
#                 if (link.find(domain) != -1):
#                     internal_links.append(link)
#
#
#     return internal_links
#
# def get_html_data (url):
#     try:
#         request = urlopen(url)
#     except HTTPError as e:
#         print('Unable to establish a connection to the server. Error : ',e)
#         return None
#     except URLError as e:
#         print('Unable to find the url. Error: ',e)
#         return None
#     try:
#         data = bs(request.read(),'html.parser')
#     except AttributeError as e:
#         print('Unable to get a html. Error: ',e)
#         return None
#
#     return data



#wikipedia = WebSite('https://www.wikipedia.org/')
#url = 'https://www.wikipedia.org/'
#testIN = Crawler().get_internal_links(Crawler().get_html_data(url),url)
#testEXT = Crawler().get_external_links(Crawler().get_html_data(url),url)
#print(testIN,'\n','_'*100,testEXT)
