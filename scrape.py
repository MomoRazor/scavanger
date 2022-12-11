from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait

print('What we scraping today?!')

print('First, we gotta get to the browser, looking for Chrome')

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver=Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver2=Chrome(service=Service(ChromeDriverManager().install()), options=options)

print('What URL are we going to?')

domain = "https://www.spelinspektionen.se"
url = domain+"/sok-licens/"

print('Going to '+url)

driver.get(url)

print('You can do further navigation (click buttons and stuff)')

searchDiv = driver.find_element(by='class name', value='license-search-form')

searchButton = searchDiv.find_element(by='class name', value='btn-primary')

searchButton.click()

searchResults = driver.find_element(by='id', value='search-results')

seperateSearchResults = searchResults.find_elements(by='class name', value='result-item')

licenses = []

for searchItem in seperateSearchResults:

    id = searchItem.get_attribute('data-license-url')

    newUrl = domain+id

    driver2.get(newUrl)

    try:
        header = driver2.find_element(by='class name', value='licensee')


        label = header.find_element("xpath", '//*[@id="company-label"]/following-sibling::div')
        print('Label - '+label.text)

        address = header.find_element("xpath", '//*[@id="company-address-label"]/following-sibling::div')
        print('Address - '+address.text.replace('\n', ', '))
    except:
        print('No Licensee for '+newUrl)


driver2.quit()
driver.quit()
    






