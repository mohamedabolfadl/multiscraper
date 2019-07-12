"""
Purpose
    After running main script, this script will extract more details from the listing such as amenities etc.
    Input:
        basic_offers_xxx.csv
    Output:
        detailed_offers_xxx.csv with amenities, furnishment, desc text, etc
"""

#-- Clear variables
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("%reset  -f")




####################################
#--      INPUT PARAMETERS        --#
####################################

USE_CHROME = False


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
import os
from selenium.webdriver.firefox.options import Options

#-- Display settings
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)


#-- Make sure we are at root of project
os. chdir("C:\\Users\\Mohamed Ibrahim\\Box Sync\\bot\\multiscraper")



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
#--      FUNCTOI DEFINITIONS     --#
####################################

#-- Initialize selenium chrome driver
def initialize_driver(chromeDriverPath = r'C:/Users/Mohamed Ibrahim/Box Sync/bot/multiscraper/03_utils/chromedriver.exe'):
    caps = DesiredCapabilities().CHROME
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument('--no-proxy-server')
    #chrome_options.add_argument("--proxy-server='direct://'")
    #chrome_options.add_argument("--proxy-bypass-list=*")

    print("Creating driver")
    caps["pageLoadStrategy"] = "none"  #  'normal': Full  'none':Just HTML
    driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=chromeDriverPath)
    #driver.set_window_size(50, 50)
    return driver


def initialize_driver_firefox(firefoxDriverPath = r'C:/Users/Mohamed Ibrahim/Box Sync/bot/multiscraper/03_utils/geckodriver.exe'):
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "normal"  #  complete
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(desired_capabilities=caps, executable_path= firefoxDriverPath, options=options)
    return driver

#-- Get HTML content from website
def get_content(driver,url):
        driver.get(url)
        time.sleep(1)
        return driver

#-- Get numeric value from an offer
def getNumericFromElement(element_name, keyword):
        try:
            val = int(re.sub("\D","",element.find(element_name,class_=re.compile(keyword)).text))
        except:
            val = -1
        return val

#-- Get link of an offer
def getObjectLink(element_name, keyword):        
    try:
        link= element.find(element_name,class_=re.compile(keyword)).get('href')
    except:
        link= ""
        pass
    return link


#-- Extract amenities from offer
def extractAmenities(bs):
    amenities = bs.find_all("div", class_=re.compile("amenities__content"))
    res = []
    for am in amenities:
        res.append(am.text.lower().strip())


    return res


            #-- Trend
def getTrend(bs):
    try:
        trend = bs.find("span",class_=re.compile("market\-trends__sub.*")).text.strip()
    except:
        trend = ""
        pass
    
    return trend

#-- comp
def getComparisons(bs):
    try:
        cmps = bs.find_all("strong",class_=re.compile("market\-trends__header.*"))
        comparisons = []
        for tr in cmps:
            comparisons.append(tr.text.lower().strip())
            
        if len(comparisons)<2:
            comparisons = ['','']
   
    except:
        comparisons = ['','']
        pass
    
    return comparisons            
            
            #-- description
def getOfferDdescription(bs):
    try:
        desc = bs.find("div",class_=re.compile("text\-trim.*")).text.lower().strip()
    except:
        desc = ""
        pass
    
    return desc
            
#-- Agency
def getAgency(bs):
    try:
        agency = bs.find("div",class_=re.compile("agent\-info__detail\-content agent\-info__detail\-content\-\-bold")).text.lower().strip()
    except:
        agency = ""
        pass
    
    return agency
            
            #-- Location
def getLocationInfo(bs):
    try:
        loc = re.sub("apartment for rent in ","",bs.find("h2",class_="property-header__sub-title").text.lower().strip())
    except:
        loc = ""
        pass
    
    return loc
            
            
            #-- Furnishing
def getFurnishmentInfo(bs):
    try:
        furnish = bs.find("div", string = re.compile("Furnishings")).parent.find("div", class_=re.compile("facts__content")).text
    except:
        furnish = ""
        pass
    
    return furnish
            
            
            

#-- Initialize Chrome driver
    

if USE_CHROME:
    driver = initialize_driver()
else:
    driver = initialize_driver_firefox()



