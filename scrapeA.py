

import time
from util import getChrome, getUrlAndDomain, hitSite, loadEnvVars

#Get Enviornmentals
envs = loadEnvVars()

#Getting the different browsers instances we need for this scrape
driver=getChrome()
driver2=getChrome(downloadUrl='./download/'+str(time.time()))

#This is the url we are using
url="https://www.spelinspektionen.se/sok-licens/"
#It might be useful to separate the domain from the url, we need it in this case
splitUrl = getUrlAndDomain(url)

#A browser instance will navigate to the url
hitSite(driver, url)

#From here we start checking the HTML and navigating according to what we need 

print('Starting Scrape') 

searchDiv = driver.find_element(by='class name', value='license-search-form')

searchButton = searchDiv.find_element(by='class name', value='btn-primary')

searchButton.click()

searchResults = driver.find_element(by='id', value='search-results')

seperateSearchResults = searchResults.find_elements(by='class name', value='result-item')

limit = 3
data = []
total = len(seperateSearchResults)

for index, searchItem in enumerate(seperateSearchResults, start=0):
    
    limit = limit -1
    id = searchItem.get_attribute('data-license-url')

    newUrl = splitUrl.get("domain")+id

    print('Scraping '+str(index)+'/'+str(total)+' at '+newUrl)

    if not hitSite(driver2, newUrl):
        continue

    exportDiv = driver2.find_element(by='class name', value='export-excel')
    link = exportDiv.find_element(by='tag name', value='a')

    link.click()

    time.sleep(5)
    
    # header = driver2.find_element(by='class name', value='licensee')

    # label = header.find_element("xpath", '//*[@id="company-label"]/following-sibling::div')
    # address = header.find_element("xpath", '//*[@id="company-address-label"]/following-sibling::div')

    # licenses = []

    # licenseTable = driver2.find_element(by='class name', value='license-list-table')

    # tableChildren = licenseTable.find_elements(by='xpath', value='*')
    # total2 = len(tableChildren)    

    # if total2 > 10:
    #     print(newUrl + ' more than 10 licenses, skipping for now')
    #     continue



    # for index2, child in enumerate(tableChildren, start=0):

    #     if child.tag_name != 'tbody':
    #         continue

    #     print('Scraping License '+str(index2)+'/'+str(total2))
    #     domains = []

    #     try:
    #         subTable = child.find_element(by='class name', value='sub-table')
    #         domainElements = subTable.find_elements(by='tag name', value='div')

    #         for domainElement in domainElements:
    #             domains.append(domainElement.text)
        
    #     except:
    #         print("SubTable not found for "+newUrl)
        
    #     licenses.append({
    #         'type': child.find_element(by='class name', value='license-type').text,
    #         'validTill': child.find_element(by='class name', value='license-end').text,
    #         'domains': domains
    #     })


    # datum = {
    #     'label': label.text,
    #     'address':address.text.replace('\n', ', '),
    #     'licenses': licenses
    # }


    # data.append(datum)

    if limit <= 0 and envs.get('limit') == 'true':
        break

print('Done Scraping')

driver2.quit()
driver.quit()
    






