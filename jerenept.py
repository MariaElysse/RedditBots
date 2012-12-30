#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Reddit bot that posts random /r/circlejerk comments
to submissions on /r/botcirclejerk.
Python 2.7 (as evidenced by the Unicode madness)

I also used this bot to practise my SQL(ite) skills.
Needless to say, not very much in that department"""


import praw,time,random
import sqlite3 as lite

#Make things simpler by declaring these up here:

user_agent="/r/botcirclejerk bot by /u/jerenept. Not particularly intelligent."
user='jerenept'
passwd='********'

#Assuming there is an SQLite DB with this name in cwd.
#it must have a table "already_done" with column "id"
connection=lite.connect('jerenept.db')
cursor=connection.cursor()

#initialise the session
random.seed()
session=praw.Reddit(user_agent=user_agent)
session.login(user,passwd)

def any_comment_replies_by(replies,username):
	result=False
	for reply in replies:
		if str(reply.author)==username:
			result=True

print """ Success, logged in as
User: "%s"
Pass: "%s"
User-agent: "%s""""" %(user,passwd,user_agent)
circlejerk=session.get_subreddit('circlejerk')
print "Loaded /r/circlejerk"
botcj=session.get_subreddit('botcirclejerk')
print "Loaded /r/botcirclejerk"
comment_list=[]

while True:
	for comment in circlejerk.get_comments(limit=100):
		comment_list.append(unicode(comment.body))
	time.sleep(2)
	print "Obtained CJ comments"
	botcj_hot=botcj.get_hot(limit=10)
	print "Obtained BotCJ posts"
	for submission in botcj_hot:
		submission_comments=submission.all_comments_flat
		print "Got comments from botCJ post %s" % str(submission.id)
		print "Checking for comments by should_be_posted_in"
		for comment in submission_comments:
			cursor.execute("SELECT id from already_done where id='%s'" % comment.id)
			if str(comment.author)=="should_be_posted_in" and str(comment.id)!=str(cursor.fetchone()):
				try:
					comment.reply(unicode(comment_list[random.randint(0,99)]))
					cursor.execute("INSERT into already_done values('%s')" % str(comment.id))
					connection.commit()
				except praw.errors.RateLimitExceeded as detail:
					print "Waiting for Reddit to stop complaining: %s minutes" %str(detail).split(' ')[9]
					print str(detail)
					time.sleep(int(str(detail).split(' ')[9])*60)
					comment.reply(str(comment_list[random.randint(0,99)]))
				print "Posted reply"
			else:
				print "Nothing posted."

