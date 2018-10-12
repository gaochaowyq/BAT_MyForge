
import requests
import json
import  os
import base64
from urllib.parse import quote
from myforge.Base.Utile import *

from myforge.Base.Data_Management import *
from myforge.Base.Model_Derivative import *


#Create Bucket
bucketname='whateverbucket'
#c=create_bucket(bucketname,policyKey='temporary')
#print(c.GetContent())

#cc=get_bucket_list()
#print(cc.result())
ccc=get_object_from_bucket(bucketname)
print(ccc.get_urn())

#c=POST_job(bucketname)
#print(c.result())
#cc=get_bucket_list()
#print(cc.result())

#c=upload_file_to_bucket("whateverbucket",'/Users/wenhaie 1/PycharmProjects/Forge/myforge/media/ShunYang_1_Center.rvt','ShunYang_1_Center.rvt')
#print(c.result())
#c=GetManifest(bucketname)
#print(c.GetContent())
#for i in c.get_derivativeurn():
#    print(i.status)
#ccc='urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/0.pf'
#cccguid='2f8a345a-8954-a963-5a89-41fbeb8c12eb'
#c=GET_manifest_derivativeurn(ccc)
#c.result()

#c=GET_SVF_Tree(ccc)
#print(c.GetContentObject().headers)
#print(c.result())

#get.svf file path

#svffilepath=c.filepath







#with open('/Users/wenhaie 1/PycharmProjects/Forge/myforge/Base/{3D}.svf','r',encoding='utf-8') as f:
#    c=f.read()
#    #cc=json.loads(c)
#    print(c)
class _item:
    def __init__(self,mime):
        self.mime=mime
    def __setitem__(self, key, value):
        self[key]=value
    def __getitem__(self,key):
        return self[key]
    def __str__(self):
        return self.mime



res=[]

def extractPathsFromGraphicsUrn(urn,result):
    urn= urn.encode(encoding="utf-8").decode()
    #urn = base64.b64encode(objectId)
    basePath =urn[0:urn.rfind('/')+1]
    localPath = basePath[basePath.find('/')+1:]
    urnBase = basePath[0:basePath.find('/')]
    localPath = localPath.replace("output/",'')
    localPrefix = '/Users/wenhaie 1/PycharmProjects/Forge/myforge/Base/output/'
    result.urn= urn
    result.basePath= basePath
    result.localPath = localPrefix + localPath
    result.rootFileName = urn[urn.rfind('/')+1:]


allitem=[]










