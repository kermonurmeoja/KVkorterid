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
kvee = []
url = input("Sisestage KV.ee portaali URL: ")
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
kinnisvara = []
a = 0
b = 1
d = 0
e = 0
while a < len(k):
    nimi = k[a].replace("  ", "")
    kinnisvara.append([k[a], hinnad[b], k2[a]])
    a += 1
    b += 1
a = 0
b = 1

# SQL andmebaas
import sqlite3


print("-------------------------------------")
print("Mustamäe kinnisvara andmebaas")
print("Saadaval olevad käsud:")
print("-- praegu - näitab praeguseid kinnisvaraüksusi koos hinna ja lingiga.")
print("-- kanna - kannab andmebaasi praegused kinnisvaraüksused koos hinna ja lingiga.")
print("-- vaata - vaata kinnisvaraüksuse hinna arengut.")
print("-- katkesta - katkestab ühenduse.")
print("-------------------------------------")
e = 0
while e < 1:
    cmd = input("$ ")
    if cmd == "praegu":
        o = 1
        print("Kuvan praegused aktiivsed pakkumised:")
        while a < len(k):
            print(str(o) + ". " + k[a].replace("  ", "") + " | Hind: " + hinnad[b] + " € | Link: " + k2[a])
            a += 1
            b += 1
            o += 1
        o = 0
        a = 0
        b = 1
        e += 1
        input("Klikka jätkamiseks...")
    elif cmd == "kanna":
        print("Kannan andmed andmebaasi...")
        ühendus = sqlite3.connect('KVdb.db')
        c = ühendus.cursor()
        c.execute("SELECT * FROM Mustamäe")
        # c.execute("INSERT INTO Mustamäe (Aadress, Hind, Link) VALUES ('x', 'x', 'x')")
        k2sk = "INSERT INTO Mustamäe (Aadress, Hind, Link) VALUES (?, ?, ?)"
        i = 0
        d = 0
        while i < len(kinnisvara):
            c.execute(k2sk, (str(kinnisvara[d][0]), str(kinnisvara[d][1]), str(kinnisvara[d][2])))
            d += 1
            i += 1
        c.close()
        ühendus.commit()
        ühendus.close()
        print("Andmed on kantud andmebaasi.")
        e += 1
        input("Klikka jätkamiseks...")
    elif cmd == "vaata":
        jrknr = int(input("Sisesta järjekorranumber, mille kinnisvarahindu soovid vaadata: "))- 1
        jrknr2 = int(jrknr) + int(1)
        selekteeritud = str(k[jrknr].replace("  ", ""))
        ühendus = sqlite3.connect('KVdb.db')
        c = ühendus.cursor()
        c.execute("SELECT * FROM Mustamäe")
        c.execute("SELECT * FROM Mustamäe WHERE Aadress = ?", (selekteeritud,))

        z = 0
        selekteeritud_yksused = c.fetchall()
        while z < len(selekteeritud_yksused):
            print(selekteeritud_yksused[z][0] + " | Hind: "+ selekteeritud_yksused[z][1] + " € | " + selekteeritud_yksused[z][2])
            z += 1

        c.close()
        ühendus.commit()
        ühendus.close()
        e += 1
        input("Klikka jätkamiseks...")
    elif cmd == "katkesta":
        print("Katkestan ühenduse.")
        exit()
    else:
        print("Sisestatud on kehtetu käsk. Katkestan ühenduse.")
        exit()
    e = 0
