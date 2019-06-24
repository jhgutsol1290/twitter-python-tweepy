from textblob import TextBlob
import numpy as np

class TranslateTweets():
  def translate_tweets(self, tweets):
    array_of_tweets = np.array([tweet.text for tweet in tweets])
    array_of_tweets_translated = []
    for tweet in array_of_tweets:
      t = TextBlob(tweet)
      ten = t.translate(to="en")
      array_of_tweets_translated.append(ten.sentiment[0])
    return array_of_tweets_translated

  def delete_zeros(self, array_of_tweets_translated):
    new_score_list = []
    for score in array_of_tweets_translated:
      if score == 0:
        pass
      else:
        new_score_list.append(score)
    return new_score_list