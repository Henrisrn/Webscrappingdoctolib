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

#driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe")    
#driver.get("https://www.doctolib.fr")
#time.sleep(4)
jobs=['osteopathe','psychologue','chiropracteur','dieteticien','psychomotricien']

full_table=[]
start=datetime.now()
count = 0

start_page=datetime.now()
for j in range(20):
        aa = pd.read_json("dossjson/sortiefin"+str(j)+".json")
        for i in range(len(aa["url"])):
                m = aa["url"][i]
                headers={'Refer':'https://www.doctolib.fr/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
                #driver.get("https://www.doctolib.fr"+str(m))
                print(m)
                a = requests.get("https://www.doctolib.fr/"+str(m),headers=headers)
                #soup=bs(driver.page_source,'lxml')
                #print(a.text)
                print(a.status_code)
                soup = bs(a.text, 'html.parser')
                d = soup.text
                my_bytes = str(soup.encode('utf-8'))
                e = my_bytes.split('div')
                
                
                if(a.status_code != 403):
                        soup = bs(a.text, 'html.parser')
                        d = soup.text
                #print(d)
                        my_bytes = str(soup.encode('utf-8'))
                        #print(my_bytes)
                        e = my_bytes.split('<script type="application/ld+json"')

                        f = e[2].split('<')
                        #print(f[0].replace(">","").replace(chr(92),""))
                        i = f[0].replace(">","").replace(chr(92),"")
                        #print(g)
                        b = open("dossjson/sortiefinpart2"+str(count)+".json","w")
                        b.write(f[0].replace(">","").replace(chr(92),""))
                        b.close
                        u = pd.read_json(f[0].replace(">","").replace(chr(92),""))
                        u.to_excel("dossjson/sortiefinpart2"+str(count)+".xlsx")
                        print(str(count)+"/800")
                        count+= 1
                time.sleep(4)
        time.sleep(3)