#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import couchdb
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from twython import Twython

def sentiment_analyzer(tweet_text):
        analyzer=SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(tweet_text)

couchserver = couchdb.Server("http://127.0.0.1:5984/")
print(couchserver)

dbname='twitter'
if dbname in couchserver:
    db=couchserver[dbname]
else:
    db=couchserver.create(dbname)

APP_KEY='olVpEB3ytC8IwuYxtZRbT0VvI'
APP_SECRET='aQdXuTU256cVO7YSCNESD6Cd6JODc7lobt03w59g3TO3jOCJbL'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

MAX_COUNT=100

##Bag of positive and negative words
pos_words = ['happy','excited','amused',':)',':D',':-)',':-D']
neg_words = ['sad','devastated','cry',':(',':-(',":'("]
keywords=pos_words+neg_words

loop=True
while loop:
    for keyword in keywords:
        try:
            t=twitter.search(q='keywords',count=MAX_COUNT, lang='en')
            tweet_object=t['statuses']
            for tweet in tweet_object:
            	if len(tweet)>0:
                    tweet['sentiment']=sentiment_analyzer(tweet['text'])
                    tw_id=tweet['id_str']
		    print("Works\n\n")
		    
		    if tw_id in db:
                    	print('Duplicate tweet')
                    else:
			db[tw_id]=tweet
			#print('Written to database')
                else:
                    	break
                        
        except:
            remainder = float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
            loop=False
            twitter.disconnect()
	    time.sleep(remainder)
	    twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	    loop=True
            continue
                
               

