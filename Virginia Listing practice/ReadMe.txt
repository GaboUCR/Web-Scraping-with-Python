*****************************************************
To complete this job, please provide two items for me:
*****************************************************
1) An CSV file or XLXS file containing the scraped data. Either format is fine. Note that I've attached an example XLSX file that I would like completed, and included a couple sample rows in it (VirginiaFacilities.xlsx).
2) A Python script (using scrapy/selenium or other python libraries) that I can reuse on my own in the future to produce the output file from above.

*****************************************************
Please scrape data from the ALL of the pages of results for BOTH of these URLs (the results for both URLs are very similarly formatted):
*****************************************************
A) https://www.dss.virginia.gov/facility/search/alf.cgi?rm=Search&search_keywords_name=&search_exact_fips=&search_contains_zip=

B) https://www.dss.virginia.gov/facility/search/adc.cgi?rm=Search&search_keywords_name=&search_exact_fips=&search_contains_zip=

*****************************************************
Specific Instructions for Scraping the Data:
*****************************************************
1) For each result, get the link to each unique result page. Put that in column A in the spreadsheet.

2) Open the link for each individual listing to parse additional details for each facility ***as shown in attached image ***"Virginia-individual-info.png"***.

When you open each individual link, please get all of the additional fields in those two tables at the top of the page (note that the rows in the second table may very slightly between the two URLs). It is fine if all results are in the same spreadsheet and some columns are blank for some of the results!

*** NOTE ***
Columns K, L, and M are special, and the data can appear in any order within the "Qualification" cell on the facility's webpage. Also note that the Qualification row in the table may NOT be present at all for every result!!

* Values for column K are either "Ambulatory Only" or "Non-Ambulatory"
* Values for column L are either "Special Care Unit" or blank.
* Values for column M are either "Residential care only" or "Residential and Assisted Living Care"


3) Put each field in the correct column in the attached Excel file (or a CSV file is fine too!). Let me know if you have any questions about the correct columns for all the data.

4) Make sure to repeat this process for both URLs as listed above (pasting the same URLs here again for clarity):

A) https://www.dss.virginia.gov/facility/search/alf.cgi?rm=Search&search_keywords_name=&search_exact_fips=&search_contains_zip=
(567 records)

B) https://www.dss.virginia.gov/facility/search/adc.cgi?rm=Search&search_keywords_name=&search_exact_fips=&search_contains_zip=
(74 records)

Final output should have 641 total rows/records in it.