class bubble:
    def __init__(self,bubble):
        self.bubble=bubble
        self.current = 0
        self.res=[]
        self.done = 0
        self.estSize = 0
        self.countedPropDb = {}
    def getitem(self,urn,filepath):
        cc = GET_manifest_derivativeurn(urn,filepath)
        cc.result()
        return filepath



    def traverse(self,node, parent):
        res=self.res
        if node.get('role') =='Autodesk.CloudPlatform.PropertyDatabase' or node.get('role') == 'Autodesk.CloudPlatform.DesignDescription' or node.get('role') == 'Autodesk.CloudPlatform.IndexableContent' or node.get('role') == 'graphics' or node.get('role') == 'raas' or node.get('role') == 'pdf' or node.get('role') == 'leaflet-zip' or node.get('role') == 'preview' or node.get('role') == 'lod':
            item = _item(node['mime'])
            extractPathsFromGraphicsUrn(node['urn'], item)

            #node['urn']= '$file$/' + item.localPath + item.rootFileName

        if node.get('role') != 'Autodesk.CloudPlatform.PropertyDatabase':
            try:
                self.res.append(item)
            except:
                pass

        if node.get('mime') == 'application/autodesk-svf' or node.get('mime')== 'application/autodesk-f2d':
            item.name = node.get('name')
            if parent.get('hasThumbnail') ==True:
                thumbnailItem = _item('thumbnail')
                thumbnailItem.urn = self.bubble.get('urn')
                thumbnailItem.guid = parent.get('urn')
                thumbnailItem.localPath = item.localPath,
                #thumbnailItem.thumbnailUrn = '$file$/thumbnails/' + parent.get('urn') + '.png',
                thumbnailItem.rootFileName = item.rootFileName + '.png',

                res.append(thumbnailItem)

        if node.get('type') == 'geometry':
            if node.get('intermediateFile') and node.get('children'):
                for i in range(0, len(node['children'])):
                    if node['children'][i]['mime'] == 'application/autodesk-f2d':
                        f2dNode = node['children'][i]

                if f2dNode:
                    f2dUrl = f2dNode['urn']
                    idx = f2dUrl.indexOf(self.bubble.urn)
                    baseUrl = f2dUrl.substr(0, idx + len(self.bubble['urn']))
                    f2dNode_item = _item('application/octet-stream')
                    f2dNode_item.urn = self.bubble['urn']
                    f2dNode_item.guid = node.guid
                    intPath = '/' + node.intermediateFile

                if baseUrl.indexOf('urn:adsk.objects') == 0:
                    intPath = quote(intPath);
                    fullPath = baseUrl + intPath
                    extractPathsFromGraphicsUrn(fullPath, item)
                    res.append(item)
        if node.get('children'):
            for i in node['children']:
                self.traverse(i,node)

        return res

    def listAllDerivativeFiles(self):
        self.traverse(self.bubble,'')

        for rootItem in self.res:
            files=rootItem.files=[]
            if rootItem.mime !='thumbnail':
                basePath = rootItem.basePath
            if rootItem.mime == 'application/autodesk-db':

                files.append ('objects_attrs.json.gz')
                files.append('objects_vals.json.gz')
                files.append('objects_avs.json.gz')
                files.append('objects_offs.json.gz' )
                files.append(rootItem.rootFileName)
            elif rootItem.mime =='thumbnail':
                rootItem.files.append(rootItem.rootFileName)
            elif rootItem.mime =='application/autodesk-svf':
                svfPath = rootItem.urn[len(basePath):]
                files.append(svfPath)
                for i in rootItem.files:
                    localsfilepath=self.getitem(rootItem.basePath+i,rootItem.localPath+i)
                    c = unzipfile(localsfilepath)
                    new = c.get('assets')
                    for i in new:

                        if not i['URI'].startswith('../') and not i['URI'].startswith('embed:/'):
                            newpath=i.get('URI')
                            downloadpath=os.path.join(rootItem.basePath,newpath)
                            print("{} is done".format(newpath))
                            c=GET_manifest_derivativeurn(downloadpath,rootItem.localPath+newpath)
                            c.result()
            elif rootItem.mime == 'application/autodesk-f2d':
                files.append('manifest.json.gz')
                manifestPath = basePath + 'manifest.json.gz'


        return self.res













