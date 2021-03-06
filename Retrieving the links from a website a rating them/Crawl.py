import urllib 
import sqlite3
import bs4
import random
#Ask for the contents of the page

def retrieve_urls(url,N_pages):
    """
    Retrieve every website url you can access from parameter url and makes a 
    dictionary linking url to a list of the urls, then picks a random url and
    does the same.
    ----------
    url : String
        The url of the website we want to make a request to.
    N_pages : int
        The number of pages we want to look
        
    Returns
    -------
    A dictionary linked to a list of all the links we can access from the url. 
    """
    web_links = dict()
    links_list = [] 
    last_page_searched = ""
    for n in range(N_pages):    
        
        while True:           
            try:                
                connection = urllib.request.urlopen(url)
                break
            except:                
                url = random.choice(links_list)
                while url in web_links.keys():
                    url = random.choice(links_list)
                
                
        links_list = []        
        request = connection.read().decode()
        info = bs4.BeautifulSoup(request,"html.parser")
        
        
        for link in info.find_all("a"):                            
            href = link.get("href")
            
            if href == None:
                continue
            if href.startswith("//"):
                href= "https:" + href
                                  
            links_list.append(href)
        
        if links_list == []:
            url = random.choice(web_links[last_page_searched])
       
        else:                               
            web_links[url] = links_list
            last_page_searched = url
            url = random.choice(web_links[last_page_searched])
        
        while url in web_links.keys():
            url = random.choice(web_links[last_page_searched])
        
        
    return web_links





def rank_urls(web_links):
    """
    

    Parameters
    ----------
    web_links : Dict
        Dictionary linking a web page with every url you can access from that 
        website

    Returns
    -------
    Dictionary linking a web page to the number of pages you can access from 
    that website divided by the keyword linked to a higher list length

    """
    rank = dict()        
    
    for key in web_links:
        rank[key] = len(web_links[key])
        
    return rank




#Save the links on a database
    
def url_database(web_links):
     """
     Saves in a database information given in a dictionary with a certain order

     Parameters
     ----------
     web_links : dict
         

     Returns
     -------
     None.

     """
     connection = sqlite3.connect("Links.sqlite3")
     cur = connection.cursor()
     #we create or override the database
     cur.execute("""CREATE TABLE IF NOT EXISTS Hrefs(
     websites_id INTEGER, url TEXT)              
     """)
     cur.execute("""CREATE TABLE IF NOT EXISTS websites(
                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,url TEXT,rank INTEGER)                      
                 """)
     connection.commit()
     dict_ranks = rank_urls(web_links)
     
     for website in web_links:
         cur.execute("INSERT INTO websites (url,rank) VALUES (?,?)",(website,dict_ranks[website]))
         cur.execute("SELECT id FROM websites WHERE url=?",(website,))
         website_id = cur.fetchone()
         for values in web_links[website]:
             cur.execute("INSERT INTO Hrefs (websites_id,url) VALUES (?,?)",(website_id[0],values))
         
         connection.commit()
     
     cur.close()
         
         
def main () :
    url = "https://www.wikipedia.org/" #input("enter the starting page")
    N_pages = 10 #int(input("how many pages do you want to look through"))    
    web_dict = retrieve_urls(url, N_pages)
    ## we save into the database
    url_database(web_dict)

if __name__ == '__main__':
    main()
            
         
         
     




