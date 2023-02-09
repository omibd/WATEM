from imports import *
from collections import *
import waxpath as wpn

def update_key_value(a, b):
    '''updating key & values (values will be appened for existing key)'''
    c = {}
    if len(a) == 0: return b
    tls = lambda ls : ls if type(ls) is list else [ls]
    for k, v in a.items():
        c[k] = tls(a[k]) + tls(b[k]) if k in list(b) else tls(a[k])
    else: return {**b, **c}
    
xpt_by_chatname = lambda chatname: "//div[@class='_21S-L']//span[@dir='auto' and contains(text(),'" + chatname + "')]//ancestor::div[@class='_8nE1Y']"

def pane_xpt(index=None, parent = "(//div[@id='pane-side']//div[@class='_8nE1Y'])", chatname=None):
    if index is not None and parent is not None:
        bi = parent + "[" + str(index) + "]"
    elif parent is None and chatname is not None:
        bi = "//div[@id='pane-side']//div[@class='_21S-L']//span[@dir='auto' and contains(text(),'" + chatname + "')]//ancestor::" + parent
    else:
        bi = parent
    dc = {'chat_name' : bi + "//div[@class='_21S-L']//span[@dir='auto']",
          'last_text' : bi + "//span[@data-testid='last-msg-status']",
          'last_sender' : bi + "//div[@class='vQ0w7']//span[@dir='auto']",
          'last_msg_time' : bi + "/div[@class='y_sn4']/div[@class='Dvjym']",
          'new_msg_notif' : bi + "//div[@class='Dvjym']//span[@data-testid='icon-unread-count']"}
    return dc

