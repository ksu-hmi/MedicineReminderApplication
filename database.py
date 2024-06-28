import sqlite3
from typing import List, Tuple


class ReminderDatabase:
    def __init__(self, db_name: str = 'reminders.db'):
        """
        Initialize the ReminderDatabase.

        Args:
            db_name (str): Name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.create_connection()
        self.create_table()

    def create_connection(self) -> None:
        """Create a database connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_table(self) -> None:
        """Create the reminders table if it doesn't exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY,
            med_name TEXT NOT NULL,
            interval INTEGER NOT NULL
        )
        '''
        try:
            with self.conn:
                self.conn.execute(query)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise

    def add_reminder(self, med_name: str, interval: int) -> None:
        """
        Add a new reminder to the database.

        Args:
            med_name (str): Name of the medication.
            interval (int): Reminder interval in minutes.
        """
        query = '''
        INSERT INTO reminders (med_name, interval)
        VALUES (?, ?)
        '''
        try:
            with self.conn:
                self.conn.execute(query, (med_name, interval))
        except sqlite3.Error as e:
            print(f"Error adding reminder: {e}")
            raise

    def get_reminders(self) -> List[Tuple[int, str, int]]:
        """
        Retrieve all reminders from the database.

        Returns:
            List[Tuple[int, str, int]]: List of reminders (id, med_name, interval).
        """
        query = 'SELECT * FROM reminders'
        try:
            with self.conn:
                cursor = self.conn.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving reminders: {e}")
            return []

    def delete_reminder(self, reminder_id: int) -> None:
        """
        Delete a reminder from the database.

        Args:
            reminder_id (int): ID of the reminder to delete.
        """
        query = 'DELETE FROM reminders WHERE id = ?'
        try:
            with self.conn:
                self.conn.execute(query, (reminder_id,))
        except sqlite3.Error as e:
            print(f"Error deleting reminder: {e}")
            raise

    def update_reminder(self, reminder_id: int, med_name: str, interval: int) -> None:
        """
        Update an existing reminder in the database.

        Args:
            reminder_id (int): ID of the reminder to update.
            med_name (str): New name of the medication.
            interval (int): New reminder interval in minutes.
        """
        query = '''
        UPDATE reminders
        SET med_name = ?, interval = ?
        WHERE id = ?
        '''
        try:
            with self.conn:
                self.conn.execute(query, (med_name, interval, reminder_id))
        except sqlite3.Error as e:
            print(f"Error updating reminder: {e}")
            raise

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        if self.conn:
            self.conn.close()
