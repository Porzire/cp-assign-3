#
# A simple example of how to use PyMongo. For more information, take
# a look at the http://api.mongodb.org/python/ documentation.


import datetime
import hashlib

#
# Make sure pymongo is installed
#
try:
    import pymongo
    pyv = pymongo.version
    pyv = pyv.partition( "+" )[0]
    if map(int, pyv.split('.')) < [1,7]:
        sys.exit("ERROR - this example requires pymongo 1.7 or higher.")
    print("pymongo version: " + pyv)
except:
    sys.exit("ERROR - pymongo not installed.")

#
# Verify the version of pymongo is kosher
#

#
# Get access to the pythonExample collection in the test database
#
mongo = pymongo.MongoClient('jiemei.cs.dal.ca', 27017)
db = mongo["notes"]
col = db["notes"]
doc = col.find_one()
print(str(doc))

# from pymongo import ASCENDING, DESCENDING
#
# #
# # Drop the pythonExample collection
# #
# testDb.drop_collection('pythonExample')
# 
# col = testDb.pythonExample
# 
# #
# # Create an index on the name field
# #
# col.create_index([("name", DESCENDING)])
# 
# #
# # Create the buoy object
# #
# buoy = {
#     '_id' : hashlib.md5('Station 44025 - LLNR - 830').hexdigest(),
#     'name' : 'Station 44025 - LLNR - 830',
#     "lastUpdate": datetime.datetime.utcnow()
# }
# 
# #
# # Insert the buoy into the collection
# #
# col.insert(buoy)
# 
# #
# # Lookup the buoy
# #
# buoy = col.find_one({ '_id' : hashlib.md5('Station 44025 - LLNR - 830').hexdigest() });
# print('Found buoy: ' + str(buoy))
# 
# #
# # Add a buoy using upsert
# #
# 
# buoyData = { 'readingType' : 'wind', 'value' : '10' }
# 
# col.update({"_id" : hashlib.md5('Station 44026 - LLNR - 831').hexdigest()}, { '$set' : { 'name' : 'Station 44026 - LLNR - 831', 'lastUpdate' : datetime.datetime.utcnow() }, '$addToSet' : { 'data' : buoyData } }, True);
# 
# #
# # Add the same data... only the lastUpdate field should change.
# #
# col.update({"_id" : hashlib.md5('Station 44026 - LLNR - 831').hexdigest()}, { '$set' : { 'name' : 'Station 44026 - LLNR - 831', 'lastUpdate' : datetime.datetime.utcnow() }, '$addToSet' : { 'data' : buoyData } }, True);
# 
# #
# # Add some new data.
# #
# buoyData = { 'readingType' : 'wind', 'value' : '20' }
# 
# col.update({"_id" : hashlib.md5('Station 44026 - LLNR - 831').hexdigest()}, { '$set' : { 'name' : 'Station 44026 - LLNR - 831', 'lastUpdate' : datetime.datetime.utcnow() }, '$addToSet' : { 'data' : buoyData } }, True);