class WhBase:
    
    pane_search = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
    body_chat_search_btn = "//div[@id='main']//div[@class='_3ndVb']"
    body_chat_name = "//div[@id='main']//div[@class='_21nHd']"
    body_text_area = "//footer[@class='_3E8Fg']//p"
    body_msg_nav_arrow = '/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[1]/span/div'
    init_info = "//div[@data-testid='intro-text'][contains(.,'Use WhatsApp on up to 4 linked devices and 1 phone at the same time.')]"
    pane_search = "//div[@id='side']//div[@data-testid='chat-list-search']"
    pane_search_back ="//div[@id='side']//span[@data-testid='search']"
    pane_search_cancel = "//div[@id='side']//span[contains(@data-testid,'x-alt')]"
    pane_search_filter = "//div[@id='side']//button[@aria-label='Unread chats filter']"
    active_chat_title = "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']"
    active_chat_search = "//div[@id='main']//span[@data-testid='search-alt']"
    msg_menu = '//*[contains(concat( " ", @class, " " ), concat( " ", "_3bcLp", " " ))'

    
    def __init__(self, url=None):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.url = 'whatsapp.com' if url is None else url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.ac = ActionChains(self.driver)
        self.read_store = defaultdict()
        self.store_msg = pd.DataFrame([])
        self.pane_data = defaultdict()
        self.chat_data = defaultdict()
        print(self.driver.title)
    
    @property
    def get_driver(self):
        return self.driver
    
    @property
    def reload(self):
        wait = WebDriverWait(self.driver, 60)
        self.driver.refresh()
        search_bar_xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, search_bar_xpt)))
        print('reload success, whatsapp ready')
        return self
    
    def log(self, data):
        nw = dt.datetime.now()
        filepath = os.getcwd() + '\\log\\' + nw.strftime('%d-%b-%Y').upper() + '.txt'
        fp = open(filepath, 'a+')
        fp.write('# ' + data + "," + nw.strftime('%H:%M %d-%b-%Y') + chr(10))
        fp.close()
    
    def xpbool(self, xpt):
        try:
            rs = self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
            return True
        except: return False
        
    def xptxt(self, xpt):
        try: return self.wait.until(EC.presence_of_element_located((By.XPATH, xpt))).text
        except: return None
        
    def xpelem(self, xpt):
        try: return self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        except: return None
    
    def xptext(self, xpt):
        print(xpt)
        try:
            xx = self.driver.find_element(By.XPATH, xpt).text
            print(xx)
            print('----------')
        except:
            try: return self.xpelem(xpt).text
            except: return None
        
    def xpget(self, xpt):
        try: self.driver.find_element(By.XPATH, xpt).text
        except: return None
        
    def xp_elements(self, xpt):
        try: return self.driver.find_elements(By.XPATH, xpt)
        except: return self.xpelem(xpt)
    
    def click(self, xpt):
        xp = self.xpelem(xpt) if type(xpt) is str else xpt
        if xp is None: 
            print(xpt , " -- xpath not present")
            return 0
        try:
            xp.click()
            return 1
        except: return 0
    
    def move_click(self, xpt):
        try: ActionChains(self.driver).move_to_element(self.xpelem(xpt)).click(xpt).perform()
        except: return 0
        
    def hover_click(self, xp1, xp2):
        try:  ActionChains(self.driver).move_to_element(self.xpelem(xp1)).click(self.xpelem(xp2)).perform()
        except: return 0
    
    def just_move(self, xpt="(//div[@data-testid='conversation-panel-body'])[2]"):
        try:
            ActionChains(self.driver).move_to_element(self.xpelem(xpt)).perform()
            tm.sleep(.5)
            return 1
        except: return self.msg_scoll_up()
    
    def move_click_send_text(self, xpt, text):
        try: ActionChains(self.driver).move_to_element(self.xpelem(xpt)).click().send_keys(text).send_keys(Keys.RETURN).perform()
        except: return 0
        
    def paste_text(self, xpt, keys):
        try: ActionChains(self.driver).send_keys_to_element(self.xpelem(xpt), keys).send_keys(Keys.RETURN).perform()
        except: return 0
        
    def click_write_enter(self, xpt, text):
        xp = self.xpelem(xpt) if type(xpt) is str else xpt
        if xp is None: return 0
        else:
            print('writing init')
            xp.clear()
            if chr(10) not in text:
                self.ac.move_to_element(xp).click().send_keys(text).send_keys(Keys.RETURN).perform()
            else:
                xx = text.split(chr(10))
                for line in xx:
                    self.ac.send_keys(line).perform()
                    self.ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                self.ac.send_keys(Keys.RETURN).perform()
    
    def sidepane_scroll(self, initial = 1, scrolls=50):
        for i in range(1, scrolls):
            self.driver.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            initial = initial + i + 1
        return initial

    def scroll_by_xpath(self, xpt="(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"):
        try:
            xp = self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", xp)
            tm.sleep(1)
        except:
            print('WhBase.scroll_by_xpath(xpt) failed to scroll')
            return 0
        
    def msg_scoll_down(self):
        try:
            self.driver.find_element(By.XPATH, "//div[@class='_5kRIK']").send_keys(Keys.END)
            tm.sleep(2)
            return 1
        except: return 0
            
    def msg_scoll_up(self):
        try:
            self.driver.find_element(By.XPATH, "//div[@class='_5kRIK']").send_keys(Keys.HOME)
            tm.sleep(2)
            return 1
        except: return 0
        
    def msg_sender_dttm(self, base="(//div[@id='main']//div[@data-testid='msg-container'])"):
        html = self.wait.until(EC.presence_of_element_located((By.XPATH, base))).get_attribute('innerHTML')
        sp = BeautifulSoup(html, "lxml")
        x = sp.find_all('div')
        for i in x:
            try:
                st = i['data-pre-plain-text']
                break
            except:pass
        else: return None, None
        try:
            split_point = st.find(']')
            sender = st[split_point+1:].replace(':','').strip(' ')
            dttm = parse(st.upper()[1:split_point])
            return dttm.strftime("%Y-%m-%d %H:%M"), sender
        except: None, None
            
    def xpbulk(self, xpt):
        try:
            if type(xpt) is str: return self.xptext(xpt)
            elif type(xpt) is list: return [self.xptext(n) for n in xpt]
            elif type(xpt) is dict: return {k : [self.xptext(n) for n in v] if type(v) is list else self.xptext(v) for k, v in xpt.items()}
            else: return None
        except:
            return None
        
    def pane_search_clear(self):
        self.click(self.pane_search_cancel)
        self.click(self.pane_search_back)
        
    def select_chat(self, chat_name):
        if chat_name is not None and chat_name != '':
            convtitle = "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']"
            xx = self.xptext(convtitle)
            if xx is not None and chat_name.lower() in xx.lower(): 
                print('already selected')
                self.click(self.body_msg_nav_arrow)
                return 1
            else:
                if self.click(xpt_by_chatname(chat_name)) == 0:
                    print('chat has no communication')
                    self.click_write_enter(xpt=self.pane_search, text=chat_name)
                y = self.xptxt(convtitle)
                print('chat body name: ', y)
                if chat_name.lower() in y.lower():
                    print('chat selection successful')
                    self.pane_search_clear()
                    self.click(self.body_msg_nav_arrow)
                    return 1
                else: 0
        else: return 0
        
    def send_message(self, chat_names, text):
        cn = [chat_names] if type(chat_names) is str else chat_names
        for n in cn:
            x = self.select_chat(n)
            if x is not None or x !=0:
                self.click_write_enter(text)
                print('message send to ', str(n), ' sucessfully')
                tm.sleep(.5)
            else:
                print('message send failed, chat: ', str(n))
    
    def dict_to_df(self, dc, out=None):
        x = dt.datetime.now().strftime('%b%d%Y_%H%M')
        opt = x  + '.csv' if out is None else x + '_' + out + '.csv'
        df = pd.DataFrame.from_dict(dc).to_csv(opt)
        return df
    
    def chat_msg(self, n=None, base="(//div[@id='main']//div[@data-testid='msg-container'])", xpt_print=False):
        bi = base + '[' + str(n) + ']' if n is not None else base
        if self.xpelem(bi) is None: return None
        else:
            self.move_click(bi + "//div[@role='button'][contains(.,'Read more')]")
            dttm, sender = self.msg_sender_dttm(bi)
            dc = {'sender' : [sender],
                  'text' : [self.xptext(bi + "//div[@class='_21Ahp']/span[1]/span")],
                  'q_sender' : [self.xptext(bi + "//div[@class='_3pMOs yKTUI']//div[1]/span")],
                  'q_text' : [self.xptext(bi + "//div[@class='_3pMOs yKTUI']//div[2]/span")],
                  'datetime' : [dttm]}
            return dc
   
    def wapane_chat_type(self, bs):
        xpt = bs + "//div[@data-testid='chatlist-status-v3-ring']"
        if self.xpelem(xpt) is None: return 'group'
        else: return 'contact'
   
    def side_pane(self, n=None, pane_base="//div[@id='pane-side']//div[@data-testid='cell-frame-container']", after=''):
        base = '(' + base + "//div[@class='_8nE1Y'])" if '_8nE1Y' not in pane_base else pane_base
        bi = base + '[' + str(n) + ']' + after if n is not None else base + after
        if self.xpelem(bi) is None: return None
        ctype = self.wapane_chat_type(pane_base)
        dc = {'chat_type': ctype,
            'chat_name' : bi + "//div[@class='_21S-L']//span[@dir='auto']",
            'last_text' : bi + "//div[@class='vQ0w7']//span[@dir='ltr']",
            'last_sender' : bi + "//div[@class='vQ0w7']//span[@dir='auto']",
            'last_msg_time' : bi + "/div[@class='y_sn4']/div[@class='Dvjym']",
            'new_msg_notif' : bi + "//div[@class='Dvjym']//span[@data-testid='icon-unread-count']",
            'time': bi + "//div[@data-testid='msg-meta']"}
        for k, v in dc.items():
            v = [v] if type(v) is str else v
            dc[k] = [self.xptext(j) for j in v]
        return dc
    
    def msginfo(self, n=None, base="(//div[@id='main']//div[@data-testid='msg-container'])", after=''):
        bi = base + '[' + str(n) + ']' if n is not None else base
        print('msgbase is being collecting:', bi)
        if self.xpelem(bi) is None: return None
        else:
            self.move_click(bi + "//div[@role='button'][contains(.,'Read more')]")
            dttm, sender = self.msg_sender_dttm(bi)
            dc = {'sender' : [sender],
                  'text' : [self.xpget(bi + "//div[@class='_21Ahp']/span[1]/span")],
                  'q_sender' : [self.xpget(bi + "//div[@class='_3pMOs yKTUI']//div[1]/span")],
                  'q_text' : [self.xpget(bi + "//div[@class='_3pMOs yKTUI']//div[2]/span")],
                  'datetime' : [dttm],
                  'sender_visible': [self.xpget(bi + "//div[@class='_27K43 _31p5Q']/div[1]//span[@dir='auto']")],
                  'time': [self.xpget(bi + "//div[@data-testid='msg-meta']/span")]
                  }
            dc['img'] = 'image' if self.xpget(bi + "//div[@data-testid='image-thumb']") is not None else 'NoImage'
            return dc
    
    def pane_chat_get(self, n=0, chatname=None, bs=None):
        ctype = wpn.wapane_chat_type(self.driver, chatname, n, bs)
        bs1 = wpn.wapane_chat_xptgen(chatname, n, bs) + wpn.wapane_chat_text_base
        dc = {'chat_type' : ctype}
        dc['chat_name'] = [self.xptext(bs1 + wpn.wapane_chat_name)]
        dc['last_update_time']= [self.xptext(bs1 + wpn.wapane_chat_last_time)]
        if ctype == 'group':
            dc['last_sender'] = [self.xptext(bs1 + wpn.wapane_chat_group_last_msg_sender )]
        else:
            dc['last_sender'] = chatname if self.xptext(bs1 + "//div[@class='_2qo4q _3NIfV']") is None else 'You'
        dc['last_msg'] = [self.xptext(bs1 + wpn.wapane_chat_last_msg)]
        dc['unread_count'] = [self.xptext(bs1 + wpn.wapane_chat_unread_count)]
        return dc


