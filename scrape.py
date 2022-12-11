from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import csv

print('What we scraping today?!')

print('First, we gotta get to the browser, looking for Chrome')

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver=Chrome(service=Service(ChromeDriverManager().install()), options=options)

print('What URL are we going to?')

url = "https://www.spelinspektionen.se/sok-licens/"

print('Going to '+url)

driver.get(url)

if driver.current_url == url:
    print('Made it to '+url+'! Up to you now!')

print('You can do further navigation (click buttons and stuff)')

searchDiv = driver.find_element(by='class name', value='license-search-form')

searchButton = searchDiv.find_element(by='class name', value='btn-primary')

print(searchButton.text)

searchButton.click()

searchResults = driver.find_element(by='id', value='search-results')

seperateSearchResults = searchResults.find_elements(by='class name', value='result-item')

for searchItem in seperateSearchResults:
    itemName = searchItem.find_element(by='class name', value='name')
    print(itemName.text)

#soup = BeautifulSoup(driver.page_source,features='html.parser')

#print(driver.page_source)



