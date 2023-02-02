import os
from datetime import *
from dateutil.relativedelta import *
from dateutil.parser import *
import pandas as pd
from sqlalchemy import Column, Integer, String, func, create_engine, DateTime, MetaData, Table, inspect
from sqlalchemy.ext.declarative import declarative_base

wh_in = lambda col, ls : col + " IN ('" +  "','".join(map(str, ls)) + "')"
wh_between = lambda col, str1, str2 : col + " BETWEEN '" + str(str1) + "' AND '" + str(str2) + "'"
wh_like = lambda col, val : col + " LIKE %'" + str(val) + "'%" if type(val) is str else ' AND '.join(list(map(lambda col, val : str(col) + "LIKE '%" + esc(val) + "%'", col, val)))
wh_equal = lambda col, val : col + " ='" + str(val) + "'" if type(val) is str else ' AND '.join(list(map(lambda col, val : str(col) + "='" + esc(val) + "'", col, val)))

def wh_by_operator(col, ls, sql_operator):
    if sql_operator == 'IN':
        return wh_in(col, ls)
    elif sql_operator == 'BETWEEN':
        try:
            return wh_between(col, ls[0], ls[1])
        except:
            return wh_equal(col, ls)
    elif sql_operator == '=':
        return wh_like(col, ls)
    elif sql_operator == 'LIKE':
        return wh_equal(col, ls)
    
def esc(tx):
    if type(tx) is str:
        sql_char_special = ["'",'"',"/","Backspace","“","_%","%"]
        sql_char_replace = ["\'",'\"',"\/","\b","\“","\_%","\%"]
        for i in range(len(sql_char_special)):
            tx = tx.replace(sql_char_special[i], sql_char_replace[i])
        else:
            return tx
    else:
        return tx
    
TS = lambda x , y : "'" + esc(x) + "'" if 'LIKE' not in y else " '%" + esc(x) + "%'"
TX = lambda x : x if type(x) is list else [x]
TSS = lambda x, y : "'" + esc(x) + "'" if y is None else y + esc(x) + y

def _where(cond, cols=None, rows=None):
    x2, logic = '', ''
    for k, v in cond.items():
        if type(v) is list and len(v)==3:
            if type(v[0]) is list:
                rr = wh_by_operator(k,v[0],v[1])
            else:
                rr = str(k) + ' ' + v[1] + TS(v[0],v[1])
        #elif k in cols and type(v) is list and len(v)==2 and cols is not None and rows is not None:
            #rr = k + ' '  + v[0] + ' ' + TS(rows[cols.index(k)],v)
        else:
            rr = k + ' '  + v[1] + ' ' + TS(v[0], v[1:])
        if x2 == '':
            x2 = x2 + rr
        else:
            x2 = x2 + ' ' + logic + ' ' + rr
        logic = v[len(v)-1]
        if 'AND' not in logic or 'OR' not in logic:
            logic = 'AND'
    else:
        if x2 == '':
            return ''
        else:
            return ' WHERE ' + x2

Select = lambda tbl, cols, cond : "select " + ",".join(cols) + " from " + tbl + _where(cond) if type(cols) is list else "select " + cols + " from " + tbl + _where(cond)
Update = lambda tbl, cols, rows, cond : "UPDATE " + tbl + " SET " +  ','.join(list(map(lambda x, y : str(x) + "='" + esc(y) + "'", TX(cols), TX(rows)))) + _where(cond, TX(cols), TX(rows))
Insert = lambda tbl, cols, rows : 'INSERT INTO ' + tbl +  ' (' + ','.join(map(str, TX(cols))) + ") values ('" +  "','".join(map(str, TX(rows))) + "')"

def df_tosql(df, tbl, cond_col= {}, column ='*'):
    df = df.fillna('0')
    check_col = list(cond_col)
    dc, ins, upd, sel, dele = {}, [], [], [], []
    if column == '*' or column==False:
        cols = df.columns.values.tolist()
        column = cols
    for i in range(len(df)):
        cond = {}
        rows = [str(y1) for y1 in df.loc[i,:].values.tolist()]
        for j in list(cond_col):
            cond[j] = [rows[cols.index(j)]] + cond_col[j]
        else:
            sel.append(Select(tbl, column, cond))
            upd.append(Update(tbl, column, rows, cond))
            ins.append(Insert(tbl, column, rows))
    else:
        return sel, upd, ins