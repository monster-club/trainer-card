from model import User
from jwt import encode
from os import environ


class Login:
  def __init__(self, database, hash_method):
    self.user = User(database, hash_method)
    self.hash_method = hash_method

  def validate(self, content, as_a = None):
    user = self.user.find_by_name(content['user_name'])
    if user == None:
      return False
    if self.hash_method.verify(content['password'], user['password']):
      if as_a is not None:
        if user['level'] != as_a:
          return False
      token = {
        'user_name': user['user_name'],
        'level': user['level']
      }
      jwt_token = encode(token, environ['JWT_KEY'], algorithm='HS256')
      user['token'] = jwt_token.decode('utf-8')
      return user
    else:
      return False
