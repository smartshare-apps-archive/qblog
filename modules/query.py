import MySQLdb
import collections

from contextlib import closing
from datetime import datetime


POST_FIELDS = ["post_id", "user_id", "post_type", "post_title", "post_author", "timeline_icon", "timestamp", "post_image", "post_content", "post_tags", "post_description", "post_published", "post_handle"]


def getAllPosts(content):
    blog_posts = None

    with closing(content.cursor()) as cursor:
        currentQuery = "SELECT post_id, user_id, post_type, post_title, post_author, timeline_icon, timestamp, post_image, post_content, post_tags, post_description, post_published, post_handle FROM posts ORDER BY timestamp DESC;"

        try:
            cursor.execute(currentQuery)
        except Exception as e:
            print "Couldn't get posts: ", e
            return None

        blog_posts = cursor.fetchall()

    if blog_posts:

        formattedBlogPosts = collections.OrderedDict()

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
        currentQuery = "SELECT post_id, user_id, post_type, post_title, post_author, timeline_icon, timestamp, post_image, post_content, post_tags, post_description, post_published, post_handle FROM posts WHERE post_id=%s;"

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



def getPostByHandle(content, post_handle):
    blog_post = None

    with closing(content.cursor()) as cursor:
        currentQuery = "SELECT post_id, user_id, post_type, post_title, post_author, timeline_icon, timestamp, post_image, post_content, post_tags, post_description, post_published, post_handle FROM posts WHERE post_handle=%s;"

        try:
            cursor.execute(currentQuery, (post_handle, ))
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
        currentQuery ="UPDATE posts SET post_type=%s, post_title=%s, post_author=%s, timeline_icon=%s, post_image=%s, post_content=%s, post_tags=%s, post_description=%s,post_published=%s,post_handle=%s WHERE post_id=%s;"
        
        try:
            cursor.execute(currentQuery, (postData["post_type"], postData["post_title"], postData["post_author"],postData["timeline_icon"], postData["post_image"], postData["post_content"], postData["post_tags"], postData["post_description"], postData["post_published"], postData["post_handle"], postData["post_id"]))
        except Exception as e:
            print "Couldn't save post: ", e
            return False

    return True


def deletePost(content, postData):

    with closing(content.cursor()) as cursor:
        currentQuery ="DELETE FROM posts WHERE post_id=%s;"
        
        try:
            cursor.execute(currentQuery, (postData["post_id"], ))
        except Exception as e:
            print "Couldn't delete post: ", e
            return False

    return True


def bulkDeletePosts(content, selectedPostIDs):
    placeholders = ','.join(['%s' for _ in selectedPostIDs])

    with closing(content.cursor()) as cursor:
        currentQuery ="DELETE FROM posts WHERE post_id IN(%s);" % placeholders

        try:
            cursor.execute(currentQuery, selectedPostIDs)
        except Exception as e:
            print "Couldn't delete posts: ", e
            return False

    return True



def createPost(content, postData):
    with closing(content.cursor()) as cursor:
        currentQuery ="INSERT INTO posts(post_type, post_title, timeline_icon, timestamp) VALUES (%s, %s, %s, %s);"
        
        try:
            cursor.execute(currentQuery, (postData["post_type"], postData["post_title"], postData["timeline_icon"], datetime.now(), ))
        except Exception as e:
            print "Couldn't save post: ", e
            return None


        insert_query = "SELECT LAST_INSERT_ID();"
        
        try:
            cursor.execute(insert_query)
        except Exception as e:
            print "Error: ", e

        post_id = cursor.fetchone()

        if post_id:
            return post_id[0]
        else:
            return None

