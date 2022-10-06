from urllib.robotparser import RequestRate
import pandas as pd
from selenium import webdriver
from lxml import etree
import time
from bs4 import BeautifulSoup as bs
import traceback
import requests
from datetime import datetime
import csv
import json
import mechanize
#driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe")    

#driver = mechanize.Browser()
#driver.set_handle_robots(False)
#driver.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')]
#resp = driver.open("https://www.doctolib.fr/osteopathe/france?page=1")
#print(resp.info())
#print(resp.read())
jobs=['osteopathe','psychologue','chiropracteur','dieteticien','psychomotricien']

full_table=[]
start=datetime.now()


start_page=datetime.now()
for j in range(1):
    try:
        headers={'Refer':'https://www.doctolib.fr/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        a = requests.get("https://www.doctolib.fr/osteopathe/france?page="+str(j),headers=headers)
        soup = bs(a.text, 'html.parser')
        d = soup.text
        #print(d)

        my_bytes = str(soup.encode('utf-8'))
        e = my_bytes.split('<script type="application/ld+json"')

        f = e[2].split('<')
        #print(f[0].replace(">","").replace(chr(92),""))
        i = f[0].replace(">","").replace(chr(92),"")
        #print(g)
        b = open("dossjson/sortiefin"+str(j)+".json","w")
        b.write(f[0].replace(">","").replace(chr(92),""))
        b.close
        u = pd.read_json(f[0].replace(">","").replace(chr(92),""))
        u.to_excel("dossjson/sortiefin"+str(j)+".xlsx")
        print(str(j)+"/800")
    except:
        continue