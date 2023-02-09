import datetime as dt
import os
import time as tm

wapane_chat = "//div[@id='pane-side']"
wapane_chat_base = "//div[@data-testid='cell-frame-container']"
wapane_chat_text_base = "//div[@class='_8nE1Y']"
wapane_chat_name = "//div[@class='y_sn4']//span"
wapane_chat_last_time = "//div[@class='y_sn4']//div[2]"
wapane_chat_last_msg = "//div[@class='vQ0w7']//span[@dir='ltr']"
wapane_chat_group_last_msg_sender = "//div[@class='vQ0w7']//span[@dir='auto']"
wapane_chat_unread_count = "//span[@data-testid='icon-unread-count']"
wapane_chat_axes = "//ancestor::" + wapane_chat_base.replace('//','')
wapane_chat_by_name = lambda chatname: wapane_chat_name + "[contains(.,'" + chatname + "')]//ancestor::" + wapane_chat_base.replace('//','')
wp_chat_name = lambda chatname : wapane_chat_by_name(chatname)
wp_chat_last_msg = lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_last_msg
wp_chat_last_msg_time = lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_last_time
wp_chat_unread_count_byname = lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_unread_count
wapane_chat_by_text = lambda text: "(" + wapane_chat_base + wapane_chat_text_base + ")[contains(.,'" + text + "')]"
wapane_chat_by_name_4select = lambda chatname: wapane_chat_name + "[contains(.,'" + chatname + "')]"
conversation_weekday_str = "//span[@class='_11JPr']"
weekday_by_text = lambda text : "//span[contains(@class,'_11JPr') and contains(.,'" + str(text) + "')]"
msg_base_start_index = "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[1]"
msg_base_last_index = "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[last()]"
msg_base_last_index_minus = lambda n: "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[last()-" + str(n) + "]"
conversation_title = "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']"
conversation_body = "//div[@data-testid='conversation-panel-body']"
conversation_text_area = "//footer[@class='_3E8Fg']//p"
msg_container_arrow = "//span[@data-testid='down-context']"
msg_container_menu = "//ul//li"
msg_menu_select = lambda bytext : "//ul//li[contains(.,'" + bytext + "')]"
msg_base = "//div[@id='main']//div[@data-testid='msg-container']"
msgbs = "//div[@class='ItfyB _3nbHh']"
msg_main_sender = "//div[@class='_27K43 _31p5Q']/div[1]//span[@dir='auto']"
msg_main_text = "//div[@class='_21Ahp']//span[@dir='ltr']"
msg_main_time = "//div[@data-testid='msg-meta']"
msg_quote_sender = "//div[@data-testid='quoted-message']/div/div/div/div[1]/span"
msg_quote_msisdn = "//div[@data-testid='quoted-message']//span[@class='WJuYU']"
msg_quote_text = "//div[@data-testid='quoted-message']//div[@dir='ltr']"
msg_container_axes = "//ancestor::div[@data-testid='msg-container']"
msg_main_contain_image = ""
msg_main_datetime = "//div[@data-pre-plain-text]"
msg_by_sender = lambda name : "(//div[@class='_27K43 _31p5Q'])/div[1]/span[contains(@dir,'auto') and contains(., '" + name + "')]"
msg_by_text_time = lambda text, time : "//div[contains(@class,'_21Ahp') and contains(., '" + text + "') and contains(.,'" + str(time) + "')]"
msg_container_by_sender = lambda name : msg_by_sender(name) + msg_container_axes
msg_container_by_text_time = lambda text, time : msg_by_text_time(text, time) + msg_container_axes
msg_xpt_append = lambda xpt, add : xpt + add

def msg_container(sender, text, time):
    x1 = msg_container_by_sender(sender) + msg_by_text_time(text, time)
    return x1

