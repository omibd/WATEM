import os, sys, time, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import subprocess, os, sys, time
mypath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,mypath)

from whatsapp import *

def typnt(hd, ob):
    try:
        if type(ob) is str:
            print(ob)
        else:
            print(hd,': ', ob.text)
    except: pass

def reload(driver, wait_sec=60):
    wait = WebDriverWait(driver, wait_sec)
    driver.refresh()
    search_bar_xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"
    element = wait.until(EC.presence_of_element_located((By.XPATH, search_bar_xpt)))
    print('element found')

def chainclick(driver, xp1="(//span[contains(@class,'caret')])[3]", xp2="/html/body/nav/div/div[2]/ul[3]/li/ul/li[5]/a"):
    try:
        el = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, xp1)))
        actions = ActionChains(driver).move_to_element(el).click().perform()
        sbmenu = driver.find_element(By.XPATH, xp2)
        ac = ActionChains(driver).move_to_element(sbmenu).click().perform()
        return True
    except:
        print('chainclick except triggered')
        return False           

def execute(driver, xpth="//a[@class='btn btn-info'][contains(.,'Execute')]"):
    clickable_elem(driver, xpth)
    print('found executed button and clicked')
    time.sleep(5)
    driver.switch_to.alert.accept()
    print('waiting for execution wip msg')
    return True

def scrol_up(driver, js="arguments[0].scrollIntoView(true);", limit=1):
    x = "//div[@class='_2gzeB']"
    l = driver.find_element('xpath', x)
    try:
        driver.execute_script(js, l)
    except:
        return -1
    
def scroll(driver, js="document.getElementById('pane-side').scrollTop={}", initial = 1, scrolls=25):
    for i in range(0, scrolls):
        driver.execute_script(js.format(initial))
        initial += 300
        
def scroll_main(driver, js="document.getElementById('main').scrollTop={}", initial = 1, scrolls=25):
    for i in range(0, scrolls):
        driver.execute_script(js.format(initial))
        initial -= 300
        
def scrolldyn(driver, js="document.getElementById('main').scrollTop={}", initial = 1, scrolls=25):
    for i in range(0, scrolls):
        driver.execute_script(js.format(initial))
        initial += 300

def xc(driver, xpt, click=True): #clickable
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpt)))
        if click: element.click()
        else: return element
    except: return False

def xp(driver, xpt): #presence
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
        print('element found and returned')
        return element
    except: return False

def xt(driver, xpt):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpt))).text
        print(xpt, " Text: ", element)
        return element
    except: return False

def xfill(driver, xpt, txt):
    wait = WebDriverWait(driver, 10)
    element = xp(driver, xpt) if type(xpt) is str else xpt
    element.clear()
    if element != False:
        ac = ActionChains(driver)
        ac.move_to_element(element).click().perform()
        if chr(10) in txt:
            xx = txt.split(chr(10))
            for line in xx:
                ac.send_keys(line).perform()
                ac.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ac.send_keys(Keys.RETURN).perform()
        else:
            ac.send_keys(txt).perform()

def process_chain(driver, xptdict):
    #dictionary_construction = {'xpat':'action', 'xpath','click'}
    actions = ActionChains(driver)
    for k, v in xptdict.items():
        if len(v) == 0:
            xt(driver, k)
        else:
            elm = xp(driver, k)
            if elm != False:
                actions.move_to_element(elm).click().perform()

def select_chat(driver, name, search_bar_xpt = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]"):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, search_bar_xpt)))
    element.clear()
    ac = ActionChains(driver)
    ac.move_to_element(element).click().perform()
    ac.send_keys(name).send_keys(Keys.RETURN).perform()

def scrollup_chat_main(driver, xpt="(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]"):
    wait = WebDriverWait(driver, 30)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return 1

def scrollDown(driver, xpt="(//div[@class='_3OvU8'])[2]"):
    wait = WebDriverWait(driver, 30)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpt)))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return 1

class Wakit(whapp):
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.chats_unread = {}
        print(self.driver.title)
        
    @property
    def get_driver(self):
        return self.driver

fp = open("ho.txt","r")
data = fp.read()
fp.close()

#count_avail_msg = "count(" + "(//div[@id='main']//div[@class='y8WcF']/div)" + "[last()]//preceding-sibling::*)"
count_avail_chat = "count(" + "(//div[@id='pane-side']//div[@class='_3OvU8'])" + "[last()]//preceding-sibling::*)"
x = Wakit()
d = x.get_driver
reload(d)
df = x._read_message('SOC-RO')
print(df)
"""/html[@class='js serviceworker adownload cssanimations csstransitions webp exiforientation webp-alpha webp-animation webp-lossless wf-loading']/body[@class='web']
/div[@id='app']
/div[@class='_1Fm4m _1h2dM app-wrapper-web font-fix os-win']
/div[@class='_1jJ70 two']
/div[@class='_2Ts6i _2xAQV']
/div[@id='main']
/div[@class='_2gzeB']
/div[@class='tm2tP copyable-area']
/div[@class='_33LGR']"""
#scrollup(d, "(//div[@id='main']//div[@class='ItfyB _3nbHh'])[2]")
#reload(d)

JS = lambda attr,  idd : "document.getElementBy" + attr + "('" + idd + "').scrollTop={}"

#x1 = "//div[@'conversation-panel-messages']"
#xfill(d, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]","onamika")
#xfill(d, "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']",data)
#xfill(d, "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']","love u futu")
#xfill(d, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]","father")
#xfill(d, "(/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer)//DIV[@role='textbox']",data)
#reload(d)
#emoji_button = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[2]/div/span"
#first_emo = "/html/body/div[1]/div/div/div[4]/div/footer/div[2]/div/div[4]/div/div/div[2]/div/div/div/div/div/div[7]/div/div/div/span"
#x._read_message('emergency')