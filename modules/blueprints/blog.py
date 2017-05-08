import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

from modules.db import *


blog_views = Blueprint('blog_views', __name__, template_folder='templates')		#blueprint definition



@blog_views.before_request
def setup_session():
	pass
	#sm = current_app.config['SessionManager']
	#s_id = current_app.config['session_cookie_id']

	#if s_id not in session:
	#	sm.open_session(current_app, session)
	#	print "Created: ", session[s_id]



@blog_views.route('/index')
@blog_views.route('/')
#@admin_required(current_app, session, login_redirect)
def index():
	ctl = current_app.config['ctl']
	timeline = ctl.timeline()
	
	data = {}
	data["ts"] = int(time.time())

	return render_template("/index.html", data=data, timeline=timeline)

