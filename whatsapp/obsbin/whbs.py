import os,sys
from datetime import *
from dateutil.parser import *
from bs4 import BeautifulSoup


def bs_div_get_date(html, search_attr='data-pre-plain-text',tag="div"):
    sp = BeautifulSoup(html, "lxml")
    x = sp.find_all(tag)
    F = "0"
    for i in x:
        try:
            tm = i[search_attr]
            try:
                F= tm.string
            except:
                F = tm
        except:
            pass
    if F == "0":
        return '0', '0'
    else:
        dt = F.strip()
        y1 = dt.find(']')
        dtt = dt[1:y1]
        d = parse(dtt, fuzzy=True, yearfirst=False)
        try:
            return d.strftime("%Y-%m-%d")
        except:
            return '0'


def bs_div_all(html, search_attr='data-pre-plain-text',tag="div"):
    sp = BeautifulSoup(html, "lxml")
    x = sp.find_all(tag)
    F = "0"
    for i in x:
        try:
            tm = i[search_attr]
            try:
                F= tm.string
            except:
                F = tm
        except:
            pass
    if F == "0":
        return '0', '0'
    else:
        dt = F.strip()
        y1 = dt.find(']')
        dtt = dt[1:y1]
        d = parse(dtt, fuzzy=True, yearfirst=False)
        dttm = d.strftime("%Y-%m-%d %H:%M:%S")
        sender = dt[y1+1:len(dt)-1]
        #print(dttm,'--', sender)
        if dttm is not None and sender is not None:
            return  dttm, sender
        else:
            return '0', '0'

#,"//span[@class='a71At i0jNr']"

def bs4_1(ht, cls = []):
    if len(cls)==0:
        cls = ['a71At _3xSVM i0jNr','i0jNr selectable-text copyable-text','a71At i0jNr','quoted-mention i0jNr','kOrB_']
    sp = BeautifulSoup(ht, "lxml")
    ls = []
    for i in cls:
        v1 = sp.find('span', class_= i)
        try:
            if v1.string is not None:
                ls.append(v1.string)
            else:
                ls.append('0')
        except:
            ls.append("0")
    return ls


def wh_msg_bs4(html, cls=[]):
    ls = bs4_1(html,cls)
    sn, dt = bs_div_all(html)
    try:
        d = parse(dt, fuzzy=True, yearfirst=False)
        d2 = d.strftime("%Y-%m-%d %H:%M")
    except:
        d2 = '0'       
    ls.append(d2)
    if ls[0] == "0":
        ls[0] = sn
    #print(ls)
    return ls
    


