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
#a.proxies = {
#  "http": "http://178.79.138.253",
#  "https": "http://178.79.138.253",
#}
#a.cookies()
full_table=[]
start=datetime.now()
#Mettre 905
try:
    for page in range(1,905):
        start_page=datetime.now()
        driver.get("https://www.doctolib.fr/osteopathe/france?page="+str(page))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        link = soup.find_all('a',class_="dl-link",href=True)
        tablink = []
        for i in link:
            if(len(tablink)>=1 and tablink[len(tablink)-1] != str(i['href']) and i['href'][0] == '/'):
                tablink.append(i["href"])
            if(len(tablink) == 0 and i['href'][0] == '/'):
                tablink.append(i['href'])
        time.sleep(random.randrange(7,11))
        
        for i in tablink:
            try:
                #driver.get("https://www.doctolib.fr"+str(url))
                #soup=BeautifulSoup(driver.page_source,'lxml')
                    #a = driver.get("https://www.doctolib.fr"+str(url))
                    print(i)
                    a = requests.get("https://www.doctolib.fr"+str(i),headers=headers)
                
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

                    job=i.split('/')[1]

                    if(len(soup.find_all('div',class_="dl-profile-row-content")[1].text)<1):
                        #print('no payment')
                        full_address=soup.find_all("div",class_="dl-profile-text")[1]
                    else:

                        #print('payment')
                        full_address=soup.find_all("div",class_="dl-profile-text")[2]
                    full_address=str(full_address).split("<")[-3].split(">")[1]
                    #print(full_address)
                    street=' '.join(full_address.split(',')[:-1])
                    rest=full_address.split(',')[-1].split(' ')
                    if(rest[0]==''):
                        zipcode=rest[1]
                        city=' '.join(rest[2:])
                    else:
                        zipcode=rest[0]
                        city=' '.join(rest[1:])
                    #print('rest',rest)
                    #print(zipcode,city)
                    if(len(soup.find_all('div',class_="dl-profile-row-content")[1].text)<1):
                        payment='n/a'
                    else:
                        payment=str(soup.find_all("div",class_='dl-profile-text')[1]).split('>')
                        if(len(payment)>3):
                            payment=payment[4].split('<')[0]
                        else:
                            payment=payment[1].split("<")[0]

                    diplomas=soup.find_all("div",class_="dl-profile-entry-label")
                    years=soup.find_all("div",class_='dl-profile-entry-time')
                    education_and_experience=[]
                    
                    for index in range(len(diplomas)):
                        name=diplomas[index].text
                        if(len(diplomas)==len(years)):
                            year=years[index].text
                        else: 
                            year ='n/a'
                        education_and_experience.append((name,year))
                    if(len(diplomas)!=len(years)):
                        #print('nb formations != nb dates :',len(diplomas),len(years))
                        #input()
                        time.sleep(0)

                    horaires_et_contact=soup.find_all('div',class_='dl-profile-box')
                    contact='n/a'
                    emergency_contact='n/a'
                    home='n/a'
                    for el in horaires_et_contact:
                        #print(el.text)
                        if('Horaires' in el.text):
                            #print('cas horaires')
                            time.sleep(1)
                        elif('urgence' in el.text):
                            #print('cas numero d_urgence')
                            emergency_contact=el.text.split(' ')
                            if (len(emergency_contact)>8):
                                emergency_contact=' '.join(emergency_contact[6:11])
                            else:
                                emergency_contact=emergency_contact[6]

                        elif('Coordonnées' in el.text):
                            #print('cas contact')
                            contact=el.text.split(' ')
                            number=[]   
                            number.append(contact[0][-2:])
                            number.extend(contact[1:])
                            contact=' '.join(number)
                        elif('domicile' in el.text):
                            #print('cas visites a domicile')
                            home=el.text.split(' ')
                            if(len(home)>1):
                                number=[]   
                                number.append(home[2][-2:])
                                number.extend(home[3:])
                                home=' '.join(number)
                            else:
                                home=home[0]
                        else:
                            #print('autre cas')
                            #input()
                            time.sleep(0)
                    #print(contact,";",emergency_contact,";",home)

                    adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                    try: 
                        rpps = soup.find_all('div',class_="dl-profile-row-section")[-2].text
                        if('RPPS' in rpps):
                            rpps_number=rpps.split('S')[1]
                            print("Numéro rpps = "+rpps_number)
                    except:
                        continue
                    adeli_number='n/a' 
                    rpps_number ='n/a'
                    if('ADELI' in adeli):
                        adeli_number=adeli[-9:]
                    if('RPPS' in adeli):
                        rpps_number=adeli.split('S')[1]
                        print("Numéro rpps = "+rpps_number)
                    
                    
                    print("Last Name : "+str(last_name))
                    print("First Name : "+str(first_name))
                    print("Job : "+str(job))
                    print("ADELI Number : "+str(adeli_number))
                    print("Street : "+str(street))
                    print("ZIP : "+str(zipcode))
                    print("RPPS Number : "+str(rpps_number))
                    full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,i,rpps_number])
                    #input()
                    
                    time_page=datetime.now()-start_page
                    print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
                    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien','Numero RPPS'])
                    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
                    time.sleep(random.randrange(7,11))
                    
            except:
                    print('error, skipping',i)
                    traceback.print_exc()
                    time.sleep(random.randrange(7,11))
                #f = my_bytes.split('<script type="application/ld+json"')[2].split('<')
                #f = my_bytes.split('<script type="application/ld+json"')[1].split('<')
                #hh = f[0].replace(">","").replace(slash,"")
                #jprint(str(hh))
                
            
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien','RPPS'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()

driver.quit()
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