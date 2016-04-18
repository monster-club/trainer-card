from bson.objectid import ObjectId
from util.insert import insert_object


class Report:
  def __init__(self, database):
    self.collection = database.report
    self.create_keys = ['user_id', 'message']
    self.update_keys = ['issue', 'resolved']

  def all(self):
    return self.collection.find()

  def find(self, report_id):
    if(isinstance(report_id, str)):
      report_id = ObjectId(report_id)
    return self.collection.find_one({'_id': report_id})

  def create(self, content):
    insert = insert_object(self.create_keys, content, True)
    created = self.collection.insert_one(insert)
    return created

  def update(self, content, report_id):
    keys = list(set(self.create_keys) | set(self.update_keys))
    insert = insert_object(keys, content)
    resource = self.collection.update_one({'_id': ObjectId(report_id)},
                                          {'$set': insert})
    return resource
