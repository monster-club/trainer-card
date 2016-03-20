from bson.objectid import ObjectId
from util.Insert import insert_object
from uuid import uuid4


class Token:
  def __init__(self, client):
    self.collection = client.trainer_card.token
    self.create_keys = ['level', 'goodies']
    self.update_keys = ['level', 'used', 'goodies']

  def all(self):
    return self.collection.find()

  def create(self, content):
    insert = insert_object(self.create_keys, content, True)
    insert['key'] = str(uuid4()).replace('-', '')
    insert['used'] = False
    resource = self.collection.insert_one(insert)
    return resource

  def update(self, content, token_id):
    insert = insert_object(self.update_keys, content)
    resource = self.collection.update_one({'_id': ObjectId(token_id)},
                                          {'$set', insert})
    return resource

  def delete(self, token_id):
    resource = self.collection.delete_one({'_id': ObjectId(token_id)})
    return resource
