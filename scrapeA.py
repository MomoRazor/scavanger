

import shutil
import time
import pandas as pd
import os
from util import getChrome, getUrlAndDomain, hitSite, loadEnvVars

#Get Enviornmentals
envs = loadEnvVars()

#set directories
downloadDir = './download/'
resultDir = './result/'

#set directories for downloads and results
timestamp = str(time.time())
downloadPath = downloadDir+timestamp
resultPath = resultDir+timestamp

#set resulting excel file name
fileName = envs.get('fileName')
if not fileName:
    print('No fileName given as Enviornmental Variable')
    quit()

#Clean up file directories if variables are set
if envs.get('clearFiles') == 'true':
    if os.path.exists(downloadDir):
        shutil.rmtree(downloadDir)
    if os.path.exists(resultDir):
        shutil.rmtree(resultDir)

#Create directories if it does not exists
if not os.path.exists(resultDir):
    os.mkdir(resultDir)
if not os.path.exists(resultPath):
    os.mkdir(resultPath)
if not os.path.exists(downloadDir):
    os.mkdir(downloadDir)
if not os.path.exists(downloadPath):
    os.mkdir(downloadPath)

#Getting the different browsers instances we need for this scrape
driver=getChrome()
driver2=getChrome(downloadUrl=downloadPath)

#This is the url we are using
url="https://www.spelinspektionen.se/sok-licens/"

#It might be useful to separate the domain from the url, we need it in this case
splitUrl = getUrlAndDomain(url)

#A browser instance will navigate to the url
hitSite(driver, url)

#From here we start checking the HTML and navigating according to what we need 
print('Starting Scrape') 

#Find and click the search all button
searchDiv = driver.find_element(by='class name', value='license-search-form')
searchButton = searchDiv.find_element(by='class name', value='btn-primary')
searchButton.click()

#Collect search results
searchResults = driver.find_element(by='id', value='search-results')
seperateSearchResults = searchResults.find_elements(by='class name', value='result-item')

limit = int(envs.get('limitNumber'))

data = []
total = len(seperateSearchResults)

for index, searchItem in enumerate(seperateSearchResults, start=0):
    
    limit = limit -1
    id = searchItem.get_attribute('data-license-url')

    newUrl = splitUrl.get("domain")+id

    print('Scraping '+str(index)+'/'+str(total)+' at '+newUrl)

    if not hitSite(driver2, newUrl):
        continue

    time.sleep(1)
    exportDiv = driver2.find_element(by='class name', value='export-excel')
    link = exportDiv.find_element(by='tag name', value='a')

    link.click()

    time.sleep(5)
    
    if envs.get('limitNumber') and limit <= 0:
        break

fileArray = os.listdir(downloadPath)

array = []

for index, file in enumerate(fileArray, start=0):

    array.append({
        "title": '',
        "address": '',
        "licenses": []
    })

    fullPath = downloadPath+'/'+file
    excelSheet = pd.read_excel(fullPath)

    keys = excelSheet.keys()

    title = keys[0]
    info = excelSheet.get(title)

    array[len(array)-1]["title"] = title
    if len(keys) >= 2:
        dateColumn = keys[1]

        dates = excelSheet.get(dateColumn)

        address = info[0]

        array[len(array)-1]["address"]  = address

        licenses = []
        indexSteps = []

        for index, date in enumerate(dates, start=0):
            if(index == 0):
                continue
            
            if not pd.isnull(date):
                indexSteps.append(index)
                newLicense = {
                    "type": info.get(index),
                    "expiry": date.strftime("%b %d, %Y"),
                    "domains": []
                }

                licenses.append(newLicense)
            else:
                if not pd.isnull(info.get(index)):
                    licenses[len(licenses)-1]['domains'].append(info[index])

        array[len(array)-1]["licenses"] = licenses

print('Done Scraping')

columns = ['title', 'address', 'licenses']

df = pd.DataFrame(array, columns=columns)

fullPath = resultPath+'/'+fileName+'.xlsx'
print(fullPath)
df.to_excel(fullPath)
    
print('Results Saved to Excel')

driver2.quit()
driver.quit()
    






