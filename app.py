from falcon import API
from pymongo import MongoClient
from controller import token, user, error, client_error, report
from util.cors import pre_cors, post_cors

client = MongoClient()
api = API(before=[pre_cors], after=[post_cors])

api.add_route('/user/', user.Base(client.trainer_card))
api.add_route('/user/{user_id}/', user.Single(client.trainer_card))
api.add_route('/user/login/', user.Login(client.trainer_card))
api.add_route('/user/login-dev/', user.DevLogin(client.trainer_card))
api.add_route('/token/', token.Base(client.trainer_card))
api.add_route('/token/{token_id}/', token.Single(client.trainer_card))
api.add_route('/error/', error.Base(client.jenny))
api.add_route('/error/{error_id}/', error.Single(client.jenny))
api.add_route('/client_error/', client_error.Base(client.jenny))
api.add_route('/client_error/{error_id}/', client_error.Single(client.jenny))
api.add_route('/report/', report.Base(client.jenny))
api.add_route('/report/{report_id}/', report.Single(client.jenny))
