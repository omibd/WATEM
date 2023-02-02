import os

def csvdir():
    csvv  = os.getcwd() + "\\.csvdump"
    try:
        os.mkdir(csvv)
    except:
        pass
    return csvv

def list_2_text(fname, lst):
    fl = open(fname,'w')
    for i in lst:
        try:
            fl.writelines(i + chr(10))
        except:
            st = ','.join(list(i))
            fl.writelines(st + chr(10))
    fl.close()
    
def nested_dic(dic, ky, vl):
    if isinstance(vl,list):
        dic[ky] = vl if not list(dic) else dic.get(ky, []) + vl
    else:
        vlx = [vl]
        dic[ky] = vlx if not list(dic) else dic.get(ky, []) + vlx
    return dic

def dic_Update_helper(st):
    x = 0
    if type(st) is not list:
        try:
            x = len(st)
        except:
            pass
        if x == 0:
            return []
        else:
            return [st]
    else:
        return st

def dic_Update(dic1, dic2):
    ndc = {}
    for k, v in dic1.items():
        if type(dic2.get(k)) is not list:
            v2 = dic_Update_helper(v) + [dic2.get(k)]
        else:
            v2 = dic_Update_helper(v) + dic2.get(k)
        ndc[k] = v2
    else:
        return ndc