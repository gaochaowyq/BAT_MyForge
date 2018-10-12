from Base.Model_Derivative import *
from Base.Data_Management import *
from urllib import parse
from bubble import bubble
#c=create_bucket("shixiang")
#print(c.GetContentObject().content)
#GetBucketList
#bucklist=get_bucket_list()
#print(bucklist.GetContentObject().content)

filepath=r'/Users/wenhaie 1/Desktop/SongYang__ALL/SONGYANG_1_code_fin.rvt'
filname='SONGYANG_1_code_fin.rvt'


#c=upload_file_to_bucket('shixiang',filepath,filname)

#print(c.GetContentObject().content)

#c=POST_job('shixiang',filname)

#print(c.GetContentObject().content)

#c=Get_urn_manifest("shixiang",filname)
#print(c.GetContentObject().content)

#c=DELETE_urn_manifest("shixiang",'SONGYANG_6.rvt')
#print(c.GetContentObject().content)

#objectfrombucket=get_object_from_bucket('whateverbucket')
#print(objectfrombucket.GetContentAsJson())


#deleteobject=delete_object_from_bucket('whateverbucket','SONGYANG_6.rvt')
#print(deleteobject.GetContentObject())

#getobject=get_object_from_bucket('whateverbucket')
#print(getobject.GetContentObject().content)

b=bubble('shixiang',filname)
ll=b.Download(r'/Users/wenhaie 1/PycharmProjects/myforge/Tem')
