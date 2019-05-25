from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from localization import languages

user_lang = ""

LANG, TIME_ZONE, MENU = range(3)

def start_command(update, context):
    keyboard = [[InlineKeyboardButton("EN 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="en"),
                 InlineKeyboardButton("UA 🇺🇦", callback_data="ua"),
                 InlineKeyboardButton("RU 🇷🇺", callback_data="ru")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=languages[update.message.from_user.language_code]["hello"],
                             reply_markup=reply_markup)

    return LANG

def lang_command(update, context):
    global user_lang

    query = update.callback_query
    user_lang = query.data

    query.edit_message_text(text=languages[user_lang]["write_time_zone"])

    return TIME_ZONE

def time_zone_handler(update, context):
    input_text = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=languages[user_lang]["time_zone"] + str(input_text) + ".")

    keyboard = [[languages[user_lang]["menu_events"],
                 languages[user_lang]["menu_settings"]]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)

    context.bot.send_message(chat_id=update.effective_message.chat_id,
                             text=languages[user_lang]["description"],
                             parse_mode="Markdown",
                             reply_markup=reply_markup)

    return MENU

def menu_handler(update, context):
    if update.message.text == languages[user_lang]["menu_events"]:
        pass
    elif update.message.text == languages[user_lang]["menu_settings"]:
        pass

    return ConversationHandler.END

def cancel_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="1",
                             reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END