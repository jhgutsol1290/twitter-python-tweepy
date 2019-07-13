from textblob import TextBlob
import numpy as np

class TranslateTweets():
  def __init__(self, array_of_tweets_translated=[], array_of_tweets_and_score=[]):
    self.array_of_tweets_translated = array_of_tweets_translated
    self.array_of_tweets_and_score = array_of_tweets_and_score

  def translate_tweets(self, tweets):
    array_of_tweets = np.array([tweet.full_text for tweet in tweets])
    #array_of_tweets_translated = []
    #array_tweets_score = []
    for tweet in array_of_tweets:
      t = TextBlob(tweet)
      ten = t.translate(to="en")
      self.array_of_tweets_translated.append(ten.sentiment[0])
      self.array_of_tweets_and_score.append({"text": tweet, "score": ten.sentiment[0]})
    return self.array_of_tweets_translated
  
  def array_of_tweets_and_score_method(self):
    return self.array_of_tweets_and_score
  
  def myFunc(self, tweets):
    my_list = np.array([tweet.full_text for tweet in tweets])
    array_tweets_score = []
    for tweet in my_list:
      t = TextBlob(tweet)
      ten = t.translate(to="en")
      array_tweets_score.append({"text": tweet, "score": ten.sentiment[0]})
    return array_tweets_score

  def order_array_of_tweets_postive(self, array_tweets_score):
    array_positive = []
    for element in array_tweets_score:
      if element['score'] > 0:
        array_positive.append(element)
    return array_positive

  def order_array_of_tweets_negative(self, array_tweets_score):
    array_negative = []
    for element in array_tweets_score:
      if element['score'] < 0:
        array_negative.append(element)
    return array_negative
  
  def text_positive_only(self, array_positive):
    text_positive = []
    for comment in array_positive:
      text_positive.append(comment['text'])
    return text_positive

  def text_negative_only(self, array_negative):
    text_negative = []
    for comment in array_negative:
      text_negative.append(comment['text'])
    return text_negative

  def delete_zeros(self, array_of_tweets_translated):
    new_score_list = []
    for score in self.array_of_tweets_translated:
      if score == 0:
        pass
      else:
        new_score_list.append(score)
    return new_score_list
  
  def calculate_percentage_neutral(self):
    total = len(self.array_of_tweets_translated)
    neutral = []
    for score in self.array_of_tweets_translated:
      if score == 0:
        neutral.append(score)
    neutral_result = len(neutral) * 100 / total
    return neutral_result
  
  def calculate_percentage_positive(self):
    total = len(self.array_of_tweets_translated)
    positive = []
    for score in self.array_of_tweets_translated:
      if score > 0:
        positive.append(score)
    positive_result = len(positive) * 100 / total
    return positive_result

  def calculate_percentage_negative(self):
    total = len(self.array_of_tweets_translated)
    negative = []
    for score in self.array_of_tweets_translated:
      if score < 0:
        negative.append(score)
    negative_result = len(negative) * 100 / total
    return negative_result