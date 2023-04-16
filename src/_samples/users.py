import logging
from hashlib import sha1
from typing import DefaultDict
from micromongo import Model, Index, fields, validate
from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET
from crm.models.group import Group
from bson.objectid import ObjectId

class User(Model):
    name = fields.Str(required=True, validate=validate.Length(min=5))
    username = fields.Str(required=True, validate=validate.Length(min=5))
    password = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Length(min=5))
    group_id = fields.ObjectId(required=True)
    admin = fields.Boolean(default=False)

    class Meta:
        collection = 'users'
        host = HOST
        database = DATABASE
        username = USERNAME
        password = PASSWORD
        indices = (
            Index('name'),
            Index('username', unique=True),
            Index('password'),
            Index('email'),
            Index('group_id'),
            Index('user_type'),
        )
        replicaset = REPLICASET

    @classmethod
    def authenticate(cls, username, password, projection=None):
        logging.debug(sha1(password.encode()).hexdigest())
        return cls.collection.find_one({'username': username, 'password': sha1(password.encode()).hexdigest()}, projection)

    @classmethod
    def getUser(cls, filters, projection=None):
        if isinstance(filters, ObjectId):
            filters = {'_id': filters}
        return cls.collection.find_one(filters, projection)

    @staticmethod
    def getUsers(filters=None, projection=None):
        return User.collection.find(filters, projection)

    @staticmethod
    def getUsersList(filters=None, projection=None):
        groups = {group._id: group.name for group in Group.getGroups({})}
        users = []
        for user in User.collection.find(filters, projection):
            user.group_name = groups.get(user.group_id)
            users.append(user)
        return users

    @classmethod
    def createUser(cls,query):
        output = cls.collection.insert_one(query)
        return output

    def update(self, newvalues):
        return User.collection.update_one({'_id': self._id}, {'$set': newvalues})

    @classmethod
    def getUserName(cls, id):
        user = cls.collection.find_one(id)
        return user.get('name')

    @classmethod
    def updateUser(cls,query, newValues):
        cls.collection.update_one(query, newValues)
        return

    @classmethod
    def getSupervisors(cls):
        logging.debug('heps')
        supervisors = cls.collection.find({'user_type': 'supervisor'},{'username','password'})
        return supervisors