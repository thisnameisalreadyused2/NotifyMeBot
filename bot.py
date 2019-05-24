import logging
import os

from telegram.ext import Updater, CommandHandler

import modules


updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler(['start'], modules.start_command, pass_args=True))

updater.start_polling()
