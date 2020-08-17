
import praw
from psaw import PushshiftAPI
import requests
import time
import copy
import pickle

class SpecialComment():
	def __init__(self,comment):
		self.comment = comment
		self.edited_blank = False
		self.edited_back = False
		self.original_message = copy.copy(comment.body)


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

while True:

	url = "https://api.pushshift.io/reddit/search/comment"
	params = {}
	comments = requests.get(url, params = params)
	
	latest_comment = comments.json()['data'][-1]

	ta = latest_comment['created_utc']

	archive_delay = latest_comment['retrieved_on'] - latest_comment['created_utc']
	
	my_comments = reddit.redditor(username).comments.new(limit=100)

	current_comments = [c for c in current_comments if c[0].edited_blank == False]
	current_ids = [c[1] for c in current_comments]

	for comment in my_comments:
		if comment.created_utc > ta and comment.id not in current_ids and comment.body != default_message:
			current_comments.append((SpecialComment(comment),comment.id))



	for c in current_comments:
		if ta + 180 > c[0].comment.created_utc and not c[0].edited_blank:
			print("editing comment " + c[0].comment.id)
			c[0].comment.edit(default_message)
			c[0].edited_blank = True
			blank.append(c[0])
			pickle.dump((c[0].comment.id,c[0].original_message),open("saved_comments/" + str(c[0].comment.id) + ".p","wb"))

	blank = [b for b in blank if b.edited_back == False]
	
	for b in blank:
		#print(b.original_message)
		comment_url = "https://api.pushshift.io/reddit/search/comment/"
		comment_params = {"ids" : b.comment.id, "author" : username}
		b_cmt = requests.get(url,params = comment_params).json()['data']
		if len(b_cmt) > 0:
			b_cmt = b_cmt[0]
		
			if b_cmt['author'] == username:
				b.comment.edit(b.original_message)
				b.edited_back = True
			
		
			
	
		
	print("------------" + "  delay: " + str(archive_delay))

	if(archive_delay < 45):
		time.sleep(0.05)
	elif(archive_delay < 180):
		time.sleep(archive_delay / 20)
	else:
		time.sleep(archive_delay / 3)

	#time.sleep(0.1)

	
