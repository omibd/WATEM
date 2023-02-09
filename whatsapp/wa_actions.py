from imports import *
from xbuilder import *
import waxpath as wpn

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
        
def wtx(d, xpt, wt=1):
    try: return d.find_element(By.XPATH, xpt).text
    except: return None

def ww(d, xpt, sec=2):
    wait = WebDriverWait(d, sec)
    try: return wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
    except: return None

def action(d, k, v):
    ac = ActionChains(d)
    if k in '_sendtxt_': 
        ac.send_keys_to_element(ww(d,v[0]), v[1]).send_keys(Keys.RETURN).perform()
        return 1
    elif 'clk' in k:
        ActionChains(d).click(ww(d, v[0],5)).perform()
        return 1
    elif k in '_hoverclk_':
        ac.move_to_element(ww(d,v[0])).perform()
        ac.click(ww(d,v[1])).perform()
        return 1
    elif 'present' in k:
        if ww(d, v[0], 5) is None: return 0
        else: return 1
    else: 
        print('nothing matched')
        return False

def key_checker():
    pass

def pending_jobs(d, action_dic, check_from_key = None):
    '''check key and return pending jobs'''
    key_found, dc = False, {}
    for k, v in action_dic.items():
        if check_from_key is not None and key_found==False:
            if k == check_from_key: 
                key_found = True
                dc = {k:v}
        else:
            dc[k] = v
    else: return dc

def rjobs(d, action_dic):
    '''check action dictionary reversely and returns key but returns 1 while last key is present'''
    for i in reversed(list(action_dic)):
        print(i, action_dic[i][0])
        elm = ww(d, action_dic[i][0])
        if elm is not None:
            if 'present' in i: return 1
            else: return i
        else: 
            print(action_dic[i][0])
            
def fw_selections(d, fw_actions,contacts_and_xpath=[('omi','xpath')]):
    for x in range(3):
        if rjobs(d, fw_actions) == 1:
            break
    else: 
        print('h1: forwared msg not found')
        return None
    print('fw selection action processing')
    for n in contacts_and_xpath:
        name, xpt = n
        try:
            ac = ActionChains(d)
            v = ["//div[@data-testid='input-placeholder']/following-sibling::div",name]
            ac.send_keys_to_element(ww(d,v[0]), v[1]).send_keys(Keys.RETURN).pause(1).perform()
            tm.sleep(1)
            ActionChains(d).click(ww(d,xpt)).pause(1).perform()
            tm.sleep(1)
            ActionChains(d).click(ww(d,"//span[@data-testid='x-alt']")).perform()
            tm.sleep(.5)
        except:
            print('fail')
            return None
    else:
        return wtx(d, "//div[@id='app']/div[1]/span[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]")

def click_write_enter(d, xpt, text):
    ac = ActionChains(d)
    xp = ww(d, xpt) if type(xpt) is str else xpt
    if xp is None: return 0
    else:
        print('writing init')
        xp.clear()
        if chr(10) not in text:
            ac.move_to_element(xpt).click().send_keys(text).send_keys(Keys.RETURN).perform()
        else:
            xx = text.split(chr(10))
            for line in xx:
                ac.send_keys(line).perform()
                ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ac.send_keys(Keys.RETURN).perform()

pnbase ="div[@data-testid='cell-frame-container']"
pane_chat_byname = lambda chatname: "//div[@class='y_sn4']//span" + "[contains(.,'" + chatname + "')]//ancestor::" + pnbase

def select_chat(d, chat_name):
    if chat_name is not None and chat_name != '':
        convtitle = "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']"
        xx = wtx(d, convtitle)
        if xx is not None and chat_name.lower() in xx.lower(): 
            print('already selected')
            wclk(d,'/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[1]/span/div/span[2]')
            return 1
        else:
            if wclk(d, pane_chat_byname(chat_name)) == 0:
                print('chat has no communication')
                ActionChains(d).send_keys_to_element(ww(d,"/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"),chat_name).send_keys(Keys.RETURN).pause(1).perform()
            y = wtx(d, convtitle)
            print('chat body name: ', y)
            if chat_name.lower() in y.lower():
                print('chat selection successful')
                wclk(d,"//div[@id='side']//span[contains(@data-testid,'x-alt')]")
                wclk(d,"//div[@id='side']//button[@aria-label='Unread chats filter']")
            else: 0
    else: return 0

forward = lambda d, chatname, search_xpath, text : \
        {'func': {
            'function': select_chat(d, chatname),
            'move_func': search_xpath
            },
         'clicking':{
            'clk_1': ["//span[@data-testid='down-context']"],
            'clk_2': ["//ul//li[contains(.,'Forward message')]"],
            'clk_3': ["//button[@title='Forward message']"],
            'is_present':["//h1[text()='Forward message to']"]
         }}

reply = lambda d, chatname, search_xpath, text : \
        {'function': select_chat(chatname),
         'move_func': search_xpath,
         'clk_1': ["//span[@data-testid='down-context']"],
         'clk_2': ["//ul//li[contains(.,'Reply')]"],
         'clk_3': ["//button[@title='Forward message']"],
         'present': ["//div[@data-testid='popup_panel']"],
         'clk_write':["//footer[@class='_3E8Fg']//p", text]}

react = {'clk_1': ["//span[@data-testid='down-context']"],
    'clk_2': ["//ul//li[contains(.,'Forward message')]"],
    'clk_3': ["//button[@title='Forward message']"],
    'is_present':["//h1[text()='Forward message to']"]}

delete = {'clk_1': ["//span[@data-testid='down-context']"],
    'clk_2': ["//ul//li[contains(.,'Forward message')]"],
    'clk_3': ["//button[@title='Forward message']"],
    'is_present':["//h1[text()='Forward message to']"]}

def fw_operations_and_xyz(d, fw_actions, xyz='OPS & RO', send=False):
    operations = x_contains(not_contains, wpn.xpath_dict['wapane_chat_by_name']('Operations'), [('.','Network'), ('.','Technology')], 'contains')
    ops_ro = wpn.xpath_dict['wapane_chat_by_name'](xyz)
    rs = fw_selections(d, fw_actions, [('operations', operations), (xyz, ops_ro)])
    if 'operations' in rs.lower() and xyz.lower() in rs.lower():
        print('fw selection ok')
        if send == True:
            ActionChains(d).click(ww(d,"//span[@data-testid='send']")).perform()
            print('success')
        return 1


#fw_operations_and_xyz(dd, xyz='OPS & RO', send=False)