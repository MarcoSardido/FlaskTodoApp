from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# connection = os.environ.get('MONGO_URI') # MongoDB Atlas URI
connection = os.environ.get('MONGO_DOCKER_URI') # Docker URI

class Database(object):

    # setup MongoDB
    def __init__(self):
        self.client = MongoClient(connection)
        self.db = self.client['todo_data']


    # Created Todo
    def insert(self, element, collection_name):
        element['created'] = datetime.utcnow()
        element['updated'] = datetime.utcnow()
        inserted = self.db[collection_name].insert_one(element)
        return str(inserted.inserted_id)


    # Get All Todos
    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):
        if "_id" in criteria:
            criteria['_id'] = ObjectId(criteria['_id'])
        
        found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)

        if cursor:
            return found
        
        found = list(found)

        for indexID in range(len(found)):
            if "_id" in found[indexID]:
                found[indexID]["_id"] = str(found[indexID]["_id"])

        return found
    

    # Get Todo
    def find_by_id(self, id, collection_name):
        found = self.db[collection_name].find_one({'_id': ObjectId(id)})

        if found is None:
            return not found
        
        if "_id" in found:
            found["_id"] = str(found["_id"])

        return found
    

    # Update Todo
    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}

        element["updated"] = datetime.utcnow()
        set_obj = {"$set": element}

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"


    # Delete Todo
    def delete(self, id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)