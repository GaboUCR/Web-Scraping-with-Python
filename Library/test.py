from Libselenium import WebSite,Crawler

url = 'https://www.manta.com/search?search_source=nav&search=Automotive&context=unknown&city=Aurora&state=CO&pt=39.729432%2C-104.8319196&device=desktop&screenResolution=1366x768'
absolute_url = 'https://www.manta.com'
dict_tags = {'BusinessName':('div.font-bold.text-lg.overflow-wrap.text-gray-800.flex.flex-row.justify-between > a','text','VARCHAR(255) UNIQUE'), 'url':('div.hidden.md\:flex.flex-row.items-start.mt-3 > a','href','VARCHAR(255) UNIQUE'), 'PhoneNumber':( 'div.hidden.md\:flex.flex-row.items-start.mt-2 > div','text','VARCHAR(255)')}
content_box_tag = r'div.flex.flex-row.items-start > div.w-2\/3.md\:w-3\/4.flex.flex-row.justify-center > div.flex.flex-col.w-full.md\:w-1\/2.pl-8.text-gray-500'
target_pattern = ' '
tor = True

manta = WebSite(url,dict_tags,absolute_url,target_pattern,tor,content_box_tag)

spongy = Crawler(manta,'Auto')
spongy.crawl_searches(40)
