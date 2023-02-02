


import os,sys
from pathlib import Path
sys.path.append(str(Path(os.path.realpath(__file__)).parent.parent.absolute()))

message_dic = {'SENDER':'','SENDER_NAME':'','SENDER_TEXT':'','Q_TEXT':'','Q_SENDER':'',
               'Q_SENDER_NAME':'','TIME':'','BASE':'','DATE_TIME':'','DATA_ID':'','CHAT':''}
msg_col = ['SENDER','SENDER_NAME','SENDER_TEXT','Q_TEXT','Q_SENDER','Q_SENDER_NAME','MSG_TIME','BASE','DATE_TIME','DATA_ID','CHAT']
ignore_text = ["message was deleted", "TODAY","YESTERDAY","FRIDAY","SATURDAY","SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY"]


# _1-lf9 _3mSPV _18q-J
# (//div[@id='main']//div[@class='_1-lf9 _3mSPV _18q-J']/div)[last()]
# ItfyB _3nbHh
# //div[@id='main']//div[@class='ItfyB _3nbHh']/div)[last()]
#S M. Farhadtawhid vaiPSA@1600_05/01. @S M. FarhadRAB assignment fail is the main cause. please engage radio team5:01 pm5:01 pm

msg_base_xpt = "(//div[@id='main']//div[@class='ItfyB _3nbHh'])"
last_msg_div = "(//div[@id='main']//div[@class='ItfyB _3nbHh'])[last()]"
search_msg_dataid = lambda x : "(//div[@id='main']//div[@class='ItfyB _3nbHh']/div)[@data-id='" + x + "']"

def msg_cls_y8wcF_dic(val, msg_xpath=""):
    dc = {}
    if msg_xpath == "":
        msg_xpath = msg_base_xpt
    msgbase = msg_xpath + "[" + str(val) + "]"
    dc['BASE'] = [msgbase]
    dic = {'SENDER':["/div/div/div/div[1]/span[1]","//span[@class='a71At _3xSVM i0jNr']","//span[@class='_1BUvv']"],
           'SENDER_NAME':['/div/div/div/div[1]/span[2]'],
           'SENDER_TEXT':['/descendant::div/span/span[1]','//span[@class="i0jNr selectable-text copyable-text"]'],
           'Q_TEXT':['/div/div/div/div[2]/div[1]/div/div/div/div/div[2]',"//span[@class='quoted-mention i0jNr']",'/div/div/div/div[1]/div[1]/div/div/div/div/div[2]'],
           'Q_SENDER':['/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/span[1]','/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/span',"//span[@class='a71At i0jNr']"],
           'Q_SENDER_NAME':['/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/span[2]'],
           'TIME':["//span[@class='kOrB_']",'/descendant::div[last()]']}
    for k, v in dic.items():
        ls = []
        for i in v:
            ls.append(msgbase + i)
        else:
            dc[k] = ls
    else:
        return dc
    
def msg_cls_child(base_xpt):
    main_div = base_xpt + "//span[@class='kOrB_']" + "/ancestor::div[4]"
    sender_text = base_xpt + '/descendant::div/span/span[1]'
    last_div = base_xpt + '/descendant::div[last()]'
    return [last_div,sender_text,main_div]

def msg_cls_child_search(base_xpt):
    at_time = base_xpt + "//span[@class='kOrB_']"
    main_div = base_xpt + "//span[@class='kOrB_']" + "/ancestor::div[4]"
    sender_text = base_xpt + '/descendant::div/span/span[1]'
    last_div = base_xpt + '/descendant::div[last()]'
    return [last_div,sender_text,main_div]

chat_search_box = "//div[contains(@class,'_13NKt copyable-text selectable-text')]"
selected_profile_header_name = "//HEADER[@class='_23P3O']//SPAN[@class='_ccCW FqYAR i0jNr']"
chat_name = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[1]/div/span"
footer = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]"
footer_textbox = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[2]"
msg_nav_arrow = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[1]/span/div/span[2]"

