import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

from modules.db import *
from modules.decorators import *
from modules import query


cms_views = Blueprint('cms_views', __name__, template_folder='templates')		#blueprint definition


@cms_views.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@cms_views.route('/view_posts')
@cms_views.route('/view_posts/')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def view_posts(user_data=None):
	ctl = current_app.config['ctl']
	data = {}
	data["ts"] = int(time.time())
	
	data["page_specific_js"] = ["/static/js/Requests.js", "/static/js/PostManager.js" ]

	if user_data:
		data["user_data"] = user_data

	db_wrapper = database_wrapper()
	posts = query.getAllPosts(db_wrapper.content)

	if posts:
		data["posts"] = posts

	return render_template("/view_posts.html", data = data)



@cms_views.route('/edit/<int:post_id>')
@cms_views.route('/edit/<int:post_id>/')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def edit_post(post_id, user_data=None):
	ctl = current_app.config['ctl']
	data = {}
	data["ts"] = int(time.time())
	data["post_data"] = ctl.get_post_content(post_id)
	
	data["page_specific_js"] = [ "/static/js/Requests.js", "/static/js/PostEditor.js" ]

	if user_data:
		data["user_data"] = user_data

	return render_template("/post_editor.html", data = data)




@cms_views.route('/settings/')
@cms_views.route('/settings')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def settings(user_data=None):
	ctl = current_app.config['ctl']
	db_wrapper = database_wrapper()

	data = {}
	data["ts"] = int(time.time())

	data["database_settings"]  = db_wrapper.getDatabaseSettings(db_wrapper.config)
	data["redis_settings"]  = db_wrapper.getRedisSettings(db_wrapper.config)
	
	data["page_specific_js"] = [ "/static/js/Requests.js", "/static/js/Settings.js" ]

	if user_data:
		data["user_data"] = user_data

	return render_template("/settings.html", data = data)





@cms_views.route('/savePost/', methods = ['POST'])
@cms_views.route('/savePost', methods = ['POST'])
#@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_post(user_data=None):
	ctl = current_app.config['ctl']

	postData = request.form['postData']
	postData = json.loads(postData)
	
	r = query.savePost(ctl.content, postData)

	if r:
		ctl.content.commit()

	return json.dumps(r)



@cms_views.route('/createPost/', methods = ['POST'])
@cms_views.route('/createPost', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def create_post(user_data=None):
	ctl = current_app.config['ctl']

	postData = request.form['postData']
	postData = json.loads(postData)
	
	post_id = query.createPost(ctl.content, postData)

	if post_id:
		ctl.content.commit()

	return json.dumps(post_id)




@cms_views.route('/deletePost/', methods = ['POST'])
@cms_views.route('/deletePost', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def delete_post(user_data=None):
	ctl = current_app.config['ctl']

	postData = request.form['postData']
	postData = json.loads(postData)
	
	r = query.deletePost(ctl.content, postData)

	if r:
		ctl.content.commit()

	return json.dumps(r)






@cms_views.route('/saveRedisConfig/', methods = ['POST'])
@cms_views.route('/saveRedisConfig', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_redis_config(user_data=None):
	ctl = current_app.config['ctl']
	db_wrapper = database_wrapper()

	redisConfig = request.form['redisConfig']
	redisConfig = json.loads(redisConfig)
	
	r = db_wrapper.saveRedisConfig(db_wrapper.config, redisConfig)

	if r:
		db_wrapper.config.commit()

	return json.dumps(r)




@cms_views.route('/saveDatabaseConfig/', methods = ['POST'])
@cms_views.route('/saveDatabaseConfig', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_database_config(user_data=None):
	ctl = current_app.config['ctl']
	db_wrapper = database_wrapper()

	databaseConfig = request.form['databaseConfig']
	databaseConfig = json.loads(databaseConfig)
	
	r = db_wrapper.saveDatabaseConfig(db_wrapper.config, databaseConfig)

	if r:
		db_wrapper.config.commit()

	return json.dumps(r)