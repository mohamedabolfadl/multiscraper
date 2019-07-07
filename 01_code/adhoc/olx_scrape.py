# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 11:58:58 2018

@author: Mohamed Ibrahim
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 22:04:51 2018

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
import statistics as st




caps = DesiredCapabilities().CHROME
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  

caps["pageLoadStrategy"] = "normal"  #  complete
driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=r'C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/chromedriver.exe')



#driver = webdriver.PhantomJS(executable_path='C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/phantomjs-2.1.1-windows/bin/phantomjs.exe')
#driver.set_window_size(50, 50)

#-- Rehab
base_link = "https://olx.com.eg/en/properties/properties-for-sale/rehab-city/?search%5Bfilter_float_price%3Afrom%5D=600000&search%5Bfilter_float_price%3Ato%5D=2500000&search%5Bfilter_float_area%3Afrom%5D=120&page="
#-- Madinaty
#base_link = "https://olx.com.eg/en/properties/properties-for-sale/Madinaty/?search%5Bfilter_float_price%3Afrom%5D=600000&search%5Bfilter_float_price%3Ato%5D=2500000&search%5Bfilter_float_area%3Afrom%5D=120&page="


#-- Harvest links
links=[]
i=1
print("Harvesting links")
while(i<11):
    link = base_link +str(i)
    print(i)
    driver.get(link)
    s=BeautifulSoup(driver.page_source)
    
    
    elements = s.findAll("div",class_=re.compile("ads__item__info"))
    for element in elements:
        if(element.find("a")):
            links.append(element.find("a").get('href'))
    time.sleep(2)
    i=i+1
    

#-- Check offer by offer
print("Checking offer by offer")
area = []
price=[]
bedrooms=[]
i=1
active_links = []
links_sel = links
for link in links_sel:
    if(re.search("user",link)):
        print("User link")
    else:
        prices_added = 0
        area_added = 0
        active_links.append(link)
        print(i)
        driver.get(link)
        s=BeautifulSoup(driver.page_source)
        if(s.find("strong",class_="xxxx-large margintop7 block arranged")):
            price.append(s.find("strong",class_="xxxx-large margintop7 block arranged").text)
            prices_added=1
            
        elif(s.find("strong",class_="xxxx-large margintop7 block not-arranged")):
            price.append(s.find("strong",class_="xxxx-large margintop7 block not-arranged").text)
            prices_added=1
                    
        if(s.find("th",text=re.compile("المساحة"))):
            if(s.find("th",text=re.compile("المساحة")).find_next("td",class_="value")):
                if(s.find("th",text=re.compile("المساحة")).find_next("td",class_="value").find_next("strong")):
                    area.append(s.find("th",text=re.compile("المساحة")).find_next("td",class_="value").find_next("strong").text.strip())
                    area_added=1
                    
        if (prices_added<1):
            price.append('999999999')
        if(area_added<1):
            area.append('999999999')
            
        i=i+1


df_curr= pd.DataFrame(
        {'price': price,
'area': area,
 'link':active_links
            })


#-- replace all nondigits in price    
df_curr['price']=df_curr['price'].str.replace("\D",'')
df_curr['price'] = df_curr['price'].astype(float)
df_curr['area']=df_curr['area'].str.replace("\D",'')
df_curr['area'] = df_curr['area'].astype(float)

df_curr['price_area']=df_curr['price']/df_curr['area']

st.median(df_curr['price_area'])

#df_curr.to_csv("rehab.csv")
#df_curr.to_csv("madinaty.csv")

driver.close()
driver.quit()


