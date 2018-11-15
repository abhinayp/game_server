from models.role import Role
from bson.objectid import ObjectId

class User:
  id = ""
  def __init__(self, name, role, api_token):
    self.name = name
    self.role = Role(role).name
    self.api_token = api_token

  def get(users, id):
    user = users.find_one({"_id": ObjectId(id)})
    u = User(user.get('name'), user.get('role'), user.get('api_token'))
    u.id = str(user.get('_id'))
    return u

  def get_by_api_token(users, api_key):
    user = users.find_one({"api_token": api_key})
    if user is None:
        return None
    u = User(user.get('name'), user.get('role'), user.get('api_token'))
    u.id = str(user.get('_id'))
    return u

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.id

  def __repr__(self):
    return '<User %r>' % (self.name)
