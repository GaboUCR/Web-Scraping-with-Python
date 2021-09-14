from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pymysql
from Libsql import create_table,insert_into,update
from urllib.robotparser import RobotFileParser
#______________________________________________________________________________#

class DataColumn:
    '''
    '''
    def __init__(self,name,tags,attribute,sql_declaration,selector):
        self.name = name
        self.tags = tags
        self.attribute = attribute
        self.sql_declaration = sql_declaration
        self.selector = selector

class WebSite:
    """Contains the information needed to scrape a webSite"""
    def __init__(self,columns,absolute_url,target_pattern,content_box_tag,tor=False,starting_url=''):
        self.starting_url = starting_url
        self.absolute_url = absolute_url
        self.columns = columns
        self.content_box_tag = content_box_tag
        self.target_pattern = target_pattern
        self.tor = tor

    def set_url(self,url):
        self.starting_url = url

    def set_column_dict(self,new_column_dict):
        self.column_dict = new_column_dict
#______________________________________________________________________________#

class Crawler:
    """Crawl and scrap information from a WebSite"""
    def __init__(self,web_site,database_name='',meta_web_sites={}):
        self.web_site = web_site
        self.database_name = database_name
        self.meta_web_sites = meta_web_sites

    def get_web_site(self):
        return self.web_site

    def obey_robots(self,url):
        if (self.web_site.absolute_url.endswith('/')):
            robot_url = self.web_site.absolute_url + 'robots.txt'
        else:
            robot_url = self.web_site.absolute_url + '/robots.txt'

        rp = RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
        return {'crawl_delay':rp.crawl_delay('*'),'can_fetch':rp.can_fetch('*',url)}

    def get_meta_content(self,content_boxes):
        content = list()
        print(len(content_boxes))
        for box in content_boxes:
            content_dict = dict()
            info = box.text.split(':')
            print(info)
            try:
                key = info[0].lower().replace(' ','_')
                val = info[1].strip(' ').replace('\n',' ')

                content_dict[key] = val
                content.append(content_dict)
            except:
                continue

        print(content)
        return content


    def get_content(self,content_boxes):
        def get_index(info,index):
            try:
                result = info[index]
            except:
                result = 'n/a'

            return result

        content = list()
        print(len(content_boxes))
        for box in content_boxes:
            #content dictionary saves the name of the column atached to the value
            content_dict = dict()
            info = box.text.split('\n')
            content_dict['name'] = get_index(info,0)
            content_dict['address'] = get_index(info,1)+' '+get_index(info,2)
            content_dict['phone'] = get_index(info,3)
            content_dict['url_to_box_info'] = box.find_element_by_css_selector('a').get_attribute('href')
            content.append(content_dict)

        return content

    def scrape_page (self):
        #initialize browser
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        if (self.web_site.tor):
            chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        driver = webdriver.Chrome(options=chrome_options)
        #make the request
        driver.get(self.web_site.starting_url)
        content_boxes = driver.find_elements_by_css_selector(self.web_site.content_box_tag)
        content = self.get_meta_content(content_boxes)
        driver.close()
        return content

    def crawl_searches (self,rounds):
        '''
        Crawls through the buttons of a web page and saves on a SQL database every field found on the tags attribute, for example the 1,2,3,4,5 buttons of a search page.
        It can start at any point and if it gets closed, then it restarts on the latest crawl button.
        '''
        #open pymysql
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Konoha.12')
        cur = conn.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS '+self.database_name)
        cur.execute('USE '+self.database_name)
        # column_dict = self.get_web_site().column_dict
        # column_dict.update(self.meta_web_sites['url_to_box_info'].column_dict)
        cur.execute(create_table(self.web_site.columns,'Content'))
        cur.execute("""CREATE TABLE IF NOT EXISTS retrieved (
            N_page INTEGER, url VARCHAR(255)
            );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS ids_retrieved (
            ids INTEGER
            );""")
        #configure the browser
        while rounds > 0:
            chrome_options = Options()
            chrome_options.add_argument("--ignore-certificate-errors")
            if (self.web_site.tor):
                chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
            driver = webdriver.Chrome(options=chrome_options)
            #the max page is the last page retrieved, so we have to get the next one
            cur.execute('SELECT MAX(N_page) FROM retrieved')
            N_page = cur.fetchone()[0]
            print(N_page)
            if (N_page == None):
                cur.execute('INSERT INTO retrieved (N_page,url) VALUES (%s,%s)',(1,self.web_site.starting_url))
                cur.execute('SELECT MAX(N_page) FROM retrieved')
                N_page = cur.fetchone()[0]
            cur.execute('SELECT (url) FROM retrieved WHERE N_page = %s',(N_page,))
            current_url = cur.fetchone()[0]
            #add the n_page column in content
            #retrieve the next page to visit so that is going to be the max in the next iteration
            driver.get(current_url)
            next_page = driver.find_element_by_link_text(str(N_page + 1)).get_attribute('href')
            cur.execute('INSERT INTO retrieved (N_page,url) VALUES (%s,%s)', (N_page + 1,next_page))
            #get the content
            content_boxes = driver.find_elements_by_css_selector(self.web_site.content_box_tag)
            #For each of elements we have to get the name, url and phone number
            print("retrieving: ", current_url,"on page number: ",N_page)
            #gets a list of columns based on column_dict, it gets info from outside the button not the inside
            content = self.get_content(content_boxes)  #{'N_page':N_page})
            #iterate over every column
            print(content)
            for column in content:
                #try:
                sql_command = insert_into(column,'Content')
                    #print(sql_command)
                cur.execute(sql_command[0],sql_command[1])
                #except:
                    #print('Not able to insert into, probably a duplicate unique value')
                    #continue
            #print('succesfully retrieved the button information :)')
            #Getting info from inside the buttons using the meta_web_sites list
            #To use this is required to have a column on Content named url_to_box_info and every attribute to retrieve
            driver.close()
            if (self.meta_web_sites != {}):
                #meta_web_sites is the template
                cur.execute('SELECT url_to_box_info,id FROM Content')  #WHERE N_page = %s',(N_page,))
                urls_to_box_info = cur.fetchall()

                cur.execute('SELECT ids FROM ids_retrieved')
                ids_retrieved = cur.fetchall()
                #insert urls values and create the websites ans dave them on a list to scrape
                page = self.meta_web_sites['url_to_box_info']

                for url,id in urls_to_box_info:
                    if ((id,) not in ids_retrieved):
                        #call scrape_page for each website and save it on the database
                        cur.execute('INSERT INTO ids_retrieved (ids) VALUES (%s)',(id))
                        page.set_url(url)
                        time.sleep(2)
                        crawl = Crawler(page)
                        content = crawl.scrape_page()
                        for column in content:
                            #try:
                            sql_command = update(column,'Content',where={'url_to_box_info':url})
                            print(sql_command)
                            cur.execute(sql_command[0],sql_command[1])
                            # except:
                            #     print('Not able to insert into, probably a duplicate unique value')
                            #     continue
            conn.commit()
            rounds -= 1
            time.sleep(2)

        cur.close()
        conn.close()

#______________________________________________________________________________#
