from bson.json_util import dumps
from falcon import HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from model import Login as LoginModel


class Login:
  def __init__(self, client):
    self.model = LoginModel(client, bcrypt)

  def on_post(self, req, resp):
    body = loads(req.stream.read().decode('utf-8'))
    user = self.model.validate(body)
    if user is not False:
      resp.body = dumps(user)
    else:
      raise HTTPUnauthorized('Unauthorized', 'Unauthorized')
