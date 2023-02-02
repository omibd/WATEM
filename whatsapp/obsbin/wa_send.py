
import os, time
from w_xpath import *
from whfn import *
import whbs as bs
import pandas as pd
import datetime
from dateutil.parser import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class whapp_send:
    def __init__(self):
        self.driver = ""
    
    def set_driver_se(self, driver):
        self.driver = driver
        
    def _msg_writer(self, msg):
        xp1 = "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']"
        try:
            x = self.driver.find_element('xpath',xp1)
            x.click()
            time.sleep(1)
            xx = msg.split('\n')
            for line in xx:
                ActionChains(self.driver).send_keys(line).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ActionChains(self.driver).send_keys(Keys.RETURN).perform()
            return 1
        except:
            print('no chat selected/writing box is not present')
            return 0
            
    def _msg_send(self, chat_name, msg, atm = 0):
        driver = self.driver
        if self._select_chat(chat_name) == 1:
            xp1 = "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']"
            x = driver.find_element('xpath',xp1)
            x.click()
            time.sleep(1)
            xx = msg.split('\n')
            for line in xx:
                ActionChains(driver).send_keys(line).perform()
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ActionChains(driver).send_keys(Keys.RETURN).perform()
        else:
            if atm == 0:
                atm = atm +1
                self._msg_send(chat_name, msg, 1)
            else:
                print("Wrong Selection - ", chat_name)
        
    def _reply_init(self, elm):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(elm).perform()
            time.sleep(1)
            try:
                self.driver.find_element('xpath',"//div[@class='_3e9My']//span[1]").click()
            except:
                arro = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[3]/div[8]/div/div/span/div/div/span"
                self.driver.find_element('xpath',arro).click()
            time.sleep(1)
            self.driver.find_element('xpath',"/html/body/div[1]/div[1]/span[4]/div/ul/div/li[1]/div[1]").click()
            return 1
        except:
            return 0
    
    def _delete_msg(self,elm):
        delete_for_me = "(//div[contains(@class,'tvf2evcx m0h2a7mj')])[2]"
        delete_for_all = "(//div[contains(@class,'tvf2evcx m0h2a7mj')])[3]"
        try:
            action = ActionChains(self.driver)
            action.move_to_element(elm).perform()
            try:
                self.driver.find_element('xpath',"//div[@class='_3e9My']//span[1]").click()
            except:
                arro = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[3]/div[8]/div/div/span/div/div/span"
                self.driver.find_element('xpath',arro).click()
            time.sleep(1)
            self.driver.find_element('xpath',"/html/body/div[1]/div[1]/span[4]/div/ul/div/li[5]/div[1]").click()
            time.sleep(1)
            try:
                self.driver.find_element('xpath',delete_for_all).click()
            except:
                self.driver.find_element('xpath',delete_for_me).click()
            return 1
        except:
            return 0

    
    def _reply_on_msg(self, chat_name, msg, src_content="", how="data-id"):
        rs = 0
        if self._select_chat(chat_name) == 1:
            if src_content=="":
                self._msg_writer(msg)
            elif src_content != "" and type(src_content) is not list and how=='data-id':
                src = search_msg_dataid(src_content)
                ls = msg_cls_child(src)
                for i in ls:
                    try:
                        eL = self.driver.find_element('xpath',i)
                        if self._reply_init(eL) == 1:
                            rs = 1
                            self._msg_writer(msg)
                            break
                        else:
                            pass
                    except:
                        pass
            elif type(src_content) is list:
                src_1 = xath_query_build_contains(src_content)
                ls = msg_cls_child(src_1)
                print(ls)
                for i in ls:
                    try:
                        eL = self.driver.find_element('xpath',i)
                        if self._reply_init(eL) == 1:
                            rs = 1
                            self._msg_writer(msg)
                            break
                        else:
                            pass
                    except:
                        pass
            else:
                print('_reply_on_msg : no match')
            return rs
        else:
            print('provided chat not found')
            return rs

def _msg_send(msg):
    messages = msg.split('\n')
    for line in messages:
        ActionChains(driver).send_keys(line).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
    else:
        ActionChains(driver).send_keys(Keys.RETURN).perform()

#xpath_footer_textbox = "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']"