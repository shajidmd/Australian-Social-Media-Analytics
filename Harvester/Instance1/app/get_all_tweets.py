#!/usr/bin/python3
# -*- coding: utf-8 -*-
import couchdb
import tweepy
import os
#Twitter API credentials
consumer_key = "9ZCG2J6WPTDksoTLAJXC35FdX"
consumer_secret = "m12ecAnIcWHHybjmUxdXzYRoCwbkbsKh9bUJfm6pMH4yOC3gQP"
access_key = "1182567540-u5bLD3OdqM0JgrcHog6mxBfSx35eVPycMJoGjkb"
access_secret = "btfK2bD7MavOAAOOAJ5iTyVmxpuwpxdYvDElpEW0tp5Up"


##Couch dB connection
##------------------------------------------------------------------
user='admin'
password='admin'
couchserver = couchdb.Server("http://%s:%s@115.146.95.146:5984/" % (user,password))
print(couchserver)


#New Scenario DB ---------------
db_name = 'sc_tweets'
if db_name in couchserver:
    db = couchserver[db_name]
else:
    db = couchserver.create(db_name)


MAX_COUNT=200
GEO_CODE1='-32.562280134847995,144.53837739637368,704.978km'

#Check if keyword in tweet
#-----------------------------------------------------------------
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, geocode=GEO_CODE1)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=MAX_COUNT,max_id=oldest, geocode=GEO_CODE1)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
        
        
	return alltweets


##Get scenario keywords
##------------------------------------------------------------------
KEY_FILE = os.path.join('scenario_words.txt')
keywords=[]
for key in open(KEY_FILE, 'r').readlines():
    keywords.append(key.rstrip())

#Create new database to store all tweets from user        
db2_name='sc_user_all_tweets'
if db2_name in couchserver:
    db2 = couchserver[db2_name]
else:
    db2 = couchserver.create(db2_name)


for item in db.view('_all_docs'):
    id = item['id']
    doc = db[id]
    uname = doc['user']['screen_name']
    print(uname)
    tw_keyword = doc['keyword']
    print(tw_keyword)
    all_tweets = get_all_tweets(uname)
    for tweet_obj in all_tweets:
        for keyword in keywords:
            tweet = tweet_obj._json
            text = tweet['text']
            ht_keyword = "#"+keyword 
            if contains_word(text.lower(), keyword) or contains_word(text.lower(), ht_keyword):
                tweet['keyword'] = keyword
                tw_id = tweet['id_str']
                print(tw_id)
                if tw_id in db2:
                    print('Duplicate tweet')
                else:
                    db2[tw_id] = tweet
                    print(text)
                    print('Written to database')

    



