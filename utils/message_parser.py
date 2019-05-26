import time
import datetime


def parser(msg_text):
    splatted_msg = msg_text.split()
    try:
        unitxtime = time.mktime(datetime.datetime.strptime(f"{splatted_msg[0]} {splatted_msg[1]}", "%d.%m.%Y %H:%M").timetuple())
        type = splatted_msg[2]
        name = " ".join(splatted_msg[3:])
    except ValueError:
        unitxtime = time.mktime(datetime.datetime.strptime(splatted_msg[0], "%d.%m.%Y").timetuple())
        type = splatted_msg[1]
        name = " ".join(splatted_msg[2:])

    return unitxtime, type, name
