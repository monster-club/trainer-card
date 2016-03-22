from bson.objectid import ObjectId
from model import Token
from pymongo import MongoClient
from pytest import yield_fixture


client = MongoClient()
collection = client.trainer_card.token_test
token = Token(client)
# use a test database
token.collection = collection

@yield_fixture(autouse=True)
def tear_down_db():
  yield
  collection.remove({})

def test_create_token():
  resource = token.create({'level': 'developer', 'goodies': 1})
  inserted = collection.find_one({'_id': resource.inserted_id})
  assert isinstance(resource.inserted_id, ObjectId) == True
  assert isinstance(inserted['key'], str) == True
  assert isinstance(inserted['used'], bool) == True

def test_get_all():
  for x in range(5):
    collection.insert_one({'level': 'player', 'goodies': x})
  assert token.all().count() == 5

def test_find_by_key():
  resource = token.create({'level': 'developer', 'goodies': 1})
  found = token.find(collection.find_one({'_id': resource.inserted_id})['key'])
  assert found['_id'] == resource.inserted_id

def test_update():
  resource = token.create({'level': 'developer', 'goodies': 1})
  before = collection.find_one({'_id': resource.inserted_id})
  token.update({'used': True}, str(resource.inserted_id))
  after = collection.find_one({'_id': resource.inserted_id})
  assert before['used'] == False
  assert after['used'] == True

def test_delete():
  resource = token.create({'level': 'developer', 'goodies': 1})
  result = token.delete(str(resource.inserted_id))
  record = collection.find_one({'_id': resource.inserted_id})
  assert result.deleted_count == 1
  assert record == None