#-- Initialize crawler class
dt = Webcrawler("dubai_property_finder")
dt.setBaseURL("https://www.propertyfinder.ae/")


#-- Links to areas
area_links = {
#"downtown":
#"en/search?c=2&l=41&ob=nd&page=1&rp=y&t=1",
#"difc":
#"en/search?c=2&l=39&ob=nd&page=1&rp=y&t=1",
# "business_bay":
#"en/search?c=2&l=36&ob=nd&page=1&rp=y&t=1",
#"marina":
#"en/search?c=2&l=50&ob=nd&page=1&rp=y&t=1",
 "sheikh_zayed":
"en/search?c=2&l=88&ob=nd&page=1&rp=y&t=1",
"jbr":
"en/search?c=2&l=67&ob=nd&page=1&rp=y&t=1",
 "jlt":
"en/search?c=2&l=71&ob=nd&page=1&rp=y&t=1",
"palm_jumeirah":
"en/search?c=2&l=86&ob=nd&page=1&rp=y&t=1"}


    
    
    
for district in area_links.keys():

    print('District = '+str(district))
    
    df_sel = pd.read_csv('02_data/output/basic_offers_'+str(district)+'.csv')

    
    if df_sel.shape[0]>10:

        
        
        #-- Initialize res
        df = pd.DataFrame(columns = ['price','area','bedrooms','bathrooms','prc_per_m','amenities','furnishment','location','agency','description','comaprisons_price','comaprisons_area','trend', 'link'])
        
        #-- Offer counter
        i = 0
        
        #-- Loop over each offer
        while i<df_sel.shape[0]:
            
            if(i%20==0):
                print("Object="+str(i)+"/"+str(df_sel.shape[0])+" "+str(round(100*i/df_sel.shape[0]))+"%")
                
                
            #start_time = time.time()
            
            #-- Get HTML
            driverWithContent = get_content(driver,df_sel.loc[i,'link'])
        
            
            #-- BS format
            bs=BeautifulSoup(driverWithContent.page_source,features="html.parser")
            
            
            #-- Amenities
            amenities = extractAmenities(bs)
            amenities = '|'.join(amenities)

            #-- Get furnishing info
            furnish = getFurnishmentInfo(bs)


            #-- Get location 
            loc = getLocationInfo(bs)
            

            #-- Agency
            agency = getAgency(bs)
            
            
            #-- Description text
            desc = getOfferDdescription(bs)
            

            #--Comparison to other apartments
            comparisons = getComparisons(bs)
            
            

            #-- Trend in the area
            trend = getTrend(bs)
                
              
            #-- Append this offer
            df.loc[i] = list([df_sel.loc[i,'price'],
                             df_sel.loc[i,'area'],
                             df_sel.loc[i,'bedrooms'],
                             df_sel.loc[i,'bathrooms'],
                             df_sel.loc[i,'prc_per_m'],
                             amenities,
                             furnish,
                             loc,
                             agency,
                             desc,
                             comparisons[0],
                             comparisons[1],
                             trend,
                             df_sel.loc[i,'link']
                             ])
            
            # Time code
            # print(round(time.time() - start_time))    

            i=i+1
     


        df.to_csv('02_data/output/detailed_offers_'+str(district)+'.csv')        
        























if False:



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





if False:

    
    df_sel = pd.read_csv('02_data/output/basic_offers_jbr.csv')
    
    for k in range(5):
        print(df_sel[ (df_sel['price']<100000) & (df_sel['bedrooms']>1)].iloc[k,5])
    
    
    for k in range(10):
        print(df_sel[df_sel.bedrooms==2].iloc[k,:])



import webbrowser


for district in area_links.keys():
    df_sel = pd.read_csv('02_data/output/basic_offers_'+str(district)+'.csv')
    df_sel = df_sel[df_sel.bedrooms == 2]
    print(district+" "+str(round(st.median(df_sel['prc_per_m']))))

    df_sel = df_sel[(df_sel['price']<100000) & (df_sel['bedrooms']>1)]

    for k in range(3):
        print(k)
        if k<1:
            webbrowser.open_new(df_sel.iloc[k,5])
        else:
            webbrowser.open_new_tab(df_sel.iloc[k,5])
