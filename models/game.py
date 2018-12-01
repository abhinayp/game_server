class Game:
  def __init__(self, number, user, health, points, wood):
    self.number = number
    self.user = user.__dict__
    self.health = health
    self.points = points
    self.wood = wood
