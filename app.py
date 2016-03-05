from falcon import API
from pymongo import MongoClient
from model import user


client = MongoClient()
api = API()
api.add_route('/v1/user/', user.Base(client))
api.add_route('/v1/user/{id}/', user.Single(client))
