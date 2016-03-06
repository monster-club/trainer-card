from bson.json_util import dumps
from falcon import HTTP_201, HTTPUnauthorized
from json import loads
from util.authorize import authorize_as
from util.Insert import insert_object
from uuid import uuid4


class Base:
  def __init__(self, client):
    self.collection = client.trainer_card.token
    self.create_keys = ['level', 'goodies']

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.collection.find())
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')

  def on_post(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      body = loads(req.stream.read().decode('utf-8'))
      insert = insert_object(self.create_keys, body, True)
      insert['key'] = str(uuid4()).replace('-', '')
      insert['used'] = False

      created = self.collection.insert_one(insert)

      resp.status = HTTP_201
      resp.body = dumps({'id': created.inserted_id})
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')