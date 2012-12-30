#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NOTE: This bot has been banned from /r/circlejerk. It's very annoying indeed."""

"""Python 2.7 (as evidenced by the Unicode madness)"""

import praw,time,random,pickle

#Make things simpler by declaring these up here
user_agent="""bot by /u/jerenept. Not particularly intelligent. Randomly labels comments as gems, or not."""
user='gem_or_not_gem'
passwd='********'

#initialise the session

jerenept_data=open("gem.data","r+")

# This program writes a serialised list to the disk after every comment
#(bad for SSDs I would assume)

print "Loaded datafile"

random.seed()

session=praw.Reddit(user_agent=user_agent)
session.login(user,passwd)

#You could do that with no args for an interactive prompt.

already_done=pickle.load(jerenept_data)

print """Success, logged in as
User: "%s"
Pass: "%s"
User-agent: "%s""""" %(user,passwd,user_agent)
circlejerk=session.get_subreddit('circlejerk')
print "Loaded /r/circlejerk/"

gong=get_redditor(user)

while True:
  for comment in circlejerk.get_comments(limit=1000):
		if comment.body not in ["NOT GEM","GEM"] and comment.id not in already_done:
			if random.randint(1,10)>4:
				try:
					comment.reply("GEM")
					print "Responded to %s: 'GEM'" % comment.body.encode('ascii','ignore')
				except praw.errors.RateLimitExceeded as detail:
					print "Waiting for Reddit to stop complaining: %s minutes" %str(detail).split(' ')[9]
					print str(detail)
					time.sleep(int(str(detail).split(' ')[9])*60)
					comment.reply("GEM")
					print "Responded to %s: 'GEM'" % comment.body.encode('ascii','ignore')
			else:
				try:
					comment.reply("NOT GEM")
					print "Responded to %s: 'NOT GEM'" % comment.body.encode('ascii','ignore')
				except praw.errors.RateLimitExceeded as detail:
					print "Waiting for Reddit to stop complaining: %s minutes" %str(detail).split(' ')[9]
					print str(detail)
					time.sleep(int(str(detail).split(' ')[9])*60)
					comment.reply("NOT GEM")
					print "Responded to %s: 'NOT GEM'" % comment.body.encode('ascii','ignore')
			already_done.append(comment.id)
			pickle.dump(already_done,jerenept_data)
			jerenept_data.close()
			jerenept_data=open("gem.data","r+")
			print "Waiting 120 seconds before posting again."
			time.sleep(120)
