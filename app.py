from falcon import API
from pymongo import MongoClient
from model import token, user
from util.cors import pre_cors, post_cors

client = MongoClient()
api = API(before=[pre_cors], after=[post_cors])

api.add_route('/v1/user/', user.Base(client))
api.add_route('/v1/user/{user_id}/', user.Single(client))
api.add_route('/v1/user/login/', user.Login(client))
api.add_route('/v1/token/', token.Base(client))
api.add_route('/v1/token/{token_id}/', token.Single(client))