xpath_dict = {
    'wapane_chat': "//div[@id='pane-side']",
    'wapane_chat_base': "//div[@data-testid='cell-frame-container']",
    'wapane_chat_text_base': "//div[@class='_8nE1Y']",
    'wapane_chat_name': "//div[@class='y_sn4']//span",
    'wapane_chat_last_time': "//div[@class='y_sn4']//div[2]",
    'wapane_chat_last_msg': "//div[@class='vQ0w7']//span[@dir='ltr']",
    'wapane_chat_group_last_msg_sender': "//div[@class='vQ0w7']//span[@dir='auto']",
    'wapane_chat_unread_count': "//span[@data-testid='icon-unread-count']",
    'wapane_chat_axes': "//ancestor::" + wapane_chat_base.replace('//',''),
    'wapane_chat_by_name': lambda chatname: wapane_chat_name + "[contains(.,'" + chatname + "')]//ancestor::" + wapane_chat_base.replace('//',''),
    'wp_chat_name': lambda chatname : wapane_chat_by_name(chatname),
    'wp_chat_last_msg': lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_last_msg,
    'wp_chat_last_msg_time': lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_last_time,
    'wp_chat_unread_count_byname': lambda chatname : wapane_chat_by_name(chatname) + wapane_chat_unread_count,
    'wapane_chat_by_text': lambda text: "(" + wapane_chat_base + wapane_chat_text_base + ")[contains(.,'" + text + "')]",
    'wapane_chat_by_name_4select': lambda chatname: wapane_chat_name + "[contains(.,'" + chatname + "')]",
    'conversation_weekday_str': "//span[@class='_11JPr']",
    'weekday_by_text': lambda text : "//span[contains(@class,'_11JPr') and contains(.,'" + str(text) + "')]",
    'msg_base_start_index': "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[1]",
    'msg_base_last_index': "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[last()]",
    'msg_base_last_index_minus': lambda n: "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[last()-" + str(n) + "]",
    'conversation_title': "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']",
    'conversation_body': "//div[@data-testid='conversation-panel-body']",
    'conversation_text_area': "//footer[@class='_3E8Fg']//p",
    'msg_container_arrow': "//span[@data-testid='down-context']",
    'msg_container_menu': "//ul//li",
    'msg_menu_select': lambda bytext : "//ul//li[contains(.,'" + bytext + "')]",
    'msg_base': "//div[@id='main']//div[@data-testid='msg-container']",
    'msgbs': "//div[@class='ItfyB _3nbHh']",
    'msg_main_sender': "//div[@class='_27K43 _31p5Q']/div[1]//span[@dir='auto']",
    'msg_main_text': "//div[@class='_21Ahp']//span[@dir='ltr']",
    'msg_main_time': "//div[@data-testid='msg-meta']",
    'msg_quote_sender': "//div[@data-testid='quoted-message']/div/div/div/div[1]/span",
    'msg_quote_msisdn': "//div[@data-testid='quoted-message']//span[@class='WJuYU']",
    'msg_quote_text': "//div[@data-testid='quoted-message']//div[@dir='ltr']",
    'msg_container_axes': "//ancestor::div[@data-testid='msg-container']",
    'msg_main_contain_image': "",
    'msg_main_datetime': "//div[@data-pre-plain-text]",
    'msg_by_sender': lambda name : "(//div[@class='_27K43 _31p5Q'])/div[1]/span[contains(@dir,'auto') and contains(., '" + name + "')]",
    'msg_by_text_time': lambda text, time : "//div[contains(@class,'_21Ahp') and contains(., '" + text + "') and contains(.,'" + str(time) + "')]",
    'msg_container_by_sender': lambda name : msg_by_sender(name) + msg_container_axes,
    'msg_container_by_text_time': lambda text, time : msg_by_text_time(text, time) + msg_container_axes,
    'msg_xpt_append': lambda xpt, add : xpt + add
    }


def logwite(data, filepath):
    try:
        fp = open('watem_log\\' + filepath + '.txt', 'a+')
        fp.write(str(data+ chr(10)))
        fp.close()
    except:
        try:
            os.system('mkdir watem_log')
            tm.sleep(.5)
            fp = open('watem_log\\' + filepath + '.txt', 'a+')
            fp.write(str(data + chr(10)))
            fp.close()
        except: pass

