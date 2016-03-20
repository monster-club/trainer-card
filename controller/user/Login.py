from bson.json_util import dumps
from falcon import HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from jwt import encode
from os import environ


class Login:
  def __init__(self, client):
    self.collection = client.trainer_card.user

  def on_post(self, req, resp):
    body = loads(req.stream.read().decode('utf-8'))
    user = self.collection.find_one({'user_name': body['user_name']})
    if user == None:
      raise HTTPUnauthorized('Unauthorized', 'Unauthorized')
    if bcrypt.verify(body['password'], user['password']):
      token = {
        'user_name': user['user_name'],
        'level': user['level'],
      }
      jwt_token = encode(token, environ['JWT_KEY'], algorithm='HS256')
      user['token'] = jwt_token.decode('utf-8')
      resp.body = dumps(user)
    else:
      raise HTTPUnauthorized('Unauthorized', 'Unauthorized')
