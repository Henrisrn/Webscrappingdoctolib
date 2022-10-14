import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import time
import traceback
import requests
from datetime import datetime
from io import StringIO
import csv
import json
import random
from selenium.webdriver.firefox.options import Options
import socket
#Strasbourg page 16
#Roubaix page 33
#Grenoble page 15
Listedevilldecharlatan = ["Rennes","Amiens","Pau","Clermont-Ferrand","Brest","Strasbourg","Bordeaux","Lille","Limoge","Besançon","Grenoble","Caen","Reims","Calais","Rouen","Anger","Avignon","Annecy","Roubaix"]


socket.getaddrinfo('localhost', 8080)
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True,indent=4)
    print(text)
driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (2)//chromedriver.exe")    

headers={'Refer':'https://www.doctolib.fr/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
jobs=['osteopathe','psychologue','chiropracteur','dieteticien','psychomotricien']
a = requests.Session()
full_df = []
#a.proxies = {
#  "http": "http://178.79.138.253",
#  "https": "http://178.79.138.253",
#}
#a.cookies()
full_table=[]
start=datetime.now()
#Mettre 905

full_df.head()

def numero_formatting(numero):
    if(len(numero)>0 and numero[0]=='0'):
        numero='+33 '+numero[1:]
    return numero

def text_formatting(text):
    if (text is None):
        return text
    text=text.replace('é','e')
    text=text.replace('è','e')
    text=text.replace('ê','e')
    text=text.replace('î','i')
    text=text.replace('à','a')
    text=text.replace('â','a')
    text=text.replace("'",'_')
    text=text.replace("ô",'o')
    text=text.replace("ç",'c')
    text=text.replace("É",'E')
    text=text.replace("È",'E')
    text=text.replace("À",'A')
    text=text.replace("Ù",'U')
    text=text.replace("Ç",'C')

    return text

def education_formatting(list):
    for index in range(len(list)):
        list[index]=(text_formatting(list[index][0]),list[index][1])

    return list

def to_upper(word):
    if (word is None):
        return word
    return word.upper()


full_df['Contact d_urgence']=full_df['Contact d_urgence'].apply(numero_formatting)
full_df['Nom']=full_df['Nom'].apply(text_formatting)
full_df['Nom']=full_df['Nom'].apply(to_upper)
full_df['Prenoms']=full_df['Prenoms'].apply(text_formatting)
full_df['Rue']=full_df['Rue'].apply(text_formatting)
full_df['Ville']=full_df['Ville'].apply(text_formatting)
full_df['Moyens de paiement']=full_df['Moyens de paiement'].apply(text_formatting)
full_df['Formations et experiences']=full_df['Formations et experiences'].apply(education_formatting)
#full_df['Formations et experiences']=full_df['Formations et experiences'].apply(text_formatting)




full_df['Visites a domicile']=full_df['Visites a domicile'].apply(numero_formatting)


full_df.head()
full_df.to_csv("all_jobs_2.csv",quoting=csv.QUOTE_ALL)
full_df.to_excel("all_jobs_2.xlsx" )

#,quoting=csv.QUOTE_ALL