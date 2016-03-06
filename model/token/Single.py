from bson.objectid import ObjectId
from falcon import HTTP_204, HTTPBadRequest, HTTPUnauthorized
from json import loads
from util.Insert import insert_object
from util.authorize import authorize_as


class Single:
  def __init__(self, client):
    self.collection = client.trainer_card.token
    self.update_keys = ['level', 'used']

  def on_put(self, req, resp, token_id):
    if authorize_as(req.auth, 'developer'):
      body = loads(req.stream.read().decode('utf-8'))
      insert = insert_object(self.update_keys, body)
      resource = self.collection.update_one({'_id': ObjectId(token_id)},
                                            {'$set': insert})
      if resource.modified_count == 1:
        resp.status = HTTP_204
      else:
        raise HTTPBadRequest('failed to update resource',
            'a resource with id: ' + token_id + 'was not found')
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')

  def on_delete(self, req, resp, token_id):
    if authorize_as(req.auth, 'developer'):
      result = self.collection.delete_one({'_id': ObjectId(token_id)})
      if result.delete_count == 1:
        resp.status = HTTP_204
      else:
        raise HTTPBadRequest('failed to update resource',
            'a resource with id: ' + token_id + 'was not found')
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')