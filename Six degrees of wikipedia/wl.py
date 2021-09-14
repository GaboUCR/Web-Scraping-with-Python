from lib import WebSite,Crawler
from bs4 import BeautifulSoup as bs
import re
import random
from urllib.parse import urljoin
import time

#______________________________________________________________________________#
class WikiCrawler(Crawler):
    """Crawls and scraps links on wikipedia"""
    def get_wiki_links(self,url):

        data = self.get_html_data(url)
        links = list()
        try:
            for link in data.find('div', {'id':'bodyContent'}).find_all('a',href = re.compile('^(/wiki/)((?!:).)*$')):
                if 'href' in link.attrs:
                    links.append(urljoin('https://en.wikipedia.org',link.attrs['href']))
        except:
            print('error retrieving ',url,'links')
            return None

        return links
#______________________________________________________________________________#
    def get_link_path(self,start,end):
        """
        Gets the fastest paths following href links from a wikipedia page
        with url Start to the page with url end.

        Parameters:
            start : string
            end : string
        return:
            path : list
                list with the fastest path in order.
        """
        path_not_found = True
        paths = [[start]]
        requests = 0
        paths_found = 0
        time_running = time.time()

        while path_not_found:
            #retrieve every link from the url.
            c_paths = paths.copy()
            for path in c_paths:
                last_path = paths.pop(0)
                links = self.get_wiki_links(last_path[-1])
                requests +=1
                time.sleep(1)
                print('requests: ',requests)
                print('paths found: ', paths_found)
                current_time = time.time()
                print('time running:', (current_time - time_running)/3600 ,'hours' )
                #check if end is in there
                if (links != None):
                    if (links != start):
                        if(end not in links):
                            #make a list of lists(paths) with each of those elements
                            for link in links:
                                new_path = last_path.copy()
                                new_path.append(link)
                                paths.append(new_path)
                                paths_found +=1
                    #what we do when the right path is found
                        else:
                            last_path.append(end)
                            return last_path

#____________________________________________________________________________#


def main():
    start = 'https://en.wikipedia.org/wiki/Kevin_Bacon'
    end = 'https://en.wikipedia.org/wiki/Hundred_Years%27_War' #'https://en.wikipedia.org/wiki/Eric_Idle'
    crawler = WikiCrawler()
    degrees = crawler.get_link_path(start,end)
    print('Best Path: ','\n',degrees)
main()
#print(len(get_wiki_links('https://en.wikipedia.org')))
