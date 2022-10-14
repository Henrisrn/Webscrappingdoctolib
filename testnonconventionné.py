from numpy import full
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

full_table=[]
start=datetime.now()
#Mettre 905
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
start=datetime.now()
try:
    for page in range(16,528):
        start_page=datetime.now()
        driver.get("https://www.doctolib.fr/osteopathe/grenoble?page=")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        link = soup.find_all('a',class_="dl-link",href=True)
        tablink = []
        for i in link:
            if(len(tablink)>=1 and tablink[len(tablink)-1] != str(i['href']) and i['href'][0] == '/'):
                tablink.append(i["href"])
            if(len(tablink) == 0 and i['href'][0] == '/'):
                tablink.append(i['href'])
        time.sleep(random.randrange(7,11))
        for result in tablink:
            try:
                a = requests.get("https://www.doctolib.fr"+str(result),headers=headers)
                soup = BeautifulSoup(a.text,'lxml')
                my_bytes = str(soup.encode('utf-8'))
                time.sleep(1)
                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    continue

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                if(len(first_name)>15 or len(last_name)>15):
                        continue
                job=result.split('/')[1]
                full_address = ""
                contact='n/a'
                if(len(soup.find_all("div",class_="dl-profile-text"))==2):
                    contact = soup.find_all('div',class_="dl-profile-row-content")[0].text.split("Téléphone")[1]
                    full_address = soup.find_all('div',class_="dl-profile-row-content")[1].text.split("Informations d'accès")[1]
                    zipcode = full_address.split(" ")[-2]
                    city = full_address.split(" ")[-1]
                    street = ""
                    for iooj in full_address.split(" ")[:-2]:
                        street += str(iooj+" ")
                elif(len(soup.find_all("div",class_="dl-profile-text"))>2):
                    full_address=soup.find_all("div",class_="dl-profile-text")[2]
                    full_address=str(full_address).split("<")[-3].split(">")[1]
                else:
                #print(full_address)
                    street=' '.join(full_address.split(',')[:-1])
                    rest=full_address.split(',')[-1].split(' ')
                    if(rest[0]=='' and len(rest)>1):
                        zipcode=rest[1]
                        city=' '.join(rest[2:])
                    else:
                        zipcode=rest[0]
                        city=' '.join(rest[1:])
                
                
                
                adeli_number='n/a' 
                rpps_number ='n/a'
                
                full_table.append([last_name,first_name,job,street,zipcode,city,contact,result])
                #input()
                print("Last Name : "+str(last_name))
                print("First Name : "+str(first_name))
                print("Job : "+str(job))
                print("Street : "+str(street))
                print("ZIP : "+str(zipcode))
                print("Contact : "+str(contact))
                time.sleep(random.randrange(7,11))
            except:
                print('error, skipping',result)
                traceback.print_exc()
                time.sleep(random.randrange(7,11))
            break
            
        break
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','Rue','Code Postal','Ville','Contact','Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()
#a.proxies = {
#  "http": "http://178.79.138.253",
#  "https": "http://178.79.138.253",
#}
#a.cookies()

full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','Rue','Code Postal','Ville','Contact','Lien'])
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

full_df['Nom']=full_df['Nom'].apply(text_formatting)
full_df['Nom']=full_df['Nom'].apply(to_upper)
full_df['Prenoms']=full_df['Prenoms'].apply(text_formatting)
full_df['Rue']=full_df['Rue'].apply(text_formatting)
full_df['Ville']=full_df['Ville'].apply(text_formatting)


full_df.head()
full_df.to_csv("all_jobs_2.csv",quoting=csv.QUOTE_ALL)
full_df.to_excel("all_jobs_2.xlsx" )

#,quoting=csv.QUOTE_ALL