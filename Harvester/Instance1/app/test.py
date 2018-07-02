#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import couchdb
import logging
from twython import Twython
from twython import TwythonError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


##Assigns sentiment scores to tweets
##------------------------------------------------------------------
def sentiment_analyzer(tweet_text):
        analyzer=SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(tweet_text)


##Tests whether the rate limit of the last request has been reached
##------------------------------------------------------------------
def test_rate_limit(api, wait=True, buffer=.1):

        # Get the number of remaining requests
        remaining = float(api.get_lastfunction_header(header='x-rate-limit-reset'))-time.time()
        # Check if we have reached the limit
        if remaining == 0:
            limit = int(api.get_lastfunction_header(header='x-rate-limit-reset'))
            reset = int(api.get_lastfunction_header(headerS='x-rate-limit-reset'))
            # Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            # Let the user know we have reached the rate limit
            logger.info("0 of %d requests remaining until %d.", limit, reset)

            if wait:
                # Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                logger.info("Sleeping for %d", delay)
                sleep(delay)
                # Rate limit reset. OK to proceed.
                return True
            else:
                # Rate limit reached.
                return False

        # Rate limit not reached
        return True


##Couch dB connection
##------------------------------------------------------------------
couchserver = couchdb.Server("http://127.0.0.1:5984/")
print(couchserver)

dbname='sentiment_tweets'
if dbname in couchserver:
    db=couchserver[dbname]
else:
    db=couchserver.create(dbname)


##Twitter search
##------------------------------------------------------------------
APP_KEY='olVpEB3ytC8IwuYxtZRbT0VvI'
APP_SECRET='aQdXuTU256cVO7YSCNESD6Cd6JODc7lobt03w59g3TO3jOCJbL'

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
keywords = keywords[0]

MAX_COUNT=100
GEO_CODE1='-32.562280134847995,144.53837739637368,704.978km'

##Fetching tweets
loop=True
while loop:
    for keyword in keywords:
        try:
            t=twitter.search(q=keyword,count=MAX_COUNT, lang='en', geocode=GEO_CODE1)
            tweet_object=t['statuses']
            for tweet in tweet_object:
                if len(tweet)>0:
                    #tweet['sentiment']=sentiment_analyzer(tweet['text'])
                    #tweet['keyword']=keyword
                    tw_id=tweet['id_str']
                    if tw_id in db:
                        print('Duplicate tweet')
                    else:
                        #db[tw_id] = tweet
                        print('Written to database')
                        user = tweet['user']['screen_name']
                        print(user)
                        #results = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=%d" % (user, 20))
                        #print(result)
                        break
                else:
                    break

        except TwythonError as inst:
            logger.error(inst.msg)
            loop=test_rate_limit(twitter)
            twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            continue
    break

