from Base.Base import Base
from . import authenticate
import  json
from urllib.parse import quote
from .Data_Management import get_object_from_bucket
import  os
import base64

class GET_formats (Base):
    pass
class POST_job(Base):
    def __init__(self,bucketkey,filename,ManiFialName=-1):
        super(POST_job,self).__init__()
        self.auth = authenticate.authenticate().get_access_token
        self.urn = get_object_from_bucket(bucketkey).get_urn(filename)
        self.ManiFileName=ManiFialName

        self.header= {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': self.auth}
        if self.ManiFileName==-1:
            self.o_data = {
               "input": {
                 "urn": self.urn.decode('ascii')

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

        else:
            self.o_data = {
            "input": {
                "urn": self.urn.decode('ascii'),
                "compressedUrn": True,
                "rootFilename": self.ManiFileName

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
        #covert to json data
        print(self.o_data)

        self.data =json.dumps(self.o_data)
        self.method = 'post'
        self.url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/job'

    def result(self):
        return self.GetContent()

class POST_reference (Base):
    pass

#GetMainfest(bucketname)
class GET_urn_thumbnail (Base):
    pass


class Get_urn_manifest (Base):
    def __init__(self,bucketname,filename):
        super(Get_urn_manifest,self).__init__()
        self.urn = get_object_from_bucket(bucketname).get_urn(filename)
        self.auth = authenticate.authenticate().get_access_token
        self.header = {'Authorization': self.auth,'Accept-Encoding': 'gzip, deflate'}
        self.method = 'get'
        self.url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/manifest' % (self.urn.decode('utf-8'))

    def result(self):
        return self.GetContent()
    def get_derivative(self):
        return self.GetItem('derivatives')

class DELETE_urn_manifest (Base):
    def __init__(self,bucketkey,filename):
        super(DELETE_urn_manifest,self).__init__()
        #self.projectname=projectname
        self.urn = get_object_from_bucket(bucketkey).get_urn(filename)
        #self.de_urn=urn

        self.auth = authenticate.authenticate().get_access_token
        self.header = {'Authorization': self.auth}
        self.method = 'delete'
        self.url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/manifest'.format(urn=self.urn.decode('utf-8'))
    def result(self):
        c=self.GetContentObject()
        return c
    def getcontent(self):
        return self.GetContent()
'''
class GET_manifest_derivativeurn(Base):
    def __init__(self,urn,filepath):
        super(GET_manifest_derivativeurn,self).__init__()
        #self.projectname=projectname
        self.urn = get_object_from_bucket('whateverbucket').get_urn()
        self.de_urn=urn
        self.filepath=filepath
        self.abslutepath=os.path.split(self.filepath)[0]


        self.auth = authenticate.authenticate().get_access_token
        self.header = {'Authorization': self.auth}
        self.method = 'get'
        self.url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/manifest/%s' % (self.urn.decode('utf-8'),quote(self.de_urn))
    def result(self):
        c=self.GetContentObject()
        if c:
            print(c.status_code)
        if os.path.exists(self.abslutepath)==0:
            os.makedirs(self.abslutepath)
        with open(self.filepath,'wb') as f:
            f.write(c.content)
            print('write file is done')
        return c
'''
class GET_manifest_derivativeurn(Base):
    def __init__(self,bucketkey,filename,derivativeUrn):
        super(GET_manifest_derivativeurn,self).__init__()
        #self.projectname=projectname
        self.urn = get_object_from_bucket(bucketkey).get_urn(filename)
        #self.de_urn=urn
        print(self.urn)

        self.auth = authenticate.authenticate().get_access_token
        self.header = {'Authorization': self.auth,"Content-Type": "application/json;charset=utf-8"}
        self.method = 'get'
        self.url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/manifest/{derivativeUrn}'.format(urn=self.urn.decode('utf-8'),derivativeUrn=quote(derivativeUrn))
    def result(self):
        c=self.GetContentObject()
        return c
    def getcontent(self):
        return self.GetContent()



class GET_urn_metadata(Base):
    pass



class GET_urn_metadata_guid(Base):
    pass

class GET_urn_metadata_guid_propertites(Base):
    pass