a={'type': 'manifest', 'region': 'US', 'version': '1.0', 'progress': 'complete', 'hasThumbnail': 'true', 'urn': 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0',
   'derivatives': [
       {
           'children': [
               {'type': 'resource', 'guid': '6fac95cb-af5d-3e4f-b943-8a7f55847ff1', 'mime': 'application/autodesk-db', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/model.sdb', 'role': 'Autodesk.CloudPlatform.PropertyDatabase', 'status': 'success'},
               {'progress': 'complete', 'type': 'geometry', 'guid': '48875ad0-a5c8-f649-239b-5a4edf6eda20', 'name': '{3D}', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '3d', 'viewableID': 'acbcdb41-9a0b-4fe9-8898-5faaad4117b2-00102bcd', 'status': 'success',
                'children': [{'progress': 'complete', 'type': 'view', 'guid': 'acbcdb41-9a0b-4fe9-8898-5faaad4117b2-00102bcd', 'camera': [988.248413, -147.824234, 397.744171, 605.858704, 234.565475, 15.354465, -0.408248, 0.408248, 0.816497, 1.52421, 0, 1, 1], 'name': '{3D}', 'role': '3d', 'status': 'success'},
                             {'type': 'resource', 'guid': '2f8a345a-8954-a963-5a89-41fbeb8c12eb', 'role': 'graphics', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}.svf', 'mime': 'application/autodesk-svf'},
                             {'type': 'resource', 'guid': '90adc752-b1e2-75fe-aec3-fe5f73936722', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '920bc216-9a60-094e-eb69-9a6783fcb9b9', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'c4b62e44-e6fa-f565-948e-6363a98294e6', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}4.png', 'role': 'thumbnail', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '7fb62af8-e38f-47a5-9374-7f9c492e2e30-00058194', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'B-01 - A-G 轴立面图、G-A轴立面图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '7fb62af8-e38f-47a5-9374-7f9c492e2e30-00058194', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '91b71f5a-dbbb-d703-51f3-6203d6389db4', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '984486d4-0383-90ff-4345-83baf41abd2c', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'b302b748-b4d5-1473-49a6-a867cd7657b3', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '6e1f1677-7208-3183-b417-1a4fba776cae', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/9179d043-873f-bb2b-0a31-d1bef12cb585_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '7fb62af8-e38f-47a5-9374-7f9c492e2e30-0005819a', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'B-04 - 3-3剖面图、4-4剖面图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '7fb62af8-e38f-47a5-9374-7f9c492e2e30-0005819a', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '3bb2b2bb-d265-06c8-e2ed-31cbaab2ce62', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '2c230b93-c06f-28c9-9f09-564262e464f6', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '253a84b3-061e-4646-ae03-7f3c8acc7bbe', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '0d1ac870-b98c-1da9-e556-9514260f1410', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/d5d8ff51-db7b-3c68-fc11-024caf2dbea4_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '3480a42a-bed2-4554-ad35-b928c4ea3b64-000589dd', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'B-02 - 1 - 4轴立面图、4 - 1 轴立面图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '3480a42a-bed2-4554-ad35-b928c4ea3b64-000589dd', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '25c46705-d371-8e6a-56c8-af37ca9be81b', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '21604c2a-e60d-4b10-d4b5-075633cbe0cc', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'fb4c8a6c-a49e-34b6-48c3-190759124903', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '96683327-b1e3-7b2b-01f1-c6f06ac8943a', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/2a4493be-a934-a055-89fb-c4cacb149669_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '62676ba6-1b9d-4284-ac51-ad885e787d3e-0005914a', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'B-03 - 1-1剖面图、2-2剖面图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '62676ba6-1b9d-4284-ac51-ad885e787d3e-0005914a', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '935260f4-f00a-df90-85b0-e8f422a69b6a', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'e31334eb-710d-e07d-b758-af4b541fec48', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'ee0303c3-d30d-68bd-089a-6402c5980cb2', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'af5e33d1-a0fe-551f-dd12-55ef507e2c23', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/127259ba-bf79-1670-458b-a0042de5c49a_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '4b1358c7-d078-45f3-9209-00d1284909a4-00084bbc', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'T-01 - 图纸目录', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '4b1358c7-d078-45f3-9209-00d1284909a4-00084bbc', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '8239ad40-f6eb-c5bb-e432-abf8eac3ee7a', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'a01e55ec-99d4-4d4a-cf04-dba70de03a85', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '5cb50e10-6c67-8aff-2680-7a999290c75a', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '953c9d9a-94c0-47ab-5b1c-14ac96f24577', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/6f64ff35-8500-2252-ac86-55a485018f62_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '1b177165-551f-4ab3-8009-dcf2df55f105-000ccfe2', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'C-01 - 墙身详图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '1b177165-551f-4ab3-8009-dcf2df55f105-000ccfe2', 'status': 'success',
                'children': [{'type': 'resource', 'guid': '493d4f54-8112-b902-9839-f43468b8c2da', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '99a501ad-c8ab-3382-1c08-4680d62761fa', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '07400920-f90b-e9fa-ba25-36e46e6740de', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '490b0d17-9c08-128b-c92e-8a32e4461224', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/f42db909-9aeb-cff7-f0e6-9261890ae1d0_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]},
               {'progress': 'complete', 'type': 'geometry', 'guid': '501d620b-cd22-4473-a39b-1075ce6b771c-000d5f59', 'properties': {'Print Setting': {'Paper size': 'ISO A4, 210 x 297 mm', 'Layout': 'Landscape'}}, 'name': 'D-01 - 曲面定位图', 'phaseNames': 'New', 'hasThumbnail': 'true', 'role': '2d', 'viewableID': '501d620b-cd22-4473-a39b-1075ce6b771c-000d5f59', 'status': 'success',
                'children': [{'type': 'resource', 'guid': 'cb8f82eb-ad58-589c-e91b-18fb217f0ebf', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图1.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '9b82ce22-3ec6-270b-d606-4cad0507020a', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图2.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': '3f9b914b-0889-ca23-e01e-a3122595f5bc', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图4.png', 'role': 'thumbnail', 'status': 'success'},
                             {'type': 'resource', 'guid': 'ef5195aa-5b50-7e5d-b0a4-0ab18c640c71', 'mime': 'application/autodesk-f2d', 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/4ce05a89-ab91-a48e-0b6a-360edd0db7b0_f2d/primaryGraphics.f2d', 'role': 'graphics', 'status': 'success'}]}],
           'messages': [{'type': 'warning', 'message': ['<message>Missing link files: <ul>{0}</ul></message>', 'REF-GRIDE_t3.dwg, 吊顶.sat, 屋顶.sat, 屋顶突出女儿墙_New.sat, 幕墙参照面.sat, 平面示意图.dwg, 曲线结构.sat'], 'code': 'Revit-MissingLink'}],
           'progress': 'complete', 'hasThumbnail': 'true', 'name': 'GanXianJianShenZhongXin.rvt', 'outputType': 'svf', 'status': 'success'},
       {
           'children': [{'type': 'resource', 'guid': '0576ce39-e54e-369e-da0e-7a306abf2144', 'mime': 'image/png', 'resolution': [100, 100], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview1.png', 'role': 'thumbnail', 'status': 'success'},
                        {'type': 'resource', 'guid': 'b5608b0b-b2e4-d4d7-85eb-3817e1a4a69f', 'mime': 'image/png', 'resolution': [200, 200], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview2.png', 'role': 'thumbnail', 'status': 'success'},
                        {'type': 'resource', 'guid': '72c1b16a-7ad7-5497-e0fd-3268ee880a0a', 'mime': 'image/png', 'resolution': [400, 400], 'urn': 'urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6bXliYWRidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview4.png', 'role': 'thumbnail', 'status': 'success'}], 'outputType': 'thumbnail', 'status': 'success', 'progress': 'complete'}], 'status': 'success'}

#listAllDerivativeFiles(a['derivatives'],'')
#print(allitem)
#done=0
#def OnProgress():
#    done+=1
#    print(done)
#   if done ==res.length:
#        result={'list':res,'totalSize':estSize}
#cc=_f2dNode(a[3])

#print(item.__dict__)
#print(res)






#

#new=c.get('assets')
#for i in new:
#    Mybasepath=os.path.dirname(ccc)
#    if not i['URI'].startswith('../') and not i['URI'].startswith('embed:/'):
#        newpath=i.get('URI')
#        downloadpath=os.path.join(Mybasepath,newpath)
#        print(downloadpath)
#        c=GET_manifest_derivativeurn(downloadpath)
#        b=c.result()
#        if b:
#            pass

#count=0
#Mybasepath=os.path.dirname(ccc)









basepath='/Users/wenhaie 1/PycharmProjects/Forge/myforge/Tem/'




#c=trverse(a[3]['children'][3],a[3])

#print(c.item)
#print(res)




a = {"type": "manifest", "hasThumbnail": "true", "status": "success", "progress": "complete", "region": "US",
     "urn": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0",
     "version": "1.0",
     "derivatives": [
        {"name": "GanXianJianShenZhongXin.rvt",
         "hasThumbnail": "true",
         "status": "success",
         "progress": "complete",
         "messages": [{"type": "warning",
                       "code": "Revit-MissingLink",
                       "message": ["<message>Missing link files: <ul>{0}</ul></message>","REF-GRIDE_t3.dwg, 吊顶.sat, 屋顶.sat, 屋顶突出女儿墙_New.sat, 幕墙参照面.sat, 平面示意图.dwg, 曲线结构.sat"]}],
         "outputType": "svf",
         "children": [
             {"guid": "6fac95cb-af5d-3e4f-b943-8a7f55847ff1",
              "type": "resource",
              "role": "Autodesk.CloudPlatform.PropertyDatabase",
                "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/model.sdb",
                "mime": "application/autodesk-db", "status": "success"},
               {"guid": "c1a929e4-bc30-be7f-1032-88ed565ad078", "type": "geometry",
                "role": "3d", "name": "{3D}",
                "viewableID": "acbcdb41-9a0b-4fe9-8898-5faaad4117b2-00102bcd",
                "phaseNames": "New", "status": "success", "hasThumbnail": "true",
                "progress": "complete",
                "children": [
                   {"guid": "acbcdb41-9a0b-4fe9-8898-5faaad4117b2-00102bcd", "type": "view",
                    "role": "3d", "name": "{3D}", "status": "success",
                    "progress": "complete",
                    "camera": [988.248413, -147.824234, 397.744171, 605.858704, 234.565475,
                               15.354465, -0.408248, 0.408248, 0.816497, 1.52421, 0, 1, 1]},
                   {"guid": "1b95a39d-01b5-df37-c9ae-0a21d16276b0", "type": "resource",
                    "role": "graphics",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}.svf",
                    "mime": "application/autodesk-svf"},
                   {"guid": "cee5a389-e074-42a4-16f2-c6491274e834", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "5e7e158b-a964-3329-3f69-79ccdfd24cd7", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "03a64d53-7ccc-054f-9ea5-719bc94913c4", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/3D View/{3D} 1059789/{3D}4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"}]},
               {"guid": "7fb62af8-e38f-47a5-9374-7f9c492e2e30-00058194", "type": "geometry",
                "role": "2d", "name": "B-01 - A-G 轴立面图、G-A轴立面图",
                "viewableID": "7fb62af8-e38f-47a5-9374-7f9c492e2e30-00058194",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "e3f4a1ff-bd89-13b8-a50c-3476dd724f26", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "7bbfacbe-9d48-bbd1-62e0-77d3b4ceec2b", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "cc8f7077-9583-f925-26c3-9c472787c7bf", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-01 - A-G 轴立面图、G-A轴立面图 360852/dwfx/B-01 - A-G 轴立面图、G-A轴立面图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "6e1f1677-7208-3183-b417-1a4fba776cae", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/c374a0f2-d9db-9036-efe0-cba79646f4e6_f2d/primaryGraphics.f2d"}]},
               {"guid": "7fb62af8-e38f-47a5-9374-7f9c492e2e30-0005819a", "type": "geometry",
                "role": "2d", "name": "B-04 - 3-3剖面图、4-4剖面图",
                "viewableID": "7fb62af8-e38f-47a5-9374-7f9c492e2e30-0005819a",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "71999f4c-8aed-828c-97c1-d3a030418861", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "6bbc96a2-fba3-70ae-2372-528831d831ef", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "30235537-f08f-6e46-3115-dc6cce8b2216", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-04 - 3-3剖面图、4-4剖面图 360858/dwfx/B-04 - 3-3剖面图、4-4剖面图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "0d1ac870-b98c-1da9-e556-9514260f1410", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/86b58b25-2ada-b716-4aa0-0363b70d0fdc_f2d/primaryGraphics.f2d"}]},
               {"guid": "3480a42a-bed2-4554-ad35-b928c4ea3b64-000589dd", "type": "geometry",
                "role": "2d", "name": "B-02 - 1 - 4轴立面图、4 - 1 轴立面图",
                "viewableID": "3480a42a-bed2-4554-ad35-b928c4ea3b64-000589dd",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "f3ab2507-d58c-92d5-464c-bf208848da47", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "94567cc0-330a-3ded-0613-754faa8161c8", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "509c76e2-72cd-052d-7262-0452775fcf6f", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-02 - 1 - 4轴立面图、4 - 1 轴立面图 362973/dwfx/B-02 - 1 - 4轴立面图、4 - 1 轴立面图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "96683327-b1e3-7b2b-01f1-c6f06ac8943a", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/e7266883-f27e-227f-042b-1483c5fa584c_f2d/primaryGraphics.f2d"}]},
               {"guid": "62676ba6-1b9d-4284-ac51-ad885e787d3e-0005914a", "type": "geometry",
                "role": "2d", "name": "B-03 - 1-1剖面图、2-2剖面图",
                "viewableID": "62676ba6-1b9d-4284-ac51-ad885e787d3e-0005914a",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "13dfa8e1-ba32-2952-2aa4-5bcf0e5c9b33", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "7d8cfff3-c68f-20db-a6b1-ed3aa9acc8df", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "2dbcc42f-d842-50f1-e576-0906f12b6039", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/B-03 - 1-1剖面图、2-2剖面图 364874/dwfx/B-03 - 1-1剖面图、2-2剖面图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "af5e33d1-a0fe-551f-dd12-55ef507e2c23", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/cdc2cb5e-3361-bbd7-c957-342e8ec2c379_f2d/primaryGraphics.f2d"}]},
               {"guid": "4b1358c7-d078-45f3-9209-00d1284909a4-00084bbc", "type": "geometry",
                "role": "2d", "name": "T-01 - 图纸目录",
                "viewableID": "4b1358c7-d078-45f3-9209-00d1284909a4-00084bbc",
                "status": "success", "progress": "complete", "properties": {
                   "Print Setting": {"Layout": "Landscape",
                                     "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "3d9cd94b-5dd8-2a21-3217-705ac2e1a740", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "f094a620-3e4d-93e7-03d4-e90ec8e4508d", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "84b2da8f-5a2b-0813-ecb9-ab3118b61cea", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/T-01 - 图纸目录 543676/dwfx/T-01 - 图纸目录4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "953c9d9a-94c0-47ab-5b1c-14ac96f24577", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/d39dc13b-137e-4ee1-6bcf-8d6c9281cb0b_f2d/primaryGraphics.f2d"}]},
               {"guid": "1b177165-551f-4ab3-8009-dcf2df55f105-000ccfe2", "type": "geometry",
                "role": "2d", "name": "C-01 - 墙身详图",
                "viewableID": "1b177165-551f-4ab3-8009-dcf2df55f105-000ccfe2",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "c27f7ed8-e7ed-927a-e2fe-3a958e0b89b9", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "4821068d-4fb3-5daa-2e20-0bf9712a8c79", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "a3597f57-e5c5-dd80-baee-75d00d1ba499", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/C-01 - 墙身详图 839650/dwfx/C-01 - 墙身详图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "490b0d17-9c08-128b-c92e-8a32e4461224", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/39e6cc34-e4a5-4337-20b0-ad633cbe52fd_f2d/primaryGraphics.f2d"}]},
               {"guid": "501d620b-cd22-4473-a39b-1075ce6b771c-000d5f59", "type": "geometry",
                "role": "2d", "name": "D-01 - 曲面定位图",
                "viewableID": "501d620b-cd22-4473-a39b-1075ce6b771c-000d5f59",
                "phaseNames": "New", "status": "success", "progress": "complete",
                "properties": {"Print Setting": {"Layout": "Landscape",
                                                 "Paper size": "ISO A4, 210 x 297 mm"}},
                "hasThumbnail": "true", "children": [
                   {"guid": "339e7d75-0153-8463-a7f2-9b81b6184bab", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图1.png",
                    "resolution": [100, 100], "mime": "image/png", "status": "success"},
                   {"guid": "3ac435c9-3cf0-bb10-b95e-54f2d9d7d346", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图2.png",
                    "resolution": [200, 200], "mime": "image/png", "status": "success"},
                   {"guid": "0d41f664-3eda-f461-d6d1-4138bd991f34", "type": "resource",
                    "role": "thumbnail",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/Resource/Sheet/D-01 - 曲面定位图 876377/dwfx/D-01 - 曲面定位图4.png",
                    "resolution": [400, 400], "mime": "image/png", "status": "success"},
                   {"guid": "ef5195aa-5b50-7e5d-b0a4-0ab18c640c71", "type": "resource",
                    "role": "graphics", "mime": "application/autodesk-f2d",
                    "status": "success",
                    "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/06ebd6e1-3f06-7145-3d55-92d51bc0ddbf_f2d/primaryGraphics.f2d"}]}]},
        {"status": "success", "progress": "complete", "outputType": "thumbnail",
         "children": [
            {"guid": "db899ab5-939f-e250-d79d-2d1637ce4565", "type": "resource", "role": "thumbnail",
             "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview1.png",
             "resolution": [100, 100], "mime": "image/png", "status": "success"},
            {"guid": "3f6c118d-f551-7bf0-03c9-8548d26c9772", "type": "resource", "role": "thumbnail",
             "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview2.png",
             "resolution": [200, 200], "mime": "image/png", "status": "success"},
            {"guid": "4e751806-0920-ce32-e9fd-47c3cec21536", "type": "resource", "role": "thumbnail",
             "urn": "urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvR2FuWGlhbkppYW5TaGVuWmhvbmdYaW4ucnZ0/output/preview4.png",
             "resolution": [400, 400], "mime": "image/png", "status": "success"}]}]}

#der=a['derivatives'][0]
#print(der)
#c=bubble(der)
#cc=c.listAllDerivativeFiles()

#for i in c.res:
#    cc=GET_manifest_derivativeurn(i.urn,i.localPath+i.rootFileName)
#    cc.result()

#i=c.res[1]
#print(i.__dict__)
#print(i.urn,i.localPath+i.rootFileName)
#cc=GET_manifest_derivativeurn(i.urn,i.localPath+i.rootFileName)
#cc.result()
