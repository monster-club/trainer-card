from bson.objectid import ObjectId
from pytest import yield_fixture
from pymongo import MongoClient
from unittest.mock import MagicMock
from passlib.hash import bcrypt
from model import Login


bcrypt.verify = MagicMock(return_value=True)
client = MongoClient()
collection = client.trainer_card.user_test

login = Login(client, bcrypt)
login.user.collection = collection

@yield_fixture(autouse=True)
def tear_down_db():
  yield
  collection.remove({})

def test_logs_in():
  user = __create_user()
  verified = login.validate({'user_name': 'wat', 'password': 'sure Jan'})
  assert len(verified['token'].split('.')) == 3 # JWT has all three parts
  assert isinstance(verified['_id'], ObjectId) == True

def test_fails_to_login_if_user_doesnt_exist():
  verified = login.validate({'user_name': 'wat', 'password': 'sure Jan'})
  assert verified == False

def test_fails_to_login_if_verification_fails():
  user = __create_user()
  shitty_login = Login(client, bcrypt)
  shitty_login.hash_method.verify = MagicMock(return_value=False)
  verified = login.validate({'user_name': 'wat', 'password': 'not right'})
  assert verified == False

def test_fails_to_login_if_as_a_does_not_match():
  user = __create_user()
  verified = login.validate({'user_name': 'wat', 'password': 'abc'},
                            'developer')
  assert verified == False


def __create_user():
  return collection.insert_one({'user_name': 'wat', 'level': 'player',
                                'password': 'someVeryLongHash'})
