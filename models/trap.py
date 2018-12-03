class Trap:
  def __init__(self, x, y, user, game, points=None):
    self.x = x
    self.y = y
    if user is not None:
      self.user = user.__dict__
    else:
      self.user = None
    self.game = game
    self.points = points
