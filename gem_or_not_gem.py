#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NOTE: This bot has been banned from /r/circlejerk. It's very annoying indeed. 
Interestingly enough, people thpought it was smart. Weird."""

"""Python 2.6+, should work equally well with 3+ (Using imports from __future__)"""

import praw
import time
import random
import pickle

from __future__ import unicode_literals, print_function
#Make things simpler by declaring these up here
user_agent="""bot by /u/jerenept. Not particularly intelligent. Randomly labels comments as gems, or not."""
user='gem_or_not_gem'
passwd='********'

gem_data=open("gem.data","r+")

# This program writes a serialised list to the disk after every comment
#(bad for SSDs I would assume)

print("Loaded datafile")

random.seed()
#initialise the session

session=praw.Reddit(user_agent=user_agent)
session.login(user,passwd)

#You could do that with no args for an interactive prompt.

already_done=pickle.load(gem_data)

print("""Success, logged in as
User: "{0}"
Pass: "{1}"
User-agent: "{2}""""".format(user,passwd,user_agent))
circlejerk=session.get_subreddit('circlejerk')
print("Loaded /r/circlejerk/")

while True:
  for comment in circlejerk.get_comments(limit=1000):
		if comment.body not in ["NOT GEM","GEM"] and comment.id not in already_done:
			if random.randint(1,10)>4:
				try:
					comment.reply("GEM")
					print("Responded to {0}: 'GEM'".format(comment.body)
				except praw.errors.RateLimitExceeded as detail:
					print(" Rate Limited. Waiting for Reddit to stop complaining: {0} minutes" .format(str(detail).split(' ')[9]))
					print( str(detail))
					time.sleep(int(str(detail).split(' ')[9])*60)
					comment.reply("GEM")
					print("Responded to {0}: 'GEM'".format(comment.body))
			else:
				try:
					comment.reply("NOT GEM")
					print("Responded to {0}: 'NOT GEM'".format(comment.body))
				except praw.errors.RateLimitExceeded as detail:
					print( "Rate Limited. Waiting for Reddit to stop complaining: {0} minutes".format(str(detail).split(' ')[9]) )
					print(str(detail))
					time.sleep(int(str(detail).split(' ')[9])*60)
					comment.reply("NOT GEM")
					print("Responded to {0}: 'NOT GEM'".format(comment.body))
			already_done.append(comment.id)
			pickle.dump(already_done,gem_data)
			gem_data.close()
			gem_data=open("gem.data","r+")
			print("Waiting 120 seconds before posting again.")
			time.sleep(120)
