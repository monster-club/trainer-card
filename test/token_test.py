from bson.objectid import ObjectId
from model import Token
from pymongo import MongoClient
from pytest import yield_fixture


client = MongoClient()
collection = client.trainer_card.token
token = Token(client)

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
