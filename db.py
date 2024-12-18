import sqlite3
import const
import datetime

class DatabaseHandler:
	def __init__(self):
		"""Initializes the connection to the database."""
		self.db_path = const.DB_PATH
		self.conn = None
	
	def connect(self):
		"""Creates a connection to the database."""
		if self.conn is None:
			# check_same_thread is not safe for concurrency; anyway we like risking
			self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
	
	def close(self):
		"""Closes the connection to the database."""
		if self.conn:
			self.conn.close()
			self.conn = None
	
	def get_users_list(self):
		"""Returns the list of user IDs."""
		self.connect()
		cursor = self.conn.cursor()
		try:
			cursor.execute("SELECT id FROM users")
			return [row[0] for row in cursor.fetchall()]
		except sqlite3.Error as e:
			return []
	
	def get_targets_list(self):
		"""Returns a list of objects with properties 'addr' (for address) and 'api_ver'."""
		self.connect()
		cursor = self.conn.cursor()
		try:
			cursor.execute("SELECT address, api_ver FROM targets")
			rows = cursor.fetchall()
			return [{"addr": row[0], "api_ver": row[1]} for row in rows]
		except sqlite3.Error as e:
			return []

	
	def add_log(self, user_id, user_full_info, content):
		"""Adds a log to the 'logs' table."""
		self.connect()
		cursor = self.conn.cursor()
		try:
			timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			cursor.execute(
				"INSERT INTO logs (user_id, timestamp, content, user_full_info) VALUES (?, ?, ?, ?)",
				(user_id, timestamp, content, user_full_info)
			)
			self.conn.commit()
		except sqlite3.Error as e:
			return False
