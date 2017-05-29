# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:10:03 2017

@author: thautwarm
"""
from sklearn.externals import joblib as j
#class read:
#    @staticmethod
#    def load(filename):
#        with open(filename,'r',encoding='utf-8') as f:
#            return f.read()
#    def dump(obj,filename):
#        with open(filename,'w',encoding='utf-8') as f:
#            f.write(str(obj))
def readFile(filename):
    with open(filename,'r',encoding='utf-8') as f:
        ret=f.read()
    return ret
import sys,os
haskmap=lambda *x:list(map(*x))
def box(code):
    return exec(code)
status=True
while True:
    if os.path.exists('subprocess.pypart'):
        stack=j.load('subprocess.pypart')
        status=1
        break
def log(var):
    with open('logging.txt','w',encoding='utf-8') as f:
        f.write(str(var))
if True:
        workspace='./work/work%s'%sys.argv[1]
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        while True:
            if not os.path.exists("go_on"):
                break
            works=haskmap(lambda x:"%s/%s"%(workspace,x),os.listdir(workspace))
            for work_i in works:
                if '.job' not in work_i:continue
                if not os.path.exists(work_i):continue
                try:
                    CONFIG=j.load(work_i)
                except:
                    log(sys.argv[1]+'\n')
                    print(work_i)
                    1/0
                    
                    
                for i,code in enumerate(stack):
                    try:
                        exec(code)
                    except:
                        print(i)
                os.remove(work_i)
                
            
                    
                
            
        
    

