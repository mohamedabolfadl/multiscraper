# Purpose:
#  Scrape check24 for offers


import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
import re

#-- Initialize selenium chrome driver
def initialize_driver():
    caps = DesiredCapabilities().CHROME
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    print("Creating driver")
    caps["pageLoadStrategy"] = "normal"  #  complete
    driver = webdriver.Chrome( options=chrome_options,desired_capabilities=caps, executable_path=r'C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/chromedriver.exe')
    driver.set_window_size(50, 50)
    return driver

#-- Get HTML content from website
def get_content(driver,url):
        driver.get(url)
        time.sleep(5)
        return driver
