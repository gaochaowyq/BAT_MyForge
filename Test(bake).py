import requests
import json
import  os
import base64
from urllib.parse import quote
#from myforge.Base import authenticate
from myforge.Base.Base import Base
#from myforge.Base.Data_Management import upload_file_to_bucket

class hub(Base):
    auth=authenticate.authenticate().get_access_token_fromfile()
    header ={"Authorization":auth}
    method = 'get'
    url = "https://developer.api.autodesk.com/project/v1/hubs"
    def result(self):
        return self.GetContent()

class create_bucket(Base):
    def __init__(self,bucketname,policyKey='transient'):
        _data = {'bucketKey': bucketname, 'policyKey':policyKey}
        self.data=json.dumps(_data)
    auth = authenticate.authenticate().get_access_token
    header ={'Authorization': auth,'Content-Type': 'application/json',}
    method = 'post'
    url = 'https://developer.api.autodesk.com/oss/v2/buckets'

    def result(self):
        return self.GetContent()







class get_object_from_bucket(Base):
    def __init__(self,bucketname):
        self.url='https://developer.api.autodesk.com/oss/v2/buckets/%s/objects' % (bucketname)
    auth = authenticate.authenticate().get_access_token
    header= {
        'Authorization': auth,
        'Content-Type': 'application/json'
    }
    method = 'get'
    def result(self):
        return self.GetContent()
    def get_urn(self):
        c=self.GetItem('items')[0]['objectId']
        objectId=c.encode(encoding="utf-8")
        urn= base64.b64encode(objectId)
        return urn


class download_file_from_bucket(Base):
    def __init__(self,bucketname,filename):
        self.bucketname=bucketname
        self.filename=filename
        self.url = 'https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s' % (self.bucketname, self.filename)
    auth = authenticate.authenticate().get_access_token
    header = {
        'Authorization': auth,
        'Content-Type': 'application/octet-stream',
    }
    method = 'put'

    def result(self):
        return self.GetContent()


class Data_Mangement:

    pass

class Design_Automation:
    pass


class Forge_Call():
    def __init__(self):
        self.Get_Access_Token_FromFile()

    filepath=os.getcwd()

    filename=filepath+'/Tem/tem.txt'
    def getAccessToken(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = [
          ('client_id', 'WY5rYjpEmULQNjkp2RHam8dFpNPd8Cjo'),
          ('client_secret', 'b0YUlKThAiJdX19g'),
          ('grant_type', 'client_credentials'),
          ('scope', 'data:read data:write viewables:read bucket:create bucket:read')
          #('scope', 'bucket:create bucket:read')
        ]

        r=requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', headers=headers, data=data)
        access_token=json.loads(r.text)['access_token']
        with open(self.filename,'w') as f:
            f.writelines('Bearer '+access_token)

    def Get_Access_Token_FromFile(self):
        self.getAccessToken()
        with open(self.filename,'r') as f:
            self.accesstoken=f.readline()

    def Check_Access_Token(self):

        return True

    def CreateBucket(self):
        headers = {
            'Authorization': self.accesstoken,
            'Content-Type': 'application/json'
        }
        data ={'bucketKey':'apptestbucket','policyKey':'transient'}

        r = requests.post('https://developer.api.autodesk.com/oss/v2/buckets', headers=headers,data=data)
        return r.text

    def getBucket(self,bucketname):
        headers = {
            'Authorization': self.accesstoken,

        }

        r=requests.get('https://developer.api.autodesk.com/oss/v2/buckets/%s/details'%(bucketname), headers=headers)

        return r.text

    def getBucketList(self):
        headers = {
            'Authorization': self.accesstoken,
        }

        r=requests.get('https://developer.api.autodesk.com/oss/v2/buckets', headers=headers)

        return r.text

    def getObject(self,bucketname):
        headers = {
            'Authorization': self.accesstoken,
            'Content-Type': 'application/json'
        }

        r=requests.get('https://developer.api.autodesk.com/oss/v2/buckets/%s/objects'%(bucketname), headers=headers)

        return r.text

    def UploadFileToBucket(self,filepath,filename,bucketname):
        headers = {
            'Authorization': self.accesstoken,
            'Content-Type': 'application/octet-stream',
        }
        with open(filepath,'rb') as f:
            data=f.read()
            #print(data.__len__())

        r=requests.put('https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s'%(bucketname,filename), headers=headers,data=data)

        return r.text

    def Geturn(self,bucketname):
        i=self.getObject(bucketname)
        print(i)
        object=json.loads(i)

        objectId=object['items'][0]['objectId']
        objectId=objectId.encode(encoding="utf-8")
        urn= base64.b64encode(objectId)
        return urn

    def Get_D_Urn(self,urn):
        headers = {
            'Authorization': self.accesstoken,
            'Content-Type': 'application/octet-stream',
        }

        r=requests.get('https://developer.api.autodesk.com/modelderivative/v2/designdata/:{}/manifest'.format(urn), headers=headers)

        return r.content
    def CovertToSVF(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.accesstoken,
        }

        data ={
            "input": {
              "urn": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6LV8ubXlidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0"
            },
            "output": {
              "formats": [
                {
                  "type": "svf",
                  "views": [
                    "2d",
                    "3d"
                  ]
                }
              ]
            }
          }
        data=json.dumps(data)

        r = requests.post('https://developer.api.autodesk.com/modelderivative/v2/designdata/job', headers=headers, data=data)
        return r.content

    def DownloadFile(self,urn,D_urn):
        headers = {
            'Authorization': self.accesstoken,
        }
        c='https://developer.api.autodesk.com/modelderivative/v2/designdata/{}/manifest/{}'.format(urn,D_urn)
        print(c)
        r = requests.get(c,headers=headers)
        return r.content

print("every th")
#c=create_bucket("mybadbucket")
#print(c.result())
#cc=get_bucket_list()
#print(cc.auth)
#cc=Model_Derivative.CovertToSvg()
#print(cc.GetContentObject())
#c=upload_file_to_bucket("mybadbucket",'/Users/wenhaie 1/Desktop/十象建筑/20180101 赣县健身中心模型/20171219_赣县健身中心_Final_Final.rvt','GanXianJianShenZhongXin.rvt')
#print(c.result())
#c=get_object_from_bucket("mybadbucket")
#print(c.get_urn())
#c=Model_Derivative.GET_manifest_derivativeurn()
#print(c.result())