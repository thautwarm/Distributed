import os,time,sys
try:
    sys.path.append('G:/tools')
except:
    pass
from tools.DSL.DConf.compile import Explain
from sklearn.externals import joblib as j

def readFile(filename):
    with open(filename,'r',encoding='utf-8') as f:
        ret=f.read()
    return ret
dc_codes=readFile('./config.dc')
strategy,Iters,body=Explain.parse(dc_codes)
j.dump(body,'./subprocess.pypart')

N_job=int(sys.argv[1]) #the Number Of Subprocesses
j.dump(0,'go_on')

#'go_on' is the signal for the persistence of each subprocessing and this one.
import subprocess
if os.name=='nt':
	startupinfo=subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	startupinfo.wShowWindow=subprocess.SW_HIDE
else:
    startupinfo=None
for i in range(N_job):
    subprocess.Popen(['python','process.py',str(i)],startupinfo=startupinfo)
    while not os.path.exists('./work/work%d'%i):
        continue
    
if True:
    #the second argv defines the function you wanna do.
    GenerateIter=None
    exec(Iters)
    NumberOfTasks=len(GenerateIter)
    workNowInput=['']*NumberOfTasks
    workNowOutput=['']*NumberOfTasks
    Strategy=[0]*NumberOfTasks
    exec(strategy)
    for index,(strate,workin,workout) in enumerate(zip(Strategy,workNowInput,workNowOutput)):
        j.dump({'workNowInput':workin,'workNowOutput':workout},'./work/work%d/job%d.job'%(strate,index))    
        time.sleep(0.01)
    WorkPath='./work'
    WorkPaths=list(map(lambda x:"%s/%s"(WorkPath,x),os.listdir(WorkPath)))
    while any([len(os.listdir(path_i)) for path_i in WorkPaths]):
            time.sleep(20)
            continue
os.remove("go_on")
     
    
