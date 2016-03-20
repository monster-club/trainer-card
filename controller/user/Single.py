from bson.objectid import ObjectId
from bson.json_util import dumps
from falcon import HTTP_204, HTTP_404, HTTPBadRequest, HTTPUnauthorized
from json import loads
from passlib.hash import bcrypt
from util.Insert import insert_object
from util.authorize import authorize_as


class Single:
  def __init__(self, client):
    self.collection = client.trainer_card.user
    self.update_keys = ['password', 'score', 'stars', 'money',
                        'currency', 'position', 'location_id']
    self.admin_keys = ['user_name', 'trainer_number', 'level']

  def on_get(self, req, resp, user_id):
    if authorize_as(req.auth, 'developer'):
      resource = self.collection.find_one({'_id': ObjectId(user_id)})
      if resource != None:
        resp.body = dumps(resource)
      else:
        resp.status = HTTP_404
    else:
      raise HTTPUnauthorized('unautharized', 'unautharized')

  def on_put(self, req, resp, user_id):
    try:
      is_dev = authorize_as(req.auth, 'developer')
    except:
      is_player = authorize_as(req.auth, 'player')
      if not is_player:
        raise HTTPUnauthorized('unautharized', 'unautharized')

    if is_dev:
      keys = list(set(self.update_keys) | set(self.admin_keys))
    else:
      keys = self.update_keys

    body = loads(req.stream.read().decode('utf-8'))
    insert = insert_object(keys, body)
    if 'password' in insert:
      insert['password'] = bcrypt.encrypt(insert['password'])
    resource = self.collection.update_one({'_id': ObjectId(user_id)},
                                          {'$set': insert})
    if resource.modified_count == 1:
      resp.status = HTTP_204
    else:
      raise HTTPBadRequest('failed to update resource',
                           'a resource with id: ' + user_id + ' was not found')