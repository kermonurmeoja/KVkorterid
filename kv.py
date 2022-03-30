from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
from fake_useragent import UserAgent
import os.path
import getpass

# selenium
chromeDriver = 'C:/Users/' + getpass.getuser() + '/Downloads/chromedriver.exe'


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
url = input("Sisestage url: ")
driver = startSelenium(url)
source = driver.page_source
k = []
k2 = []
doc = BeautifulSoup(source, "html.parser")
# tiitel ja lingid
objektid = doc.find_all("a", {"class": "object-title-a text-truncate"})
for obj in objektid:
    k.append(obj.text.strip())
    k2.append(obj['href'])

hinnad = []
# bsoup
doc = BeautifulSoup(source, "html.parser")
# hinna leidmine
hind = doc.find_all("p", {"class": "object-price-value"})
a = re.findall(r'[\d ]+', str(hind))
# print(a)
t = "".join(a)
a = re.sub("( ){2,}", " ", t)
hinnad = a.split(" ")
#print(hinnad)
kinnisvara = []
a = 0
b = 1
d = 0
e = 0
print("-------------------------------------")
print("Praegune kinnisvara info")
print("-------------------------------------")
while a < len(k):
    nimi = k[a].replace("  ", "")
    kinnisvara.append([k[a], hinnad[b], k2[a]])
    print(k[a].replace("  ", "") + " | Hind: " + hinnad[b] + " € | Link: " + k2[a])
    a += 1
    b += 1

# Siin on SQL db kood
import sqlite3

ühendus = sqlite3.connect('KVdb.db')
c = ühendus.cursor()
c.execute("SELECT * FROM Mustamäe")
# 3 value
#c.execute("INSERT INTO Mustamäe (Aadress, Hind, Link) VALUES ('x', 'x', 'x')")

k2sk = "INSERT INTO Mustamäe (Aadress, Hind, Link) VALUES (?, ?, ?)"
i = 0
d = 0
while i < len(kinnisvara):
    c.execute(k2sk, (str(kinnisvara[d][0]), str(kinnisvara[d][1]), str(kinnisvara[d][2])))
    d = d + 1
    i = i + 1

c.close()

ühendus.commit()

ühendus.close()
