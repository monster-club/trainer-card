from bson.json_util import dumps
from falcon import HTTP_201, HTTPUnauthorized
from model import Error
from json import loads
from util.authorize import authorize_as


class Base:
  def __init__(self, database):
    self.model = Error(database)

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'player'):
      resp.body = dumps(self.model.all())
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')

  def on_post(self, req, resp):
    if authorize_as(req.auth, 'player'):
      body = loads(req.stream.read().decode('utf-8'))
      created = self.model.create(body)
      resp.status = HTTP_201
      resp.body = dumps({'id': created.inserted_id})
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')
