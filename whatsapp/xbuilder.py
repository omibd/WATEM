from collections import defaultdict

contains = lambda attr, value: "contains(" + attr + ",'" + value + "')"
starts_with = lambda attr, value: "starts-with(normalize-space(" + attr + "),'" + value + "')"
ends_with = lambda attr, value: "ends-with(normalize-space(" + attr + "),'" + value + "')"
contains_no_attr = lambda value: "contains(.,'" + value + "')"
starts_with_no_attr = lambda value: "starts-with(normalize-space(),'" + value + "')"
ends_with_no_attr = lambda value: "ends-with(normalize-space(),'" + value + "')"

text_equal = lambda value : "contains(normalize-space(text())='" + value + "')"
not_contains = lambda attr, value: 'not(' + contains(attr, value) + ')'

def contains_tuple(func, n:tuple=('div','@class','_3wQ5i')):
    if type(n) is str: return None,func('.', n)
    elif len(n)==2:return None,func(n[0], n[1])
    elif len(n)==3:return n[0],func(n[1], n[2])
    else:
        print('function contains_mix_tuple(n:tuple): can only handdle 3 element as (tag, attr, value)')
        return None, n

def contains_gen(func, text=[('@class', '_21Ahp'),('text()','Net Status'), '11:13 pm'], tag='*'):
    ls = text if type(text) is list else [text]
    x = [contains_tuple(func, n)[1] if type(n) is tuple else contains('.', n)  for n in ls]
    return "//" + tag + '[' + ' and '.join(x) + ']'

def contains_add(func, xpath:str, new_item:tuple=('attr', 'attr_value'), str_search='contains'):
    '''xpath : existing xpath, tuple_arg: conition that transform and add into exting contains
    call :: contains_add("//span[contains(@class,'YESTERDAY')]",('.','TODAY'), not_expr)
    return ::
    '''
    if xpath.rfind(str_search) == -1:
        mid1, mid2 = contains_tuple(func, new_item)
        if mid1 is None: return xpath + ' | *['+ mid2 + ']'
        else: return xpath + ' | ' + mid1 + '[' + mid2 + ']'
    else:
        start = xpath[:xpath.find(']',xpath.rfind(str_search))]
        mid1, mid2 = contains_tuple(func, new_item)
        end = xpath[xpath.find(']',xpath.rfind(str_search)):]
        nwxpt = start + ' and '+ mid2 + end
        return nwxpt.replace('(.)','()')

def x_contains(func, xpath:str, new_item:tuple=('attr', 'attr_value'), str_search='contains'):
    if type(new_item) is tuple: return contains_add(func, xpath, new_item, str_search)
    if type(new_item) is list:
        for x in new_item:
            if type(x) is tuple:
                xpath = contains_add(func, xpath, x, str_search)
        else: return xpath

def xpath_items_split(i = "//div[@class='_21Ahp']"):
    '''RETURN TUPLE -> (TAG,ATTR, VALUE)'''
    tag, attr, value = i[0:i.find('[')], i[i.find('@'):i.find('=')], i[i.find('=')+1:i.find(']')]
    return tag.replace('/',''), attr, value.replace("'","")

def pickmid(s:str="//div[@class='_21Ahp']", start_key:str='@', upto_key=']'):
    n1 = s.find(start_key)
    n2 = s.find(upto_key, n1)
    return s[:n1], s[n1:n2], s[n2:]

def xpath_chunk(xpath):
    y= xpath.replace("//","$//").split('$')
    ls1 = [n.replace('])[',']$)$[').split('$') for n in y]
    ls2 = [element for innerList in ls1 for element in innerList]
    ls3 = [i.replace('][',']$[').split('$') for i in ls2]
    ls4 = [element for innerList in ls3 for element in innerList]
    ls5 = [i.replace('](',']$(').replace('])',']$)').split('$') for i in ls4]
    ls = [element for innerList in ls5 for element in innerList]
    return ls

#xpath_chunk("(//div[@data-testid='cell-frame-container']//div[@class='_8nE1Y'])[last()]/span/div[1]")
def search_msg_bytext(text = [('@class','_21Ahp'), 'omi'], index=None):
    txtm = '(' + contains_gen(contains, text,'div') 
    txtm = txtm + "[" + str(index) + "]" if type(index) is not None else txtm
    fxpt = txtm + "/ancestor::div[@data-testid='msg-container']"
    return fxpt

