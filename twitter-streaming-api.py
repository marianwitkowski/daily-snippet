
"""
install required packages:
$ sudo pip install google-cloud-datastore
$ sudo pip install tweepy
"""

import json
import tweepy
import sys

"""
    https://cloud.google.com/datastore/docs/reference/libraries#client-libraries-install-python
    Before using click "Create Service Account Key Page" button, generate and save JSON file with credentials

    Set variables before using command line
    $ export GOOGLE_APPLICATION_CREDENTIALS="/Users/test/app/datastore.json"
"""
from google.cloud import datastore

# create access tokens and consumer key on https://developer.twitter.com/en/apps by register new app
consumer_key = 'm6GYBalC1eXXXXXXXXXXXXXX'
consumer_secret = 'iYxQh279JZsKcL7R9eQVsXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXX-ZI0kjYDNaBHfiPBoJ8gAhY17XXXXXXXXXXXXX'
access_token_secret = 'NPrZEIeEMaaUVQzEG4Nyo4jKTjeMEXXXXXXXXXXXXX'

# looking for these keywords
keywords = ['python', 'machinelearning', 'bigdata']
# in these languages
lng = ['en']

class TweetStreamListener(tweepy.streaming.StreamListener):

    # on success
    def on_data(self, data):
        # decode json
        tweet = json.loads(data)
        if 'text' in tweet: # only messages contains 'text' field is a tweet
                    print(tweet['id']) # This is the tweet's id
                    print(tweet['created_at']) # when the tweet posted
                    print(tweet['text']) # content of the tweet
                                
                    print(tweet['user']['id']) # id of the user who posted the tweet
                    print(tweet['user']['name']) # name of the user
                    print(tweet['user']['screen_name']) # name of the user account

                    hashtags = []
                    for hashtag in tweet['entities']['hashtags']:
                        hashtags.append(hashtag['text'])
                    print(hashtags)


                    # The kind for the new entity
                    kind = 'Tweets'
                    # The ID for the new entity
                    name = tweet['id']
                    # The Cloud Datastore key for the new entity
                    task_key = datastore_client.key(kind, name)

                    # Prepares the new entity and store tweet data
                    task = datastore.Entity(key=task_key)
                    task.update(tweet)

                    # Saves the entity
                    datastore_client.put(task)

                    print "=" * 40
        return True

    # on failure
    def on_error(self, status):
        if status == 420:
            sys.stderr.write('Too Many Requests\n')
            return True
        else:
            sys.stderr.write('Error {}\n'.format(status))
            return True

if __name__ == '__main__':

    # Instantiates a client of GCP datastore
    datastore_client = datastore.Client()

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = tweepy.Stream(auth, listener)

    # search twitter for hashtags list
    stream.filter(languages=lng, track=keywords)
