"""
Purpose
    Scrape and model prices of apartments in Dubai
    
    
    Input:
        NA
    Output:
        price | area | bedrooms | bathrooms | link | price_per_m csv for each neighbourhood
"""

#-- Clear variables
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("%reset  -sf")


####################################
#--      INPUT PARAMETERS        --#
####################################

MAX_PAGES = 30



####################################
#--      IMPORT LIBRARIES        --#
####################################




import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
import re
import statistics as st


####################################
#--      CLASS DEFINITIONS       --#
####################################

#-- Webcrawler class
class Webcrawler:

   def __init__(self, site_name, description=""):
    self.site_name = site_name
    self.description = description

   def setBaseURL(self,baseurl):
       self.baseurl = baseurl

   def setStartDate(self,start_date):
       self.start_date = start_date

   def setEndDate(self,end_date):
       self.end_date = end_date

   def setActiveLink(self,link):
       self.activelink= link
       
   def setPageNumber(self,pg):
       self.activelink=re.sub("page=\d+","page="+str(pg),self.activelink)

####################################
#--      FUNCTOI DEFINITIONS       --#
####################################

#-- Initialize selenium chrome driver
def initialize_driver(chromeDriverPath = r'C:/Users/Mohamed Ibrahim/Box Sync/bot/multiscraper/03_utils/chromedriver.exe'):
    caps = DesiredCapabilities().CHROME
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    print("Creating driver")
    caps["pageLoadStrategy"] = "normal"  #  complete
    driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=chromeDriverPath)
    driver.set_window_size(50, 50)
    return driver

#-- Get HTML content from website
def get_content(driver,url):
        driver.get(url)
        time.sleep(5)
        return driver

def getNumericFromElement(element_name, keyword):
        try:
            val = int(re.sub("\D","",element.find(element_name,class_=re.compile(keyword)).text))
        except:
            val = -1
        return val

def getObjectLink(element_name, keyword):        
    try:
        link= element.find(element_name,class_=re.compile(keyword)).get('href')
    except:
        link= ""
        pass
    return link

#-- Initialize Chrome driver
driver = initialize_driver()

#-- Initialize crawler class
dt = Webcrawler("dubai_property_finder")
dt.setBaseURL("https://www.propertyfinder.ae/")


#-- Links to areas
area_links = {
"downtown":
"en/search?c=2&l=41&ob=nd&page=1&rp=y&t=1",
"difc":
"en/search?c=2&l=39&ob=nd&page=1&rp=y&t=1",
 "sheikh_zayed":
"en/search?c=2&l=88&ob=nd&page=1&rp=y&t=1",
"jbr":
"en/search?c=2&l=67&ob=nd&page=1&rp=y&t=1",
 "business_bay":
"en/search?c=2&l=36&ob=nd&page=1&rp=y&t=1",
"marina":
"en/search?c=2&l=50&ob=nd&page=1&rp=y&t=1",
 "jlt":
"en/search?c=2&l=71&ob=nd&page=1&rp=y&t=1",
"palm_jumeirah":
"en/search?c=2&l=86&ob=nd&page=1&rp=y&t=1"}


    
    
    
for district in area_links.keys():

    if district != "downtown":
        print("Scraping "+str(district))

        #-- Get link of area
        dt.setActiveLink(area_links[district])
        
        #-- Initialize result
        df = pd.DataFrame(columns = ['price','area','bedrooms','bathrooms','link'])
        
        #-- Offer counter
        j = 1
        
        #-- Page counter
        i = 1
        FINISHED_PAGES = False
        
        while(not FINISHED_PAGES and i<=MAX_PAGES):
            print("Page = "+str(i))
        
        
            #-- Set URL to current page
            dt.setPageNumber(i)
            
            #-- Retrieve html content
            driverWithContent = get_content(driver,dt.baseurl+dt.activelink)
            
            
            #-- Format as Beautifulsoup
            bs=BeautifulSoup(driverWithContent.page_source,features="html.parser")
            
            
            #-- Get all offers in the page
            elements = bs.findAll("div",class_=re.compile("card\-list__item"))
            
            
            if(len(elements)<1):
                FINISHED_PAGES = True
                break
            else:
                i = i + 1
            #-- Get basic info from the offers
            for element in elements:
                
                
                #-- Get price
                prc = getNumericFromElement("span","price")
                #-- Get area
                area = getNumericFromElement("p","area")
                #-- Get bedrooms
                bedrooms = getNumericFromElement("p","bedroom")
                #-- Get bathrooms
                bathrooms = getNumericFromElement("p","bathroom")
                #-- Get link
                link = getObjectLink("a", "clickable")
        
        
                df.loc[j] = list([prc,area,bedrooms,bathrooms,link])
                j=j+1
        
        
        
        df['prc_per_m'] = df['price']/df['area']
        
        df_sel = df[df.prc_per_m>10]
        
        df_sel = df_sel.sort_values(by=['prc_per_m'])
        
        
        df_sel.to_csv('02_data/output/basic_offers_'+str(district)+'.csv')


######################################################################################################################


if False:

    #-- Median price per neighbourhood    
    for district in area_links.keys():
        df_sel = pd.read_csv('02_data/output/basic_offers_'+str(district)+'.csv')
        df_sel = df_sel[df_sel.bedrooms == 2]
        print(district+" "+str(round(st.median(df_sel['prc_per_m']))))

    
    df_sel = pd.read_csv('02_data/output/basic_offers_jbr.csv')
    
    for k in range(5):
        print(df_sel[ (df_sel['price']<100000) & (df_sel['bedrooms']>1)].iloc[k,5])
    
    
    for k in range(10):
        print(df_sel[df_sel.bedrooms==2].iloc[k,:])



import webbrowser


for district in area_links.keys():

    df_sel = pd.read_csv('02_data/output/basic_offers_'+str(district)+'.csv')
    df_sel = df_sel[(df_sel['price']<100000) & (df_sel['bedrooms']>1)]

    for k in range(3):
        print(k)
        if k<1:
            webbrowser.open_new(df_sel.iloc[k,5])
        else:
            webbrowser.open_new_tab(df_sel.iloc[k,5])
