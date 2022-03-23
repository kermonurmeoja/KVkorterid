from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import ssl
from fake_useragent import UserAgent
ssl._create_default_https_context = ssl._create_unverified_context
defaultURL = 'https://www.kv.ee/?act=search.simple&company_id=237&deal_type=1&company_id_check=237&county=1&search_type=new&parish=1061&city%5B0%5D=1007'
chromeDriver = 'C:/Users/kevin.sutt/Downloads/selenium/chromedriver.exe'

def startSelenium():
    optionss = webdriver.ChromeOptions()
    optionss.add_argument('--disable-blink-features=AutomationControlled')
    optionss.add_experimental_option("excludeSwitches", ["enable-automation"])
    optionss.add_experimental_option('useAutomationExtension', False)
    optionss.add_argument("window-size=1600,1200")
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    optionss.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(options=optionss, executable_path=chromeDriver)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.get(defaultURL)
    return browser

driver = startSelenium()
parsedURL = defaultURL
driver.get(parsedURL)
source = driver.page_source

#headers = {'User-Agent': 'Mozilla/5.0'}

#r = requests.get(url, headers=headers)

#doc = BeautifulSoup(r.text, "html.parser")

#kv = doc.find_all("tbody")

#tags = doc.find_all('a', class_="nav-title")
#links = [url + tag["href"] for tag in tags]

