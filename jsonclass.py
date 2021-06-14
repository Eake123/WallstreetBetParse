import json
import os

class Json:
    
    
    def __init__(self,file,directory):
        self.file = file
        self.fileKey = file.replace(".txt","")
        self.directory = directory
        

    
    
    def changeDump(self,info):
        os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        json_decoded.update({self.fileKey:info})
        with open(self.file, 'w') as f:
            f.write(json.dumps(json_decoded, sort_keys=True, indent=4, separators=(',', ': ')))
    
    
    def dicDump(self,infoDic):
        os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        dic = json_decoded[self.fileKey]
        fullDic = {}
        for i in dic.keys():
            if(infoDic.get(i) == None):
                fullDic[i] = dic[i]
            else:
                fullDic[i] = dic[i] + infoDic[i]
        for j in infoDic.keys():
            if(dic.get(j) == None):
                fullDic[j] = infoDic[j]
        realDic = {self.fileKey:fullDic}
        with open(self.file, 'w') as f:
            f.write(json.dumps(realDic, sort_keys=True, indent=4, separators=(',', ': ')))

    
    def addDump(self,add):
        os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        dic = json_decoded[self.fileKey]
        for i in add:
            dic.append(i)
        realDic = {self.fileKey:dic}
        with open(self.file, 'w') as f:
            f.write(json.dumps(realDic, sort_keys=True, indent=4, separators=(',', ': ')))
    
    def createDump(self,add):
        os.chdir(self.directory)
        dic = {self.fileKey:add}
        with open(self.file, 'w') as f:
            f.write(json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': ')))
    
    
    def readKey(self):
        os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
            
        dic = json_decoded[self.fileKey]
        return dic


    def jsonNuke(self,str):
        os.chdir(self.directory)
        if(str == True):
            nuke = {self.fileKey:"N/A"}
        else:
            nuke = {self.fileKey:{"N/A":1}}
        with open(self.file, 'w') as f:
            f.write(json.dumps(nuke, sort_keys=True, indent=4, separators=(',', ': ')))



class Stock:
    def __str__(self):
        return r"C:\Users\Erik\Desktop\daytradeJSON\Stonks"

class Reddit:
    def __str__(self):
        return r"C:\Users\Erik\Desktop\daytradeJSON\Reddit"

class Tech:
    def __str__(self):
        return r"C:\Users\Erik\Desktop\daytradeJSON\technicals"

class Test:
    def __str__(self):
        return r"C:\Users\Erik\Desktop\daytradeJSON\test"

    
        