import requests
import json
class Base(object):
    def __init__(self):
        self.header=""
        self.data=""
        self.method=''
        self.url=""
    def GetContentObject(self):
        if self.method=='get':
            r = requests.get(self.url, headers=self.header,data=self.data)
        elif self.method=='post':
            r = requests.post(self.url, headers=self.header,data=self.data)
        elif self.method == 'put':
            r = requests.put(self.url, headers=self.header, data=self.data)
        elif self.method == 'delete':
            r = requests.delete(self.url, headers=self.header, data=self.data)
        else:
            r='bad run'
        return  r
    def GetContent(self):
        return  self.GetContentObject().text
    def GetContentAsJson(self):
        return  json.loads(self.GetContent())
    #从返回的Json中读取需要的内容
    def GetItem(self,name):
        content=json.loads(self.GetContent())
        return content[name]