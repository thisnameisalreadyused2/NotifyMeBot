from DB import Database

db = Database("db")

MENU = range(1)

def reminder_handler(user_id, obj):
    date, type, name = obj
    db.add_event(user_id, date, "birthday" if type == "Birthday" else "regular", name)

    if type == "Birthday":
        db.add_reminder(user_id, date - 7 * 24 * 60 * 60, "birthday" if type == "Birthday" else "regular", name)
        db.add_reminder(user_id, date - 3 * 24 * 60 * 60, "birthday" if type == "Birthday" else "regular", name)
        db.add_reminder(user_id, date - 1 * 24 * 60 * 60, "birthday" if type == "Birthday" else "regular", name)
    db.add_reminder(user_id, date, "birthday" if type == "Birthday" else "regular", name)
