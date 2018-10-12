from myforge.Base.Model_Derivative import *
import json
import base64
import os
import zlib
from io import StringIO,BytesIO
class bubble:
    def __init__(self,bucketkey,filename):
        self.bucketkey=bucketkey
        self.filename=filename
        self._outPath = './'
        self._token = ''
        #self._progress = progress
        self._sqllite = True
        # self._filesToFetch = 0;
        # self._estimatedSize = 0;
        # self._progress = 0;
        self._viewables = [] # {path: '', name: ''}
        self._errors = [] # ''
    def downloadBubble(self,urn,outPath,token):
        if token:
            self._token=""


        return ""

    def parseManifest(self,bubble):
        # getmainfest file
        #file=[{"name":"BAT_1.rvt","hasThumbnail":"true","status":"success","progress":"complete","outputType":"svf","children":[{"guid":"6fac95cb-af5d-3e4f-b943-8a7f55847ff1","type":"resource","role":"Autodesk.CloudPlatform.PropertyDatabase","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/model.sdb","mime":"application/autodesk-db","status":"success"},{"guid":"ca321dea-6d37-293a-25dc-6567c5dcad8a","type":"geometry","role":"3d","name":"{3D}","viewableID":"c26f95a2-e834-4473-8607-eff289a5f9ac-00041105","phaseNames":"New Construction","status":"success","hasThumbnail":"true","progress":"complete","children":[{"guid":"c26f95a2-e834-4473-8607-eff289a5f9ac-00041105","type":"view","role":"3d","name":"{3D}","status":"success","progress":"complete","camera":[315.333221,-152.736816,728.586182,-106.740509,269.336914,306.512451,-0.408248,0.408248,0.816497,0.663031,0,1,1]},{"guid":"4b1d315a-504d-2713-2c80-9b013ca075ae","type":"resource","role":"graphics","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/3D View/{3D} 266501/{3D}.svf","mime":"application/autodesk-svf"},{"guid":"c1b3c672-e344-858a-9ae7-dd7fe05a704b","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/3D View/{3D} 266501/{3D}1.png","resolution":[100,100],"mime":"image/png","status":"success"},{"guid":"e5f34e78-79e3-4a2d-78af-1e5d31d7b6a8","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/3D View/{3D} 266501/{3D}2.png","resolution":[200,200],"mime":"image/png","status":"success"},{"guid":"87faa7ef-3555-b72c-d00a-0e08b3908887","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/3D View/{3D} 266501/{3D}4.png","resolution":[400,400],"mime":"image/png","status":"success"}]}]},{"status":"success","progress":"complete","outputType":"thumbnail","children":[{"guid":"db899ab5-939f-e250-d79d-2d1637ce4565","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/preview1.png","resolution":[100,100],"mime":"image/png","status":"success"},{"guid":"3f6c118d-f551-7bf0-03c9-8548d26c9772","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/preview2.png","resolution":[200,200],"mime":"image/png","status":"success"},{"guid":"4e751806-0920-ce32-e9fd-47c3cec21536","type":"resource","role":"thumbnail","urn":"urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/preview4.png","resolution":[400,400],"mime":"image/png","status":"success"}]}]
        file=bubble
        items =[]

        def parseNodeRec (node):
            roles = [
                'Autodesk.CloudPlatform.DesignDescription',
                'Autodesk.CloudPlatform.PropertyDatabase',
                'Autodesk.CloudPlatform.IndexableContent',
                'leaflet-zip',
                'thumbnail',
                'graphics',
                'preview',
                'raas',
                'pdf',
                'lod',
            ]
            if node.get('role') in roles:
                item = {
                    "guid": node.get('guid'),
                    "mime": node.get('mime')
                }
                _items={}
                _items['pathInfo'] = self.getPathInfo(node.get('urn'))
                _items['item'] =item
                items.append(_items)

            if node.get('children'):
                for i in node.get('children'):
                    parseNodeRec(i)

        parseNodeRec({'children':file})
        return items







        pass

    def downloadAllDerivativeFiles(self,fileList, destDir):
        pass

    def getPathInfo(self,encodedURN):

        urn =encodedURN
        #print(urn[urn.rindex('/'):])

        rootFileName = urn[urn.rindex('/'):]
        #return rootFileName

        basePath =  urn[0:urn.rindex('/')]

        localPathTmp = basePath[urn.index('/'):]
        localPath =localPathTmp.replace('/output', '')

        return {rootFileName,localPath,basePath,urn}

    def getManifest(self):
        cc=GetManifest(self.bucketkey,self.filename)
        return cc.get_derivative()

    def getDerivatives(self,manifest):
        items = self.parseManifest(manifest)
        def c(item):
            if item.get("mime")=='application/autodesk-svf':
                return self.getSVFDerivatives(item)
            #elif item.get("mime")=='application/autodesk-f2d':
            #    return self.getF2dDerivatives(item)
            elif item.get("mime")=='application/autodesk-db':
                item['files']=[
                'objects_attrs.json.gz',
                'objects_vals.json.gz',
                'objects_offs.json.gz',
                'objects_ids.json.gz',
                'objects_avs.json.gz',
                item.rootFileName]

                return item
        return items
    def getSVFDerivatives(self,item):
        try:
            svfPath = item.get('urn')[item.basePath.length:]
            files = [svfPath]
            data =self.getDerivative(item.urn)
            buffer = BytesIO(data)

            z = zipfile.ZipFile(buffer, 'r')
            manifestData =z.read('manifest.json').decode('utf-8')
            manifest=json.loads(manifestData)
            if manifest.get('assets'):
                for i in manifest.get('assets'):
                    if i['URI'].index('embed:/') == 0:
                        pass
                    else:
                        files.append(i['URI'])


        except:
            pass

    def getDerivative (self,urn):
        c=GetDerivative(self.bucketkey, self.filename,urn)
        return c.GetContentObject().content

b=bubble('whateverbucket','BAT_1.rvt')

#cc=b.getManifest()

urn='urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2hhdGV2ZXJidWNrZXQvQkFUXzEucnZ0/output/Resource/3D View/{3D} 266501/{3D}.svf'
import gzip
import zipfile
import zlib
c=b.getDerivative(urn)

#print(c)
#what=zlib.adler32(c)
#cc=zlib.decompress(c,-zlib.MAX_WBITS)


