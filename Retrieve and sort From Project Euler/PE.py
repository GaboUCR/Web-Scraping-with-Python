from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup

def parse_PE(url):
    """
    Parses one page from the webpage Project Euler, saves the amount of times a problem has been solved linked to an ID on a dictionary.
    Arguments:
        url: String
            Url of the webpage
    Returns:
        Ids: dictionary
            ID ===> times_solved
    """

    browser = webdriver.Chrome()
    browser.get(url)
    data = BeautifulSoup(browser.page_source , 'html.parser')
    ids = dict()
    id = data.find_all('td', class_ = 'id_column')
    times_solved = data.find_all('div', class_ = 'center')
    browser.close()
    for i in range(len(id)):
        ids[id[i].string] =  times_solved[i].string

    return ids



def change_page_PE():
    '''
    Uses parse_PE to retrieve a dictionary from the current page and uses selenium to click the next page on the website https://projecteuler.net/archives until
    it has retrieved every problem.

    Returns:
        Ids : List
            Every problem id sorted from most solved problem to least solved
    '''
    Ids = dict()
    page = 14
    url = 'https://projecteuler.net/archives;page=15'
    css_selector = '#problems_table_page > div:nth-child(5) > a:nth-child(16)'
    while True:

        Ids.update(parse_PE(url))
        browser = webdriver.Chrome()
        browser.get(url)
        try:
            button = browser.find_element_by_css_selector(css_selector)
        except:
            break
        button.click()
        url = browser.current_url
        browser.close()
        page += 1
        css_selector = css_selector[:-2] + str(page) +')'

    return Ids

print(change_page_PE())

#print(parse_PE('https://projecteuler.net/archives'))
