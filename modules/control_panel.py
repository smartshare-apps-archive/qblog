from flask import Blueprint, render_template, abort, current_app, session, request, Markup

from db import database_wrapper

import markdown
import query	


class BlogCMS(object):
	def __init__(self):
		self.db_wrapper = database_wrapper()
		self.content = self.db_wrapper.content


	def timeline(self):
		posts = query.getAllPosts(self.content)

		for post_id, data in posts.iteritems():

			post_content = data.get("post_content", None)

			if post_content:
				data["post_content"] = posts[post_id]["post_content"].split(r'<br />')

				for idx, line in enumerate(data["post_content"]):
					data["post_content"][idx] = markdown.markdown(line)

				posts[post_id]["post_content"] = ''.join(data["post_content"])
				
				print posts[post_id]["post_content"] 
			else:
				posts[post_id]["post_content"] = ""
		

		return render_template("/timeline.html", posts = posts)


	def get_post_content(self, post_id):
		post = query.getPost(self.content, post_id)
		return post