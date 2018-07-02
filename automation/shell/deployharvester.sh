sudo apt-get install python3-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
sudo apt-get update

which python3.4
virtualenv -p /usr/local/bin/python3.4 Vpy34
source Vpy34/bin/activate

sudo python3 -m pip install twython
sudo python3 -m pip install couchdb
sudo python3 -m pip install vaderSentiment

cd ~/Harvester/
python3 myfile.py
