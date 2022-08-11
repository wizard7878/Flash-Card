import random

class Question:
  """
  This object can generate exam
  selects a word as question 
  and options.
  in the end of exam
  can see how many of your selected 
  option were true or false
  you must have at least 4 flashcard to 
  start a exam
  """
  def __init__(self, words):
    self.words = words
    self.qs = [word for word in words]
    self.options = []
    self.answer = None
    self.correct_answers = 0
    self.false_answers = 0
    self.is_valid = True if len(self.words) >= 4 else False

  def generate_question(self):
      self.options.clear()
      self.answer = None

      random.shuffle(self.qs)

      choose_word = random.randint(0,len(self.qs)-1)
      test_question = self.qs[choose_word]

      self.qs.remove(self.qs[choose_word])
      self.options.append(test_question['persian'])
      self.answer = self.options[0]
      random.shuffle(self.words)
      for x in range(3):
        if self.options.__contains__(self.words[x]['persian']):
          self.options.append(self.words[x + 1]['persian'])
        else:
          self.options.append(self.words[x]['persian'])

      random.shuffle(self.options)
      return test_question

