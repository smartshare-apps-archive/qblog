import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Response
from uuid import uuid4

#ecomm module imports
from modules.db import *


login_routes = Blueprint('login_routes', __name__, template_folder='templates')		#blueprint definition


#this method creates a session for the store visitor before any request occurs
@login_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@login_routes.route('/login')
@login_routes.route('/login/')
@redirect_logged_in(current_app, session, Home)
@with_user_data(current_app, session)
def login_redirect(product_id = None, collection_id = None):
	ctl = current_app.config["auth_ctl"]
	store_ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)


	return render_template("auth/login.html", data=data)




@login_routes.route('/auth/login', methods=['POST'])
@db_required
def auth_login(db):
	login_info = request.form['login_info']
	login_info = json.loads(login_info)
	
	user_data = auth_user(login_info, db)
	
	if user_data:
		sm = current_app.config['SessionManager']
		set_session_data(sm, current_app, session, user_data);
		return json.dumps(user_data)
	else:
		return json.dumps("invalid")



@login_routes.route('/auth/logout')
@db_required
def logout(db):
	sm = current_app.config['SessionManager']
	destroy_session_data(sm, current_app, session);

	db.close()

	return Home()
	


def destroy_session_data(session_manager, app, session):
	s_id = current_app.config['session_cookie_id']

	data = {}
	data['key'] = session[s_id]
	
	val = session_manager.get_session_key(app, session, data)

	if val and val != "guest":
		#delete all session data associated with this user from the redis table
		for prefix in sessionPrefixList:
			data["table"] = prefix + session[s_id]
			result = session_manager.delete_session_hashTable(app, session, data)

		#preserve distinct login to a session
		data["key"] = session[s_id]
		data["value"] = "guest"

		session_manager.update_session_key(app, session, data)

	if result:
		return result
	else:
		return None




def set_session_data(session_manager, app, session, user_data):
	s_id = current_app.config['session_cookie_id']

	data = {}
	data['key'] = session[s_id]
	
	val = session_manager.get_session_key(app, session, data)

	if val:
		prefix = "auth:"
		data["table"] = prefix + session[s_id]

		for key, value in user_data.iteritems():
			if type(value) is type(None):
				continue

			data["key"] = key
			data["value"] = value
			
			session_manager.set_session_hashKey(app, session, data)


		#preserve distinct login to a session
		data["key"] = session[s_id]
		data["value"] = user_data["username"]
		
		session_manager.update_session_key(app, session, data)