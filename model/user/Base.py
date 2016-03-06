from bson.json_util import dumps
from falcon import HTTP_201, HTTPBadRequest, HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from util.Insert import insert_object
from util.authorize import authorize_as


class Base:
  def __init__(self, client):
    self.collection = client.trainer_card.user
    self.token_collection = client.trainer_card.token
    self.create_keys = ['user_name', 'password', 'position', 'location_id']

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.collection.find())
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_post(self, req, resp):
    body = self.__authorize_body(req)
    insert = insert_object(self.create_keys, body, True)
    used = self.__user_name_used(insert['user_name'])
    token = self.__check_token(body['token'])
    insert = self.__default_values(insert, token)

    created = self.collection.insert_one(insert)
    new_user = self.collection.find_one({'_id': created.inserted_id})
    self.token_collection.update_one({'_id': token['_id']},
                                     {'$set': {'used': True}})
    new_user['goodies'] = token['goodies']

    resp.status = HTTP_201
    resp.body = dumps(new_user)

  def __default_values(self, insert, token):
    insert['password'] = bcrypt.encrypt(insert['password'])
    insert['score'] = 0
    insert['stars'] = 0
    insert['money'] = 3000.0
    insert['level'] = token['level']
    insert['trainer_number'] = token['key']
    return insert

  def __user_name_used(self, name):
    check_user = self.collection.find_one({'user_name': name})
    if check_user == None:
      return True
    else:
      raise HTTPBadRequest('User name is in use',
                           'The username ' + insert['user_name'] + ' is in use')

  def __authorize_body(self, request):
    body = loads(request.stream.read().decode('utf-8'))
    if 'token' in body:
      return body
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def __check_token(self, token_key):
    token = self.token_collection.find_one({'key': token_key})
    if token == None or token['used'] == True:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')
    else:
      return token
