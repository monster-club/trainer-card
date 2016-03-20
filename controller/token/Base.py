from bson.json_util import dumps
from falcon import HTTP_201, HTTPUnauthorized
from model import Token
from json import loads
from util.authorize import authorize_as


class Base:
  def __init__(self, client):
    self.model = Token(client)

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.model.all())
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')

  def on_post(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      body = loads(req.stream.read().decode('utf-8'))
      created = self.model.create(body)
      resp.status = HTTP_201
      resp.body = dumps({'id': created.inserted_id})
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')