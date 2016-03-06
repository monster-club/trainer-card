from bson.json_util import dumps
from falcon import HTTP_201, HTTPBadRequest, HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from util.Insert import insert_object
from util.authorize import authorize_as


class Base:
  def __init__(self, client):
    self.collection = client.trainer_card.user
    self.create_keys = ['user_name', 'password', 'trainer_number',
                        'position', 'location_id']

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.collection.find())
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_post(self, req, resp):
    body = loads(req.stream.read().decode('utf-8'))
    insert = insert_object(self.create_keys, body, True)

    check_user = self.collection.find_one({'user_name': insert['user_name']})
    if check_user != None:
      raise HTTPBadRequest('User name is in use',
                           'The username ' + insert['user_name'] + ' is in use')

    insert['password'] = bcrypt.encrypt(insert['password'])
    insert['score'] = 0
    insert['stars'] = 0
    insert['money'] = 3000.0
    # TODO: get the level from the sign-up key
    insert['level'] = 'player'

    insert = self.collection.insert_one(insert)

    resp.status = HTTP_201
    resp.body = dumps({'id': insert.inserted_id})
