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

datacol = msg_col

class whapp_read:
    def __init__(self):
        self.driver = ""
        self.title = ""
        self.ls_msg = []
        
    def set_driver_rd(self, driver):
        self.driver = driver
        self.title = self.driver.title
        
    def _is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def _action(self, el, attempt=0):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(el).perform()
            return 1
        except:
            try:
                if attempt==0:
                    time.sleep(1)
                    self._action(el, 1)
                else:
                    return -1
            except:
                return -1
            
    def _xpath(self, xpt, attempt=0):
        try:
            a1 = self.driver.find_element('xpath',xpt)
            ht = a1.get_attribute('innerHTML')
            return a1, ht
        except:
            if attempt == 0:
                self._xpath(xpt,1)
            else:
                return "0", "0"
        
    def _scrol_up(self, limit=1):
        x = "(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"
        l = self.driver.find_element('xpath',x)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", l)
            return 1
        except:
            return -1
    
    def _loop_rev(self, mx=50, lw=1, n=0):
        el = ""
        cnt = 0
        for i in range(mx, lw, -1):
            cnt = cnt + 1
            try:
                el = self.driver.find_element('xpath',msg_b_dyn(i))
                n  = i
                break
            except:
                pass
        return n, el
    
    def _loop_div(self, mx=50, lw=2, n = 0):
        el = ""
        cnt = 0
        for i in range(lw, mx, 1):
            cnt = cnt + 1
            try:
                el = self.driver.find_element('xpath',msg_b_dyn(i))
                etx = el.text
                n = i
            except:
                return n, el
        return n, el
    
    def content_correction(self, ls, tx):
        lx = ls
        for i in ls:
            t1 = tx.replace(i,'')
            tx = t1
        else:
            ftx = tx.strip()
            ls[1] = ftx
            return ls
        
    def read_message(self, requied=50, chat_name=""):
        try:
            self.driver.find_element('xpath',msg_nav_arrow).click()
        except:
            pass
        self.unique_msg = ['0']
        self.msgdic = message_dic
        pre_av = 0
        wc = 0
        wl = 0
        av, el = self._loop_rev()
        self.read_msg_store_3(chat_name, av+1, 1)
        print('av-one-', av)
        if av is not None:
            while(av < requied):
                wl = wl + 1
                xp, ht = self._xpath(msg_b)
                ack = self._action(xp)
                av, el = self._loop_rev(av+30,av)
                print(wl, ' - scraping in while loop, current available -', av, ' - previous available-', pre_av, ' required - ', requied)
                if pre_av == av or pre_av > av:
                    wc = wc + 1
                    if wc > 5:
                        print('scrollin to up forecefully')
                        self._scrol_up()
                        time.sleep(2)
                else:
                    start = 1
                    if int(requied) - int(av) < 0:
                        start = abs(int(requied) - int(av)) - 1                      
                    self.read_msg_store_3(chat_name, av, start)  #msg store
                    print('msg read successful upto - ' + str(av - start), ' - quired reading upto ',requied )
                    pre_av = av
                    wc = 0
            print('scraper is outside - ', av)
            print(self.msgdic)
            df = pd.DataFrame.from_dict(self.msgdic).reset_index()
            try:
                df['DATE_TIME'] = df.apply(lambda x : pd.to_datetime(x['DATE_TIME']), axis = 1)
                df['DATE_TIME'] = df.apply(lambda x : pd.to_datetime(x['DATE_TIME'], format='%Y-%m-%d %H:%M:%S'), axis = 1)
                df = df.sort_values(by='DATE_TIME', ignore_index=True)
            except:
                pass
            chat_name = chat_name.replace("&","")
            chat_name = chat_name.replace("/","$")
            file = csvdir() + '\\' + str(chat_name) + '.csv'
            try:
                ndf = pd.read_csv(file)
                df_cnct = pd.concat([df, ndf])
                df_cnct.to_csv(file, index=False)
                print('-------------',chr(10),file,'msg downloaded at csv')
                self.df_msg = df_cnct
                return df_cnct
            except:
                try:
                    df.to_csv(file, index=False)
                    self.df_msg = df
                except:
                    pass
                return df
        else:
            print('chat name not found/ failed to select')
            return ""
        
    def read_msg_store_3(self, name, mdv, et):
        dc = {}
        cnt = 0
        basedate = '0'
        for i in range(et, mdv ,1):
            base = msg_b_dyn(i)
            basetext = self.xpath_text(base)
            if basetext != '0' and basetext is not None:
                try:
                    basedt = parse(basetext)
                    basedate = '1'
                except:
                    basedate = "0"
                if basetext not in ignore_text and basedate != '1' "message was deleted" not in basetext:
                    dtid = self.xpath_text(base,'data-id')
                    if dtid not in self.unique_msg:
                        dc = self.msg_y8WcF_dic(i)
                        dc['DATA_ID'] = [dtid]
                        dc['CHAT'] = [name]
                        self.unique_msg.append(dtid)
                        self.msgdic = dic_Update(self.msgdic,dc)
                    else:
                        cnt = cnt + 1
                        if cnt > 2:
                            break
                    
    def xpath_text(self, xp, attr=False):
        rs = '0'
        try:
            eL = self.driver.find_element('xpath',xp)
            if attr==False:
                rs = eL.text
            else:
                rs = eL.get_attribute(attr)
                if rs is None:
                    rs = "0"
        except:
            rs = '0'
        return rs
    
    def msg_y8WcF_dic(self, val):
        dc = {}
        dic = msg_cls_y8wcF_dic(val)
        for k, v in dic.items():
            rs = '0'
            for i in v:
                rs = self.xpath_text(i)
                if rs != '0':
                    break
            dc[k] = rs
        else:
            tmx = "0:0"
            try:
                tmy = parse(dc.get('MSG_TIME'))
                tmx = tmy.strftime("%H:%M")
            except:
                pass
            dttm, sender = self.date_time_finder(tmx, val)
            dc['DATE_TIME'] = dttm
            if dc.get('SENDER_NAME') == '0':
                dc['SENDER_NAME'] = sender
            return dc
            
    def date_time_finder(self, tmx, val):
        el = self.driver.find_element('xpath',msg_b_dyn(val))
        ht = el.get_attribute('innerHTML')
        dtm = "0"
        sender = "0"
        if ht is not None:
            dttm, sender = bs.bs_div_all(ht)
            if dttm == "0":
                el = self.driver.find_element('xpath',msg_b_dyn(val+1))
                ht = el.get_attribute('innerHTML')
                dttm = bs.bs_div_get_date(ht)
                if dttm != '0':
                    dtm = dttm + " " + tmx + ":00"
                else:
                    dtm = '0'
            else:
                dtm = dttm
        else:
            pass
        return str(dtm), sender
        
    def dt_find(self, base):
        dt = ""
        i0 = base + "//div[@class='_2jGOb copyable-text']"
        i1 = base + "//div[@class='copyable-text']"
        i2 = base + "//div[@class='Nm1g1 _22AX6']/div"
        ii = [i0,i1,i2]
        for n in ii:
            dt = self.xpath_text(n,'data-pre-plain-text')
            if dt != '0':
                break
        try:
            y1 = dt.find(']')
            dtt = dt[1:y1]
            d = parse(dtt, fuzzy=True, yearfirst=False)
            dttm = d.strftime("%Y-%m-%d %H:%M")
            sender = dt[y1+1:len(dt)-1]
            return dttm, sender
        except:
            return "0", "0"
        
    def search_content(self, content):
        self._select_user_group(content)
        time.sleep(5)
        ls = []
        for i in range(20):
            try:
                cht_name = self.driver.find_element('xpath',side_chatname(i)).text
                sms = self.driver.find_element('xpath',side_sms(i)).text
                sender = self.driver.find_element('xpath',side_sms_sender(i)).text
                dttm = self.driver.find_element('xpath',side_sms_datetime(i)).text
                try:
                    d = parse(dttm)
                    dttm = d.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
                lx = [cht_name,sender,sms,dttm]
                ls.append(lx)
            except:
                pass
            self._load()
        return ls
    
    def search_msg_in_chat(self, chat_name, ls=['name','msg'], msg_to_check_=50):
        src_1 = xath_query_build_contains(ls) 
        msg_time = src_1 + "//span[@class='kOrB_']"
        msg_sender = src_1 + "//span[@class='a71At _3xSVM i0jNr']"
        msg_text = src_1 + "//span[@class='i0jNr selectable-text copyable-text']"
        if self._select_chat(chat_name) == 1:
            print(src_1)
            
        








        