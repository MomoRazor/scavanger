from random import randrange
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

#This file contains a bunch of code that can be reused between scrapes

def getChrome(downloadUrl=None):
    envs = loadEnvVars()

    options = Options()
    
    if(envs.get('headless') == 'true'):
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

    if(downloadUrl):
        options.add_experimental_option('prefs',{
            "download.default_directory": downloadUrl
        })
    
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.set_page_load_timeout(15)

    return driver
            
def loadEnvVars():
    load_dotenv()

    return os.environ

def getUrlAndDomain(url):
    parsedUrl = urlparse(url)
    domain = parsedUrl.scheme+'://'+parsedUrl.netloc
    endpoint = parsedUrl.path
    return {
        "domain": domain,
        "endpoint": endpoint
    }

def hitSite(driver, url):

    time.sleep(randrange(6))

    try:
        driver.get(url)
        return True
    except:
        print(url + ' timed out!')
        return False

