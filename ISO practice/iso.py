from Libselenium import WebSite,Crawler,DataColumn
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv

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

    def crawl (self,to_search):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(options=chrome_options)
        #iterate over each search
        for search in to_search:
            driver.get(self.web_site.starting_url)
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
            for lawer in lawers:
                content = {'name':'N/A','last name':'N/A','Email':'N/a','Area of Law':'N/A','Business Name':'N/A','Phone':'N/A','Business Address':'N/A'}
                driver.get(lawer)
                time.sleep(2)
                text_box = driver.find_elements_by_css_selector('#content-wrapper > div.tps-two-column-wrapper > section > div > div.grid-x.content-area.member-info-wrapper > div.cell.small-12.large-7 > div > div > div.member-info-wrapper')
                name , last_name = driver.find_element_by_css_selector('h2.member-info-title').text.split(' ')[0] , driver.find_element_by_css_selector('h2.member-info-title').text.split(' ')[-1]
                print('Name: ', name)
                content['name'] = name
                print('last name:', last_name)
                content['last name'] = last_name
                for info in text_box:
                    data = info.text.split('\n')
                    if (data[0] == 'Email Address'):
                        print('Email Address:', ''.join(data[1:len(data)]))
                        content['Email'] =' '.join(data[1:len(data)])

                    if (data[0] == 'Area(s) of Law/Legal Services'):
                        print('Area Of Law:', ' '.join(data[1:len(data)]))
                        content['Area of Law'] =' '.join(data[1:len(data)])

                    if (data[0] == 'Business Name'):
                        print('Business Name: ', ''.join(data[1:len(data)]))
                        content['Business Name'] =''.join(data[1:len(data)])

                    if (data[0] == 'Business Address'):
                        print('Business Address: ', ' '.join(data[1:len(data)]))
                        content['Business Address'] =' '.join(data[1:len(data)])

                    if (data[0] == 'Phone'):
                        print('Phone: ', ''.join(data[1:len(data)]))
                        content['Phone'] =''.join(data[1:len(data)])

                with open('lawers.csv', mode='a') as lawers_file:
                    fieldnames = ['name','last name','Email','Area of Law','Business Name','Phone','Business Address']
                    writer = csv.DictWriter(lawers_file, fieldnames=fieldnames)
                    writer.writerow(content)


        driver.quit()

#
# with open('lawers.csv', mode='w') as lawers_file:
#     fieldnames = ['name','last name','Email','Area of Law','Business Name','Phone','Business Address']
#     writer = csv.DictWriter(lawers_file, fieldnames=fieldnames)
#     writer.writeheader()

columns = []
absolute_url = 'https://www.lso.ca/'
target_pattern = ''
content_box_tag = ''
starting_url = 'https://www.lso.ca/public-resources/finding-a-lawyer-or-paralegal/lawyer-and-paralegal-directory'
iso = WebSite(columns,absolute_url,target_pattern,content_box_tag,starting_url=starting_url)
p = IsoCrawler(iso)
# print('dad')
# read_csv()
p.crawl(['New York','Calgary, AB, Canada','Colonel Samuel Smith Park, Lake Shore Boulevard West, Etobicoke, ON, Canada'])
