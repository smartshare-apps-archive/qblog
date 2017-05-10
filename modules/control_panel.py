from flask import Blueprint, render_template, abort, current_app, session, request, Markup


from db import database_wrapper

import query	
import markdown

class BlogCMS(object):
	def __init__(self):
		self.db_wrapper = database_wrapper()
		self.content = self.db_wrapper.content


	def timeline(self):
		posts = query.getAllPosts(self.content)

		for post_id, data in posts.iteritems():

			post_content = data.get("post_content", None)

			if post_content:
				post_content = post_content.replace('<br />', '\n')
				print post_content
				data["post_content"] = markdown.markdown(post_content, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.nl2br'])

			else:
				posts[post_id]["post_content"] = ""
		

		return render_template("/timeline.html", posts = posts)


	def get_post_content(self, post_id):
		post = query.getPost(self.content, post_id)
		return post