import praw
import argparse

with open("user_data.txt","r") as f:
	client_id = f.readline()
	client_secret = f.readline()
	user_agent = f.readline()
	username = f.readline()
	password = f.readline()
	
reddit = praw.Reddit(client_id=client_id,
					 client_secret=client_secret,
					 user_agent='Python38:pushshift avoider tool:v1.0 (by u/thetrombonist)',
					 username=username,
					 password=password)
					 
parser = argparse.ArgumentParser()
parser.add_argument("mode",help = "reply to a post ('s'), or reply to a comment ('c')")
parser.add_argument("url",help = "post or comment url")
args = parser.parse_args()



