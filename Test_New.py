from Base.Model_Derivative import *
from Base.Data_Management import *
from urllib import parse
from bubble import bubble
#c=create_bucket("shixiangpersistent",policyKey="persistent")
#print(c.GetContent())
#GetBucketList
#bucklist=get_bucket_list()
#print(bucklist.GetContent())
bucketkey='shixiangpersistent'
filepath=r'C:\Users\2016028\Desktop\Tem\BAT_GanXianTestFile.rvt'
filname='BAT_GanXianTestFile.rvt'
#bucklist_detail=get_bucket_detail('shixiangpersistent')
#print(bucklist_detail.GetContent())

#c=upload_file_to_bucket(bucketkey,filepath,filname)

#print(c.GetContent())
## List Object in Bucket
#objectfrombucket=get_object_from_bucket('shixiangpersistent')
#print(objectfrombucket.GetContent())
## List Object in Bucket Detail
#objectfrombucket=get_object_from_bucket_detail('shixiangpersistent',filname)
#print(objectfrombucket.GetContent())



#c=POST_job(bucketkey,filname)

#print(c.GetContent())

#c=Get_urn_manifest(bucketkey,filname)
#print(c.GetContent())



#c=DELETE_urn_manifest(bucketkey,filname)
#print(c.GetContent())




#deleteobject=delete_object_from_bucket('whateverbucket','SONGYANG_6.rvt')
#print(deleteobject.GetContentObject())

#getobject=get_object_from_bucket('whateverbucket')
#print(getobject.GetContentObject().content)

b=bubble(bucketkey,filname)
ll=b.Download(r'F:\Autodesk\myforge\Tem\{filname}'.format(filname=filname))
