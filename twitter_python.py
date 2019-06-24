from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
import seaborn as sns
import translate_tweets
import tweet_analyzer

####input your credentials here
consumer_key = 'wtFRuCKCv8uB4zchxPpj0IxF7'
consumer_secret = 'SUPHCNtK7QWe8fKpYwPt11CKQ9vWdGwawrrMaItEFIuuSAe9d1'
access_token = '2205718165-0nE4pGg3XxLVDQztEGdKmmiXfOkFBRPF4D7SDTm'
access_token_secret = 'n9HnBZgoH1gXUWEo8KGYepYkNHi9lyJNe3hnfEvmxxy67'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

###### Twitter Client######
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
      return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():
  def authenticate_twitter_app(self):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

class TwitterStreamer():
  """
  class for streaming and processing live tweets
  """
  def __init__(self):
    self.twitter_authenticator = TwitterAuthenticator()
  
  def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
    #This handles twitter authentication and the cpnnection to the Twitter Streaming API
    
    listener = TwitterListener(fetched_tweets_filename)
    auth = self.twitter_authenticator.authenticate_twitter_app()  
    stream = Stream(auth, listener)
  
    stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
  """
  This is a basic listener class that just prints recieved tweets to stdout
  """
  
  def __init__(self, fetched_tweets_filename):
    self.fetched_tweets_filename = fetched_tweets_filename

    
  def on_data(self, data):
    try:
      print(data)
      with open(self.fetched_tweets_filename, 'a') as tf:
        tf.write(data)
      return True
    except BaseException as e:
      print("Error on data:", str(e))
    return True
      
  
  def on_error(self, status):
    if status == 420:
        #Returning false on_data method in case limit occurs
        return False
    print(status)



if __name__ == "__main__":

  twitter_client = TwitterClient()
  tweet_analyzer = tweet_analyzer.TweetAnalyzer()
  api = twitter_client.get_twitter_client_api()

  screen_name_search = input('Ingresa cuenta a buscar: ')
  count_search = input('Ingresa tweets a buscar (máx. 100): ')
  filter_value = float(input('Ingresa el número de likes de los tweets para filtrar: '))
  quey_string_tweet = input('Ingresa término a evaluar sentimiento: ')

  tweets = api.user_timeline(screen_name=screen_name_search, count=count_search)
  tweets_search = api.search(q=quey_string_tweet, count=100, lang='es')
  """ print(dir(tweets[0].entities))
  print(tweets[0].text) """
  

  ################################
  ###Here begins searchig for the likes and retweets of an a acount
  ################################
  df = tweet_analyzer.tweets_to_data_frame(tweets)

  #print(df.head())

  # Get average length over all tweets.
  print('---------------------------')

  print(f"Promedio de likes de los últimos {count_search} tweets de", screen_name_search, ":", np.mean(df['likes']))

  number_most_liked_tweet = np.max(df['likes'])

  #Get the number of likes for the most liked tweet
  print('---------------------------')
  print(f"Número de likes del tweet más popular de los úlitmos {count_search} tweets de", screen_name_search, ":", number_most_liked_tweet)

  
  df_tweets_array = df.sort_values(by=['likes'], ascending=[False])
  df_tweet = df_tweets_array[:1]
  df_filtered = df[df['likes'].values > filter_value]

  print('---------------------------')
  print("Tweets:", df_tweets_array)
  print('---------------------------')
  print("Tweet con más likes:", df_tweet['text'])
  print('---------------------------')
  print("Filtrado:", df_filtered)
  print('---------------------------')


  #Time Series
  time_likes = pd.Series(data= df_filtered['likes'].values, index=df_filtered['date'])
  time_likes.plot(figsize=(16,4), label='likes', legend=True)

  time_likes = pd.Series(data= df_filtered['retweets'].values, index=df_filtered['date'])
  time_likes.plot(figsize=(16,4), label='retweets', legend=True)
  plt.show()
  ################################
  ###Here ends searchig for the likes and retweets of an a acount
  ################################



  
  ################################
  ###Here begins searching for the analysis of a single term search in the last 100 tweets
  ################################
  """ tweets_translated = translate_tweets.TranslateTweets()
  tweets_translated_array = tweets_translated.translate_tweets(tweets_search)

  array_without_zeros = tweets_translated.delete_zeros(tweets_translated_array)

  print(array_without_zeros)

  print('---------------------------')
  print("Promedio del análisis de sentimiento de los tweets:", np.mean(array_without_zeros))

  scores_array = np.array(array_without_zeros)
  sns.set()
  ax = sns.distplot(scores_array)
  plt.show() """
  ##################################
  ######Here ends sentiment analysis
  ##################################
  


  ################################
  ###Here begins the streamer given a list of terms
  ################################
  #hash_tag_list = ['muertos', 'asesinado', 'fallecido', 'finado']
  #fetched_tweets_filename = "tweets.txt"

  # twitter_client = TwitterClient('pycon')
  # print(twitter_client.get_user_timeline_tweets(1))
  
  #twitter_streamer = TwitterStreamer()
  #twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
  ################################
  ###Here ends the streamer given a list of terms
  ################################
