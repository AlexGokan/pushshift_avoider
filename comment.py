import praw
import argparse
import time

import praw
from psaw import PushshiftAPI
import requests
import time
import copy

class SpecialComment():
	def __init__(self,comment):
		self.comment = comment
		self.edited_blank = False
		self.edited_back = False
		self.original_message = copy.copy(comment.body)
	

class CommentNotFoundError(Exception):
	pass

with open("user_data.txt","r") as f:
	client_id = f.readline().rstrip()
	client_secret = f.readline().rstrip()
	user_agent = f.readline().rstrip()
	username = f.readline().rstrip()
	password = f.readline().rstrip()
	
with open("default_message.txt","r") as f:
	default_message = f.read()
	
	
reddit = praw.Reddit(client_id=client_id,
					 client_secret=client_secret,
					 user_agent='Python38:pushshift avoider tool:v1.0 (by u/thetrombonist)',
					 username=username,
					 password=password)
	
blank = []
current_comments = []
current_ids = []

message = "this is a blank comment"

while True:
	url = "https://api.pushshift.io/reddit/search/comment"
	params = {}
	comments = requests.get(url, params = params)
	
	latest_comment = comments.json()['data'][-1]

	ta = latest_comment['created_utc']
	
	my_comments = reddit.redditor(username).comments.new(limit=10)
	
	for comment in my_comments:
		if comment.created_utc > ta and comment.id not in current_ids and comment.body != message:
			current_comments.append(SpecialComment(comment))
			current_ids.append(comment.id)
	
	
	for c in current_comments:		
		if ta + 180 > c.comment.created_utc and not c.edited_blank:
			print("editing comment " + c.comment.id)
			c.comment.edit(message)
			c.edited_blank = True
			blank.append(c)
			
			current_comments.remove(c)
			current_ids.remove(c.comment.id)
	
	blank = [b for b in blank if b.edited_back == False]
	
	for b in blank:
		print(b.original_message)
		comment_url = "https://api.pushshift.io/reddit/search/comment/"
		comment_params = {"ids" : b.comment.id}
		b_cmt = requests.get(url,params = comment_params).json()['data']
		if len(b_cmt) > 0:
			b_cmt = b_cmt[0]
		
			if b_cmt['author'] == username:
				b.comment.edit(b.original_message)
				b.edited_back = True
			
		
			
	
		
	print("------------")
	time.sleep(3)

	
