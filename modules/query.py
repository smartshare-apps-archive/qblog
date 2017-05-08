import MySQLdb
from contextlib import closing


POST_FIELDS = ["post_id", "user_id", "post_type", "post_title", "timeline_icon", "timestamp", "post_image", "post_content"]


def getAllPosts(content):
	blog_posts = None

	with closing(content.cursor()) as cursor:
		currentQuery = "SELECT post_id, user_id, post_type, post_title, timeline_icon, timestamp, post_image, post_content FROM posts;"

		try:
			cursor.execute(currentQuery)
		except Exception as e:
			print "Couldn't get posts: ", e
			return None

		blog_posts = cursor.fetchall()

	if blog_posts:

		formattedBlogPosts = {}

		for post in blog_posts:
			post_id = str(post[0])

			formattedBlogPosts[post_id] = {}

 			for idx, field in enumerate(post):
				formattedBlogPosts[post_id][POST_FIELDS[idx]] = field

		return formattedBlogPosts

	else:
		return {}



def getPost(content, post_id):
	blog_post = None

	with closing(content.cursor()) as cursor:
		currentQuery = "SELECT post_id, user_id, post_type, post_title, timeline_icon, timestamp, post_image, post_content FROM posts WHERE post_id=%s;"

		try:
			cursor.execute(currentQuery, (post_id, ))
		except Exception as e:
			print "Couldn't get post: ", e
			return None

		blog_post = cursor.fetchone()

	if blog_post:
		formattedBlogPost = {}

		for idx, field in enumerate(blog_post):
			formattedBlogPost[POST_FIELDS[idx]] = field

		return formattedBlogPost

	else:
		return {}




def savePost(content, postData):
	with closing(content.cursor()) as cursor:
		currentQuery ="UPDATE posts SET post_type=%s, post_title=%s, timeline_icon=%s, post_image=%s, post_content=%s WHERE post_id=%s;"
		
		try:
			cursor.execute(currentQuery, (postData["post_type"], postData["post_title"], postData["timeline_icon"], postData["post_image"], postData["post_content"], postData["post_id"]))
		except Exception as e:
			print "Couldn't save post: ", e
			return False

	return True


def createPost(content, postData):
	with closing(content.cursor()) as cursor:
		currentQuery ="INSERT INTO posts(post_type, post_title, timeline_icon, post_image) VALUES (%s, %s, %s, %s);"
		
		try:
			cursor.execute(currentQuery, (postData["post_type"], postData["post_title"], postData["timeline_icon"], postData["post_image"]))
		except Exception as e:
			print "Couldn't save post: ", e
			return False

	return True