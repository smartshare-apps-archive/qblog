# a basic cart object implementing redis

import json, time

from flask import Blueprint, render_template, current_app, session, request
from uuid import uuid4
import redis


#ecomm module imports
from modules.db import *
from modules.decorators import *

db_wrapper = database_wrapper()

redis_config = db_wrapper.getRedisSettings(db_wrapper.config)


REDIS_SERVER = redis_config["host"]
REDIS_PORT = int(redis_config["port"])
REDIS_PASSWORD = redis_config["password"]


SESSION_DURATION = 3000


class SessionManager(object):
	def __init__(self):
		self.r = redis.StrictRedis(host=REDIS_SERVER,port=REDIS_PORT, password=REDIS_PASSWORD)
		try:
			client_name = self.r.client_list()
		except redis.exceptions.ConnectionError as e:
			self.r = None

		
	def open_session(self, app, session):
		auth_id = app.config['session_cookie_id']
			
		if auth_id not in session:
			new_UUID = str(uuid4())
			session[auth_id] = new_UUID
			
			return self.r.setex(new_UUID, int(SESSION_DURATION), "guest")

		else:
			return self.r.setex(session[auth_id], int(SESSION_DURATION), "guest")

				


	#redis calls 


	@session_required
	def get_session_keys(self, app, session):
		all_keys = self.r.keys('*')
		for idx, key in enumerate(all_keys):
			#print idx,":", key
			pass
		return all_keys


	@session_required
	def update_session_key(self, app, session, data):
		return self.r.setex(data['key'], int(SESSION_DURATION), data['value'])


	@session_required
	def get_session_key(self, app, session, data):
		return self.r.get(data['key'])


	@session_required
	def set_session_hashKey(self, app, session, data):
		return self.r.hset(data['table'], data['key'], data['value'])


	@session_required
	def delete_session_hashKey(self, app, session, data):
		return self.r.hdel(data['table'], data['key'])

	@session_required
	def delete_session_hashTable(self, app, session, data):
		return self.r.delete(data['table'])

	@session_required
	def get_session_hashTable(self, app, session, data):
		return self.r.hgetall(data['table'])


	@session_required
	def get_session_list(self, app, session, data):
		result = self.r.lrange(data['key'],0,-1)
		return result


	@session_required
	def append_session_list(self, app, session, data):
		result = self.r.lpush(data['key'], data['value'])
