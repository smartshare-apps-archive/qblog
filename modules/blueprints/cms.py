import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

from modules.db import *
from modules import query

cms_views = Blueprint('cms_views', __name__, template_folder='templates')		#blueprint definition



@cms_views.before_request
def setup_session():
	pass
	#sm = current_app.config['SessionManager']
	#s_id = current_app.config['session_cookie_id']

	#if s_id not in session:
	#	sm.open_session(current_app, session)
	#	print "Created: ", session[s_id]



@cms_views.route('/view_posts')
@cms_views.route('/view_posts/')
#@admin_required(current_app, session, login_redirect)
def view_posts():
	ctl = current_app.config['ctl']
	data = {}
	data["ts"] = int(time.time())
	
	
	data["page_specific_js"] = ["/static/js/Requests.js", "/static/js/PostManager.js" ]

	return render_template("/view_posts.html", data = data)



@cms_views.route('/edit/<int:post_id>')
@cms_views.route('/edit/<int:post_id>/')
#@admin_required(current_app, session, login_redirect)
def edit_post(post_id):
	ctl = current_app.config['ctl']
	data = {}
	data["ts"] = int(time.time())
	data["post_data"] = ctl.get_post_content(post_id)
	
	data["page_specific_js"] = [ "/static/js/Requests.js", "/static/js/PostEditor.js" ]

	return render_template("/post_editor.html", data = data)




@cms_views.route('/savePost/', methods = ['POST'])
@cms_views.route('/savePost', methods = ['POST'])
#@admin_required(current_app, session, login_redirect)
def save_post():
	ctl = current_app.config['ctl']

	postData = request.form['postData']
	postData = json.loads(postData)
	
	r = query.savePost(ctl.content, postData)

	if r:
		ctl.content.commit()

	return json.dumps(r)



@cms_views.route('/createPost/', methods = ['POST'])
@cms_views.route('/createPost', methods = ['POST'])
#@admin_required(current_app, session, login_redirect)
def create_post():
	ctl = current_app.config['ctl']

	postData = request.form['postData']
	postData = json.loads(postData)
	
	r = query.createPost(ctl.content, postData)

	if r:
		ctl.content.commit()

	return json.dumps(r)
