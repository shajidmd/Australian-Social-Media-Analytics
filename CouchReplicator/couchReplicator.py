# Author: shajidm@student.unimelb.edu.au
# Australian Socail Media Analytics Rest Service

#!/usr/bin/python
# -*- coding: utf-8 -*-
import couchdb
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

user = 'admin'
password = 'admin'
couchserver = couchdb.Server('http://%s:%s@115.146.95.146:5984/'
                             % (user, password))

for dbname in couchserver:
    print(dbname)

dbname = 'alltweetsx2015'
if dbname in couchserver:
    db1 = couchserver[dbname]
else:
    db1 = couchserver.create(dbname)


##Bag of positive and negative words
##------------------------------------------------------------------

KEY_FILE = os.path.join('scenario_words.txt')
keywords = []
for key in open(KEY_FILE, 'r').readlines():
    keywords.append(key.rstrip())


user2 = 'readonly'
password2 = 'ween7ighai9gahR6'
couchserver2 = couchdb.Server('http://%s:%s@45.113.232.90/couchdbro/'
                              % (user2, password2))

db2 = couchserver2['twitter']

def sentiment_analyzer(tweet_text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(tweet_text)

count1 = 0
count2 = 333
while count2 < 3333333:

    for item in db2.view('twitter/summary', startkey=["melbourne",2015,1,1], endkey=["melbourne",2015,12,31], include_docs='true', reduce='false', skip=count1, limit=count2):
        for keyword in keywords:
            string1 = ' ' + keyword + ' '
            string2 = '#' + keyword + ' '
            if string1 in item['doc']['text'] or string2 in item['doc']['text']:
                if item.doc.id not in db1:
                    item['doc']['sentiment'] = sentiment_analyzer(item['doc']['text'])
                    db1[item.doc.id] = item
                    print('tweet inserted') 

    count1 = count1 + 333
    count2 = count2 + 333