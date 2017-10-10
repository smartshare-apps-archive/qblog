from __future__ import print_function 
import os, sys, re, requests, time, json

from werkzeug.contrib.fixers import ProxyFix

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, url_for, abort, request, Response, make_response, g, current_app, session

from modules.control_panel import BlogCMS

from modules.db import *
from modules import query

from modules.blueprints import cms
from modules.blueprints import blog
from modules.blueprints import login


#authentication and session management modules
from modules.auth import session_manager


application = Flask(__name__)


#generate a random secret key
application.secret_key = os.urandom(24)

application.config['ctl'] = BlogCMS()       #this instance of ControlPanel can be accessed through the application context so blueprints can use it
application.config['session_cookie_id'] = "sess_id"
application.config['SessionManager'] = session_manager.SessionManager()
application.config['GOOGLE_API_KEY'] = 'AIzaSyDq21enWEblUp7Tvo7W4BNSr18p9BSRPnA'
application.config['GOOGLE_API_JSON'] = 'client_secrets.json'
assert application.config['SessionManager'].r is not None, "Can't connect to redis server."


application.register_blueprint(cms.cms_views)
application.register_blueprint(blog.blog_views)
application.register_blueprint(login.login_routes)



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



@application.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml """
    pages = ["/index", "/", "/login", "/logout"]
    # All pages registed with flask apps
    db_wrapper = database_wrapper()
    post_pages = ["/post/" + post_id for post_id, post_data in query.getAllPosts(db_wrapper.content).iteritems()]
    post_pages += ["/post/" + post_data["post_handle"] for post_id, post_data in query.getAllPosts(db_wrapper.content).iteritems() if post_data["post_handle"]]
    pages += post_pages

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response

application.wsgi_app = ProxyFix(application.wsgi_app)
if __name__ == "__main__":
    extra_files = debug_dirUpdate()

    #live_host = "0.0.0.0"
    live_host = "127.0.0.1"

    application.run(host = live_host, debug=True, extra_files=extra_files, threaded=True, port=8080)