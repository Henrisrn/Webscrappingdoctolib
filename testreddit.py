from bs4 import BeautifulSoup
import requests
import urllib.request
import random
import time
import pandas as pd
import json
from selenium import webdriver
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True,indent=4)
    print(text)
# Request to website and download HTML contents

#Chaque spécialité a une id propre : Il faut donc les référencé
#Chaque personne a aussi une id propre du coup il faut donc les référencé
#https://www.doctolib.fr/search_results/6004813.json?limit=4&speciality_id=10&search_result_format=json&page=2

driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe")    
nom = ""
prenom = ""
driver.get("https://www.doctolib.fr")
#url='https://sdk.privacy-center.org/sdk.d8d9b3b0f63d7d5011309533a99e82ca765fcbd8.js'
for j in range(50):
    text = ""
    url = "https://www.doctolib.fr"
    #url = "https://www.doctolib.fr/search_results/6069977.json?limit=3&speciality_id=10&search_result_format=json&page=1"
    headers={'Refer':'https://www.doctolib.fr/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    req=requests.get(url,headers=headers)
    print(driver.get_network_conditions())
    url = "https://www.doctolib.fr/search_results/"+str(6004617+j)+".json?limit=4&speciality_id=10&search_result_format=json&page=2"
    print(url)
    #req=BeautifulSoup(driver.page_source,'lxml')
    content=req.json()
    for i in content:
        if(i == "search_result"):
            print(prenom)
            print(nom)
            print(content["search_result"]["first_name"])
            print(content["search_result"]["last_name"])
            if(prenom != content["search_result"]["first_name"] and nom != content["search_result"]["last_name"]):
                print("Rentre dans boucle")
                prenom = content["search_result"]["first_name"]
                nom = content["search_result"]["last_name"]
                a = open("output"+str(j)+".json","w")
                text = json.dumps(content, sort_keys=True,indent=4)
                b = a.write(text)
                a.close()
        print(i)
        time.sleep(random.randint(1,5))