from falcon import HTTPBadRequest
from pytest import yield_fixture
from pymongo import MongoClient
from pymongo.errors import WriteError
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
  new_user = user.create(__user_insert('junk'))
  assert new_user == False

def test_returns_false_if_name_in_use():
  # ensure the failure is not because of a missing token
  new_token = __test_token()
  collection.insert_one({'user_name': 'dummy'})
  new_user = user.create(__user_insert(new_token['key']))
  assert new_user == False

def test_raises_a_bad_request_if_key_is_missing():
  new_token = __test_token()
  with raises(HTTPBadRequest):
    insert = __user_insert(new_token['key'])
    insert.pop('location_id')
    new_user = user.create(insert)

def test_creates_a_user():
  new_token = __test_token()
  new_user = user.create(__user_insert(new_token['key']))
  assert new_user['password'] == 'lololTotallySecureHash'
  assert new_user['level'] == new_token['level']
  assert new_user['money'] == 3000.0
  assert new_user['stars'] == 0
  assert new_user['score'] == 0

def test_updates_a_user():
  # no need to invoke a full integration
  inserted = collection.insert_one({'user_name': 'Test', 'password': 'wat',
                                    'position': 0, 'location_id': 0})
  before = collection.find_one({'_id': inserted.inserted_id})
  user.update({'position': 1}, str(inserted.inserted_id))
  after = collection.find_one({'_id': inserted.inserted_id})
  assert before['position'] == 0
  assert after['position'] == 1

def test_should_not_update_dev_keys_as_player():
  # no need to invoke a full integration
  inserted = collection.insert_one({'user_name': 'Test', 'password': 'wat',
                                    'position': 0, 'location_id': 0,
                                    'level': 'player'})
  before = collection.find_one({'_id': inserted.inserted_id})
  user.update({'level': 'developer', 'position': 1}, str(inserted.inserted_id))
  after = collection.find_one({'_id': inserted.inserted_id})
  assert before['level'] == 'player'
  assert before['position'] == 0
  assert after['level'] == 'player'
  assert after['position'] == 1

def test_should_throw_write_error_if_nothing_in_set():
  # no need to invoke a full integration
  inserted = collection.insert_one({'user_name': 'Test', 'password': 'wat',
                                    'position': 0, 'location_id': 0,
                                    'level': 'player'})
  before = collection.find_one({'_id': inserted.inserted_id})
  with raises(WriteError):
    user.update({'level': 'developer'}, str(inserted.inserted_id))

def test_should_be_able_to_update_dev_keys():
  inserted = collection.insert_one({'user_name': 'Test', 'password': 'wat',
                                    'position': 0, 'location_id': 0,
                                    'level': 'player'})
  before = collection.find_one({'_id': inserted.inserted_id})
  user.update({'level': 'developer'}, str(inserted.inserted_id), True)
  after = collection.find_one({'_id': inserted.inserted_id})
  assert before['level'] == 'player'
  assert after['level'] == 'developer'


def __test_token():
  resource = token.create({'level': 'developer', 'goodies': 1})
  return tokens.find_one({'_id': resource.inserted_id})

def __user_insert(token):
  return {'user_name': 'dummy', 'password': 'wat', 'position': 0,
          'location_id': 0, 'token': token}
