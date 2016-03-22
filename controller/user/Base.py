from bson.json_util import dumps
from falcon import HTTP_201, HTTPBadRequest, HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from util.authorize import authorize_as
from model import User


class Base:
  def __init__(self, client):
    self.model = User(client, bcrypt)

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.model.all())
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_post(self, req, resp):
    body = self.__authorize_body(req)
    new_user = self.model.create(body)
    resp.status = HTTP_201
    resp.body = dumps(new_user)

  def __authorize_body(self, request):
    body = loads(request.stream.read().decode('utf-8'))
    if 'token' in body:
      return body
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')
