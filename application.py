from __future__ import print_function 
import os, sys, re, requests, time, json

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, url_for, abort, request, Response, make_response, g, current_app, session

from modules.control_panel import BlogCMS


from modules.blueprints import cms
from modules.blueprints import blog



#authentication and session management modules
from modules.auth import login
from modules.auth import session_manager



application = Flask(__name__)

#generate a random secret key
application.secret_key = os.urandom(24)

application.config['ctl'] = BlogCMS()		#this instance of ControlPanel can be accessed through the application context so blueprints can use it
application.config['auth_ctl'] = Auth()		#

assert application.config['SessionManager'].r is not None, "Can't connect to redis server."


application.register_blueprint(cms.cms_views)
application.register_blueprint(blog.blog_views)



#only for debugging, makes sure to check all the js files and templates for changes
def debug_dirUpdate():
	extra_dirs = ['templates/','static/js/']
	extra_files = extra_dirs[:]

	for extra_dir in extra_dirs:
	    for dirname, dirs, files in os.walk(extra_dir):
	        for filename in files:
	            filename = os.path.join(dirname, filename)
	            if os.path.isfile(filename):
	                extra_files.append(filename)

	return extra_files






if __name__ == "__main__":
	extra_files = debug_dirUpdate()

	#live_host = "0.0.0.0"
	live_host = "127.0.0.1"

	application.run(host = live_host, debug=True, extra_files=extra_files, threaded=True)