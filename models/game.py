class Game:
  def __init__(self, number, user, health, points, wood, current_location, intro):
    self.number = number
    self.user = user.__dict__
    self.health = health
    self.points = points
    self.wood = wood
    self.current_location = current_location
    self.intro = intro
