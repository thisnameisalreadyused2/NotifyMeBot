import time, datetime
from threading import Thread

from DB import Database
db = Database("db")


def format_str(type, timestamp):
    format_str = "%d.%m.%Y" if type == "birthday" else "%d.%m.%Y %H:%M"
    return datetime.datetime.utcfromtimestamp(timestamp).strftime(format_str)


class MyThread(Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        while True:
            reminds_list = db.get_reminders_for_time(datetime.datetime.now().timestamp())
            for item in reminds_list:
                user_id,date,name,type = item
                msg = f"New notification!\n"
                if type == "birthday":
                    birthday_date = db.get_birthday_date(user_id, name)
                    msg += f"Birthday of "
                msg += f"*{name}* at {format_str(type, date)}"
                self.bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown")
            time.sleep(60)
