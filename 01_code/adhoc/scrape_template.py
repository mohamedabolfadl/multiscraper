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



####### Read proxies ################

df_pr=pd.read_csv("C:/Users/Mohamed Ibrahim/Box Sync/bot/prod/proxies_with_speed.csv",sep=";")
idx = df_pr.groupby(['country'])['speed'].transform(max) == df_pr['speed']
df_pr = df_pr[idx]
df_pr = df_pr[df_pr['speed']>29]

#-- Read in scope countries
inscope=pd.read_csv("C:/Users/Mohamed Ibrahim/Box Sync/bot/prod/countries.csv",sep=",")

#-- Select only main countries
df_pr  = df_pr[df_pr['country'].isin( inscope['Code'])]


df_pr = df_pr.reset_index(drop=True)

country_codes = df_pr.country.unique()

###### Scrape ##############
i=0
prices = []
count = []
done_count = []
while(i<len(country_codes)):
    if(i!=28):
        print(str(i)+"/"+str(len(country_codes)))
        print(country_codes[i])
        df_sel = df_pr[df_pr['country'] == country_codes[i] ]
        
        df_sel = df_sel.reset_index()
        
        PROXY = str(df_sel.loc[0,'ip'])+":"+str(df_sel.loc[0,'port'])
        
        #-- Setup the driver
        print("Setting up the driver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument("--headless")  
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"  #  complete
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps, executable_path=r'C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/chromedriver.exe')
    #    driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        driver.implicitly_wait(10)
        driver.set_window_size(50,50)    
    #    link = "https://www.booking.com/hotel/ae/habtoor-grand-resort-spa.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaDuIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgM;sid=82b799de928963232b507b582106a108;age=1;all_sr_blocks=6730829_94284695_0_2_0;checkin=2019-03-01;checkout=2019-03-07;dest_id=-782831;dest_type=city;dist=0;group_adults=2;group_children=1;hapos=1;highlighted_blocks=6730829_94284695_0_2_0;hpos=1;req_adults=2;req_age=1;req_children=1;room1=A%2CA%2C1;sb_price_type=total;sr_order=popularity;srepoch=1546202844;srpvid=e9f4922d9d38008c;type=total;ucfs=1&#hotelTmpl"
    #    link = "https://www.booking.com/hotel/ae/habtoor-grand-resort-spa.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaDuIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgM;sid=82b799de928963232b507b582106a108;age=1;all_sr_blocks=6730829_94284695_0_2_0;checkin=2019-03-01;checkout=2019-03-07;dest_id=-782831;dest_type=city;group_adults=2;group_children=1;hapos=1;highlighted_blocks=6730829_94284695_0_2_0;hpos=1;no_rooms=1;req_adults=2;req_age=1;req_children=1;room1=A%2CA%2C1;sb_price_type=total;sr_order=popularity;srepoch=1546202844;srpvid=e9f4922d9d38008c;type=total;ucfs=1&;selected_currency=EUR;changed_currency=1;top_currency=1"
        link = "https://www.booking.com/hotel/do/occidental-grand-punta-cana.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaDuIAQGYAQm4ARfIAQzYAQPoAQGIAgGoAgM;sid=82b799de928963232b507b582106a108;age=1;all_sr_blocks=34534301_114174046_3_85_0;checkin=2019-02-01;checkout=2019-02-08;dest_id=-3364907;dest_type=city;group_adults=2;group_children=1;hapos=1;highlighted_blocks=34534301_114174046_3_85_0;hpos=1;no_rooms=1;req_adults=2;req_age=1;req_children=1;room1=A%2CA%2C1;sb_price_type=total;sr_order=popularity;srepoch=1546369105;srpvid=d816856897fd00b8;type=total;ucfs=1&;selected_currency=EUR;changed_currency=1;top_currency=1"
        #link = "https://www.booking.com/hotel/us/the-plymouth-miami-beach.en-gb.html?aid=304142;label=gen173nr-1DCAEoggI46AdIM1gEaDuIAQGYAQm4ARfIAQzYAQPoAQGIAgGoAgM;sid=82b799de928963232b507b582106a108;age=1;all_sr_blocks=166879605_109157800_3_1_0;checkin=2019-03-01;checkout=2019-03-07;dest_id=20023182;dest_type=city;group_adults=2;group_children=1;hapos=4;highlighted_blocks=166879605_109157800_3_1_0;hpos=4;nflt=class%3D5%3B;no_rooms=1;req_adults=2;req_age=1;req_children=1;room1=A%2CA%2C1;sb_price_type=total;sr_order=popularity;srepoch=1546272996;srpvid=f49672724d640029;type=total;ucfs=1&;selected_currency=EUR;changed_currency=1;top_currency=1"
        print("fetching the link")
        try:
            driver.get(link)
        except:
            print("Couldnt fetch")
        s=BeautifulSoup(driver.page_source)


