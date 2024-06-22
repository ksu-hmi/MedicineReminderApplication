import sqlite3

class ReminderDatabase:
    def __init__(self, db_name='reminders.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY,
            med_name TEXT NOT NULL,
            interval INTEGER NOT NULL
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_reminder(self, med_name, interval):
        query = '''
        INSERT INTO reminders (med_name, interval)
        VALUES (?, ?)
        '''
        self.conn.execute(query, (med_name, interval))
        self.conn.commit()

    def get_reminders(self):
        query = '''
        SELECT * FROM reminders
        '''
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_reminder(self, reminder_id):
        query = '''
        DELETE FROM reminders WHERE id = ?
        '''
        self.conn.execute(query, (reminder_id,))
        self.conn.commit()

    def update_reminder(self, reminder_id, med_name, interval):
        query = '''
        UPDATE reminders
        SET med_name = ?, interval = ?
        WHERE id = ?
        '''
        self.conn.execute(query, (med_name, interval, reminder_id))
        self.conn.commit()
