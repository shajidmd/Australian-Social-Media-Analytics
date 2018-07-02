import couchdb
import json
import os
from os import listdir

##Couch dB connection
##------------------------------------------------------------------
user='admin'
password='admin'
couchserver = couchdb.Server("http://%s:%s@115.146.95.146:5984/" % (user,password))
print(couchserver)

#Divorce Rate Dataset DB ---------------
db_name = 'divorce_rate_2016'
if db_name in couchserver:
    db = couchserver[db_name]
else:
    db = couchserver.create(db_name)

sourcepath = "/volume/aurin_dataset/extracted_files/"


from os.path import isfile, join
filelist = [f for f in listdir(sourcepath) if isfile(join(sourcepath, f))]
print(filelist)

#Store all data to couchdb
for file in filelist:
    f = open(sourcepath + file, 'r')
    data = json.load(f)
       
    doc_id, doc_rev = db.save(data)
    print("Written to database")
    f.close()
 
