import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path)


def fn():
    print('printing from sub_module_1.py')