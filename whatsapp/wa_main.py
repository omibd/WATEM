from wabs import *

def sidepane_scroll(d, initial = 1, scrolls=50):
    for i in range(1, scrolls):
        d.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
        initial = initial + i + 1
    return initial

def msg_scoll_up(d):
    d.find_element(By.XPATH, "//div[@class='_5kRIK']").send_keys(Keys.HOME)
    tm.sleep(2)
    return 1

def just_move(d, xpt="(//div[@data-testid='conversation-panel-body'])[2]"):
    try:
        ActionChains(d).move_to_element(ww(d, xpt, 3)).perform()
        tm.sleep(1)
        return 1
    except: return msg_scoll_up(d)
    
def wtx(d, xpt, wt=1):
    try: return d.find_element(By.XPATH, xpt).text
    except: return None

def ww(d, xpt, sec=2):
    wait = WebDriverWait(d, sec)
    try: return wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
    except: return None

def move_click(d, xp1, xp2=None):
    ac = ActionChains(d)
    ac.move_to_element(ww(d,xp1)).click().perform()
    if xp2 is None: ac.click(ww(d,xp1)).perform()
    else: ac.click(ww(d,xp2)).perform()
    
def wclk(d, xpt):
    elm = ww(d, xpt) if type(xpt) is str else xpt
    if elm is None:
        print(xpt, ' not found')
        return None
    else:
        try:
            elm.click()
            print('click success')
            return 1
        except: return 0

def write_msg(d, xpt, text):
    ac = ActionChains(d)
    ac.move_to_element(xpt).click().perform()
    if chr(10) not in text:
        ac.send_keys(text).send_keys(Keys.RETURN).perform()
    else:
        xx = text.split(chr(10))
        for line in xx:
            ac.send_keys(line).perform()
            ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ac.send_keys(Keys.RETURN).perform()

def update_dict_values(a, b):
    '''updating key & values using append then set procedure'''
    c = {}
    for k, v in a.items():
        if k in list(b):
            c[k] = list(set(a[k] + b[k]))
        else:
            c[k] = a[k]
    return {**b, **c}

def update_key_value(a, b):
    '''updating key & values (values will be appened for existing key)'''
    c = {}
    if len(a) == 0: return b
    tls = lambda ls : ls if type(ls) is list else [ls]
    for k, v in a.items():
        c[k] = tls(a[k]) + tls(b[k]) if k in list(b) else tls(a[k])
    else: return {**b, **c}

def search_msg_in_chat(d, chat_name, search_xpath, base):
    no_of_items, same_elm_count = defaultdict(list), 0
    while same_elm_count<=3:
        pre_no_of_items = no_of_items
        no_of_items = len(d.find_elements(By.XPATH, base))
        if no_of_items == pre_no_of_items: same_elm_count = same_elm_count + 1
        else: same_elm_count = 0
        el = ww(d, search_xpath)
        if el is not None: 
            yield el
        msg_scoll_up(d)
    print(same_elm_count, ' is 3/3+ so, seems there is no more content to scroll')
        
        
def is_duplicate(dmain, dnew, key_list=['chat_name', 'last_text']):
    try:
        duplicate = []
        for n in key_list:
            if dnew[n] in dmain[n]: duplicate.append(True)
            else: pass
        if len(key_list) == len(duplicate): return True
        else: return False
    except: return False

def wapane_chat_type(d, bs):
    xpt = bs + "//div[@data-testid='chatlist-status-v3-ring']"
    if ww(d, xpt.strip(' ')) is None: 
        return 'group'
    else: 
        return 'contact'
    
