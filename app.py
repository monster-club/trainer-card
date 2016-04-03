from falcon import API
from pymongo import MongoClient
from controller import token, user
from util.cors import pre_cors, post_cors

client = MongoClient()
database = client.trainer_card
api = API(before=[pre_cors], after=[post_cors])

api.add_route('/v1/user/', user.Base(database))
api.add_route('/v1/user/{user_id}/', user.Single(database))
api.add_route('/v1/user/login/', user.Login(database))
api.add_route('/v1/user/login-dev/', user.DevLogin(database))
api.add_route('/v1/token/', token.Base(database))
api.add_route('/v1/token/{token_id}/', token.Single(database))
