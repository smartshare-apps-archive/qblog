from functools import wraps
from modules.db import *



#gives the function access to a database object; function must accept db as an argument
def db_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		instance_db = instance_handle()
		db = db_handle(instance_db)
		db_cursor = db.cursor()
		return f(db)
	return wrapper



#forces a page to require a valid session to continue
def session_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		session_manager = args[0]
		app = args[1]
		session = args[2]
		s_id = app.config['session_cookie_id']

		if session_manager.r.get(session[s_id]):
			expiration = session_manager.r.ttl(session[s_id])
			print "Session expiration in: ", expiration
			
			return f(*args, **kwargs)
		else:
			print "Opening new session first"
			session_manager.open_session(app, session)

	return wrapper


#gives a route access to session data if an authenticated session token is present (non-guests)
def with_user_data(app, session):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			data = {}
			s_id = app.config['session_cookie_id']
			session_manager = app.config['SessionManager']
			data["key"] = session[s_id]

			#if we have a session token, see if this session has any user data associated with it
			if s_id in session:
				auth_token = session_manager.get_session_key(app, session, data)

				#if the authentication token is not a guest token, it has user data associated with it
				if (auth_token != "guest"):

					data = { "table": "auth:" + session[s_id] }

					#grab the auth hash table, other session prefix will follow
					user_data = session_manager.get_session_hashTable(app, session, data)

					if user_data:
						kwargs["user_data"] = user_data
						return f(*args, **kwargs)
					else:
						return f(*args, **kwargs)

				#if there is no session established, we have no user data		
				else:
					return f(*args, **kwargs)
		return wrapper
	return decorator


#add this decorator to any route that needs admin level privleges
def admin_required(app, session, redirect):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			s_id = app.config['session_cookie_id']
			session_manager = app.config['SessionManager']

			data = {}
			data["key"] = session[s_id]
			
			auth_token = session_manager.get_session_key(app, session, data)
			print "auth token: ", auth_token

			if(auth_token and auth_token in config.admin_names()):
				return f(*args, **kwargs)
			else:
				return redirect(*args, **kwargs)

		return wrapper
	return decorator


#this is for preventing redundant login attempts, they shouldn't be able to see this page if they are logged in
def redirect_logged_in(app, session, redirect):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			s_id = app.config['session_cookie_id']
			data = {}
			data["key"] = session[s_id]

			session_manager = app.config['SessionManager']
			authenticated_token = session_manager.get_session_key(app, session, data)

			if(authenticated_token and authenticated_token != "guest"):
				return redirect(*args, **kwargs)
			else:
				return f(*args, **kwargs)
			
		return wrapper
	return decorator