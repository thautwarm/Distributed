import re

# a function similar as "map" but return a list not a iterator 
haskmap=lambda *x:list(map(*x)) 

#like "tokenize", which divides the codes into several modules with single function.
moduleSplit=lambda var: haskmap(lambda v:v.split("\n"), re.findall("(?<=#)[\W|\w]*?(?=#)",re.sub('\$[\w|\W]*?\$','',var))) 
haskfil=lambda var:list(filter(lambda v:v,var)) 

def removeEndl(str):
    if not str: return str
    if str[-1]=='\n':str=str[:-1]
    return str 
def conutTab(str):
    str=str.replace("    ",'\t')
    str=removeEndl(str)
    for i,char in enumerate(str):
        if char != '\t':
            return i,str[i:]
    return None,None
    # return None  # if do not has '\t' return None, it means this str will be ignored.
def startWith(str,begin):
    return str[:len(begin)]==begin


# parsing Reqirementss
class Requirements:
    @staticmethod
    def parse(codes):
        Req=[]
        now=-1
        t=1
        for code_line in codes:
            t_r,code_line=conutTab(code_line)
            if not t_r:continue
            if t_r==1:
                Req.append([code_line])
                now+=1
            elif t_r>t:
                Req[now].append(code_line)
        return '\n'.join(["import %s"%root[0] \
                    if len(root)==1 \
                    else "from %s import %s"%(root[0],','.join(root[1:]) ) for root in Req])   

#Parsing Do-In structure.
class Do_In:
    @staticmethod
    def parse(codes,name):
        status=0
        Do=[]
        In=[]
        for code_line in codes:
            code_line=removeEndl(code_line)
            if status==0 and startWith(code_line,'Do'):
                status=1
            elif status==1:
                if startWith(code_line,'In'):
                    status=2
                else:
                    Do.append(code_line)
            elif status==2:
                In.append(code_line)
        return "def "+name+"():\n    %s\n    %s"%('\n    '.join(Do),"return %s"%( ','.join(In)) )


# it's the structure of analyzing the codes. 
# 暂未解析WorkArg
class Explain:
    @staticmethod
    def parse(codes):
        modules=moduleSplit(codes)
        requirements=''
        generateIter=''
        action=''
        strategy=''
        for module in modules:
            module=haskfil(module)
            if not module:continue
            if module[0] == 'Requirements':
                requirements=Requirements.parse(module[1:])
            elif module[0] == 'GenerateIter':
                generateIter= Do_In.parse(module[1:],'Gen')
            elif module[0] == 'Action':
                action=Do_In.parse(module[1:],'Act')
            elif module[0] == 'Strategy':
                strategy= '\n'.join(module[1:])

        Iters=\
"""
exec(r'''%s''')
GenerateIter=Gen()
"""%generateIter
        return strategy,Iters,[requirements,action,"Act()"]






