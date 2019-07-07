# Purpose:
#  Scrape check24 for offers


import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
import re
import webcrawler



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

#-- Initialize Chrome driver
driver = initialize_driver()

#-- Initialize crawler class
c24 = webcrawler.Webcrawler("check24")
c24.setBaseURL("https://urlaub.check24.de/")


driverWithContent = get_content(driver,"https://urlaub.check24.de/suche/hotel?areaId=821&budget=&extendedSearch=1&sorting=categoryDistribution&order=desc&offerSort=price&offerSortOrder=asc&areaSort=topregion&areaSortOrder=asc&airport=CGN,DTM,DUS,EIN,FMO,FRA,HHN,KSF,LGG,LUX,MST,NRN,PAD,SCN,SXB&ds=r&travelDuration=5-6&departureDate=2019-02-01&returnDate=2019-12-31&adult=2&childrenCount=1&roomCount=1&children_0[age]=2&hotelCategoryList=5,4&cateringList=fullboard,allinclusive&")


pageBS=BeautifulSoup(driverWithContent.page_source,features="html.parser")
links = []
elements = pageBS.findAll("div",class_=re.compile("offer\-cnt"))




###############################
#--      JUNK               --#
###############################

#pip install selenium
#pip install pandas
