import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import time
import traceback
from datetime import datetime
import csv
import requests


jobs=['osteopathe','psychologue','chiropracteur','dieteticien','psychomotricien']

full_table=[]
start=datetime.now()
try:
    for page in range(1,905):
        start_page=datetime.now()
        a = requests.get("https://www.doctolib.fr/osteopathe/france?page="+str(page))
        result_soup=BeautifulSoup(a.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                full_link="https://www.doctolib.fr"+link
                b = requests.get(full_link)
                soup=BeautifulSoup(b,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done osteopathes! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Psychologues

# %%
try:
    for page in range(391,528):
        start_page=datetime.now()
        c = requests.get("https://www.doctolib.fr/psychologue/france?page="+str(page))
        result_soup=BeautifulSoup(c,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                full_link="https://www.doctolib.fr"+link
                d = requests.get(full_link)
                soup=BeautifulSoup(d,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)
                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done psychologues! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Chiropracteurs

# %%
try:
    for page in range(1,46):
        start_page=datetime.now()
        g = requests.get("https://www.doctolib.fr/chiropracteur/france?page="+str(page))
        result_soup=BeautifulSoup(g.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)
        #print(search_results[0])
        #input()
        for result in search_results:
            try:
                #link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                link=result.find('a',class_="dl-link")['href']
                #print(link)
                
                full_link="https://www.doctolib.fr"+link
                h = requests.get(full_link)
                soup=BeautifulSoup(h,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done chiropracteurs! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Diététicien

# %%
try:
    for page in range(1,177):
        start_page=datetime.now()
        h = requests.get("https://www.doctolib.fr/dieteticien/france?page="+str(page))
        result_soup=BeautifulSoup(h.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                #link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                i = requests.get(full_link)
                soup=BeautifulSoup(i.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)
                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done dieteticiens! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Psychomotricien

# %%
try:
    for page in range(1,27):
        start_page=datetime.now()
        j = requests.get("https://www.doctolib.fr/psychomotricien/france?page="+str(page))
        result_soup=BeautifulSoup(j.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                #link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                u = requests.get(full_link)
                soup=BeautifulSoup(u.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)
                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done psychomotriciens! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %%
try:
    for page in range(1,27):
        start_page=datetime.now()
        v = requests.get("https://www.doctolib.fr/psychomotricien/france?page="+str(page))
        result_soup=BeautifulSoup(v.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                #link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                t = requests.get(full_link)
                soup=BeautifulSoup(t.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)
                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done psychomotriciens! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Ergotherapeutes

# %% [markdown]
# ## pedicure podologue

# %%
try:
    for page in range(1,349):
        start_page=datetime.now()
        r = requests.get("https://www.doctolib.fr/pedicure-podologue/france?page="+str(page))
        result_soup=BeautifulSoup(r.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                b = requests.get(full_link)
                soup=BeautifulSoup(b.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)
                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("all_jobs.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done pedicures podologues! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## Sophrologues

# %%
try:
    for page in range(1,160):
        start_page=datetime.now()
        aa = requests.get("https://www.doctolib.fr/sophrologue/france?page="+str(page))
        result_soup=BeautifulSoup(aa.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                bb = requests.get(full_link)
                soup=BeautifulSoup(bb.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)

                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done sophrologues! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## hypnothérapeutes

# %%
try:
    for page in range(1,273):
        start_page=datetime.now()
        cc = requests.get("https://www.doctolib.fr/hypnotherapeute/france?page="+str(page))
        result_soup=BeautifulSoup(cc.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                dd = requests.get(full_link)
                soup=BeautifulSoup(dd.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)

                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done hypnotherapeutes! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## psychanalystes

# %%
try:
    for page in range(1,117):
        start_page=datetime.now()
        ee = requests.get("https://www.doctolib.fr/psychanalyste/france?page="+str(page))
        result_soup=BeautifulSoup(ee.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                ff = requests.get(full_link)
                soup=BeautifulSoup(ff.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)

                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done psychanalystes! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## naturopathes

# %%
try:
    for page in range(1,85):
        start_page=datetime.now()
        gg = requests.get("https://www.doctolib.fr/naturopathe/france?page="+str(page))
        result_soup=BeautifulSoup(gg.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                hh = requests.get(full_link)
                soup=BeautifulSoup(hh.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)

                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done naturopathes! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %% [markdown]
# ## acupuncteur

# %%
try:
    for page in range(1,41):
        start_page=datetime.now()
        ii = requests.get("https://www.doctolib.fr/acupuncteur/france?page="+str(page))
        result_soup=BeautifulSoup(ii.text,'lxml')
        search_results = result_soup.find_all('div',class_="dl-search-result")
        time.sleep(4)

        for result in search_results:
            try:
                link=result.find('a',class_="dl-search-result-name js-search-result-path")['href']
                #link=result.find('a',class_="dl-link")['href']
                full_link="https://www.doctolib.fr"+link
                jj = requests.get(full_link)
                soup=BeautifulSoup(jj.text,'lxml')

                if(len(soup.find_all('div',class_="dl-profile-row-content"))<2):
                    break

                name=etree.HTML(str(soup)).xpath('//span[@itemprop="name"]')[0].text
                name_list=name.split(' ')
                last_name=name_list[-1]
                first_name=' '.join(name_list[:-1])
                job=link.split('/')[1]

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
                if(len(diplomas)==len(years)):
                    #print('nb formations != nb dates :',len(diplomas),len(years))
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
                        time.sleep(0)

                        #input()
                #print(contact,";",emergency_contact,";",home)

                adeli=soup.find_all('div',class_="dl-profile-row-section")[-1].text
                if('ADELI' in adeli):
                    adeli_number=adeli[-9:]
                else :
                    adeli_number='n/a' 

                full_table.append([last_name,first_name,job,adeli_number,street,zipcode,city,payment,education_and_experience,contact,emergency_contact,home,full_link])
                #input()
            except:
                print('error, skipping',full_link)
                traceback.print_exc()
        
        time_page=datetime.now()-start_page
        print("page "+str(page)+" done;",'time taken for 20 profils : ',time_page)
        full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
        full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')

    print('all done acupuncteurs! Time taken :',datetime.now()-start)
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    
except Exception:
    full_df= pd.DataFrame(full_table,columns=['Nom','Prenoms','Profession','No ADELI','Rue','Code Postal','Ville','Moyens de paiement','Formations et experiences','Contact',"Contact d_urgence","Visites a domicile",'Lien'])
    full_df.to_csv("osteopathes.csv",quoting=csv.QUOTE_ALL,quotechar='"')
    print('something went wrong')
    traceback.print_exc()


# %%
full_df.head()

# %%
def numero_formatting(numero):
    if(len(numero)>0 and numero[0]=='0'):
        numero='+33 '+numero[1:]
    #print('numero formatté : '+numero)
    return numero

# %%
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

# %%
def education_formatting(list):
    for index in range(len(list)):
        list[index]=(text_formatting(list[index][0]),list[index][1])

    return list

# %%
def to_upper(word):
    if (word is None):
        return word
    return word.upper()

# %%
#cleaning
full_df['Contact d_urgence']=full_df['Contact d_urgence'].apply(numero_formatting)
full_df['Nom']=full_df['Nom'].apply(text_formatting)
full_df['Nom']=full_df['Nom'].apply(to_upper)
full_df['Prenoms']=full_df['Prenoms'].apply(text_formatting)
full_df['Rue']=full_df['Rue'].apply(text_formatting)
full_df['Ville']=full_df['Ville'].apply(text_formatting)
full_df['Moyens de paiement']=full_df['Moyens de paiement'].apply(text_formatting)
full_df['Formations et experiences']=full_df['Formations et experiences'].apply(education_formatting)
#full_df['Formations et experiences']=full_df['Formations et experiences'].apply(text_formatting)



# %%
full_df['Visites a domicile']=full_df['Visites a domicile'].apply(numero_formatting)


# %%
full_df.head()

# %%
full_df.to_csv("all_jobs_2.csv",quoting=csv.QUOTE_ALL )
