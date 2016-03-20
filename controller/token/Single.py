from falcon import HTTP_204, HTTPBadRequest, HTTPUnauthorized
from model import Token
from json import loads
from util.authorize import authorize_as


class Single:
  def __init__(self, client):
    self.model = Token(client)

  def on_put(self, req, resp, token_id):
    if authorize_as(req.auth, 'developer'):
      body = loads(req.stream.read().decode('utf-8'))
      resource = self.model(body, token_id)
      if resource.modified_count == 1:
        resp.status = HTTP_204
      else:
        raise HTTPBadRequest('failed to update resource',
            'a resource with id: ' + token_id + 'was not found')
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')

  def on_delete(self, req, resp, token_id):
    if authorize_as(req.auth, 'developer'):
      result = self.model(token_id)
      if result.deleted_count == 1:
        resp.status = HTTP_204
      else:
        raise HTTPBadRequest('failed to update resource',
            'a resource with id: ' + token_id + 'was not found')
    else:
      raise HTTPUnauthorized('unauthorized', 'unauthorized')