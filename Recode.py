import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import time
import traceback
from datetime import datetime
import csv
import requests
#driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe")
#driver.get("https://www.doctolib.fr/osteopathe/sainghin-en-melantois/philippe-moreau?pid=practice-75731")
#result_soup=BeautifulSoup(driver.page_source,'lxml')
#url = "https://www.doctolib.fr/osteopathe/sainghin-en-melantois/philippe-moreau?pid=practice-75731"
url = "https://www.lazada.sg/catalog/?_keyori=ss&from=input&q=mask"
requeee = requests.get(url)
soup=BeautifulSoup(requeee.text)
raw=soup.findAll('script')[3].text
page=pd.read_json(raw.split("window.pageData=")[1],orient='records')
#Store data
print(page)
#for item in page.loc['listItems','mods']:
#    brand_name.append(item['brandName'])
#    price.append(item['price'])
#    location.append(item['location'])
#    description.append(ifnull(item['description'],0))
#    rating_score.append(ifnull(item['ratingScore'],0))
