from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from localization import languages

from DB import Database
db = Database("db")

user_lang = ""

LANG, TIME_ZONE, MENU, SETTINGS, APPLY_SETTINGS = range(5)

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

    query.edit_message_text(text=languages[user_lang]["write_time_zone"], parse_mode="Markdown")

    return TIME_ZONE

def time_zone_handler(update, context):
    input_text = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=languages[user_lang]["time_zone"] + str(input_text) + ".")

    db.add_user(update.message.from_user.id, int(input_text), user_lang)

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
        keyboard = [[InlineKeyboardButton(languages[user_lang]["birthday_info"], callback_data="birthday_info"),
                     InlineKeyboardButton(languages[user_lang]["birthday_settings"], callback_data="birthday_settings")],
                    [InlineKeyboardButton(languages[user_lang]["common_info"], callback_data="common_info"),
                     InlineKeyboardButton(languages[user_lang]["common_settings"], callback_data="common_settings")],
                    [InlineKeyboardButton(languages[user_lang]["facebook_info"], callback_data="facebook_info"),
                     InlineKeyboardButton(languages[user_lang]["facebook_settings"], callback_data="facebook_settings")],
                    [InlineKeyboardButton(languages[user_lang]["language_change"], callback_data="language_change")],
                    [InlineKeyboardButton(languages[user_lang]["time_zone_change"], callback_data="time_zone_change")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=languages[user_lang]["settings_info"],
                                 reply_markup=reply_markup)

    return MENU

def cancel_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="bye",
                             reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END