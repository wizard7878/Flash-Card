from menu import (
  create_reply_keyboard_markup,
  flash_card_category_menu,
  main_menu, 
  flash_card_menu
)
from config import bot

from callbacks import (
  get_several_category,
  delete_category_word,
  get_or_create_category
)

from apis import create_user_api



@bot.message_handler(commands =['start'])
def welcome(message):
  """
  Welcome message after users command start
  and shows main menu
  """
  create_user_api(message.from_user.id, message.chat.username)
  bot.send_message(message.chat.id, f"Welcome dear {message.chat.username}")
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))



@bot.message_handler(func= lambda message: message.text == 'main menu')
def menu(message):
  """
  Returns main menu to run another Feature
  """
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(main_menu))


@bot.message_handler(func= lambda message: message.text == 'About 🧑🏻‍💻')
def about(message):
  """
  This bot has been made by Peyman Shomalzadeh
  """
  bot.send_message(message.chat.id, "Made by Peyman Shomalzadeh")


@bot.message_handler(func=lambda message: message.text == "Lunch FlashCard Exam 🧾")
def message_handler(message):
  """
  Lunch an exam with selected categories
  """
  bot.send_message(message.chat.id, "Please Select categories and click on 'Done' ", reply_markup= create_reply_keyboard_markup(flash_card_menu(message.from_user.id)))
  bot.register_next_step_handler(message, get_several_category)


@bot.message_handler(func= lambda message: message.text == 'Create FlashCard 🔨')
def build_new_flash_card(message):
  """
  Create FlashCard you can build a category and put the words in them
  """
  bot.send_message(message.chat.id, "Select menu..", reply_markup= create_reply_keyboard_markup(flash_card_category_menu(message.from_user.id)))
  bot.register_next_step_handler(message, get_or_create_category)
  

@bot.message_handler(func= lambda message: message.text == "Delete FlashCard 🗑️")
def delete_flashCard(message):
  """
  Delete Category or a word
  """
  bot.send_message(message.chat.id, "Which one do you want to delete? ", reply_markup=create_reply_keyboard_markup(["Category", "Word", "main menu"]))
  bot.register_next_step_handler(message, delete_category_word)
  
bot.infinity_polling()

