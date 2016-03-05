class Single:
  def __init__(self, client):
    self.client = client.trainer_card.user
    self.update_keys = ['password', 'score', 'stars', 'money',
                        'currency', 'position', 'location_id']
    self.admin_keys = ['user_name', 'trainer_number', 'level']
