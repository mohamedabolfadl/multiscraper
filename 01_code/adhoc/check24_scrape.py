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
#import statistics as st



earliest_date = "2019-04-12"
return_date   = "2019-04-21"




#-- Hurghada
base_link_hur = "https://urlaub.check24.de/suche/hotel?areaId=673&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5&cateringList=fullboard,allinclusive&"

#-- Sharm
base_link_sha = "https://urlaub.check24.de/suche/hotel?areaId=674&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5&cateringList=fullboard,allinclusive&"

#-- Dubai
base_link_dub = "https://urlaub.check24.de/suche/hotel?areaId=764&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&"

#-- Antalya
base_link_ant = "https://urlaub.check24.de/suche/hotel?areaId=578&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

#-- Dominican
base_link_dom = "https://urlaub.check24.de/suche/hotel?areaId=696,697,698&countryId=32&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=co&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

#-- Thailand
base_link_tha = "https://urlaub.check24.de/suche/hotel?areaId=821&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

#-- Miami
base_link_mia = "https://urlaub.check24.de/suche/hotel?areaId=720&cityId=2405&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=ci&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&"

#-- Cancun
base_link_can = "https://urlaub.check24.de/suche/hotel?areaId=734&hotelId=233362&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&dhs=233362&ds=h&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

#-- Maldives
base_link_mal = "https://urlaub.check24.de/suche/hotel?areaId=1079&countryId=69&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate="+earliest_date+"&returnDate="+return_date+"&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

if(False):
    #-- Hurghada
    base_link_hur = "https://urlaub.check24.de/suche/hotel?areaId=673&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5&cateringList=fullboard,allinclusive&"
    
    #-- Sharm
    base_link_sha = "https://urlaub.check24.de/suche/hotel?areaId=674&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5&cateringList=fullboard,allinclusive&"
    
    #-- Dubai
    base_link_dub = "https://urlaub.check24.de/suche/hotel?areaId=764&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&"
    
    #-- Antalya
    base_link_ant = "https://urlaub.check24.de/suche/hotel?areaId=578&budget=&extendedSearch=1&sorting=categoryDistribution&order=asc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"
    
    #-- Dominican
    base_link_dom = "https://urlaub.check24.de/suche/hotel?areaId=696,697,698&countryId=32&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=co&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"
    
    #-- Thailand
    base_link_tha = "https://urlaub.check24.de/suche/hotel?areaId=821&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"
    
    #-- Miami
    base_link_mia = "https://urlaub.check24.de/suche/hotel?areaId=720&cityId=2405&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=ci&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&"
    
    #-- Cancun
    base_link_can = "https://urlaub.check24.de/suche/hotel?areaId=734&hotelId=233362&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&dhs=233362&ds=h&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&directFlight=1&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"
    
    #-- Maldives
    base_link_mal = "https://urlaub.check24.de/suche/hotel?areaId=1079&countryId=69&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&"

destinations = {"hurghada":base_link_hur,
                "sharm":base_link_sha,
                "dubai":base_link_dub,
"antalya":base_link_ant,
"dominican":base_link_dom,
"thailand":base_link_tha,
"miami":base_link_mia,
"cancun":base_link_can,
"maldives":base_link_mal

                }

j=1
for dest in destinations:
    print(dest)
    caps = DesiredCapabilities().CHROME
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  
    print("Creating driver")
    caps["pageLoadStrategy"] = "normal"  #  complete
    driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=r'C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/chromedriver.exe')
    driver.set_window_size(50, 50)
    print("Harvesting links")
    
    driver.get(destinations[dest])
    time.sleep(5)
    s=BeautifulSoup(driver.page_source)
    links = []
    elements = s.findAll("div",class_=re.compile("offer\-cnt"))
    for element in elements:
        if(element.find_next("a")):
            links.append(element.find_next("a").get('href'))
    
    
    hotel_name = []
    price =[]
    airport=[]
    days=[]
    departure=[]
    i=1
    print("Checking offer by offer")
    
    for link in links:
        print(str(i)+"/"+str(len(links)))
        try:
            driver.get(link)
            e=0
        except:
            print("Failed to retrieve link")
            e=1
        if(e==0):
            time.sleep(30)
            s=BeautifulSoup(driver.page_source)
            
            #-- Get the hotel name
            if(s.find_all("span",class_="hotelname")):
                hotel_name.append(s.find_all("span",class_="hotelname")[0].text.strip())
            else:
                print("Couldnt find Hotel name")
                hotel_name.append("-1")
        
            #-- Get Price
            if(s.find_all("span",class_="price-ele js-total-price")):
                price.append(s.find_all("span",class_="price-ele js-total-price")[0].get('data-total-price'))
            else:
                print("Couldnt find price")
                price.append("-1")
                
            #-- Get Airport
            if(s.find_all("span",class_="airport-info")):
                airport.append(s.find_all("span",class_="airport-info")[0].find("span").get('title'))
            else:
                print("Couldnt find airport")
                airport.append("-1")
        
            #-- Get Number of nights
            if(s.find_all("span",class_="duration")):
                days.append(s.find_all("span",class_="duration")[0].text.strip())
            else:
                print("Couldnt find number of nights")
                days.append("-1")
            if(s.find("div",class_="column-date successed")):
                departure.append(re.search("\d+\.\d+\.\d+",s.find("div",class_="column-date successed").text).group())
            else:
                print("Couldnt find Departure")
                departure.append("-1")
        i=i+1
        
    

    N_min =     min(len(price),len(links),len(days),len(airport),len(hotel_name),len(departure))
    if(len(price)>0):
        print("Creating df")
        df_curr= pd.DataFrame(
            {'price': price[0:N_min],
             'hotel':hotel_name[0:N_min],
     'aiport': airport[0:N_min],
     'days':days[0:N_min],
     'departure':departure[0:N_min],
     "link":links[0:N_min]
                })
        df_curr['Destination']=dest
    
    print("Appending")
    
    if (j==1 & len(price)>0):
        df=df_curr
    else:
        df=df.append(df_curr)
    print("Closing drivers")
    driver.close()
    driver.quit()
    j=j+1
    print("################################################")
          
          
          
          
          
df.to_csv('ch24_results.csv')      
          
          
          
          
#--- plots     

df['price']=df['price'].astype(float)          
          
df_sel = df[df['price']>0 ]
df_sel = df_sel[df_sel['price']<2500]
 
  

import plotly
import plotly.graph_objs as go
df_sel=df_sel.sort_values(['price'])

plotly.offline.plot({
    "data": [go.Bar(x=df_sel['hotel'], y=df_sel['price'],text=df_sel['Destination'])],
    "layout": go.Layout(title="Hotels")
}, auto_open=True)



















