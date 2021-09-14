from Err import get_soup_html
from bs4 import BeautifulSoup as bs
import re

url = 'http://www.pythonscraping.com/pages/page3.html'
response = get_soup_html(url)
img_tags_re = re.compile('../img/gifts/img[1-9].jpg')
img_gifts = response.find_all('img',{'src':img_tags_re})

for image in img_gifts:
    print(image.get("src"))
