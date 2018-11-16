class Trap:
  def __init__(self, x, y, user, game):
    self.x = x
    self.y = y
    self.user = user.__dict__
    self.game = game
