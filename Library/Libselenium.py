from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from Libsql import create_table,insert_into,update
from urllib.robotparser import RobotFileParser
import sqlite3
import csv
#______________________________________________________________________________#

def createDatabase():
    con = sqlite3.connect('web.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS url ( path text, retrieved int)")
    sql = ""

    for i in range(40):
        sql = "t"+str(i)+" "+"text, "


    cur.execute("CREATE TABLE IF NOT EXISTS info "+"("+ sql +"url_id int)")
    cur.close()
    con.close()



def read_csv(filename):
    dict = {}
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print (row)
                for key in row:
                    row[key] =[row[key]]

                dict.update(row)

            else:

                for key in row:
                    dict[key].append(row[key])

            line_count = line_count +1

    return dict

class ContentTag(object):
    """
    type determines how the content is going to be read
    """
    def __init__(self, type, tag):

        self.type = type
        self.tag = tag

class WebSite:
    """Contains the information needed to scrape a webSite"""
    def __init__(self, rootUrl, absolute_url, contentSelector, tor=False):
        self.rootUrl = rootUrl
        self.absolute_url = absolute_url
        self.tor = tor
        self.contentSelector = contentSelector
#______________________________________________________________________________#

class Crawler:
    """Crawls and scraps information from a WebSite"""
    def __init__(self, web_site, rootLinks):
        self.web_site = web_site
        self.rootLinks = rootLinks


    def get_web_site(self):
        return self.web_site

    def scrape(self, urls):

        con = sqlite3.connect('web.db')
        cur = con.cursor()
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")

        if (self.web_site.tor):
            chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")

        driver = webdriver.Chrome(options=chrome_options)

        cur.execute("SELECT path FROM url WHERE retrieved = ?", (0,))
        links = set([link[0] for link in cur.fetchall()])

        for link in links:
            driver.get(link)
            #get all of the links that we need
            anchorsTags = driver.find_elements_by_css_selector("a")
            anchorLinks = [anchor.get_attribute("href") for anchor in anchorsTags]

            for anchorLink in anchorLinks:
                if anchorLink[0] != "/":
                    anchorLink = "/"+anchorLink

                if "https://" not in anchorLink:
                    anchorLink = self.web_site.absolute_url + anchorLink

                cur.execute("INSERT INTO url (path, retrieved) VALUES (?,?)", (anchorLink,0))

            self.get_content(body)  


        cur.close()
        con.close()
    #Tag dict has the headers and each individual row

    def get_content(self,body):

        if self.web_site.contentSelector["type"] == "table":
            return self.get_table_content(body)


    def get_table_content(self, body):
        """
        Retrieve the text inside tables from a website
        """
        headersTag, rowsTag = self.web_site.contentSelector.tag["headers"], self.web_site.contentSelector.tag["rows"]
        headersElements = body.find_elements_by_css_selector(headersTag)
        rowsElements = body.find_elements_by_css_selector(rowsTag)

        headers = [h.text for h in headersElements]
        rows = [h.text for h in rowsElements]

        return {"headers":headers, "rows":rows}

    def obey_robots(self,url):
        if (self.web_site.absolute_url.endswith('/')):
            robot_url = self.web_site.absolute_url + 'robots.txt'
        else:
            robot_url = self.web_site.absolute_url + '/robots.txt'

        rp = RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
        return {'crawl_delay':rp.crawl_delay('*'),'can_fetch':rp.can_fetch('*',url)}



    def get_text_content(self,content_boxes,content_dict={}):

        counter = 1
        for box in content_boxes:
            #Save them on csv here
            content_dict['t'+str(counter)] = box.text
            counter += 1

        return content_dict

# print(read_csv("lol.csv"))
# chrome_options = Options()
# chrome_options.add_argument("--ignore-certificate-errors")
#
#
#
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://en.wikipedia.org/wiki/Mother%27s_Day")
# path = "/html/body/div[3]/div[3]/div[5]/div[1]/div[7]/div/a/img"
# print(len(driver.find_elements_by_xpath(path)))
# print(driver.find_elements_by_xpath(path)[0].text == "")

#______________________________________________________________________________#
