#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import couchdb
import logging
from twython import Twython
from twython import TwythonError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sys.path.append('/usr/local/lib/python3.4/dist-packages')

##Assigns sentiment scores to tweets
##------------------------------------------------------------------
def sentiment_analyzer(tweet_text):
        analyzer=SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(tweet_text)


##Tests whether the rate limit of the last request has been reached
##------------------------------------------------------------------
def test_rate_limit(api, wait=True, buffer=.1):

        log=logging.getLogger(__name__)
        # Get the number of remaining requests
        remaining = float(api.get_lastfunction_header(header='x-rate-limit-reset'))-time.time()
        # Check if we have reached the limit
        if remaining == 0:
            limit = int(api.get_lastfunction_header(header='x-rate-limit-reset'))
            log.info("0 of %d requests remaining", limit)
            #time.sleep(600)
        time.sleep(600)
        #Rate limit not reached
        return True


##Couch dB connection
##------------------------------------------------------------------
user='admin'
password='admin'
couchserver = couchdb.Server("http://%s:%s@115.146.95.146:5984/" % (user,password))
print(couchserver)

dbname='sentiment_tweets'
if dbname in couchserver:
    db=couchserver[dbname]
else:
    db=couchserver.create(dbname)


##Twitter search
##------------------------------------------------------------------
APP_KEY='bSqSQkqyuTww5QIiY2EMNAw9n'
APP_SECRET='YRVjJSULfmK2RVRQHGAJ0AH3YSsqV0Q3DYdrzKpLPVVRyatuyy'

##KEY_FILE = os.path.join('app_keys.txt')
##keys=[]
##for key in open(KEY_FILE, 'r').readlines():
##    keys.append(key.rstrip())
##    
##APP_KEY=keys[0]
##APP_SECRET=keys[1]

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

##Bag of positive and negative words
POS_WORDS_FILE = os.path.join('positive-words.txt')
NEG_WORDS_FILE = os.path.join('negative-words.txt')

pos_words = []
neg_words = []

for pos_word in open(POS_WORDS_FILE, 'r').readlines()[35:]:
    pos_words.append(pos_word.rstrip())

for neg_word in open(NEG_WORDS_FILE, 'r').readlines()[35:]:
    neg_words.append(neg_word.rstrip())

keywords=pos_words+neg_words
MAX_COUNT=100
GEO_CODE3='-42.02716074013492,146.29993989639877,181.108km'
#GEO_CODE1=keys[2]

##Fetching tweets
loop=True
while loop:
    for keyword in keywords:
        try:
            t=twitter.search(q=keyword,count=MAX_COUNT, lang='en', geocode=GEO_CODE3)
            time.sleep(6)
            tweet_object=t['statuses']
            for tweet in tweet_object:
                if len(tweet)>0:
                    tweet['sentiment']=sentiment_analyzer(tweet['text'])
                    tweet['keyword']=keyword
                    tw_id=tweet['id_str']
                    if tw_id in db:
                        print('Duplicate tweet')
                    else:
                        db[tw_id] = tweet
                        print('Written to database')
                else:
                    break
        except TwythonError:
            print("Twython error")
            loop=test_rate_limit(twitter)
            continue

