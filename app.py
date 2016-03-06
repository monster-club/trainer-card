from falcon import API
from pymongo import MongoClient
from model import token, user


client = MongoClient()
api = API()

api.add_route('/v1/user/', user.Base(client))
api.add_route('/v1/user/{user_id}/', user.Single(client))
api.add_route('/v1/user/login/', user.Login(client))
api.add_route('/v1/token/', token.Base(client))
api.add_route('/v1/token/{id}/', token.Single(client))
