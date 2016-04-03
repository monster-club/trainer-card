from bson.json_util import dumps
from falcon import HTTP_201, HTTPUnauthorized
from passlib.hash import bcrypt
from util.authorize import authorize_as, authorize_body
from model import User


class Base:
  def __init__(self, database):
    self.model = User(database, bcrypt)

  def on_get(self, req, resp):
    if authorize_as(req.auth, 'developer'):
      resp.body = dumps(self.model.all())
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_post(self, req, resp):
    body = authorize_body(req)
    new_user = self.model.create(body)
    resp.status = HTTP_201
    resp.body = dumps(new_user)
