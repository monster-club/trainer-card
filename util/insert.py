from falcon import HTTPBadRequest


def insert_object(keys, body, fail = False):
  insert = {}
  for k in keys:
    if k in body:
      insert[k] = body[k]
    else:
      if fail:
        raise HTTPBadRequest('Missing keys for user creation',
                             'Missing the key: ' + k)
  return insert