class WABS(WhBase):
    
    def __init__(self):
        super().__init__()
        
    def msg_xpath_by_text_last_index(self, text, get_text=False):
        txtm = "(//div[contains(@class,'_21Ahp') and contains(., '" + text + "')])[last()]"
        fxpt = txtm + "/ancestor::div[@data-testid='msg-container']"
        return fxpt if get_text==False else self.chat_msg(base=fxpt)
    
    def msg_xpath_by_text_time(self, text, time, get_text=False):
        txtm = "//div[contains(@class,'_21Ahp') and contains(., '" + text + "') and contains(.,'" + str(time) + "')]"
        fxpt = txtm + "/ancestor::div[@data-testid='msg-container']"
        return fxpt if get_text==False else self.chat_msg(base=fxpt)

    def msg_info_by_text_time(self, text, time):
        msg_xpath = self.msg_xpath_by_text_time(text, time)
        return self.chat_msg(base=msg_xpath)
    
    def duplicate_none_chk(self, sdic, dc):
        dpcount, nonecount = 0, 0
        for k, v in dc.items():
            if v is None: nonecount = nonecount + 1
            else:
                if v in list(sdic.values()): 
                    dpcount = dpcount + 1
        else:
            if nonecount >=3: none_flag = True
            else: none_flag = False

            if dpcount>=3: dp_flag = True
            else: dp_flag = False
            return none_flag, dp_flag

    def msgread(self, to_index=50 ,from_index=0, base="(//div[@id='main']//div[@data-testid='msg-container'])", sdict=defaultdict(list)):
        duplicate, nonecount, n, whileloop= 0, 0, from_index+1, 0
        while len(list(sdict.values()))<to_index and duplicate<5 and nonecount<5:
            whileloop = whileloop + 1
            dc = self.msginfo('[last()-' + str(n) + ']', base)
            if dc is not None:
                nf, dpf = self.duplicate_none_chk(sdict, dc)
                if nf == False and dpf == False:
                    sdict = update_key_value(sdict, dc)
                    duplicate, nonecount = 0, 0
                    n = n + 1
                else:
                    duplicate = duplicate  + 1
                    if duplicate>1: 
                        self.msg_scoll_up()
                        n = n + 1
            else:
                nonecount = nonecount + 1
                if nonecount>2: 
                    self.just_move("(//div[@id='main']//div[@data-testid='msg-container'])[2]")
            print('whileloop:', whileloop, ' len of dic:', len(list(sdict.values())), 'current n: ', n, 'nonecount:', 
                  nonecount, 'duplicate: ',duplicate)
        else: 
            print('total looped: ', whileloop, ' len of dic:', len(sdict))
            return sdict
    
    def pane_chat_info(self, store_dc = defaultdict(), bs="//div[@id='pane-side']//div[@class='_21S-L']//span[@dir='auto']"):
        'fetch available chats info from pane without scroll'
        lschat = self.xp_elements(bs)
        for i in lschat:
            bychat = xpt_by_chatname(i.text)
            dc = pane_xpt(parent=bychat)
            for k, v in dc.copy().items():
                q = self.xptext(v)
                dc[k] = q if q is not None else ''
            store_dc = update_key_value(store_dc, dc)
        else: return self.dict_to_df(store_dc)
        
    def get_unread_msg(self, chatname='Emergency SOC Group',store_dc = defaultdict(),msgbase="(//div[@id='main']//div[@data-testid='msg-container'])"):
        'fetch unread available msg inside group without scroll'
        chatxpt = xpt_by_chatname(chatname)
        dc = pane_xpt(parent=chatxpt)
        print('chatname: ', chatname, 'unread_sms: ',  self.xptext(dc['new_msg_notif']))
        if self.xptext("//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']") not in chatname:
            self.click(chatxpt)
        i = 1
        avmsg = self.xp_elements(msgbase)
        for n in range(i, len(avmsg)):
            dc = self.chat_msg('last()-' + str(n))
            store_dc = update_key_value(store_dc, dc)
        else:
            df = self.dict_to_df(store_dc, chatname)
            return store_dc, df
    
    def msgrd(self, en, st=1, dc = defaultdict(list)):
        nc = 0
        for n in range(st, en):
            dic = self.msginfo('last()-' + str(n))
            if dic is not None:
                if len(dc) == 0 : dc = dic
                else: dc = update_key_value(dc, dic)
                nc = 0
            else: 
                if nc>2: self.msg_scoll_up()
                if nc>1: self.just_move()
                elif nc>3: return dc
                else: print('nc: ', nc)
                nc = nc + 1
        else: return dc
        
    def pane_dyn_xpath(self, by_chatname=None, by_msgtxt=None, by_last_sender=None, get_text=False):
        contain = []
        if by_chatname is not None: 
            contain.append("contains(@title,'" + by_chatname + "')")
        if by_msgtxt is not None: 
            contain.append("contains(@data-testid='last-msg-status') and contains(.,'" + by_msgtxt + "')")
        if by_last_sender is not None: 
            contain.append("contains(@dir='auto') and contains(., '" + by_last_sender + "')")
        fxpt = "(//div[@id='pane-side'])//*[" + ' and '.join(map(str,contain)) + "]" + "//ancestor::div[@class='_8nE1Y']"
        rs = fxpt if get_text==False else self.side_pane(base=fxpt)
        return rs
    
    def inspect(self):
        dc = {
            'pn_search_textarea' : self.xpbool("/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"),
            'pn_search' : self.xpbool("//div[@id='side']//div[@data-testid='chat-list-search']"),
            'pn_search_filter' : self.xpbool("//div[@id='side']//button[@aria-label='Unread chats filter']"),
            'chat_title' : self.xptext("//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']"),
            'chat_text_area' : self.xpbool("//footer[@class='_3E8Fg']//p"),
            'msg_base' : self.xpbool("(//div[@id='main']//div[@data-testid='msg-container'])")
        }
        return dc
    
    def ensure_click_attempt(self, hover_xpt, click_xpt, required_visibility_xpt):
        q = self.xpelem(hover_xpt)
        if q is not None:
            ActionChains(self.driver).move_to_element(q).pause(1).click(self.xpelem(click_xpt)).perform()
        else:
            self.just_move()
            tm.sleep(1)
            ActionChains(self.driver).move_to_element(self.xpelem(hover_xpt)).pause(.5).click(self.xpelem(click_xpt)).perform()
        p = self.xpelem(required_visibility_xpt)
        if p is not None: return p
        else: 
            print('ensure_click_attempt fail')
            self.reload
            return 0
            
    def action(self, chat_name='OPS & RO', search_text="battery backup degraded?", msg_time=None, forward=None,
               reply=None, react=None):
        x = self
        clk_1 = "//span[@data-testid='down-context']"
        clk_2="//ul//li[contains(.,'Forward message')]"
        clk_3= "//button[@title='Forward message']"
        select_chat_= lambda _chat_ : "(//div[@class='_8nE1Y' and contains(.,'" + _chat_ + "')])/" + \
        "ancestor::div[@class='lhggkp7q ln8gz9je rx9719la']"
        write_txt = "//div[@data-testid='chat-list-search']"
        clk_send_btn = "//span[@data-testid='send']"
        msg_write_area = "//footer[@class='_3E8Fg']//p"

        chat_selected, while_counter = False, 0
        a1 = x.pane_dyn_xpath(by_chatname=chat_name)
        if x.click(a1) == 0:
            tm.sleep(.5)
            if x.select_chat(chat_name) != 0:
                chat_selected = True
            else: chat_selected = False
        else:
            chat_selected = True
        print('chat_selected; ', chat_selected)
        if chat_selected == True:
            if msg_time is not None: a2 = x.msg_xpath_by_text_time(search_text,msg_time)
            else: a2 = x.msg_xpath_by_text_last_index(search_text)
            print('Time is None, selecting by last index')
            move = 1 if x.just_move(a2) is None else 0
            while move == 0 or move > -5 and move !=1:
                while_counter= while_counter + 1
                x.just_move("(//div[@id='main']//div[@data-testid='msg-container'])[2]")
                if x.just_move(a2) == 0:
                    move = move - 1
                else:
                    move = 1
                    break
                print('while_counter:', while_counter,' inside while Move: ',move)
            print('move Outside: ', move)
            if move > 0:
                print('executute clicking operation')
                x.click("//span[@data-testid='down-context']")
                tm.sleep(.5)
                if self.xpelem("//ul//li") is None:
                    q = self.ensure_click_attempt(a2, a2 + "//span[@data-testid='down-context']", "//ul//li")
                    if q == 0:
                        print('msg ul/li not found.. run again')
                        return 0
                if forward is not None and len(forward)>1:
                    print('msg forward init')
                    x.click("//ul//li[contains(.,'Forward message')]")
                    x.click("//button[@title='Forward message']")
                    #x.move_click_send_text("//div[@data-testid='chat-list-search']","SM POOL")
                    x.paste_text("//div[@data-testid='chat-list-search']",forward)
                    if x.click(select_chat_(forward)) != 0:
                        tm.sleep(.5)
                        x.click("//span[@data-testid='send']")
                        return 1
                    else:
                        q = self.click("(//div[contains(@class,'_199zF _3j691') and contains(.,'" + forward + "')])")
                        if x.click("//span[@data-testid='send']") == 1:
                            print('forward success')
                        else: print('forward fail')
                elif reply is not None and len(reply) > 1:
                    x.click("//ul//li[contains(.,'Reply')]")
                    x.click_write_enter(msg_write_area, reply)
                    return 1
                elif react is not None:
                    x.click("//ul//li[contains(.,'React')]")
                    x.click("//div[@data-testid='reactions-option-0']")
                    return 1
            