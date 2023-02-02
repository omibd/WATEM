import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path)

import pandas as pd
import time, datetime
from dateutil.parser import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from collections import defaultdict


class whapp():
    
    def __init__(self, chrome_driver ='chromedriver.exe'):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        time.sleep(2)
        print(self.driver.title)
    
    def _is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
        
    def _load(self, wait_sec=60):
        self.driver.refresh()
        pas = "please load failed despite wait for 1 minutes"
        for i in range(wait_sec):
            try:
                self.driver.find_element_by_xpath(chat_search_box)
                pas = "page loaded succefully"
                break
            except:
                time.sleep(1)
        print(pas)
        return pas
    
    def _xpath(self, xpt, attempt=0):
        try:
            a1 = self.driver.find_element_by_xpath(xpt)
            ht = a1.get_attribute('innerHTML')
            return a1, ht
        except:
            if attempt == 0:
                self._xpath(xpt,1)
            else:
                return "0", "0"
    
    def gd(self):
        return self.driver
    
#selenium.getAttribute("(//div[@id='main']//div[@class='y8WcF']/div)[last()]/@data-id");
#(//div[@id='main']//div[@class='y8WcF']/div)[last()]/@data-id
x = whapp()._load()

