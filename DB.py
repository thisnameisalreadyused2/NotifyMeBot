import sqlite3

#conn = sqlite3.connect("db")
#cursor = conn.cursor()

class Database:
    def __init__(self, name=None):

        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):

        try:
            self.conn = sqlite3.connect(name, check_same_thread=False)
            self.cursor = self.conn.cursor()

        except sqlite3.Error:
            print("Error connecting to database!")

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()

    def add_user(self, id, timezone, language):
        query = f"INSERT OR IGNORE INTO users (id, timezone, language) VALUES ({id}, {timezone}, '{language}')"
        self.cursor.executescript(query)
        self.conn.commit()

    def add_event(self, user_id, date, type, name):
        query = f"INSERT INTO events (user_id, date, type, name) VALUES ({user_id}, {date}, '{type}', '{name}')"
        self.cursor.executescript(query)
        self.conn.commit()

    def add_reminder(self, user_id, date, type, name):
        query = f"INSERT INTO reminders (user_id, date, type, name) VALUES ({user_id}, {date}, '{type}', '{name}')"
        self.cursor.executescript(query)
        self.conn.commit()

    def get_events_for_user_by_type(self, user_id, type):
        query = f"SELECT date,name FROM events WHERE user_id = {user_id} AND type = '{type}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_events_for_user(self, user_id):
        query = f"SELECT date,name,type FROM events WHERE user_id = {user_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_reminders_for_time(self, time):
        query = f"SELECT user_id,date,name,type FROM reminders WHERE date >= {time-60} AND date <= {time}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_reminders_for_user(self, user_id):
        query = f"SELECT date,name,type FROM reminders WHERE user_id = {user_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_language(self, user_id):
        query = f"SELECT language FROM users WHERE user_id = {user_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_birthday_date(self, user_id, name):
        query = f"SELECT date FROM events WHERE user_id = {user_id} AND name = '{name}' AND type = 'birthday'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def query(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
