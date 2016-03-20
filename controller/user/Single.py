from bson.json_util import dumps
from falcon import HTTP_204, HTTP_404, HTTPBadRequest, HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from util.authorize import authorize_as
from model import User


class Single:
  def __init__(self, client):
    self.model = User(client, bcrypt)

  def on_get(self, req, resp, user_id):
    if authorize_as(req.auth, 'developer'):
      resource = self.model.find(user_id)
      if resource != None:
        resp.body = dumps(resource)
      else:
        resp.status = HTTP_404
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_put(self, req, resp, user_id):
    try:
      if(authorize_as(req.auth, 'developer')):
        is_dev = True
    except:
      is_player = authorize_as(req.auth, 'player')
      is_dev = False
      if not is_player:
        raise HTTPUnauthorized('unautharized', 'unautharized')

    body = loads(req.stream.read().decode('utf-8'))
    resource = self.model.update(body, user_id, is_dev)
    if resource.modified_count == 1:
      resp.status = HTTP_204
    else:
      raise HTTPBadRequest('failed to update resource',
                           'a resource with id: ' + user_id + ' was not found')