def chatinfo(d, n=None, pane_base="//div[@id='pane-side']//div[@data-testid='cell-frame-container']"):
    base = '(' + pane_base + "//div[@class='_8nE1Y'])" if '_8nE1Y' not in pane_base else pane_base
    bi = base + '[' + str(n) + ']' if n is not None else base
    bi4ctype = '(' + pane_base + ')[' + str(n) + ']' if n is not None else pane_base 
    if ww(d, bi) is None: return None
    print('pane coll xpt not none: ', bi)
    dc = {'chat_type': [wapane_chat_type(d, bi4ctype)],
        'chat_name' : [bi + "//div[@class='y_sn4']//span"],
        'last_text' : [bi + "//div[@class='vQ0w7']//span[@dir='ltr']"],
        'last_sender' : [bi + "//div[@class='vQ0w7']//span[@dir='auto']"],
        'time' : [bi + "/div[@class='y_sn4']//div[@class='Dvjym']"],
        'new_msg_notif' : [bi + "//span[@data-testid='icon-unread-count']"]}
    for k, v in dc.items():
        v = [v] if type(v) is str else v
        dc[k] = [wtx(d, j) for j in v]
    return dc

def msg_sender_dttm(d, xpt):
    elm = ww(d, xpt) if type(xpt) is str else xpt
    html = elm.get_attribute('innerHTML')
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

def msginfo(d, n=None, base="(//div[@id='main']//div[@data-testid='msg-container'])"):
    bi = base + '[' + str(n) + ']' if n is not None else base
    print('msgbase is being collecting:', bi)
    elm = ww(d, bi)
    if elm is None: return None
    else:
        try: ActionChains(d).move_to_element(ww(d, bi + "//div[@role='button'][contains(text(),'Read more')]")).click().perform()
        except: pass
        dttm, sender = msg_sender_dttm(d, elm)
        dc = {'sender' : [sender],
              'text' : [wtx(d, bi + "//div[@class='_21Ahp']/span[1]/span")],
              'q_sender' : [wtx(d, bi + "//div[@class='_3pMOs yKTUI']//div[1]/span")],
              'q_text' : [wtx(d, bi + "//div[@class='_3pMOs yKTUI']//div[2]/span")],
              'datetime' : [dttm],
              'sender_visible': [wtx(d, bi + "//div[@class='_27K43 _31p5Q']/div[1]//span[@dir='auto']")],
              'time': [wtx(d, bi + "//div[@data-testid='msg-meta']/span")]
              }
        dc['img'] = 'image' if ww(d, bi + "//div[@data-testid='image-thumb']", 1) is not None else 'NoImage'
        return dc

def iwh(d, func, end=20, start=1, from_last=False, base=None, where='pane', sdc=defaultdict(list)):
    n, nc, sc, sdclen = start, 0, 1, 0
    while end > sdclen and nc<5 :
        inx = n if from_last == False else 'last()-' + str(n)
        dc = func(d, inx, base) if base is not None else func(d, inx)
        if dc is not None:
            if len(sdc) == 0: sdc = dc
            else:
                if where == 'pane':
                    sdc = update_dict_values(sdc, dc)
                    nc, n = 0, n+1
                elif where == 'msg':
                    if is_duplicate(sdc, dc) == False:
                        sdc = update_key_value(sdc, dc)
                        nc, n = 0, n+1
                    else:
                        if nc>1 and n<2: x.just_move(base + '[' + str(2) +']')
                        else: msg_scoll_up(d)
                        nc = nc + 1
                else: 
                    print('please where args, exiting')
                    return None
                sdclen = len(sdc['time'])
                print('sdc_length:', sdclen)
        else:
            if where == 'pane':
                sc = sidepane_scroll(d,sc)
                n = 1
            elif where == 'msg':
                msg_scoll_up(d)
            nc = nc + 1
    print('none found consecutive even 4 scroll is 3/3+ so, seems there is no more content to scroll')
    return sdc

def current_chat_title(d):
     return wtx(d, "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']")

def loop_read(d, x, chatname=None, end=20, start=1, from_last=None, base=None, where='pane', sdc=defaultdict()):
    if chatname is not None:
        last = True if from_last is None else False
        y = current_chat_title(d)
        if y is not None and chatname.lower() in y.lower():
            dd =  iwh(d, msginfo, end, start, last, base,'msg',defaultdict(list))
            return dd
        else:
            if x.select_chat(chatname) == 1:
                dd =  iwh(d, msginfo, end, start, last, base,'msg',defaultdict(list))
                return dd
            else:
                print(chatname, ' not selected')
    else:
        last = False if from_last is None else True
        dd =  iwh(d, chatinfo, end, start, last, base,'pane',defaultdict(list))
        return dd
