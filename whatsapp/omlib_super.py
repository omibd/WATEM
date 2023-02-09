from functools import wraps
import subprocess
import datetime as dt
import pandas as pd
from collections import defaultdict

def tyfn(f, *arg, **kw):
    fn = f[0] if type(f) is list else f
    try:
        return fn(*arg, **kw)
    except:
        if type(f) is list:
            L = len(f)
            if L>1: return tyfn(f[1:len(f)], *arg, **kw)
            elif L==1: return tyfn(f[0], *arg, **kw)
            else: raise
        else: raise
        
LC = lambda x,y : str(x) + str(y)
LY = lambda x,y : x - y
LX = lambda x,y : x + y

#print(tyfn([LX,LY], 5 ,'4'))

def totxt(fp:str, data:str, method='a+'):
    with open(fp, method) as f:
        f.write(data)

def outer_function(is_print=False, save_path=None):
    def debug(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_print == True:
                print('function Name: ', func.__name__)
                print('Running from: ', func.__module__)
                for n, i in enumerate(args):
                    print('arbitary arg >> number:',n ,'| value:', i, '|', type(i))
                for k, n in kwargs.items():
                    print('keyword arg: name:', k, '| value: ', n, '|', type(i))
            result = func(*args, **kwargs)
            print('Result:', result)
            if save_path is not None:
                totxt(save_path, result)
            return arg + str(result)
        return wrapper
    return debug

#@outer_function('calculated result: ')
#def av(a1,a2):
#    print('av result ', a1*a2)
#    return a1*a2
#q = av(2,3)
#print(q)

def tex(f):
    @wraps(f)
    def te(*a, **k):
        try: return f(*a, **k)
        except: return 0
    return te

def closr(f):
    def inn(*a, **k):
        return f(*a, **k)
    return inn

def subp_execute(cmd):
    command = cmd.split(' ') if type(cmd) is not list and ' ' in cmd else cmd
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return str(process.stdout.read())

def xpbulk(self, xpt):
    try:
        if type(xpt) is str: return self.xptext(xpt)
        elif type(xpt) is list: return [self.xptext(n) for n in xpt]
        elif type(xpt) is dict: return {k : [self.xptext(n) for n in v] if type(v) is list else self.xptext(v) for k, v in xpt.items()}
        else: return None
    except:
        return None

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
    
def value_already_exist(dc, ky, val):
    try:
        a = dc.get(ky, val)
        return True
    except: return False
    
def dict_to_df(self, dc, out=None):
    x = dt.datetime.now().strftime('%b%d%Y_%H%M')
    opt = x  + '.csv' if out is None else x + '_' + out + '.csv'
    df = pd.DataFrame.from_dict(dc).to_csv(opt)
    return df