pane_base = "(//div[@id='pane-side']//div[@class='_3OvU8'])"
pane_search_parent = lambda x : pane_base + "[" + str(x) + "]"
pane_group_last_sender = lambda i: pane_search_parent(i) + "//span[@class='FqYAR i0jNr']"
pane_user_sms =  lambda i : pane_search_parent(i) + "//span[@class='_ccCW FqYAR i0jNr']"
pane_sms_date = lambda i: pane_search_parent(i) + "//div[@class='_3vPI2']/div[@class='_1i_wG']"
pane_notif = lambda i: pane_search_parent(i) + "//div[@class='_1pJ9J']/span"
pane_username = lambda i: pane_search_parent(i) + "//div[@class='zoWT4']"
side_sms = lambda i: pane_search_parent(i) + "/child::div[2]/div/span/span[3]"
side_sms_sender = lambda i: pane_search_parent(i) + "//span[@class='FqYAR i0jNr']"
side_sms_datetime = lambda i: pane_search_parent(i) + "//div[@class='_3vPI2']/div[@class='_1i_wG']"

msg_b = "(//div[@id='main']//div[@class='ItfyB _3nbHh'])"
msg_b_dyn = lambda x : msg_b + "[" + str(x) + "]"
msg_b_axis = lambda div_number, axis, trail_path : msg_b_dyn(div_number) + axis + "::" + trail
msg_last_element = msg_base_xpt + "[last()]"
count_avail_msg = "count(" + "(//div[@id='main']//div[@class='y8WcF']/div)" + "[last()]//preceding-sibling::*)"
count_avail_chat = "count((" + "(//div[@id='pane-side']//div[@class='_3OvU8'])" + "[last()]//preceding-sibling::*)"
count_dyn = lambda xp : "count((" + xp + "[last()]//preceding-sibling::*)"

def xath_query_build_contains(ls, xpt=""):
    hp = []
    if xpt == "":
        xpt = "(//div[@id='main']//div[@class='y8WcF'])"
    if type(ls) is list:
        for i in ls:
            st = "contains(.,'" + str(i) + "')"
            hp.append(st)
        else:
            xx = xpt + "//*[" + ' and '.join(list(hp)) + "]"
            return xx
    else:
        return xpt + "//*[" + "(contains(.," + str(ls) + ")]"

x = msg_cls_y8wcF_dic(2)
#print(x)
#print(x)

#xxx  = xath_query_build_contains(['jalal ahmad'])
#print(xxx)
#msg_base = "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]"
#msg_base_from_top = "//div[@id='main']/div[3]/div[1]/div[2]/div[2]/div[2]"
#msg_dyn = lambda mx : "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[" + str(mx) + "]"
#msg_preceding = lambda xp, i : xp + "/preceding-sibling::div[" + str(i) + "]"

#msg_base_multi = ["//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]",
#        "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]/preceding-sibling::div[1]",
#        "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]/preceding-sibling::div[2]",
#        "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]/preceding-sibling::div[3]",
#        "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]/preceding-sibling::div[4]",
#        "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]/preceding-sibling::div[5]"]
#

#axis_keys = ['ancestor','parent''self','child','Descendant','following','following-sibling','preceding','preceding-sibling']
#axis_info = {
#    'ancestor':["//input//ancestor::div[@id='reg_box']","Find the div which will be grandarent of input"],
#    'parent':["//input[@id='2']/parent::div","Find the immediate parent Div of the current node"],
#    'child':["//div[@id='reg_form_box']/child::span"," return immidiate child span those are child div"],
#    'Descendant':["//div[@id='reg_form_box']/child::span","return all child and granchild span tag those are under div"],
#    'following':["//div[@id='2']/following::input[@name='first']","return all input after end of curren div"],
#    'following-sibling':["following-sibling","Select all the sibling nodes of the current node"],
##    'preceding':["//form/preceding::form//input[@id='email']","Select Email Text Box in form"],
#    'preceding-sibling':["//table//tr[3]/preceding-sibling::tr","Select the second row from table"]
#    }

#XPath_Methods = {
#    'starts-with()' : ["//input[starts-with(@id,'ema')]"," Find any input tag whose attribute id starts with value 'ema'"],
#    'contains' : ["//input[contains(@id,'pass')]","Find only input tag whose attribute contains 'pass'"],
##    'end-with()': ["//input[ends-with(@id,'pass')]","Find only input tag whoxse attribute text end-with 'pass'"],
#    'contains': ["//a[contains(text(),'stagr')","Find a tag whose value or text contains 'stagr' i.e.  Instagram"]
#    }

