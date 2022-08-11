from config import bot
from menu import create_reply_keyboard_markup, main_menu, delete_category_menu,flash_card_menu
from telebot.types import ReplyKeyboardRemove

from questions import Question

from apis import (
  create_category_api, 
  create_word_api, 
  delete_category_api, 
  list_categories_api, 
  list_words_api, 
  delete_word_api
)
post_new_data = {}
post_category = []


def start_exam(message, question= None):
  """
  start an exam if flashcards were more than three
  and generates questions
  """
  if question is None:
    question = Question(words=list_words_api(message.from_user.id, *post_category))
    post_category.clear()
  if question.is_valid:
    question_word = question.generate_question()
    bot.send_message(message.chat.id, f"whats the meaning of {question_word['english']}",reply_markup=create_reply_keyboard_markup(question.options))
    bot.register_next_step_handler(message, exam_builder, question)
  else:
    bot.send_message(message.chat.id, "Flash Cards must be more than 3")
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))


def exam_builder(message,question):
  """
  Checks if still have questions continues
  and computes correct and false answers
  """
  if question.answer == message.text:
    bot.send_message(message.chat.id, "Correct ✅")
    question.correct_answers += 1
  else:
    bot.send_message(message.chat.id, "False ❌")
    question.false_answers += 1
  if len(question.qs) > 0:
    start_exam(message, question)
  else:
    bot.send_message(message.chat.id, f"Corrects {question.correct_answers}, Falses {question.false_answers}")
    bot.send_message(message.chat.id, "Test has been finished, Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))

    
def get_category(message):
  """
  creates flashcard category and word
  and gets english word in next step
  """
  post_new_data['category'] = message.text
  res = create_category_api(message.from_user.id, message.text)
  if res == "Created!":
    bot.send_message(message.chat.id, f'{message.text} Created!')
  bot.send_message(message.chat.id, f'Please Enter your Word in English: ',reply_markup=ReplyKeyboardRemove())
  bot.register_next_step_handler(message, get_english_word)


def get_english_word(message):
  """
  Gets persian word in next step
  and put english in post new data dictionary
  """
  post_new_data['english'] = message.text
  bot.send_message(message.chat.id, f'Please Enter your Word in Farsi: ')
  bot.register_next_step_handler(message, get_farsi_word)


def get_farsi_word(message):
  """
  put persian in post new data dictionary
  and creates word with api
  """
  post_new_data['persian'] = message.text
  res = create_word_api(message.from_user.id, **post_new_data)
  if res == "Created!":
    bot.send_message(message.chat.id, f'Word Created!')
  else:
    bot.send_message(message.chat.id, f'Something went wrong, try again later')
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))


def get_several_category(message):
  """
  We can select several categories
  to start a exam
  """
  if message.text == "Done":
    if post_category != []: 
      start_exam(message)
      return 0
    else:
      post_category.clear()
      bot.send_message(message.chat.id, "Please Select categories and click on 'Done' ", reply_markup= create_reply_keyboard_markup(flash_card_menu(message.from_user.id)))
      bot.register_next_step_handler(message, get_several_category)
    
  elif message.text == 'main menu':
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))
    
  else:
    post_category.append(message.text)
    bot.register_next_step_handler(message, get_several_category)



def delete_category_word(message):
  """
  Delete a word or category
  if select category bot will get category in next step
  if select word bot will get word id in next step
  """
  if message.text == "Word":
    words = list_words_api(message.from_user.id, "all categories")
    w = ""
    for word in words:
      w += f"Id: {word['id']}\nEnglish: {word['english']}\nPersian: {word['persian']}\n {'-'*20}\n"
    bot.send_message(message.chat.id, w , reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Please Enter Word Id: " , reply_markup=create_reply_keyboard_markup(['Cancel']))
    bot.register_next_step_handler(message, delete_word)
  
  if message.text == "Category":
    bot.send_message(message.chat.id,"⚠️ Attention deleting a category means deleting all the words in that category")
    bot.send_message(message.chat.id, "Select a category", reply_markup= create_reply_keyboard_markup(delete_category_menu(message.from_user.id)))
    bot.register_next_step_handler(message, delete_category)
  
  if message.text == 'main menu':
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))
    

def delete_category(message):
  """
  Delete Category by name
  """
  if message.text == 'main menu':
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))
    return 0
  category_id = [x['id'] for x in list_categories_api(message.from_user.id) if x['title'] == message.text][0]
  delete_category_api(message.from_user.id, category_id)
  bot.send_message(message.chat.id,"Category Deleted")
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))


def delete_word(message):
  """
  Delete word by selecting id
  """
  if message.text == 'Cancel':
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))
    return 0
  res = delete_word_api(message.from_user.id, message.text)
  if res == "Deleted!":
    bot.send_message(message.chat.id,"Word Deleted")
  else:
    bot.send_message(message.chat.id,"Word Not Found!")
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))


def get_or_create_category(message):
  """
  If select Create new category 
  bot will get category name in next step
  """
  if message.text == "Create new category":
    bot.send_message(message.chat.id, "Enter New category Name: ", reply_markup= ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_category)
  elif message.text == "main menu":
    bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))
  else:
    get_category(message)