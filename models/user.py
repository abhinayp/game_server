from models.role import Role

class User:
  def __init__(self, name, role):
    self.name = name
    self.role = Role(role).name
