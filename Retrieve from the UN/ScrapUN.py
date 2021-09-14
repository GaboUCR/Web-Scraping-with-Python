import requests
import lxml.html
import sqlite3
def get_year_urls():
    start_url = 'https://www.un.org/securitycouncil/content/resolutions'
    response = requests.get(start_url)
    tree = lxml.html.fromstring(response.text)
    links = tree.cssselect('div[class="field-item even"] > ul > li > h4 > a')  # or tree.xpath('//a')

    year_dict = dict()
    for link in links:
        url = requests.compat.urljoin(start_url,link.attrib['href'])
        year_dict[link.text_content()] = url
        # we use this if just in case some <a> tags lack an href attribute
    #    if 'href' in link.attrib:
    #        url = requests.compat.urljoin(start_url,link.attrib['href'])
    #        out.append(url)
    return year_dict

def create_DB (year_dict):
    connection = sqlite3.connect('UN_Resolutions.db')
    cur = connection.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS UN_resolutions(

    Url TEXT,
    Name TEXT,
    Date INTEGER,
    Description TEXT
    )
                """)

    for year in year_dict:
        response = requests.get(year_dict[year])
        tree = lxml.html.fromstring(response.text)
        links = tree.cssselect('table  tbody  tr')

        for link in links:
            td = link.cssselect('td')
            #In case that a text table is in the middle of the data
            try:
                anchor = td[0].cssselect('a')[0]
            except:
                continue

            if (int(year) < 2014) : #there is no year column
                url = requests.compat.urljoin(year_dict[year],anchor.attrib['href'])
                name = anchor.text_content()
                descr = td[1].text_content()
                date = "No date reported"
                print(name,url,date,descr)
                cur.execute("INSERT INTO UN_resolutions(Url,Date,Name,Description) VALUES(?,?,?,?)",(url,date,name,descr))
                connection.commit()
                continue

            url = requests.compat.urljoin(year_dict[year],anchor.attrib['href'])
            name = anchor.text_content()
            date = td[1].text_content()
            try:
                descr = td[2].text_content()
            except:
                descr = "No Description"
            cur.execute("INSERT INTO UN_resolutions(Url,Date,Name,Description) VALUES(?,?,?,?)",(url,date,name,descr))
            connection.commit()

            print(name,url,date,descr)



create_DB(get_year_urls())
#print(get_year_urls())
