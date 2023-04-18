# import logging
# from hashlib import sha1
# from typing import DefaultDict
from micromongo import Model, Index, fields, validate
# from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET
# from crm.models.group import Group
from bson.objectid import ObjectId
from datetime import datetime
import pytz

myTimezone = pytz.timezone('Asia/Manila')

class Todo(Model):
    title = fields.Str(required=True, validate=validate.Length(min=5))
    description = fields.Str(required=True, validate=validate.Length(min=5))
    completed = fields.Boolean(default=False)
    created = fields.Date(datetime.now(myTimezone))
    updated = fields.Date(datetime.now(myTimezone))

    class Meta:
        collection = 'todo_data'
        host = 'mongodb'
        database = 'todo_data'
        username = 'mongouser'
        password = 'mongopassword'
        indices = (
            Index('title'),
            Index('description'),
            Index('completed'),
            Index('created'),
            Index('updated')
        )

    @classmethod
    def get(cls, id):
        found = cls.collection.find_one({'_id': ObjectId(id)})
        found["_id"] = str(found["_id"]) #convert ObjectId into string
        return found

    @staticmethod
    def getList(filters=None, projection=None):
        return Todo.collection.find(filters, projection)

    @classmethod
    def create(cls, query):
        output = cls.collection.insert_one(query)
        return output

    
    def update(self, newValues):
        newValues["updated"] = datetime.now(myTimezone)
        Todo.collection.update_one({"_id": ObjectId(self._id)}, {"$set": newValues})
        return self, newValues
    
    
    def delete(self):
        Todo.collection.delete_one({"_id": ObjectId(self._id)})
        return