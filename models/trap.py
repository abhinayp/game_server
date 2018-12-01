class Trap:
  def __init__(self, x, y, user, game, points=None):
    self.x = x
    self.y = y
    self.user = user.__dict__
    self.game = game
    self.points = points
