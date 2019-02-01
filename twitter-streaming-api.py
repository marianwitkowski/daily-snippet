import json
import tweepy
import sys

# create access tokens and consumer key on https://developer.twitter.com/en/apps by register new app
consumer_key = 'm6GYBalC1eXXXXXXXXXXXXXXX'
consumer_secret = 'iYxQh279JZsKcL7RXXXXXXXXXXXXXXX'
access_token = '133860407-ZI0kjYDNaBHXXXXXXXXXXXXXXX'
access_token_secret = 'NPrZEIeEMaaUVQzEGXXXXXXXXXXXXXXX'

# looking for these keywords
hashtags = ['python', 'machinelearning', 'bigdata']
# in these languages
lng = ['pl']

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
                    print "=" * 40
        return True

    # on failure
    def on_error(self, status):
        if status == 420:
            sys.stderr.write('Too Many Requests')
            return True
        else:
            sys.stderr.write('Error {}\n'.format(status))
            return True

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = tweepy.Stream(auth, listener)

    # search twitter for hashtags list
    stream.filter(languages=lng, track=hashtags)
