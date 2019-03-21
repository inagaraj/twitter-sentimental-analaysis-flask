import tweepy
from random import random

from TwitApp.models import Tweet
from TwitApp.utils import twit_auth_handler



from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import credentials
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
consumer_key = "foVcRMOv9MD7sB63dZDwhATOq"
consumer_secret = "j4ke4amMa1ydFmgBXKTDBgcr8fcxNtvRgFOhiyja2PR2NbYy94"
access_token = "2923384237-Z3B7GDEXG3p9ioNhc2KKKUXaYHjWpsGXBhb2mkN"
access_token_secret = "bkl5hC9qPjYF0Hen5pYJvYFfIyN39BoWnVNc9SlgHqiFV"

class TwitterMain:

    def __init__(self):
        self.api = twit_auth_handler()

    def get_tweet_html(self, id):
        oembed = self.api.get_oembed(id=id, hide_media=True, hide_thread=True)
        return oembed["url"]

    def get_trends(self, text_query, count):
        tt_buff = list()
        rand_id = round(random() * 1000)
        for t in tweepy.Cursor(self.api.search,
                               q=text_query + ' -filter:retweets',
                               lang='en').items(count):
            tweet = Tweet(rand_id, text_query, str(t.id),
                          t._json["lang"], t._json["text"])
            tt_buff.append(tweet)


    
        

        return [self.get_tweet_html(int(t.tweet_id)) for t in tt_buff[:10]], rand_id
    def get_results(self, text_query, count):
        twitter_client = TwitterClient()
        tweet_analyser = TweetAnalyzer()

        api = twitter_client.get_twitter_client_api()
        keyword=text_query
        limit=count
        tweets = api.search(q=keyword, count=limit)

       
        #-----------------------------------------------------------------------
        # print out the contents, and any URLs found inside
        #-----------------------------------------------------------------------
       
        
        
        df = tweet_analyser.tweets_to_data_frame(tweets)
        
        df['sentiment'] = np.array([tweet_analyser.analyze_sentiment(tweet) for tweet in df['tweet']])
        
       
        print(df)
        df.to_csv('twitter-sentimental-analysis.csv', encoding='utf-8', index=False)
        df.to_csv('./TwitApp/static/twitter-sentimental-analysis.csv', encoding='utf-8', index=False) 
        df = df.to_records()
        return df
    @classmethod
    def get_analysis_data(cls, text_query,count):
        
        twitter_client = TwitterClient()
        tweet_analyser = TweetAnalyzer()
        api = twitter_client.get_twitter_client_api()
        keyword=text_query
        limit=count
        tweets = api.search(q=keyword, count=limit)
        df = tweet_analyser.tweets_to_data_frame(tweets)
        df['sentiment'] = np.array([tweet_analyser.analyze_sentiment(tweet) for tweet in df['tweet']])
        pos_tweets = [ tweet for index, tweet in enumerate(df['tweet']) if df['sentiment'][index] == "Positive"]
        neu_tweets = [ tweet for index, tweet in enumerate(df['tweet']) if df['sentiment'][index] == "Neutral"]
        neg_tweets = [ tweet for index, tweet in enumerate(df['tweet']) if df['sentiment'][index] == "Negative"]

    

       
        print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(df['tweet'])))
        print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(df['tweet'])))
        print("Percentage of negative tweets: {}%".format(len(neg_tweets)*100/len(df['tweet'])))
        postive_percentage=round(float(format(len(pos_tweets)*100/len(df['tweet']))),2)
        neutral_percentage=round(float(format(len(neu_tweets)*100/len(df['tweet']))),2)
        negative_percentage=round(float(format(len(neg_tweets)*100/len(df['tweet']))),2)

        print(postive_percentage)
        print(neutral_percentage)
        print(negative_percentage)
      
        return [postive_percentage, neutral_percentage, negative_percentage]
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client


    

   

    

# # #Twitter Authenticator # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth =OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        return auth

# # #Twitter Streamer # # #
class TwitterStreamer():

    def __init__(self):
        self.TwitterAuthenticator = TwitterAuthenticator()

    


# # # Twitter Stream Listener # # #
class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on Data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
        #Returing False on Data method in case of data limit hit
            return False 
        print(status)


# # # Tweet Analyser # # #

class TweetAnalyzer():
    def __init__(self):
        self.api = twit_auth_handler()

    def get_tweet_html(self,id):
        oembed = self.api.get_oembed(id=1107609036189360129, hide_media=True, hide_thread=True)
        return oembed["url"] 
        
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            return "Neutral"
        else:
            return "Negative"

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweet'])
        df['id'] = np.array([tweet.id_str for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
       
        return df