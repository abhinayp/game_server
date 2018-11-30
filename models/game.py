class Game:
  def __init__(self, number, user, answer):
    self.number = number
    self.user = user.__dict__
    self.answer = answer
