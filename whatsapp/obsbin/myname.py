
import os
import time

def str2list(st):
    lsx = []
    try:
        ls = st.split()
        for n in range(len(ls)):
            lsx.append(ls[n])
        return lsx
    except:
        return lsx
    
def st2ls(st):
    ls = []
    for i in range(len(st)):
        ls.append(ord(st[i]))
    return ls

def ls2st(ls):
    hp = ""
    for i in range(len(ls)):
        if hp == "":
            hp = chr(ls[i])
        else:
            hp = hp + chr(ls[i])
    return hp

def aptxt(lsst,filename):
    fin = open(os.getcwd() + "\\" + filename + ".txt", "a+")
    hp = []
    if isinstance(lsst,list):
        for i in range(len(lsst)):
            hp.append(str(lsst[i]))
        xx = ",".join(list(hp)) + chr(10)
        fin.write(xx)
    else:
        fin.write(lsst)
    fin.close()

def prep(pth):
    fp = open(pth,"r")
    xx = fp.read()
    xy = xx.split("\n")
    ls1 = []
    ls2 = []
    xx=""
    for i in range(len(xy)):
        a1 = st2ls(xy[i])
        a2 = ls2st(a1)
        aptxt(a1,"A8")

sx = """91,42,42,42,42,42,42,95,95,95,95,42,42,95,95,42,42,95,95,42,42,32,95,42,42,32,42,42,42,42,42,42,42,33
42,42,42,42,42,32,47,32,95,95,32,92,124,32,32,92,47,32,32,124,42,124,32,124,42,42,42,42,42,42,42,42,42,33
42,42,42,42,42,124,32,124,32,32,124,32,124,32,92,32,32,47,32,124,42,124,32,124,42,42,42,42,42,42,42,42,42,33
42,42,42,42,42,124,32,124,32,32,124,32,124,32,124,92,47,124,32,124,42,124,32,124,42,42,42,42,42,42,42,42,42,33
42,42,42,42,42,124,32,124,95,95,124,32,124,32,124,32,32,124,32,124,42,124,32,124,42,42,42,42,42,42,42,42,42,33
42,42,42,42,42,42,92,95,95,95,95,47,92,95,124,42,42,124,95,124,42,124,95,124,42,42,42,42,42,42,42,42,93,33"""

def say_my_name():
    time.sleep(1)
    xx = sx.replace("42","32")
    yy = xx.replace("33","xx")
    ls = yy.split("xx")
    hp = ""
    for i in range(len(ls)):
        xz = ls[i].split(",")
        hp = ""
        for n in range(len(xz)):
            if xz[n] == "":
                print(hp)
                hp = ""
            else:
                hp = hp + chr(int(xz[n]))
    print("---------------------------------")
    return 1
        
say_my_name()
#time.sleep(5)

# prepare the sx using prep(os.getcwd() + "\\N2.txt")
# prep(os.getcwd() + "\\N2.txt")