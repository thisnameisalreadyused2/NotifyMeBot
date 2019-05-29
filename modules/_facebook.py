import os
import re

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = [[InlineKeyboardButton("I will come", callback_data="come"),
                 InlineKeyboardButton("Remind", callback_data="remind"),
                 InlineKeyboardButton("Not interested", callback_data="not_interested")]]


def get_event_info(event_id):
    r = requests.get(f"https://graph.facebook.com/v3.3/{event_id}?access_token={os.environ['FACEBOOK_TOKEN']}").json()
    place = r['place']
    return {"event_name": r['name'],
     "loction_name": place['name'],
     "adress": f"{place['location']['country'], place['location']['City'], place['location']['street'], place['location']['zip']}",
     "lat": place['location']['latitude'],
     "lon": place['location']['longitude'],
     "start_time": r['start_time']
     }

def facebook_handler(update, context):
    event_id = re.match(r"https?://www.facebook\.com/events/(\d+)/?", update.message.text)[0]
    event_info = get_event_info(event_id)
    msg = f"*{event_info[event_name]}*\n" \
        f"Location: {event_info['adress']}" \
        f"Start time: {event_info['start_time']}"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             reply_markup=reply_markup,
                             parse_mode="Markdown")