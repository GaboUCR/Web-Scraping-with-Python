from Libselenium import WebSite,Crawler,KeyUrl
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
from multiprocessing import Process,Queue

def read_csv():
    with open('lawers.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (row == []):
                continue
            if (row[2] == 'N/a'):
                continue
            print(row[2])
            line_count +=1


class IsoCrawler(Crawler):

    def scrape_page_process (self,new_urls,request_urls,page_content,flawed_urls,to_search):
        #initialize process by sending links on starting_urls
        new_urls.put(self.web_site.starting_urls.copy())
        #initialize browser
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        if (self.web_site.tor):
            chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        driver = webdriver.Chrome(options=chrome_options)

        while 1:
            if (not request_urls.empty()):
                for get_url in request_urls.get().copy():
                    if (get_url.type == 'main'):
                        for search in to_search:
                            driver.get(get_url.url)
                            driver.find_element_by_id('addressOrPostalCode').send_keys(search)
                            driver.find_element_by_id('member-search-submit').click()
                            time.sleep(2)
                            #look for every lawer link
                            while 1:
                                try:
                                    driver.find_element_by_css_selector('button.show-more-button.hide-for-print').click()
                                    time.sleep(3)
                                except:
                                    print('no more results')
                                    break

                            lawers_web = driver.find_elements_by_css_selector('#member-search-results > div > div.cell.auto > div.grid-x.grid-margin-x > div.cell.small-8.small-order-1.large-order-1.large-3.member-listing-name > span > a')
                            #iterate over each lawyer
                            lawers = [lawer.get_attribute('href') for lawer in lawers_web]
                            to_send = list()
                            for lawer in lawers:
                                to_send.append(KeyUrl(lawer,'profile'))

                            get_url.done = True
                            to_send.append(get_url)
                            new_urls.put(to_send)
                            
                    if(get_url.type == 'profile'):
                        info = driver.find_elements_by_css_selector(self.web_site.content_box_tag)
                        profile = self.get_text_content(info,{'url':get_url.url})
                        #set ground rules for profile to know if we got an error
                        if (len(profile) < 3):
                            get_url.err_message = 'Missing field'
                            flawed_urls.put(get_url)
                            continue
                        page_content.put(profile)

            else:
                time.sleep(0.1)

        driver.close()
        return content


#
# with open('lawers.csv', mode='w') as lawers_file:
#     fieldnames = ['name','last name','Email','Area of Law','Business Name','Phone','Business Address']
#     writer = csv.DictWriter(lawers_file, fieldnames=fieldnames)
#     writer.writeheader()


absolute_url = 'https://www.lso.ca/'

content_box_tag = '#content-wrapper > div.tps-two-column-wrapper > section > div > div.grid-x.content-area.member-info-wrapper > div.cell.small-12.large-7 > div > div.member-info-wrapper'
starting_urls = [KeyUrl('https://www.lso.ca/public-resources/finding-a-lawyer-or-paralegal/lawyer-and-paralegal-directory','main')]
iso = WebSite(absolute_url,content_box_tag,starting_urls=starting_urls)
p = IsoCrawler(iso,'lawerscrap')
print('TheCrow')
new_urls,request_urls,page_content,flawed_urls,to_search = Queue(),Queue(),Queue(),Queue(),['New York','Calgary, AB, Canada','Colonel Samuel Smith Park, Lake Shore Boulevard West, Etobicoke, ON, Canada']

def pipe_process (new_urls,request_urls,page_content,flawed_urls):
    p.pipeline_process(new_urls,request_urls,page_content,flawed_urls)

def scraping_process (new_urls,request_urls,page_content,flawed_urls,to_search):
    p.scrape_page_process(new_urls,request_urls,page_content,flawed_urls,to_search)

if __name__ == '__main__':
    processes = []
    processes.append(Process(target=scraping_process,args=(new_urls,request_urls,page_content,flawed_urls,to_search)))
    processes.append(Process(target=pipe_process,args=(new_urls,request_urls,page_content,flawed_urls)))

    for p in processes:
        p.start()
