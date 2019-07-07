# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 22:01:56 2018

@author: Mohamed Ibrahim
"""

#import numpy as np
#import matplotlib.pyplot as plt

import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
import re

#driver = webdriver.PhantomJS(executable_path='C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/phantomjs-2.1.1-windows/bin/phantomjs.exe')
#driver.set_window_size(50, 50)

caps = DesiredCapabilities().CHROME
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  
caps["pageLoadStrategy"] = "normal"  #  complete
driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=r'C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/chromedriver.exe')


#-- Requests
#import requests
#r = requests.get(link)
#s=BeautifulSoup(r.text)

###############################################################################
print("Scraping proxylistplus.com")


i=1
while (i<6):
    print("Starting loop "+str(i))
    #link = "https://list.proxylistplus.com/SSL-List-1"
    link = "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-"+str(i)
    
    driver.get(link)
    print("finished fetching")
    s=BeautifulSoup(driver.page_source)
    
    
    elements= s.findAll("tr",class_="cells")
    ips = []
    ports=[]
    country = []
    print("Analyzing")
    for element in elements:
        if(len(element.findAll("td"))>4):
            if(element.findAll("td")[1]):
                ips.append(element.findAll("td")[1].get_text())
            if(element.findAll("td")[2]):
                ports.append(element.findAll("td")[2].get_text())
            if(element.findAll("td")[4]):
                country.append(element.findAll("td")[4].get_text())
        
        
        
    
    print("We got "+str(len(ips))+" ips")
    
    if(len(ips)>5):
        print("appending")
        if(i==1):
            df= pd.DataFrame(
                {'ip': ips,
                 'port': ports,
                 'country': country
                })
        else:
            df_curr= pd.DataFrame(
                {'ip': ips,
                 'port': ports,
                 'country': country
                })
            df=df.append(df_curr)
    
    
    i=i+1
    print("Sleeping a bit")
    time.sleep(2)

###############################################################################
print("##############################################################################")
print("Scraping ssl.proxies")


link = "https://www.sslproxies.org/"

driver.get(link)
time.sleep(5)
s=BeautifulSoup(driver.page_source)
elements_odd = s.findAll("tr",class_="odd")
elements_even= s.findAll("tr",class_="even")


ips = []
ports=[]
country = []
for element in elements_odd:
          
    ips.append(element.findAll("td")[0].get_text())
    ports.append(element.findAll("td")[1].get_text())
    country.append(element.findAll("td")[3].get_text())

for element in elements_even:
          
    ips.append(element.findAll("td")[0].get_text())
    ports.append(element.findAll("td")[1].get_text())
    country.append(element.findAll("td")[3].get_text())



df_curr= pd.DataFrame(
    {'ip': ips,
     'port': ports,
     'country': country
    })

df=df.append(df_curr)

df.to_csv("C:/Users/Mohamed Ibrahim/Box Sync/bot/prod/proxies.csv", sep=';')


##############################################################################
print("##############################################################################")
print("Scraping spys.one")
#-- Get country codes
link="http://spys.one/en/proxy-by-country/"
driver.get(link)
time.sleep(5)
s=BeautifulSoup(driver.page_source)


elements= s.findAll("tr",class_="spy1x")
country_codes = []
for element in elements:
    code = element.find("font",class_="spy4").get_text()
    if(len(code)==2):
        country_codes.append(code)


df_country_codes = pd.DataFrame({'code':country_codes})


N_count = len(country_codes)
i=1

for curr_country_code  in country_codes:

    #curr_country_code = str(df_country_codes.loc[3,'code'])
    print("Scarping "+curr_country_code+ " "+str(i)+"/"+str(N_count))
    link="http://spys.one/free-proxy-list/"+curr_country_code +"/" 
    
    #link="http://spys.one/free-proxy-list/SE/" 
    
    
    driver.get(link)
    time.sleep(1)
    s=BeautifulSoup(driver.page_source)
    
    print("Got "+str(len(elements))+" elements")
    
    elements= s.findAll("tr",class_=re.compile("spy1x+"))
    
    
    if(len(elements)>2):
        ips = []
        ports=[]
        speed=[]
        for element in elements:
            if(element.find("font",class_="spy14")):
                if (re.match("\d+\.\d+.\d+.\d+",element.find("font",class_="spy14").text)):
                    ips.append(re.match("\d+\.\d+.\d+.\d+",element.find("font",class_="spy14").text).group())
                if (re.search("\d+$",element.find("font",class_="spy14").text)):
                    ports.append(re.search("\d+$",element.find("font",class_="spy14").text).group())
                if(element.findAll("table",width=re.compile("\d+$"))):
                    speed.append(element.find("table",width=re.compile("\d+$")).get('width'))
                    
    if i==1:
        df_res= pd.DataFrame(
            {'ip': ips,
             'port': ports,
             'country': curr_country_code,
             'speed' :speed
            })
    else:
        df_curr= pd.DataFrame(
            {'ip': ips,
             'port': ports,
             'country': curr_country_code,
             'speed' :speed
            })
        df_res=df_res.append(df_curr)    
    
    #print("Sleeping a bit")    
    time.sleep(1)    
    i=i+1



df_res.to_csv("C:/Users/Mohamed Ibrahim/Box Sync/bot/prod/proxies_with_speed.csv", sep=';')





driver.quit()
