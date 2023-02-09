import datetime as dt
from wabs import *

contains = lambda attr, value: "contains(" + attr + ",'" + value + "')"
starts_with = lambda attr, value: "starts-with(normalize-space(" + attr + "),'" + value + "')"
ends_with = lambda attr, value: "ends-with(normalize-space(" + attr + "),'" + value + "')"

def xpgen_1(fn, tag='*', attr=['.'], value=['TEXT']):
    ls = lambda x: x if type(x) is list else [x]
    tag = tag if tag is not None else "*"
    attr, value = ls(attr), ls(value)
    lx = []
    for a, b in zip(attr, value):
        if a.find('.') != -1: lx.append(fn(a, b))
        else: lx.append(fn('@' + a, b))
    xpg = tag + "[" + ' and '.join(lx) + "]"
    return xpg

def xpgen_2(d, base, fn):
    def xpg(index=None, before=None, after=None):
        bi = base + "[" + str(index) + "]" if index is not None else base
        bi = str(before) + bi if before is not None else bi
        bi = bi + str(after) if after is not None else bi
        return bi
    return xpg

def xpgen_3(base):
    def xpg(index=None, before=None, after=None):
        bi = base + "[" + str(index) + "]" if index is not None else base
        bi = str(before) + bi if before is not None else bi
        bi = bi + str(after) if after is not None else bi
        dc = {'p_chatname': bi + "//div[@class='y_sn4']//span",
                'p_time' : bi + "//div[@class='y_sn4']//div[2]",
                'p_msg' : bi + "//div[@class='vQ0w7']//span[@dir='ltr']",
                'p_sender' : bi + "//div[@class='vQ0w7']//span[@dir='auto']",
                'p_count' : bi +"//span[@data-testid='icon-unread-count']"}
        return bi
    return xpg

def contain(text):
    tx = [text] if type(text) is str else text
    rs = [contains('.', i) for i in tx]
    return ' and '.join(rs)

pside = "//div[@id='pane-side']"
pbs = "//div[@data-testid='cell-frame-container']"
pbtx = "//div[@class='_8nE1Y']"
pb = '(' + pbs + ')'
pbt = '(' + pbs + pbtx + ')'
pbx = '(' + pside + pbs + ')'
p_chatname = "//div[@class='y_sn4']//span"
p_time = "//div[@class='y_sn4']//div[2]"
p_msg = "//div[@class='vQ0w7']//span[@dir='ltr']"
p_sender = "//div[@class='vQ0w7']//span[@dir='auto']"
p_count = "//span[@data-testid='icon-unread-count']"
paxes = "//ancestor::" + pbs.replace('//','')

pn_byname = lambda chatname: '(' + pbtx + p_chatname + ")[contains(.,'" + chatname + "')]" + paxes
pn_bytext = lambda text: "(" + pbtx + ")[" + contain(text) + "]" + paxes
pn_unread = lambda chatname : pn_byname(chatname) + p_count


#ob.action(chat_name='Alauddin vai', search_text='bKash due to security issue',reply='got it vai')


def msgloop(chatname, text=None, base=None):
    bs = "(//div[@data-testid='msg-container'])" if base is None else base
    if ob.click(pn_byname(chatname)) is None:
        if ob.select_chat(chatname) == 0: return "chat not found"
    else:
        bi = bs + "[" + contain(text) + "]" if text is not None else bs
        i, nonecount = 0, 0
        while nonecount<10:
            if i > 0: inx='last()-' + str(i)
            else: inx = 'last()'
            xpdic = ob.msginfo(base = bi + "[" + inx + "]")
            if xpdic is None:
                nonecount = nonecount + 1
                ob.just_move()
                tm.sleep(1)
            else:
                nonecount = 0
                i = i + 1
            yield xpdic, i, nonecount
            
def read_msg_action(chatname='emergency', no_of_sms=50, action_dict={'text_match':'update of site down', 'forward':'halim vai'}):
    loop_done = 0
    ob.select_chat(chatname)
    while comloop<=no_of_sms:
        dd = ob.watem_iter('chat_msg', start=1, end=100, step=1, sdict=defaultdict())
        for dc, loop_done in zip(dd):
            print(loop_done)























