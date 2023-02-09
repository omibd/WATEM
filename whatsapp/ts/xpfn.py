import os
import time as tm
import datetime as dt

def logwite(data, filepath):
    try:
        fp = open('watem_log\\' + filepath, 'a+')
    except:
        os.system('watem_log')
        tm.sleep(.5)
        fp = open('watem_log\\' + filepath, 'a+')
    fp.write(str(data))
    fp.close()
    
    
def xpelm(driver, xpt, text=False,):
    def log(rs):
        dttm = dt.datetime.now()
        logwite(xpt + ',' + rs, dttm.strftime('%d%m%Y'))
    try:
        x = driver.find_element(By.XPATH, xpt)
        if text == False:
            log('Exist:1')
            return x
        else:
            log('text:' + str(x.text))
            return x.text
    except:
        log('Exist:0')
        return None

pane_chat_by_name = lambda chatname: "//div[@class='_21S-L']//span[@dir='auto' and contains(text(),'" + chatname + "')]//ancestor::div[@class='_8nE1Y']"
pane_chat_unread_msg_count = lambda chatname : "//div[@class='_21S-L']//span[@dir='auto' and contains(text(),'" + chatname + "')]//ancestor::div[@class='_8nE1Y']//div[@class='Dvjym']//span[@data-testid='icon-unread-count']"

def wpane_contact_or_group(driver, container_xpt):
    xpt = container_xpt + "//div[@data-testid='chatlist-status-v3-ring']"
    if xpelm(driver, xpt) is None or xpelm(driver, xpt) == '0' or type(xpelm(driver, xpt)) is int:
        return 'group'
    else: return 'contact'
    
def wbody_last_msg_by_text(text):
    txtm = "(//div[contains(@class,'_21Ahp') and contains(., '" + text + "')])[last()]"
    fxpt = txtm + "/ancestor::div[@data-testid='msg-container']"
    return fxpt

def wbody_last_msg_by_text_time(text, time):
    txtm = "//div[contains(@class,'_21Ahp') and contains(., '" + text + "') and contains(.,'" + str(time) + "')]"
    fxpt = txtm + "/ancestor::div[@data-testid='msg-container']"
    return fxpt


def pane_chats_info(index=None, chatname=None, parent = "(//div[@id='pane-side']//div[@class='_8nE1Y'])"):
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