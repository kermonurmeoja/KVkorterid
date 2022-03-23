from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import ssl
from fake_useragent import UserAgent
ssl._create_default_https_context = ssl._create_unverified_context
# selenium
chromeDriver = 'C:/Users/kevin.sutt/Downloads/selenium/chromedriver.exe'

def startSelenium(url):
    optionss = webdriver.ChromeOptions()
    optionss.add_argument('--disable-blink-features=AutomationControlled')
    optionss.add_experimental_option("excludeSwitches", ["enable-automation"])
    optionss.add_experimental_option('useAutomationExtension', False)
    optionss.add_argument("window-size=1920,1080")
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    optionss.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(options=optionss, executable_path=chromeDriver)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.get(url)
    return browser
a = []
url = "https://www.kv.ee/?act=search.simple&company_id=237&deal_type=1&company_id_check=237&county=1&search_type=new&parish=1061&city%5B0%5D=1007"
driver = startSelenium(url)
source = driver.page_source
# näide praegu
# saab asendada neid kohti inputiga hiljem
# regex nimed
nimed = re.findall('((Tallinn, Mustamäe)(.*)( ))', source)
#print(nimed)
for nimi in nimed:
    a.append(nimi[1])

# regex lingid
lingid = re.findall('((https://)(.*)(html))', source)
#print(lingid)

# bsoup    
doc = BeautifulSoup(source, "html.parser")
# hinna leidmine
hind = doc.find_all("p", {"class": "object-price-value"})
a = re.findall(r'[\d ]+', str(hind))
#print(a)
t = "".join(a)
a = re.sub("( ){2,}", " ", t)
print(a.split(" "))

    


        

