**-----Steps for Accessing Jupyter Notebook-----**
------------------------------------------------------------------
ssh -i cloudkey -L 8000:localhost:8888 ubuntu@115.146.95.146

token: http://localhost:8000/?token=a30fa4afe693ab4057263f614de2be7349aecc858fa67ea0

Open the link in your browser: http://localhost:8000/notebooks/Untitled.ipynb?kernel_name=python3#

**-----Steps for Creating and Deploying Twitter Harvester-----**
------------------------------------------------------------------

**Login details**
--------------------
ssh -i cloudkey -L 5984:127.0.0.1:5984 ubuntu@115.146.95.146

**Check database**
--------------------
Open the following on your local systems (browser): http://localhost:5984/_utils/index.html.

**Requirements**
--------------------
1. Twython 3.6.0
2. Couchdb 1.2
3. vaderSentiment

**Virtual Env setup**
--------------------
1. root:~# which python3.4
2. /usr/local/bin/python3.4
3. root:~# virtualenv -p /usr/local/bin/python3.4 Vpy34
4. root:~# source Vpy34/bin/activate
5. (Vpy34) root:~# python -V
6. Python 3.4.4

**Installation on python3**
-----------------------
1. python3 -m pip install twython.
2. python3 -m pip install couchdb.
3. python3 -m pip install vaderSentiment.

**Sentiment Analysis data**
------------------------
1. Keywords: extracted from positive-words.txt and negative-words.txt
2. Sentiment score: obtained for each tweet using vaderSentiment and stored as tweet attribute in dB.

**Steps**
-----------------------
1. Create a twitter Application online. 
2. Get Consumer key and Consumer secret key to fetch tweets.
3. Fetch tweets as json object for keywords.
4. Fetch tweet 'id' as its unique id in database
5. Store tweets by id in dB, after looking for duplicates.
6. Exception handling for twitter time limit. Sleep for remaining time.

**Test Harvester working** 
------------------------
1. Instance 1.
2. Harvester folder: /volume/twitter_harvester/app.
3. Main file: tw_harvester2.py.
4. keyword files: positive-words.txt, negative-words.txt.
5. Collecting global tweets according to GEO COD 1.
