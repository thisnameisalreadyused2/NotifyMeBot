def start_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm notifier bot!")