def xpelem(driver, xpt, text=False):
    print(xpt)
    def log(rs):
        dttm = dt.datetime.now()
        #logwite(xpt + ',' + rs, dttm.strftime('%d%m%Y'))
    try:
        x = driver.find_element(By.XPATH, xpt)
        if text == False:
            #log('Exist:1')
            return x
        else:
            #log('text:' + str(x.text))
            return x.text
    except:
        #log('Exist:0')
        return None

def wapane_chat_xptgen(chatname=None, n=0, bs=None):
    default_pane_base = '(' + wapane_chat + wapane_chat_text_base + ')'
    #"(//div[@id='pane-side']//div[@data-testid='cell-frame-container'])"
    if chatname is not None and bs is None:
        bs0 = "//div[@class='_21S-L']//span[@dir='auto' and contains(.,'" + chatname + "')]//ancestor::div[@data-testid='cell-frame-container']"
    elif chatname is None and bs is None:
        bs0 = default_pane_base + '[last()]' if n==0 else default_pane_base + '[' + str(n) + ']'
    elif chatname is not None and bs is not None:
        bs1 = bs + "[contains(.'" + chatname + "')"
        bs0 = bs1 if n==0 else bs1 + "[" + str(n) + ']'
    elif chatname is None and bs is not None:
        bs0 = default_pane_base + '[last()]' if n==0 else bs + '[' + str(n) + ']'
    else:
        print('else printed from func: wpane_chat_by_name')
        bs0 = None
    return bs0

def wapane_chat_type(d, chatname=None, n=0, bs=None):
    xpt = wapane_chat_xptgen(chatname, n, bs) + "//div[@data-testid='chatlist-status-v3-ring']"
    if xpelem(d, xpt) is None or xpelem(d, xpt) == '0':
        return 'group'
    else: return 'contact'

def wapane_chat_xpath(chatname=None, text=None):
    if chatname is not None and text is not None:
        bs = wapane_chat_text_base + "div[contains(.,'" + str(chatname) + "') and contains(.,'" + str(text) + "')]" + wapane_chat_axes
    elif chatname is not None:
        bs = wapane_chat_by_name(chatname)
    elif chatname is not None:
        bs = wapane_chat_by_text(text) + wapane_chat_axes
    else:
        return None
    dc = {'chat_name' : bs + "//div[@class='y_sn4']//span",
        'last_time' : bs +  "//div[@class='y_sn4']//div[2]",
        'last_msg' : bs + "//div[@class='vQ0w7']//span[@dir='ltr']",
        'group_last_sender' : bs + "//div[@class='vQ0w7']//span[@dir='auto']",
        'wapane_chat_unread_count' : bs + "//span[@data-testid='icon-unread-count']"}
    return dc

def wapane_contacts_last_msg(d,  chatname):
    bs1 = wapane_chat_xptgen(chatname)
    ctype = wapane_chat_type(d, chatname)
    if ctype == 'group':
        return xpelem(d, bs1 + wapane_chat_group_last_msg_sender ,text=True)
    else:
        return chatname if xpelem(d, bs1 + "//div[@class='_2qo4q _3NIfV']") is None else 'You'

def wapane_chat_info(d, chatname=None, n=0, bs=None):
    ctype = wapane_chat_type(d, chatname, n, bs)
    bs1 = wapane_chat_xptgen(chatname, n, bs) + wapane_chat_text_base
    print(bs1)
    dc = {'chat_type' : ctype}
    dc['chat_name'] = [xpelem(d, bs1 + wapane_chat_name, text=True)]
    dc['last_update_time']= [xpelem(d, bs1 + wapane_chat_last_time,text=True)]
    if ctype == 'group':
        dc['last_sender'] = [xpelem(d, bs1 + wapane_chat_group_last_msg_sender ,text=True)]
    else:
        dc['last_sender'] = chatname if xpelem(d, bs1 + "//div[@class='_2qo4q _3NIfV']") is None else 'You'
    dc['last_msg'] = [xpelem(d, bs1 + wapane_chat_last_msg, text=True)]
    dc['unread_count'] = [xpelem(d, bs1 + wapane_chat_unread_count,text=True)]
    return dc