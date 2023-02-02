import os, sys, time, subprocess
from collections import defaultdict
import datetime as dt
from dateutil.parser import *
import time as tm
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
mypath = os.path.dirname(os.path.realpath('.')) #'__file__'
sys.path.insert(0,mypath)
#from whatsapp import *


# ### Developed Scrap Functions 

# In[26]:


def xc(driver, xpt, click=True): #clickable
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpt)))
        if click: element.click()
        else: return element
    except: return False    

def xfill(driver, xpt, txt=None, search_only =True):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpt))) if type(xpt) is str else xpt
    if element != False:
        element.clear()
        ac = ActionChains(driver)
        ac.move_to_element(element).click().perform()
        if txt is not None and chr(10) in txt and search_only==False:
            xx = txt.split(chr(10))
            for line in xx:
                ac.send_keys(line).perform()
                ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ac.send_keys(Keys.RETURN).perform()
        elif txt is not None and search_only==False:
            ac.send_keys(name).send_keys(Keys.RETURN).perform()
        elif txt is not None and search_only==True:
            ac.send_keys(name).perform()


def bs_div_attr(html, search_attr='data-pre-plain-text',tag="div"):
    sp = BeautifulSoup(html, "lxml")
    x = sp.find_all(tag)
    for i in x:
        try:
            st = i[search_attr]
            break
        except:pass
    else: return None, None
    try:
        split_point = st.find(']')
        sender = st[split_point+1:].replace(':','').strip(' ')
        dttm = parse(st[1:split_point].upper())
        return dttm.strftime("%Y-%m-%d %H:%M"), sender
    except: None, None
        
def xpob(driver, xpt):
    wait = WebDriverWait(driver, 2)
    try: return wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
    except: return False
    
def msg_scrap(driver, n=4, base="(//div[@id='main']//div[@class='ItfyB _3nbHh'])"):
    msgdiv = base + "[" + str(n) + "]"
    try: ActionChains(driver).move_to_element(xpob(driver, msgdiv)).perform()
    except: pass
    dt_plus_sender_xpt = msgdiv + "//div[@class='_27K43 _31p5Q']"
    sender_msg_xpt = msgdiv + "//div[@class='_21Ahp']/span[1]/span"
    sender_msg_xpt_1 = msgdiv + "//div[@class='_27K43 _31p5Q']//span/span"
    quoted_sender_xpt = msgdiv + "//div[@class='_3pMOs yKTUI']//div[1]/span"
    quoted_text_xpt = msgdiv + "//div[@class='_3pMOs yKTUI']//div[2]/span"
    read_more_button = msgdiv + '/div[1]/div[2]/div/div'
    rd = xpob(d, read_more_button)
    if type(rd) is not bool:
        if 'more' in rd.text.lower() or 'Read' in rd.text:
            try: ActionChains(driver).move_to_element(rd).click().perform()
            except: pass
            xc(driver, read_more_button)
    
    dttm,sender,sender_msg,quoted_sender,quoted_text = '','','','',''
    a = xpob(driver, dt_plus_sender_xpt)
    if type(a) is bool: return None
    
    b = a.get_attribute('innerHTML')
    dttm, sender = bs_div_attr(b)
    try:
        sender_msg = xpob(driver, sender_msg_xpt).text
    except:
        sender_msg = xpob(driver, sender_msg_xpt_1).text
    if type(xpob(d, quoted_sender_xpt)) is not bool:
        quoted_sender = xpob(driver, quoted_sender_xpt).text
        quoted_text = xpob(driver, quoted_text_xpt).text
    return [dttm,sender,sender_msg,quoted_sender,quoted_text]

def sidepane_scroll_by_id(driver, initial = 1, scrolls=25):
    for i in range(0, scrolls):
        driver.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
        initial += 300
    return initial

def scroll_by_xpath(driver, xpt="(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"):
    wait = WebDriverWait(driver, 30)
    driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.presence_of_element_located((By.XPATH, xpt))))
    return 1
    
def reload(driver, wait_sec=60):
    wait = WebDriverWait(driver, wait_sec)
    driver.refresh()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    search_bar_xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
    element = wait.until(EC.presence_of_element_located((By.XPATH, search_bar_xpt)))
    print('reloaded success')

