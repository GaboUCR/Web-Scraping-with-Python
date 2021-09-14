from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pymysql
#open pymysql
cur.execute('CREATE DATABASE IF NOT EXISTS AutomotiveCO')
cur.execute('USE AutomotiveCO')
cur.execute("""CREATE TABLE IF NOT EXISTS Content (
    BusinessName VARCHAR(255) UNIQUE, url VARCHAR(255) UNIQUE, PhoneNumber VARCHAR(255), id INTEGER UNIQUE NOT NULL AUTO_INCREMENT, PRIMARY KEY(id)
    );""")
cur.execute("""CREATE TABLE IF NOT EXISTS retrieved (
    N_page INTEGER, url VARCHAR(255)
    );""")

#configure the browser
starting_page = 'https://www.manta.com/search?search_source=nav&search=Automotive&context=unknown&city=Aurora&state=CO&pt=39.729432%2C-104.8319196&device=desktop&screenResolution=1366x768'
tests = 10

while tests > 0:
    chrome_options = Options()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=chrome_options)
    #the max page is the last page retrieved, so we have to get the next one
    cur.execute('SELECT MAX(N_page) FROM retrieved')
    N_page = cur.fetchone()[0]

    if (N_page == None):
        cur.execute('INSERT INTO retrieved (N_page,url) VALUES (%s,%s)',(1,starting_page))
        cur.execute('SELECT MAX(N_page) FROM retrieved')
        N_page = cur.fetchone()[0]
    cur.execute('SELECT (url) FROM retrieved WHERE N_page = %s',(N_page,))
    #retrieve the next page to visit so that is going to be the max in the next iteration
    current_url = cur.fetchone()[0]
    driver.get(current_url)
    next_page = driver.find_element_by_link_text(str(N_page + 1)).get_attribute('href')
    cur.execute('INSERT INTO retrieved (N_page,url) VALUES (%s,%s)', (N_page + 1,next_page))
    #get the content
    Content_boxes = driver.find_elements_by_css_selector(r'div.flex.flex-row.items-start > div.w-2\/3.md\:w-3\/4.flex.flex-row.justify-center > div.flex.flex-col.w-full.md\:w-1\/2.pl-8.text-gray-500')
    #For each of elements we have to get the name, url and phone number
    print("retrieving: ", current_url,"on page number: ",N_page)
    for box in Content_boxes:
        try:
            name = box.find_element_by_css_selector('div.font-bold.text-lg.overflow-wrap.text-gray-800.flex.flex-row.justify-between > a').text
            phone = box.find_element_by_css_selector('div.hidden.md\:flex.flex-row.items-start.mt-2 > div').text
            url = box.find_element_by_css_selector('div.hidden.md\:flex.flex-row.items-start.mt-3 > a').get_attribute('href')
            cur.execute('INSERT INTO Content (BusinessName,PhoneNumber,url) VALUES (%s,%s,%s)',(name,phone,url))
        except:
            print('error retrieving, probably a missing field')
            continue
        print('succesfully retrieved :)')
        print('name: ',name,'phone: ',phone,'url: ',url,'\n','-'*100)

    conn.commit()
    tests -= 1
    time.sleep(3)
    driver.close()
    time.sleep(7)


cur.close()
conn.close()
