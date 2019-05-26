from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from localization import languages
from utils.message_parser import parser

from ._regular_reminder import reminder_handler

import datetime

from DB import Database
db = Database("db")

user_lang = ""

LANG, TIME_ZONE, MENU, CHOOSE_EVENT, ADD_EVENT = range(5)

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

    db.add_user(update.effective_message.chat_id, int(input_text), user_lang)

    keyboard = [[languages[user_lang]["menu_add_events"],
                 languages[user_lang]["menu_show_events"]],
                [languages[user_lang]["menu_settings"]]]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)

    context.bot.send_message(chat_id=update.effective_message.chat_id,
                             text=languages[user_lang]["description"],
                             parse_mode="Markdown",
                             reply_markup=reply_markup)

    return MENU

def menu_handler(update, context):
    if update.message.text == languages[user_lang]["menu_add_events"]:
        context.bot.send_message(update.effective_chat.id, languages[user_lang]["enter_event_text"])
        return ADD_EVENT

    elif update.message.text == languages[user_lang]["menu_show_events"]:
        all_user_events = db.get_all_events_for_user(update.message.from_user.id)

        counter = 1
        result = ""
        for user_event in all_user_events:
            result += "*№{}*\n*Date:* {}\n*Name:* {}\n*Type:* {}\n\n"\
                .format(str(counter),
                        str(datetime.datetime.utcfromtimestamp(user_event[0]).strftime("%d.%m.%Y %H:%M")),
                        str(user_event[1]),
                        str(user_event[2]))
            counter += 1
        context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode="Markdown")


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

def add_event_handler(update, context):
    event_text = parser(update.message.text)
    #context.bot.send_message(chat_id=update.effective_chat.id, text=event_text)
    reminder_handler(update.effective_chat.id, event_text)
    context.bot.send_message(chat_id=update.message.chat_id, text=languages[user_lang]["added_successfully"])

    return MENU

def cancel_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="bye",
                             reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
