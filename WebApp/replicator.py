import couchdb

user = 'admin'
password = 'admin'
try:
    couch = couchdb.Server('http://%s:%s@115.146.95.146:5984/' % (user, password))
    db_sc_tweets = couch['sc_tweets']
    print('Connection Success')
    for doc in db_sc_tweets.view('_all_docs'):
    	print(doc)
except:
    print('Connection Failed')

