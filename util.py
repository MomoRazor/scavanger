from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

#This file contains a bunch of code that can be reused between scrapes

def getChrome():
    envs = loadEnvVars()

    if(envs.get('headless') == 'true'):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        return Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return Chrome(service=Service(ChromeDriverManager().install()))
            
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