#(//div[@id='main']//div[@class='y8WcF']/div)[@data-id='false_8801817183680-1533043027@g.us_95DE05E667AAD4E32F5E2C0E5B8EAC8B']         
#mxp = "//div[@id='main']/div[3]/div[1]/div[2]/div[3]/div[2]"
#print(count_dyn(find_element_and_operation(contain=['ABCD','5:32'])))
#(//div[@id='main']//div[@class='y8WcF']/div)[2]
#sender_msg_tm = lambda sender, msg, tm : "(//div[@id='main'])//div[@class='_22Msk'][contains(.,'" + str(msg) + "') and contains(.,'" + str(tm) + "') and contains(.,'" + str(sender) + "')]"
#sender_msg_tm_msg = lambda sender, msg, tm : sender_msg_tm(sender, msg, tm) + "//div[@class='_1Gy50']"
#sender_msg_tm_sender = lambda sender, msg, tm : sender_msg_tm(sender, msg, tm) + "//div[@class='_1Gy50']/ancestor::div[2]/div[1]"
#sender_msg_tm_tm = lambda sender, msg, tm : sender_msg_tm(sender, msg, tm) + "//div[@class='kOrB_']"
#def msg_cls_y8WcF(msgbase):
#    sender = msgbase + "/div/div/div/div[1]/span[1]"
#    sender_name = msgbase +"/div/div/div/div[1]/span[2]"
#    sender_text = msgbase + "/descendant::div/span/span[1]"
#    q_text = msgbase + "/div/div/div/div[2]/div[1]/div/div/div/div/div[2]"
#    q_sender = msgbase + "/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/span[1]"
#    q_sender_name = msgbase + "/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/span[2]"
#    tm = msgbase + "/descendant::div[last()]"
#    ls = [msgbase,sender,sender_name,sender_text,q_text,q_sender,q_sender_name,tm]
#    return ls

#//DIV[@role='textbox'][text()='test']
#//DIV[@id='pane-side']
#//div[@id="head" and position()=2]
#//*[contains(concat( " ", @class, " " ), concat( " ", "_22Msk", " " )) and position()=2]
#//h4/a[contains(text(),'SAP M')]
#//div[contains(@class, '_22Msk')]
#//div[@id='main']//div[@class='Nm1g1_22AX6']
#//div[@id='main']/div[@class='Nmigl_22AX6'][2]
#y1, y2 = x._xpath("/html//div[@id='main']//div[@class='_33LGR']/div[@role='region']/div[22]")
#y3 = y1.text
#y4 = y3.replace(chr(10),"")
#b33 = "//div[@class='_22Msk'][contains(.,'" + y3 + "')]"
#b34 = "//div[@class='_22Msk'][contains(.,'" + y4 + "')]"
#[contains(.,'ARABI')]
#print(msg_tag(x, a1, y2))
#//div[@id='main']
#//div[@id='main']
#//DIV[@role='textbox'][text()='test']
#/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[3]/div[22]//span[@class='a71At _3xSVM i0jNr']
#y5,y6 = x._xpath(b33)
#y7,y8 = x._xpath(b34)
#b4 = b3 + "//div[@class='_3e9My']/span]"
#y1, y2 = x._xpath(b3)
#d = x._DRV()
#action = ActionChains(d)
#action.move_to_element(b3).perform()
#el1 = d.find_element_by_xpath("//a[@href='https://www.pickaboo.com/electronics-appliances.html'][contains(.,'Electronics & Appliances')]")
#el2 = d.find_element_by_xpath("")
#action = ActionChains(d)
#action.move_to_element(el1).perform()
#action.moveToElement(el1).click(el2).build().perform()
#//*[contains(concat( " ", @class, " " ), concat( " ", "_22Msk", " " )) and position()=2]
#//h4/a[contains(text(),'SAP M')]
#//tagname[contains(@attribute, 'value')]
#//div[@id="head" and position()=2]
#//div[(x and y) or not(z)]
#concat(//cricketer[name='Shami']/@type,//cricketer[name='Zaheer Khan']/@type
#concat(String s1, String s2, String... s3)
#//DIV[@role='textbox'][text()='test']
#//DIV[@id='pane-side']
#//div[@id="head" and position()=2]
#//*[contains(concat( " ", @class, " " ), concat( " ", "_22Msk", " " )) and position()=2]
#//h4/a[contains(text(),'SAP M')]
#//div[contains(@class, '_22Msk')]