def search_msg_by_sender_text(sender='omi', text=None, index=None):
    txtm = "(//div[@class='ItfyB _3nbHh'])[" + starts_with_no_attr(sender) + ']'
    axes="/ancestor::div[@data-testid='msg-container']"
    if text is not None:
        for n in text:
            nd = tuple(n) if n is str else n
            txtm = contains_add(contains, txtm, nd , 'starts-with')
    xptx = txtm + '[' + str(index) + ']'  + axes if index is not None else txtm + axes
    return xptx

pnbase ="div[@data-testid='cell-frame-container']"
pane_chat_byname = lambda chatname: "//div[@class='y_sn4']//span" + "[contains(.,'" + chatname + "')]//ancestor::" + pnbase
pane_chat_unread_byname = lambda chatname : pane_chat_byname(chatname) + "//span[@data-testid='icon-unread-count']"

waxpath = {
    'welcome_msg': "//div[@data-testid='intro-text'][contains(.,'Use WhatsApp on up to 4 linked devices')]",
    'pane':{
        'pane_search' : "//div[@id='side']//div[@data-testid='chat-list-search']",
        'pane_search_back' : "//div[@id='side']//span[@data-testid='search']",
        'pane_search_cancel' :"//div[@id='side']//span[contains(@data-testid,'x-alt')]",
        'pane_search_filter' : "//div[@id='side']//button[@aria-label='Unread chats filter']"
        },
    'pane_side':{'wapane_chat': "//div[@id='pane-side']",
            'wapane_chat_base': "//div[@data-testid='cell-frame-container']",
            'wapane_chat_text_base': "//div[@class='_8nE1Y']",
            'wapane_chat_name': "//div[@class='y_sn4']//span",
            'wapane_chat_last_time': "//div[@class='y_sn4']//div[2]",
            'wapane_chat_last_msg': "//div[@class='vQ0w7']//span[@dir='ltr']",
            'wapane_chat_group_last_msg_sender': "//div[@class='vQ0w7']//span[@dir='auto']",
            'wapane_chat_unread_count': "//span[@data-testid='icon-unread-count']",
            'wapane_chat_axes' : "//ancestor::" + "div[@data-testid='cell-frame-container']"
           },
    'msg': {
        'conversation_weekday_str': "//span[@class='_11JPr']",
        'msg_base_last_index': "(//div[@data-testid='conversation-panel-body']//div[@data-testid='msg-container'])[last()]",
        'conversation_title': "//div[@id='main']//span[@data-testid='conversation-info-header-chat-title']",
        'conversation_body': "//div[@data-testid='conversation-panel-body']",
        'conversation_text_area': "//footer[@class='_3E8Fg']//p",
        'active_chat_search' : "//div[@id='main']//span[@data-testid='search-alt']",
        'msg_container_arrow': "//span[@data-testid='down-context']",
        'msg_container_menu': "//ul//li",
        'body_msg_nav_arrow' : '/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[1]/span/div',
        'msg_base': "//div[@id='main']//div[@data-testid='msg-container']",
        'msgbs': "//div[@class='ItfyB _3nbHh']",
        'msg_main_sender': "//div[@class='_27K43 _31p5Q']/div[1]//span[@dir='auto']",
        'msg_main_text': "//div[@class='_21Ahp']//span[@dir='ltr']",
        'msg_main_time': "//div[@data-testid='msg-meta']",
        'msg_quote_sender': "//div[@data-testid='quoted-message']/div/div/div/div[1]/span",
        'msg_quote_msisdn': "//div[@data-testid='quoted-message']//span[@class='WJuYU']",
        'msg_quote_text': "//div[@data-testid='quoted-message']//div[@dir='ltr']",
        'msg_container_axes': "//ancestor::div[@data-testid='msg-container']",
        'msg_main_contain_image': "//div[@data-testid='image-thumb']",
        'msg_main_datetime': "//div[@data-pre-plain-text]",
    }
}



