# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from items import Content
import pymysql
from TextLib import rank_text

class AmericanliteraturealgorithmPipeline:
    def process_item(self, Content, spider):
        #Content = ItemAdapter(Content)
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Konoha.12')
        cur = conn.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS AmericanLiterature')
        cur.execute('USE AmericanLiterature')
        cur.execute("""CREATE TABLE IF NOT EXISTS Content (
            title VARCHAR(255) UNIQUE, url VARCHAR(255) UNIQUE, type VARCHAR(255), preferences TEXT, length INTEGER ,id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,
            retrieved INTEGER, PRIMARY KEY(id)
            );""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Links (
            tourl INTEGER, fromurl INTEGER, id INTEGER UNIQUE NOT NULL AUTO_INCREMENT, PRIMARY KEY(id));""")
        #check if the page has been registered
        cur.execute('SELECT retrieved FROM Content WHERE url = %s',(Content['url']))
        if (len(cur.fetchall()) == 0):
            cur.execute('INSERT INTO Content (url,retrieved,type) VALUES (%s,%s,%s)',(Content['url'],1,Content['type']))
            if (Content['type'] != "Transition"):
                #We check the preferences of the user with a helper function
                length,preferences = rank_text(Content)

                cur.execute('UPDATE Content SET title = %s,preferences = %s,length = %s  WHERE url = %s',(Content['title'],preferences,length,Content['url']))
            #do the process for the Transition pages, without an if because every page is considered a Transition page
            cur.execute('SELECT id FROM Content WHERE url = %s',(Content['url'],))
            from_id = cur.fetchone()
            #Go through the links from current page, create the connections and a template for the new pages to be retrieved
            for ToUrl in Content['links']:
                #is ToUrl already in our database?
                cur.execute('SELECT id FROM Content WHERE url = %s',(ToUrl,))

                if (len(cur.fetchall()) == 0):
                    cur.execute('INSERT INTO Content (url) VALUES(%s)',(ToUrl,))
                    cur.execute('SELECT id FROM Content WHERE url = %s',(ToUrl,))
                cur.execute('SELECT id FROM Content WHERE url = %s',(ToUrl,))
                to_id = cur.fetchone()
                cur.execute('INSERT INTO Links (ToUrl,FromUrl) Values (%s,%s)',(to_id,from_id))
            conn.commit()
        #commit and close

        cur.close()
        conn.close()
        return Content
