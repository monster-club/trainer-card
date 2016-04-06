from model import User
from jwt import encode
from os import environ
from util.authorize import sign_token


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
      user['token'] = sign_token(user['user_name'], user['level'])
      return user
    else:
      return False
