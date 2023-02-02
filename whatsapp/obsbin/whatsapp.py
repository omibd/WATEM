
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path)

import pandas as pd
import time, datetime
from dateutil.parser import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup
from collections import defaultdict

from wa_read import *
from wa_send import *
from w_xpath import *
from myname import *
from whfn import *
#import wh_sql as sq


class whapp(whapp_read,whapp_send):
    
    def __init__(self, chrome_driver ='chromedriver.exe'):
        #chrome_options = Options()
        #chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        #time.sleep(2)
        print(self.driver.title)
        self.chats_cnt = 0
        self.message = []
        self.unique_msg = []
        self.attempt = 0
        self.chats = {""}
        self.chats_unread = {}
        self.chats_unread_count = 0
        self.chats_list = []
        self.df_msg = pd.DataFrame()
        self.set_driver_rd(self.driver)
        self.set_driver_se(self.driver)
        self.msgdic = {}
        
    def _getdriver(self):
        return self.driver
    
    def _load(self, wait_sec=30):
        self.driver.refresh()
        pas = "please load failed despite wait for 1 minutes"
        for i in range(wait_sec):
            try:
                self.driver.find_element('xpath',"/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]")
                pas = "page loaded succefully"
                break
            except:
                time.sleep(1)
        print(pas)
        return pas
    
    def _select_chat(self, name, atm=0):
        rs = self._select_user_group(name)
        if rs == 1:
            return 1
        else:
            self._load()
            rs = self._select_user_group(name)
            time.sleep(3)
        try:
            nm = self.driver.find_element('xpath',selected_profile_header_name).text
            if name.lower() in nm.lower():
                print(name, ' is selected')
                return 1
            else:
                if atm == 0:
                    self._load()
                    self._select_chat(name,1)
                else:
                    print(name, ' selection failed')
                    return 0
        except:
            if atm == 0:
                self._load()
                self._select_chat(name,1)
            else:
                print(name, ' selection failed')
                return 0
    
    def _select_user_group(self, name):
        if self._is_element_present(By.XPATH, chat_search_box):
            try:
                elm = self.driver.find_element('xpath',chat_search_box)
                actions = ActionChains(self.driver)
                actions.move_to_element(elm).perform()
                actions.click(elm).perform()
                ActionChains(self.driver).send_keys(name).perform()
                ActionChains(self.driver).send_keys(Keys.RETURN).perform()
                time.sleep(2)
                return 1
            except:
                return -1
        else:
            return -1
    
    def _click_on(self, xpt):
        try:
            self.driver.find_element('xpath',xpt).click()
            time.sleep(1)
            return 1
        except:
            return 0
    
    def _read_message(self, chat_name, no_of_sms=10, atm=0):
        rs = self._select_chat(chat_name)
        try:
            no_of_sms = no_of_sms.strip()
        except:
            pass
        print(rs)
        if rs == 1:
            self._click_on(msg_nav_arrow)
            name = chat_name.replace('/','-')
            print('initiate msg reading on ', name, ' for sms no: ', no_of_sms)
            rs = self.read_message(int(no_of_sms), chat_name)
            if isinstance(rs, pd.DataFrame):
                return rs
            else:
                if atm == 0:
                    self._load()
                    self.read_message(name,no_of_sms,1)
                else:
                    return ''
            
    def _user(self):
        cntx = 0
        for i in range(1,40):
            name_1 = pane_username(i)
            notif = pane_notif(i)
            try:
                rs = self.driver.find_element('xpath', name_1).text
                L1 = len(self.chats)
                self.chats.add(rs)
                L2 = len(self.chats)
                if L2 > L1:
                    try:
                        nt = self.driver.find_element('xpath', notif).text
                        self.chats_unread[rs] = nt
                    except:
                        nt = 0
                    self.chats_unread_count = self.chats_unread_count + 1
                    print(self.chats_unread_count, ": ", rs," =>", nt)
            except:
                break
        
    def unread_message(self, initial = 0, scrolls=25):
        self._load()
        self.chats_unread_count = 0
        self.chats = {""}
        print('scrolling to collect unread sms')
        for i in range(0, scrolls):
            self._user()
            self.driver.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            initial += 300
        else:
            print('unread sms for groups')
            print(self.chats_unread)
            
            
x = whapp()
q = m