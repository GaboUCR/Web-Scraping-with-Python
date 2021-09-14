from Libselenium import WebSite,Crawler,DataColumn

starting_url = 'https://www.dss.virginia.gov/facility/search/alf.cgi?rm=Search;'
absolute_url = 'https://www.dss.virginia.gov'


columns = [DataColumn('name','','','VARCHAR(255)',''), DataColumn('url_to_box_info','','href','VARCHAR(255)',''), DataColumn('address','','','VARCHAR(255)',''), DataColumn('phone','','','VARCHAR(255)','') ,
            DataColumn('facility_type','','','VARCHAR(255)',''), DataColumn('license_type','','','VARCHAR(255)',''), DataColumn('expiration_date','','','VARCHAR(255)',''), DataColumn('qualification','','','VARCHAR(255)','')
            ,DataColumn('administrator','','','VARCHAR(255)',''), DataColumn('business_hours','','','VARCHAR(255)',''), DataColumn('capacity','','','VARCHAR(255)',''), DataColumn('inspector','','','VARCHAR(255)','')]

content_box_tag = r'#main_content > table.cc_search > tbody > tr > td[valign=TOP]'
target_pattern = ' '

# //*[@id="main_content"]/table[2]/tbody/tr/td
virginia = WebSite(columns,absolute_url,target_pattern,content_box_tag,starting_url=starting_url)


absolute_url1 = 'https://www.dss.virginia.gov'
dict_tags1 = [ ]
content_box_tag1 = r'#main_content > table.cc_search > tbody > tr'
target_pattern1 = ' '


# //*[@id="main_content"]/table[2]/tbody/tr[1]/td[1]/text()[1]
# //*[@id="main_content"]/table[2]/tbody/tr[1]/td[1]/text()[2]
virginia_meta = WebSite(dict_tags1,absolute_url1,target_pattern1,content_box_tag1)

spongy = Crawler(virginia,'Virginia',{'url_to_box_info':virginia_meta})
spongy.crawl_searches(100)
#spongy.obey_robots(,)
#spongy.scrape_page()
