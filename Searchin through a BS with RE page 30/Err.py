from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as bs

def get_soup_html(url):
    try:
        request = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None
    try:
        data = bs(request.read(),'html.parser')
    except AttributeError as e:
        print(e)
        return None

    return data