class Wakit:
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.ac = ActionChains(self.driver)
        self.cdata = defaultdict()
        self.parsed_counter = 0
        self.store_msg = pd.DataFrame(columns=['dttm','sender','sender_msg','quoted_sender','quoted_text','insert_dttm','chat_name'])
        print(self.driver.title)
        
    def isPresent(self, xpt):
        try: return self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        except: return 0
    
    def FetchText(self, xpt):
        try: return self.wait.until(EC.presence_of_element_located((By.XPATH, xpt))).text
        except: return 0
        
    def select_chat(self, name):
        xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        element.clear()
        self.ac.move_to_element(element).click().perform()
        self.ac.send_keys(name).send_keys(Keys.RETURN).perform()
        return 1
        
    def chain(self, xptdict):
        ''' following xpdict argument open chat name 'onami' and send message 'HI'
            xptdict = {"//div[@class='_2vDPL']" : {'cmd':'paste', 'text':'onami'},
             "//footer[@class='_3E8Fg']//p": {'cmd':'paste','text':'HI'}}
        '''
        for xp, v in xptdict.items():
            x1 = self.isPresent(xp)
            if x1 != 0: 
                self.chain_1(x1, v)
            else:
                print(xp, ' Not Found')

    def chain_1(self, x1,  v):
        if 'click' in v['cmd']:
            self.ac.move_to_element(x1).click().perform()
            print('clicked')
        elif 'paste' in v['cmd']:
            if v['text'] is not None and chr(10) in v['text']:
                self.write_multiline(v['text'])
            elif v['text'] is not None:
                self.ac.move_to_element(x1).click().perform()
                if 'paste-only' in v['cmd']:
                    self.ac.send_keys(v['text']).perform()
                else:
                    self.ac.send_keys(v['text']).send_keys(Keys.RETURN).perform()
    
    def write_long_msg(self, x1, text):
        x1 = isPresent(x1) if type(x1) is str else x1
        self.ac.move_to_element(x1).click().perform()
        xx = text.split(chr(10))
        for line in xx:
            self.ac.send_keys(line).perform()
            self.ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        else: 
            self.ac.send_keys(Keys.RETURN).perform()
            
    def storing_msg(self, ls):
        if ls is not None and len(ls)>1:
            self.store_msg.loc[len(self.store_msg.index)] = ls
    
    def getxpt(self, xpt):
        wait = WebDriverWait(self.driver, 3)
        try: return wait.until(EC.presence_of_element_located((By.XPATH, ''.join(xpt)))).text
        except: 0
    
    def message_scraper(self, chat_name='emergency', msg_container=30):
        insert_dttm = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        if self.select_chat(chat_name) == 1: pass
        else: return chat_name + " selection problem"
        base = "(//div[@id='main']//div[@class='ItfyB _3nbHh'])"
        for i in range(1, msg_container):
            bs = base + '[' + str(msg_container) + ']'
            while self.getxpt(bs) == 0 or self.getxpt(bs) == None or self.getxpt(bs) == '':
                scroll_by_xpath(self.driver, xpt="(//div[@id='main']//div[@class='ItfyB _3nbHh'])[1]")
                tm.sleep(0.5)
                try: self.ac.move_to_element(isPresent("(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"))
                except: pass
                bs = base + '[' + str(msg_container) + ']'
            print('container: ', i)
            m = msg_scrap(self.driver, i)
            mx = m + [insert_dttm , chat_name] if m is not None else m
            print(mx)
            self.storing_msg(mx)
        else:
            self.store_msg.to_csv(chat_name + dt.datetime.now().strftime('%d-%M-%Y_%H%M') + '.csv')
    
    @property
    def get_driver(self):
        return self.driver
    
    def clkcross(self, cross_search_bar = ["//div[@class='_2vDPL']",]):
        for ii in cross_search_bar:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, ii)))
                self.ac.move_to_element(element).click().perform()
            except:
                pass

#x = Wakit()
#d = x.get_driver
#x.message_scraper('emergency', 20)

def sidepane_item(driver, base="(//div[@id='pane-side']//div[@class='_8nE1Y'])",dc=defaultdict(), n=2, fn=None):
    wait = WebDriverWait(driver, 1)
    def xp(xpt):
        try: return wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        except: return None
    bi = base + '[' + str(n) + ']'
    if xp(bi) is None: return None
    if len(dc) == 0:
        dc = {'chat_name' : bi + "//div[@class='_21S-L']",
              'last_text' : bi + "//div[@class='vQ0w7']/span[1]/span[3]",
              'last_sender' : bi + "//div[@class='vQ0w7']/span[1]/span[1]",
              'last_msg_time' : bi + "/div[@class='y_sn4']/div[@class='Dvjym']",
              'new_msg_notif' : bi + "//div[@class='Dvjym']//div[@class='_1pJ9J']/span"}
    for k, v in dc.items():
        x = xp(v)
        dc[k] =  None if x is None else x.text
        if fn is not None: fn(bi,x,k,v)
    return pnitem
        
#print(sidepane_item(driver=d, base="(//div[@id='pane-side']//div[@class='_8nE1Y'])", n=2))

