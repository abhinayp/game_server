class Riddle:
  def __init__(self, answer):
    self.answer = answer

  def riddleTypes():
    return ['Hospital', 'GrocerryStore', 'Movies']

  def riddleQuestions():
    options = Riddle.riddleTypes()
    rQuestions = {
      'Movies': [
        {
          'question': 'I sometimes come in a bag but I’m not new clothes from a store' +
                      'I sometimes come in a bucket but I’m not fried chicken' +
                      'I get bigger when I’m heated but I’m not bread dough' +
                      'I can be salted but I’m not a french fry' +
                      'I can be buttered but I’m not a pancake',
          'answer': 'popcorn'
        },
        {
          'question': 'jumble',
          'answer': 'ticket'
        },
        {
          'question': 'Something different to show every week, but I`m still the same place.' +
                      'If you`re eating it`s probably butter that you taste',
        },
        {
          'question': 'options',
          'options': options
        }
      ],
      'GrocerryStore': [
        {
          'question': 'Want to be clean, do not say nope... Go ahead and get a _____',
          'answer': 'soup'
        },
        {
          'question': 'jumble',
          'answer': 'checkout'
        },
        {
          'question': 'The hunt is almost over but before you relax... Check the place where' +
                      'you can find delicious snacks',
        },
        {
          'question': 'options',
          'options': options
        }
      ]
    }

    return rQuestions
