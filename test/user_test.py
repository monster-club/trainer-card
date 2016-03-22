from falcon import HTTPBadRequest
from pytest import yield_fixture
from pymongo import MongoClient
from model import User, Token
from passlib.hash import bcrypt
from pytest import raises
from unittest.mock import MagicMock


client = MongoClient()
collection = client.trainer_card.user_test
tokens = client.trainer_card.token_test
bcrypt.encrypt = MagicMock(return_value='lololTotallySecureHash')
user = User(client, bcrypt)
token = Token(client)
# use a test database
user.collection = collection
user.token.collection = tokens
token.collection = tokens

@yield_fixture(autouse=True)
def tear_down_db():
  yield
  collection.remove({})
  tokens.remove({})

def test_get_all():
  for x in range(5):
    collection.insert_one({'user_name': 'Test' + str(x), 'password': 'wat',
                           'position': 0, 'location_id': 0})
  assert user.all().count() == 5

def test_key_error_raised_without_token():
  with raises(KeyError):
    user.create({'user_name': 'test user', 'password': 'wat',
                 'position': 0, 'location_id': 0})

def test_returns_false_with_bad_key():
  new_user = user.create({'user_name': 'test user', 'password': 'wat',
                          'position': 0, 'location_id': 0, 'token': 'junk'})
  assert new_user == False

def test_returns_false_if_name_in_use():
  # ensure the failure is not because of a missing token
  resource = token.create({'level': 'developer', 'goodies': 1})
  new_token = tokens.find_one({'_id': resource.inserted_id})

  collection.insert_one({'user_name': 'dummy'})
  new_user = user.create({'user_name': 'dummy', 'password': 'wat',
                          'position': 0, 'location_id': 0,
                          'token': new_token['key']})
  assert new_user == False

def test_raises_a_bad_request_if_key_is_missing():
  resource = token.create({'level': 'developer', 'goodies': 1})
  new_token = tokens.find_one({'_id': resource.inserted_id})
  with raises(HTTPBadRequest):
    new_user = user.create({'user_name': 'dummy', 'password': 'wat',
                            'position': 0, 'token': new_token['key']})

def test_creates_a_user():
  resource = token.create({'level': 'developer', 'goodies': 1})
  new_token = tokens.find_one({'_id': resource.inserted_id})
  new_user = user.create({'user_name': 'dummy', 'password': 'wat',
                          'position': 0, 'location_id': 0,
                          'token': new_token['key']})
  assert new_user['password'] == 'lololTotallySecureHash'
  assert new_user['level'] == new_token['level']
  assert new_user['money'] == 3000.0