#-- Booking
        elements = s.findAll("td",class_=re.compile("totalPrice"))
        print("Done")
        if(elements):
            if(elements[0].findAll("span")):
                pr=re.sub("\xa0"," ",re.sub("\n","",elements[0].findAll("span")[1].get_text()))
                print(pr)
                prices.append(pr)
                count.append(country_codes[i])
        else:
            prices.append("-1")
            print("Nothing found")
#-- Trivago
#        elements = s.findAll("span",class_=re.compile("font-trv-maincolor-05 fw-bold"))
#        print("Done")
#        if(elements):
#            if(elements[0].text):
#                pr= elements[0].text
#                print(pr)
#                prices.append(pr)
#                count.append(country_codes[i])
#        else:
#            prices.append("-1")
#            print("Nothing found")

    
    #    driver.close()
        driver.quit()
        print("#########################")
    i=i+1  
      
      
#-- trivago
link = "https://www.trivago.de/?aDateRange%5Barr%5D=2019-03-01&aDateRange%5Bdep%5D=2019-03-07&aPriceRange%5Bto%5D=0&aPriceRange%5Bfrom%5D=0&iPathId=549&aGeoCode%5Blat%5D=25.085922&aGeoCode%5Blng%5D=55.141243&iGeoDistanceItem=55326&iGeoDistanceLimit=20000&aCategoryRange=0%2C1%2C2%2C3%2C4%2C5&aOverallLiking=1%2C2%2C3%2C4%2C5&sOrderBy=relevance%20desc&bTopDealsOnly=false&iRoomType=7&cpt=5532602&iIncludeAll=0&iViewType=0&bIsSeoPage=false&bIsSitemap=false&"
driver.get(link)
s=BeautifulSoup(driver.page_source)
elements = s.findAll("span",class_=re.compile("font-trv-maincolor-05 fw-bold"))
elements[0].text

#-- limak limra
link = "https://limakhotels.hweb.com/en/limak-limra-hotel/2019-05-12/2019-05-18/2/"
driver.get(link)
s=BeautifulSoup(driver.page_source)
elements = s.findAll("span",class_=re.compile("bestDealPrice money"))
elements[0].get("amount")


#-- Booking.com
link = "https://www.booking.com/hotel/ae/habtoor-grand-resort-spa.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaDuIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgM;sid=82b799de928963232b507b582106a108;age=1;all_sr_blocks=6730829_94284695_0_2_0;checkin=2019-03-01;checkout=2019-03-07;dest_id=-782831;dest_type=city;dist=0;group_adults=2;group_children=1;hapos=1;highlighted_blocks=6730829_94284695_0_2_0;hpos=1;req_adults=2;req_age=1;req_children=1;room1=A%2CA%2C1;sb_price_type=total;sr_order=popularity;srepoch=1546202844;srpvid=e9f4922d9d38008c;type=total;ucfs=1&#hotelTmpl"
driver.get(link)
s=BeautifulSoup(driver.page_source)
elements = s.findAll("td",class_=re.compile("totalPrice"))
re.sub("\xa0"," ",re.sub("\n","",elements[0].findAll("span")[1].get_text()))


driver.close()





driver.quit()


