from Base.Model_Derivative import *
import json
import os
from io import BytesIO
import zipfile

import gzip


class progress:
    def __init__(self):
        pass

class bubble:
    def __init__(self,bucketkey,filename):
        self.bucketkey=bucketkey
        self.filename=filename
        self._progress = progress()
        self._outPath = './'
        self._token = ''
        self._sqllite = True
        self._viewables = [] # {path: '', name: ''}
        self._errors = [] # ''

    def downloadBubble(self,urn,outPath,token):
        if token:

            self._token =authenticate.two_legged_access().get_access_token()
            self._outPath = outPath

            self._progress.msg = 'Downloading manifest'
            #Get MainFest as JSON
            bubble=Get_urn_manifest(self.bucketkey,self.filename).GetContentAsJson()

            self._progress.msg = 'Listing all derivative files'
            #listAllDerivativeFiles
            self.listAllDerivativeFiles(bubble)
        else:
            print("token is bad")
    # list all DerivativeFile
    #input is Mainfest is bubble
    def listAllDerivativeFiles(self,Mainfest):
        #bubble=Get_urn_manifest(self.bucketkey,self.filename).GetContentAsJson()
        bubble=Mainfest
        res = []
        def traverse(node,parent):
            if node.get('role')=='Autodesk.CloudPlatform.PropertyDatabase' or \
                    node.get('role')=='Autodesk.CloudPlatform.DesignDescription' or \
                    node.get('role') == 'Autodesk.CloudPlatform.IndexableContent'or \
                    node.get('role') == 'graphics' or node.get('role') == 'raas' or \
                    node.get('role') == 'pdf' or node.get('role') == 'leaflet-zip' or \
                    node.get('role') == 'preview' or node.get('role') == 'lod':
                print('well')

                item = {'mime': node.get('mime')}
                self.extractPathsFromGraphicsUrn(node.get('urn'),item)

                node['urn']='$file$/' + item.get('localPath')+ item.get('rootFileName')
                if node.get('role')!='Autodesk.CloudPlatform.PropertyDatabase' or (self._sqllite and self._sqllite =='true' ) :
                    res.append(item)
                if node.get('mime')!='application/autodesk-svf' or node.get('mime')!='application/autodesk-f2d' :
                    item['name']=node['name']=parent.get('name')
                    if parent.get('hasThumbnail')=='true':
                        thumbnailItem = {'mime': 'thumbnail', 'urn': bubble.get('urn'), 'guid': parent.get('guid'),
                                         'localPath': item.get('localPath'),
                                         'thumbnailUrn': '$file$/thumbnails/' + parent.get('guid') + '.png',
                                         'rootFileName': (item.get('rootFileName')+ '.png')
                                         }
                        res.append(thumbnailItem)
                if node.get('type')=='geometry':
                    if node.get('intermediateFile') and node.get('children'):
                        for i in range(0,len(node.get('children'))):
                            if node.get('children')[i].get('mime')=='application/autodesk-f2d':
                                f2dNode=node.get('children')[i]
                        if f2dNode:
                            f2dUrl=f2dNode.get('urn')
                            idx=f2dUrl.index(bubble.get('urn'))
                            baseUrl=f2dUrl[0:idx+len(bubble.get('urn'))]
                            item={ 'mime': 'application/octet-stream', 'urn': bubble.get('urn'), 'guid': node.get('guid')}
                            intPath='/' + node.get('intermediateFile')
                            if baseUrl.index('urn:adsk.objects')==0:
                                intPath=quote(intPath)
                            fullPath=baseUrl+intPath
                            self.extractPathsFromGraphicsUrn(fullPath,item)
                            res.append(item)
                if node.get('children'):
                    for i in node.get('children'):
                        traverse(i,node)
        node=bubble['derivatives'][0].get('children')
        map(traverse(node,''),node)

        print('Manifests to process:{}'.format(len(res)))

        '''
        if len(res)==0:
            return callback('',{'list':[],'totalSize':0})
        self.current=0
        self.done=0
        self.estSize=0
        self.countedPropDb={}
        def processOne():
            def onProgress():
                self.done+=1
                print('Manifests done{}'.format(self.done))
                if (self.done==len(res)):
                    result = {
                        'list': res,
                        'totalSize': estSize}
                    callback('',result)
                else:
                    processOne()

            if self.current>=len(res):
                return
            self.current+=1

            rootItem=res[self.current]
            files=rootItem['files']=[]
            print(rootItem.get('mime') + ': ' + rootItem.get('rootFileName'))
            if rootItem.get('mime')!='thumbnail':
                basePath=rootItem.get('basePath')
            if rootItem.get('mime')=='application/autodesk-db':
                files.append('objects_attrs.json.gz')
                files.append('objects_vals.json.gz')
                files.append('objects_avs.json.gz')
                files.append('objects_offs.json.gz')
                files.append('objects_ids.json.gz')
                onProgress()
            elif rootItem.get('mime')=='thumbnail':
                rootItem['files'].append(rootItem.get('rootFileName'))
            elif rootItem.get('mime')=='application/autodesk-svf':
                svfPath=rootItem.get('urn')[0:len(basePath)]
                files.append(svfPath)
                def run():
                    myItem=rootItem
                    def _getItem(error,success):
                        if (error):
                            self._errors.append('Failed to download'+myItem.get('urn'))
                        if (success):
                            self.estSize+=len(success)
                            manifest=''
                            try:
                                if success[0]==0x1f and success[1]==0x8b:
                                    success=zlib.decompress(success)
                                    manifest=json.loads(success.decode('utf-8'))
                            except Exception:
                                print('Error',Exception.args)
                            if (manifest and manifest.get('assets')):
                                for i in range(0,len(manifest.get('assets'))):
                                    asset=manifest.get('assets')
                                    if asset.get('URI').index('../')==0:
                                        continue
                                    self.estSize+=asset.get('size')
                                    myItem.get('files').append(asset.get("URI"))
                        self.countedPropDb[rootItem.get('basePaht')]=1
                        onProgress()
                    self.getItem(rootItem.get('urn'),'',_getItem(error,success))

                run()
            elif rootItem.get('mime')=='application/autodesk-f2d':
                files.append('manifest.json.gz')
                mainfestPath=basePath+'manifest.json.gz'
        '''
        return res


    def downloadAllDerivativeFiles(self,fileList, destDir):
        pass
    def extractPathsFromGraphicsUrn(self,urn, result):
        pass
    def getManifest(self):
        bubble = Get_urn_manifest(self.bucketkey, self.filename).GetContentAsJson()
        return bubble
    def parseManifest(self,MainFest):
        file=MainFest.get("derivatives")
        items =[]

        def getPathInfo( encodedURN):

            urn = encodedURN
            # print(urn[urn.rindex('/'):])

            rootFileName = urn[urn.rindex('/'):]
            # return rootFileName

            basePath = urn[0:urn.rindex('/')]

            localPathTmp = basePath[urn.index('/'):]
            localPath = localPathTmp.replace('/output', '')

            return {'rootFileName':rootFileName, 'localPath':localPath, 'basePath':basePath, 'urn':urn}

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
                item.update(getPathInfo(node.get('urn')))
                items.append(item)

            if node.get('children'):
                for i in node.get('children'):
                    parseNodeRec(i)

        parseNodeRec({'children':file})
        return items

    def downloadItem(self,urn):
        pass
    def getDerivatives(self,manifest):
        items = self.parseManifest(manifest)
        def c(item):
            if item.get("mime")=='application/autodesk-svf':
                return self.getSVFDerivatives(item)
            elif item.get("mime")=='application/autodesk-f2d':
                return self.getF2dDerivatives(item)
            elif item.get("mime")=='thumbnail':
                pass

            elif item.get("mime")=='application/autodesk-db':
                item['files']=[
                '/objects_attrs.json.gz',
                '/objects_vals.json.gz',
                '/objects_offs.json.gz',
                '/objects_ids.json.gz',
                '/objects_avs.json.gz',
                item.get('rootFileName')]
                return item
            else:
                item['files']=[item.get('rootFileName')]
                return item
        ll=map(c,items)
        return list(ll)
    #GetSVFDerivative
    def getSVFDerivatives(self,item):
        try:
            svfPath = item.get('urn')[len(item.get('basePath')):]
            files = [svfPath]
            data =self.getDerivative(item.get('urn'))
            #将svf存储到内存
            buffer = BytesIO(data)
            z = zipfile.ZipFile(buffer, 'r')
            manifestData =z.read('manifest.json').decode('utf-8')
            manifest=json.loads(manifestData)
            if manifest.get('assets'):
                for i in manifest.get('assets'):
                    if i.get('URI').find('embed:/') == 0:
                        pass
                    elif i.get('URI').find('../../')==0:
                        pass
                    else:
                        files.append('/'+i['URI'])

            item.update({'files':files})

            return item


        except :
            pass
    def getF2dDerivatives(self,item):
        try:
            files = ['/manifest.json.gz']
            manifestPath = item.get('basePath') +'/manifest.json.gz'
            print(manifestPath)
            data =self.getDerivative(manifestPath)
            #将svf存储到内存
            buffer = BytesIO(data)
            z = gzip.GzipFile(fileobj=buffer)
            manifestData =z.read().decode('utf-8')
            manifest=json.loads(manifestData)
            if manifest.get('assets'):
                for i in manifest.get('assets'):
                    if i.get('URI').find('embed:/') == 0:
                        pass
                    elif i.get('URI').find('../../')==0:
                        pass
                    else:
                        files.append('/'+i['URI'])
            item.update({'files': files})
            return item


        except :
            pass

    #GetDerivative
    def getDerivative (self,urn):
        c=GET_manifest_derivativeurn(self.bucketkey, self.filename,urn)
        return c.GetContentObject().content

    def getItem(self,itemUrn, outFile, callback):
        pass
    def getThumbnail(self,urn, guid, sz, outFile, callback):
        pass

    def Download(self,Localpath):
        bubble=Get_urn_manifest(self.bucketkey,self.filename).GetContentAsJson()
        list=self.getDerivatives(bubble)
        print(list)
        #for i in list:
        #    print(i)
        def getpathbycount(path,num):
            c = path.split("/")
            new = "/".join(c[num:])
            return new
        for i in list:
            if i:
                filename=i.get('files')
                baseurn= os.path.dirname(i.get('urn'))

                downloadfileurn=[baseurn+i for i in filename]

                basepath='/'+getpathbycount(i.get('basePath'),2)


                Local=[os.path.abspath(Localpath+basepath+i) for i in filename]
                print(Local)
                for i,p in zip(downloadfileurn,Local):
                    print("{} start".format(i))
                    get=GET_manifest_derivativeurn(self.bucketkey,self.filename,i).GetContentObject().content

                    if os.path.exists(os.path.dirname(p)):
                        pass
                    else:
                        os.makedirs(os.path.dirname(p))

                    with open(p,'wb') as f :
                        f.write(get)
                    print("{} done".format(i))




#b=bubble('shixiang','MULTIFILES.zip')

#with open(r'E:\BIM\06_Forge_平台\myforge\Tem\MainFest','r') as f :
#    c=f.read()
#    cc=json.loads(c)


#ll=b.parseManifest(cc)
#for i in ll:
#    print(i)
#c=b.getManifest()
#print(c)
#ll=b.getDerivatives(c)
#for i in ll:
#    print(ll)
#c=b.getManifest()
#print(c)
#ll=b.Download('E:\\BIM\\06_Forge_平台\\myforge\\static\\New')


