import logging
import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

import modules


updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
dp = updater.dispatcher

conv_handler = ConversationHandler(
        entry_points=[CommandHandler(['start'], modules.start_command, pass_args=True)],

        states={
            modules.LANG: [CallbackQueryHandler(modules.lang_command)],
            modules.TIME_ZONE: [MessageHandler(Filters.text, modules.time_zone_handler, pass_user_data=True)],
            modules.MENU: [MessageHandler(Filters.text, modules.menu_handler, pass_user_data=True)],
            modules.ADD_EVENT: [MessageHandler(Filters.text, modules.add_event_handler, pass_user_data=True)]
        },

        fallbacks=[CommandHandler(['cancel'], modules.cancel_command)]
    )

dp.add_handler(conv_handler)

updater.start_polling()
