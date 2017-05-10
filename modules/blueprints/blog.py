import json, time, markdown

from flask import Blueprint, render_template, abort, current_app, session, request, Markup, redirect, url_for

from modules.db import *
from modules.decorators import *



blog_views = Blueprint('blog_views', __name__, template_folder='templates')		#blueprint definition



@blog_views.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@blog_views.route('/index')
@blog_views.route('/')
@with_user_data(current_app, session)
def index(user_data=None):
	ctl = current_app.config['ctl']
	timeline = ctl.timeline()
	
	data = {}
	data["ts"] = int(time.time())

	if user_data:
		data["user_data"] = user_data

	return render_template("/index.html", data=data, timeline=timeline)






@blog_views.route('/post/<int:post_id>')
@blog_views.route('/post/<int:post_id>/')
@with_user_data(current_app, session)
def view_post(post_id, user_data=None):
	ctl = current_app.config['ctl']
	
	data = {}
	data["ts"] = int(time.time())

	if user_data:
		data["user_data"] = user_data

	post_data = ctl.get_post_content(post_id)

	if post_data:
		data["post_data"] = post_data

		post_content = post_data.get("post_content", None)
		post_tags = post_data.get("post_tags", None)
		
		if post_content:
			post_content = post_content.replace('<br />', '\n')
			data["post_data"]["post_content"] = markdown.markdown(post_content, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.nl2br'])
		else:
			data["post_data"]["post_content"] = ""


		if post_tags:
			post_tags = filter(lambda t: t != "", post_tags.split(','))
			data["post_data"]["post_tags"] = post_tags
		else:
			data["post_data"]["post_tags"] = None
		
	else:
		return redirect(url_for('blog_views.index'))


	return render_template("/post.html", data=data)

