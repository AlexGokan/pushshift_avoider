import praw
import argparse
import time

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
					 
parser = argparse.ArgumentParser()
parser.add_argument("mode",help = "reply to a post ('s'), or reply to a comment ('c')")
parser.add_argument("url",help = "post or comment url")
args = parser.parse_args()

if args.mode == 's':
	submission = reddit.submission(url=args.url)
	comment = submission.reply(".")
	
	
	comment_list = reddit.redditor(username).comments.new(limit=10)
	found = False
	for i in range(10):
		for c in comment_list:
			if c.id == comment.id:
				found = True
				break
		
		comment_list = reddit.redditor(username).comments.new(limit=10)
	if not found:
		raise CommentNotFoundError
		
	edited_comment = comment.edit("new message")
		
	#get comment id
	#scan user's page for newest comment, until the newest one matches the id of what we just posted
	#then update
	
elif args.mode == 'c':
	pass
	
else:
	print("invalid mode")
	

