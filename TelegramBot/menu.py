from telebot.types import (
  KeyboardButton,
  ReplyKeyboardMarkup,
  InlineKeyboardMarkup,
  InlineKeyboardButton
)

from apis import (
  list_categories_api,
)


main_menu = [
  "Lunch FlashCard Exam 🧾",
  "Create FlashCard 🔨",
  "Delete FlashCard 🗑️",
  "About 🧑🏻‍💻",
  "Help 🆘",
]

def flash_card_menu(telegram_id):
  """
  Menu for lunch an exam
  """
  categories = [categories['title'] for categories in list_categories_api(telegram_id)]
  if categories != []:
    return categories +\
      [
        "all categories",
        "Done",
        "main menu"
      ]
  else:
    return ["main menu"]

def flash_card_category_menu(telegram_id):
  """
  Menu for create a flash card
  """
  return  [categories['title'] for categories in list_categories_api(telegram_id)] +\
    [
      "Create new category",
      "main menu"
    ]

def delete_category_menu(telegram_id):
  """
  Menu for delete a category
  """
  categories = [categories['title'] for categories in list_categories_api(telegram_id)]
  if categories != []:
    return categories +\
      [
        "main menu"
      ]


## bot menu tools

def create_reply_keyboard_markup(menu):
  reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
  rk_menu = []
  for t in menu:
    rk_menu.append(
      KeyboardButton(t)
    )
  reply_keyboard.add(*rk_menu)
  return reply_keyboard


def create_inline_keyboard_markup(options):
  inline_keyboard = InlineKeyboardMarkup(row_width=4)
  question_options = []
  for option in options:
    question_options.append(InlineKeyboardButton(option, callback_data=options))
  inline_keyboard.add(*question_options)
  return inline_keyboard
