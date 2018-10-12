from Base.Model_Derivative import *
import json
from collections import namedtuple
import base64
import os
import zlib
import zipfile
import gzip
from urllib.parse import quote

from io import StringIO,BytesIO
bucketname='shixiang'
filename='MULTIFILES.zip'
derivativeUrn='urn:adsk.viewing:fs.file:dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6c2hpeGlhbmcvTVVMVElGSUxFUy56aXA/output/preview1.png'

#c=Get_urn_manifest(bucketname,filename)

#print(c.GetContentAsJson())


#c=GET_manifest_derivativeurn(bucketname,filename,derivativeUrn)
#file=c.GetContentObject().content
#print(file)

#buffer=BytesIO(file)

#with open(r'E:\BIM\06 Forge 平台\myforge\static\{3D}.svf','wb') as f:
#    f.write(c.GetContentObject().content)

#p=gzip.GzipFile(mode="rb",fileobj=file)

#filename=r'E:\BIM\06_Forge_平台\myforge\static\NewFile\Resource\3D View\{3D} 396838\Materials.json.gz'

#print(p.read1())
#zip_file  = gzip.GzipFile(fileobj=buffer)

#print(zip_file.read())
b=[1,2,3,4,5]
def c():
    if 1:
        print('star')
        return
    print('what')
    if 1:
        print('good')
c()


