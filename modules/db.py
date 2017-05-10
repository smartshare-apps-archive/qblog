import sqlite3
import MySQLdb

from contextlib import closing

INSTANCE_DB = "modules/config.db"


import query


class database_wrapper(object):

	def __init__(self):
		self.config = database_wrapper.config_db()
		self.content = database_wrapper.content_db(self.config)


	@classmethod
	def config_db(cls):	
		try:
			conn=sqlite3.connect(INSTANCE_DB)
			conn.text_factory = str
			
		except Exception as e:
			print "Error opening instance database: ", e
			return None
		
		return conn



	@classmethod
	def content_db(self, config_db):
		db_settings = database_wrapper.getDatabaseSettings(config_db)
		try:
			conn=MySQLdb.connect(host=db_settings["host"],port=int(db_settings["port"]),user=db_settings["username"],passwd=db_settings["password"], db=db_settings["default_db"], use_unicode=True, charset="utf8", connect_timeout=1)
		except Exception as e:
			print "Exception connecting: ", e
			return None

		return conn




	@classmethod
	def getDatabaseSettings(cls, config_db):

		formattedDatabaseConfig = {}

		with closing(config_db.cursor()) as cursor:
			currentQuery = """SELECT FieldList FROM settings WHERE setting_id="DatabaseConfig";"""

			try:
				cursor.execute(currentQuery)
			except Exception as e:
				print "Error: ", e
				return None

			databaseConfig = cursor.fetchone()

			if databaseConfig:
				databaseConfig = [field.split('=') for field in  filter(lambda i: i != '', databaseConfig[0].split('<database_split>'))]
				

				for field in databaseConfig:
					formattedDatabaseConfig[field[0]] = field[1]

		return formattedDatabaseConfig




	@classmethod
	def getRedisSettings(cls, config_db):

		formattedDatabaseConfig = {}

		with closing(config_db.cursor()) as cursor:
			currentQuery = """SELECT FieldList FROM settings WHERE setting_id="RedisConfig";"""

			try:
				cursor.execute(currentQuery)
			except Exception as e:
				print "Error: ", e
				return None

			databaseConfig = cursor.fetchone()

			if databaseConfig:
				databaseConfig = [field.split('=') for field in  filter(lambda i: i != '', databaseConfig[0].split('<redis_split>'))]
				

				for field in databaseConfig:
					formattedDatabaseConfig[field[0]] = field[1]

		return formattedDatabaseConfig



	@classmethod
	def saveRedisConfig(cls, config_db, redisConfig):
		formatted_redis_config = ""

		for field, value in redisConfig.iteritems():
			formatted_redis_config += field + "=" + value + "<redis_split>"


		with closing(config_db.cursor()) as cursor:
			currentQuery = """UPDATE settings SET FieldList=? WHERE setting_id="RedisConfig";"""

			try:
				cursor.execute(currentQuery, (formatted_redis_config, ))
			except Exception as e:
				print "Error: ", e
				return False
		return True



	@classmethod
	def saveDatabaseConfig(cls, config_db, databaseConfig):
		formatted_database_config = ""

		for field, value in databaseConfig.iteritems():
			formatted_database_config += field + "=" + value + "<database_split>"


		with closing(config_db.cursor()) as cursor:
			currentQuery = """UPDATE settings SET FieldList=? WHERE setting_id="DatabaseConfig";"""

			try:
				cursor.execute(currentQuery, (formatted_database_config, ))
			except Exception as e:
				print "Error: ", e
				return False

		return True



	def auth_user(self, login_info):
		
		userData = None
		
		with closing(self.content.cursor()) as cursor:
			currentQuery = "SELECT user_id, username, access_level  FROM users WHERE username=%s AND password=%s;"

			try:
				cursor.execute(currentQuery, (login_info["username"], login_info["password"],))
			except Exception as e:
				print "Error: ", e
				return None

			userData = cursor.fetchone()
			
		if userData:
			formattedUserData = {}
			formattedUserData["user_id"] = userData[0]
			formattedUserData["username"] = userData[1]
			formattedUserData["access_level"] = userData[2]
			print "User data: ", userData
			return formattedUserData


