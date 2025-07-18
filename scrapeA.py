

import shutil
import time
import pandas as pd
import os
from util import getChrome, getUrlAndDomain, hitSite, loadEnvVars

#Get Enviornmentals
envs = loadEnvVars()

#set directories
downloadDir = '.'+os.sep+'download'+os.sep
resultDir = '.'+os.sep+'result'+os.sep

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

#set limit
if envs.get('limitNumber'):
    limit = int(envs.get('limitNumber'))
else:
    limit = 0
total = len(seperateSearchResults)

#iterate through results
for index, searchItem in enumerate(seperateSearchResults, start=0):
    #decrease from limit in case of limited scrape
    limit = limit -1

    #Get id of individual result
    id = searchItem.get_attribute('data-license-url')

    #Generate individual result url
    newUrl = splitUrl.get("domain")+id

    #Notify User of Progress
    print('Scraping '+str(index)+'/'+str(total)+' at '+newUrl)

    #Hit generated url
    if not hitSite(driver2, newUrl):
        continue

    #Wait to make sure that page is loaded
    time.sleep(1)
    
    #Find Excel Export Link and click it
    exportDiv = driver2.find_element(by='class name', value='export-excel')
    link = exportDiv.find_element(by='tag name', value='a')
    link.click()

    #Wait to make sure that excel is loaded
    time.sleep(5)
    
    #If limited run, check if limit was passed and stop loop
    if envs.get('limitNumber') and limit <= 0:
        break

#Get list of downloaded excel exports
fileArray = os.listdir(downloadPath)

array = []

#Check for downloaded excel files
if len(fileArray) == 0:
    print('Download Folder was found empty :(')
    quit()

for index, file in enumerate(fileArray, start=0):

    array.append({
        "title": '',
        "address": '',
        "licenses": []
    })

    fullPath = downloadPath+os.sep+file
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

columns = ['title', 'address', 'licenseType', 'licenseExpiry', 'licenseDomains']

formatedArray = []
for item in array:
    for item2 in item.get('licenses'):
        newItem = {
            "title": item.get('title'),
            "address": item.get('address'),
            "licenseType": item2.get('type'),
            "licenseExpiry": item2.get('expiry'),
            "licenseDomains": item2.get('domains'),  
        }
        formatedArray.append(newItem)


df = pd.DataFrame(formatedArray, columns=columns)

fullPath = resultPath+os.sep+fileName+'.xlsx'
print(fullPath)
df.to_excel(fullPath)
    
print('Results Saved to Excel')

driver2.quit()
driver.quit()
    






