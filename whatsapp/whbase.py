from imports import *

def update_key_value(a, b):
    '''updating key & values (values will be appened for existing key)'''
    c = {}
    tls = lambda ls : ls if type(ls) is list else [ls]
    for k, v in a.items():
        c[k] = tls(a[k]) + tls(b[k]) if k in list(b) else tls(a[k])
    else: return {**b, **c}


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
    def reload_get(self):
        wait = WebDriverWait(self.driver, 60)
        self.driver.refresh()
        search_bar_xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, search_bar_xpt)))
        print('reload success, whatsapp ready')
        return self.driver
    
    def xpelem(self, xpt):
        try: return self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        except: return None
    
    def xptext(self, xpt):
        try: return self.driver.find_element(By.XPATH, xpt).text
        except: return None
        
    def xpget(self, xpt):
        try: return self.driver.find_element(By.XPATH, xpt)
        except: return None
    
    def click(self, xpt):
        xp = self.xpelem(xpt) if type(xpt) is str else xpt
        if xp is None: 
            print("xpath not present")
            return None
        try:
            xp.click()
            return 1
        except: return 0
    
    def move_click(self, xpt):
        try: 
            self.ac.move_to_element(self.xpget(xpt)).click(xpt).perform()
            return 1
        except: return 0
        
    def hover_click(self, xp1, xp2):
        try: 
            self.ac.move_to_element(self.xpelem(xp1)).click(self.xpelem(xp2)).perform()
            return 1
        except: return 0
    
    def just_move(self, xp1):
        try:
            self.ac.move_to_element(self.xpget(xp1)).perform()
            return 1
        except: return 0
        
    def paste_text(self, text):
        try: self.ac.send_keys(text).perform()
        except: pass
        
    def k2e(self, xpt, value):
        x = self.xplem(xpt)
        if x is not None: 
            ActionChains(self.driver).send_keys_to_element(x, value).perform()
            return 1
        else:
            print('action not executed, xpath not found')
            return 0
        
    def click_write_enter(self, xpt, text):
        xp = self.xpelem(xpt) if type(xpt) is str else xpt
        if xp is None: return None
        xp.clear()
        if chr(10) not in text:
            self.ac.move_to_element(xp).click().send_keys(text).send_keys(Keys.RETURN).perform()
        else:
            xx = text.split(chr(10))
            for line in xx:
                self.ac.send_keys(line).perform()
                self.ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            self.ac.send_keys(Keys.RETURN).perform()
    
    def sidepane_scroll(self, initial = 1, scrolls=35):
        for i in range(1, scrolls):
            self.driver.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            initial = initial + i + 1
        return initial

    def scroll_by_xpath(self, xpt="(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"):
        try:
            xp = self.wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", xp)
            return 1
        except:
            print('WhBase.scroll_by_xpath(xpt) failed to scroll')
            return 0
        
    def msg_sender_dttm(self, n, base="(//div[@id='main']//div[@data-testid='msg-container'])"):
        xpt = base + "[" + str(n) + "]"
        html = self.wait.until(EC.presence_of_element_located((By.XPATH, xpt))).get_attribute('innerHTML')
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
    
    def select_chat(self, chat_name):
        if chat_name is not None and chat_name != '':
            x = self.click_write_enter(xpt=self.pane_search, text=chat_name)
            y = self.xptext(self.body_chat_name)
            print('chat body name: ', y)
            if chat_name.lower() in y.lower():
                print('chat selection successful')
                return y
            else: 0
        else: return None
        
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
                
    def chat_msg_menu(self, msgdiv):
        
        try:
            msgtime, msgarrow = msgdiv + "//div[@class='_2_-To']", msgdiv + "//span[@data-testid='down-context']"
            ActionChains(self.driver).move_to_element(self.xpelem(msgtime)).perform()
            tm.sleep(.2)
            ActionChains(self.driver).click(self.xpelem(msgarrow)).perform()
            tm.sleep(.2)
            return 1
        except: return 0
        
        
                
    def forward_msg(self, forward_to, msgdiv="(//div[@id='main']//div[@data-testid='msg-container'])[last()]"):
        acc = ActionChains(self.driver)
        if self.chat_msg_menu(msgdiv) == 0 and self.xpelem(msg_menu) is not None:
            print('failed to click message arrow')
            return None
        if self.click("//div[@class='_2sDI2']//div[contains(text(),'Forward')]") == 1:
            time.sleep(.5)
            if self.click("//div[@class='_2IUvV']//span[@data-testid='forward']") == 1:
                time.sleep(.5)
                xpel  = self.xpelem("(//div[contains(@role,'textbox')])[1]")
                acc.move_to_element(xpel).click().send_keys_to_element(xpel, forward_to).perform()
                tm.sleep(1)
                if self.click("(//div[@class='_199zF _3j691 _2N1Gm'])[1]") == 1:
                    tm.sleep(1)
                    if self.click("//*[@data-testid='send']") == 1:
                        print('forward success')
                else: print('cound not select')
            else: print('forward button from foter not found')
        else:  print('msg additional menu not found')
    
    def dict_to_df(self, dc, out=None):
        x = dt.datetime.now().strftime('%b%d%Y_%H%M')
        opt = x  + '.csv' if out is None else x + '_' + out + '.csv'
        pd.DataFrame.from_dict(dc).to_csv(opt)
    
    def chat_msg(self, n, base="(//div[@id='main']//div[@data-testid='msg-container'])", xpt_print=False):
        bi = base + '[' + str(n) + ']' if n is not None else base
        if self.xpelem(bi) is None: return None
        else:
            self.move_click(bi + "//div[@role='button'][contains(.,'Read more')]")
            dttm, sender = self.msg_sender_dttm(n)
            dc = {'sender' : [sender],
                  'text' : [self.xptext(bi + "//div[@class='_21Ahp']/span[1]/span")],
                  'q_sender' : [self.xptext(bi + "//div[@class='_3pMOs yKTUI']//div[1]/span")],
                  'q_text' : [self.xptext(bi + "//div[@class='_3pMOs yKTUI']//div[2]/span")],
                  'datetime' : [dttm]}
            return dc
   
    def side_pane(self, n=2, base="(//div[@id='pane-side']//div[@class='_8nE1Y'])"):
        bi = base + '[' + str(n) + ']' if n is not None else base
        if self.xpelem(bi) is None: return None
        dc = {'chat_name' : bi + "//div[@class='_21S-L']//span[@dir='auto']",
              'last_text' : bi + "//span[@data-testid='last-msg-status']",
              'last_sender' : [bi + "//div[@class='vQ0w7']//span[@dir='auto']", 
                               bi + "//span[@data-testid='status-dblcheck']"],
              'last_msg_time' : bi + "/div[@class='y_sn4']/div[@class='Dvjym']",
              'new_msg_notif' : bi + "//div[@class='Dvjym']//span[@data-testid='icon-unread-count']"}
        for k, v in dc.items():
            v = [v] if type(v) is str else v
            dc[k] = [self.xptext(j) for j in v]
        return dc
    
    