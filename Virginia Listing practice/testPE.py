from Libselenium import WebSite,Crawler

starting_url = 'https://projecteuler.net/archives'
absolute_url = 'https://projecteuler.net'
dict_tags = {'description':('td > a','text','VARCHAR(255) UNIQUE'), 'url_to_box_info':('td > a','href','VARCHAR(255) UNIQUE'), 'Solved_by':('td > div','text','VARCHAR(255)')}
content_box_tag = r'#problems_table > tbody > tr'
target_pattern = ' '


pe = WebSite(dict_tags,absolute_url,target_pattern,content_box_tag,starting_url=starting_url)


absolute_url1 = 'https://www.dss.virginia.gov'
dict_tags1 = {'half_problem':('p','text','VARCHAR(500) UNIQUE')}
content_box_tag1 = r'#content > div.problem_content'
target_pattern1 = ' '


pe_meta = WebSite(dict_tags1,absolute_url1,target_pattern1,content_box_tag1)

spongy = Crawler(pe,'projecteuler',{'url_to_box_info':pe_meta})
#spongy.obey_robots(,)
spongy.crawl_searches(2)
