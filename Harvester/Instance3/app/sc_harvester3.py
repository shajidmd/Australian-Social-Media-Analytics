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

dbname='sc_tweets'
if dbname in couchserver:
    db=couchserver[dbname]
else:
    db=couchserver.create(dbname)


##Twitter search
##------------------------------------------------------------------
APP_KEY='6eg78maFDC2YVWooJ0aMPNGhv'
APP_SECRET='IoF5XG29FtpTfylhea2gCWLvqB0Lx4Dr4jDrB08AMCif3tSdLR'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)


##Bag of positive and negative words
##------------------------------------------------------------------
KEY_FILE = os.path.join('scenario_words.txt')
keywords=[]
for key in open(KEY_FILE, 'r').readlines():
    keywords.append(key.rstrip())


##HARVESTING
##------------------------------------------------------------------
MAX_COUNT=100
GEO_CODE3='-42.02716074013492,146.29993989639877,181.108km'

loop=True
while loop:
    for keyword in keywords:
        try:
            string='#'+keyword+' '
            t=twitter.search(q=string,count=MAX_COUNT, lang='en', geocode=GEO_CODE3)
            time.sleep(6)
            tweet_object=t['statuses']
            for tweet in tweet_object:
                if len(tweet)>0:
                    tweet['sentiment']=sentiment_analyzer(tweet['text'])
                    keyword_text='#'+keyword
                    tweet['keyword']=keyword_text
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

