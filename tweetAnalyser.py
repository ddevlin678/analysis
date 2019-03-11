from __future__ import division
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time 
import sys
import numpy as np
import re
import unicodedata
import numpy as np 
import re 
import json
import unicodedata 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
#import TextBlob
from collections import defaultdict
from textblob import TextBlob, Word, Blobber
from textblob.classifiers import NaiveBayesClassifier
from textblob.taggers import NLTKTagger
import threading
import matplotlib.pyplot as plt


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""
fullTweets = []
cleanTweets = []

#tweetObject = []

class listener(StreamListener):
#obtaining full tweet object, parsing and creating dictionary to sort are per tweet 
 def on_data(self, data):
  try:

   all_data = json.loads(data)
   tweet_text = all_data['text']
   user_id = all_data['id']
   user = all_data['user']
   f_count = user['followers_count']
   retweet_count = all_data['retweet_count']
   favorite_count = all_data['favorite_count']

   newTweet = (tweet_text.encode('ascii', 'ignore')).decode("utf-8")
   newTweet = re.sub('RT @[\w]*:',  '',    newTweet)
   newTweet = re.sub('@[\w]*',  '',    newTweet)
   newTweet = re.sub('https?://[A-Za-z0-9./]*',  '',    newTweet)

   
   #print(newTweet)
   #newTweet = np.vectorize(remove_pattern)(newTweet, "RT @[\w]*:")
   #newTweet = np.vectorize(remove_pattern)(newTweet, "@[\w]*")
   #newTweet = np.vectorize(remove_pattern)(newTweet, "https?://[A-Za-z0-9./]*")
   #newTweet = np.core.defchararray.replace(newTweet, "[^a-zA-Z#]", " ")

   if all_data['truncated'] == True:
    extended_tweet = all_data['extended_tweet']
    tweet_text = extended_tweet['full_text']
    #newTweet = tweet_text.encode('utf-8')
    newTweet = (tweet_text.encode('ascii', 'ignore')).decode("utf-8")
    newTweet = re.sub('RT @[\w]*:',  '',    newTweet)
    newTweet = re.sub('@[\w]*',  '',    newTweet)
    newTweet = re.sub('https?://[A-Za-z0-9./]*',  '',    newTweet)
    #newTweet = np.core.defchararray.replace(newTweet, "[^a-zA-Z#]", " ")
       

   if all_data['coordinates'] == True:
    location = all_data['coordinates']
    tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : location}
    
   else: 
    tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : ''}

   #print(tweetObject['new_tweet'])

   sent(tweetObject)

   #threading.Timer(60.0, cleanTweet(tweetObject)).start()
   #print(tweetObject.keys())
   
   
    

   #return(True)

  except:
   print(sys.exc_info()[0])
 
 def on_error(self, status):
  print(status)

pos = int() 
neg = int()
neut = int()
Chelsea = int()


#list of team names and their alias for searching tweets against
PremierLeague = {}
PremierLeague['Arsenal'] = ["Arsenal", "The Gunners", "ARS"]
PremierLeague['Aston Villa'] = [ "Aston Villa", "The Villains", "Villa", "AST"]
PremierLeague['Burnley'] = [ "The Clarets", "Burnley"]
PremierLeague['Chelsea'] = ["Chelsea", "The Blues", "The Pensioners", "CHE"]
PremierLeague['Crystal Palace'] = ["Crystal Palace","Crystal", "Palace", "The Eagles", "CRY"]
PremierLeague['Everton'] =[ "Everton", "The Toffees", "EVE"]
PremierLeague['Hull City'] = ["Hull City", "Hull", "The Tigers"]
PremierLeague['Leicester City'] = ["Leicester City", "Leicester", "The Foxes", "LEI"]
PremierLeague['Liverpool'] = ["Liverpool", "The Reds", "LIV"]
PremierLeague['Manchester City'] = ["Manchester City", "City", "The Citizens", "MCI"]
PremierLeague['Manchester United'] = ["Manchester United", "United", "The Red Devils", "MUN"]
PremierLeague['Newcastle United'] = ["Newcastle United", "Newcastle", "The Magpies", "NEW"]
PremierLeague['Queens Park Rangers'] = ["Queens Park Rangers", "Super Hoops", "QPR"]
PremierLeague['Southampton'] = ["Southampton", "The Saints", "SOU"]
PremierLeague['Stoke City'] = ["Stoke City", "The Potters", "STK"]
PremierLeague['Sunderland'] = ["Sunderland", "The Black Cats", "SUN"]
PremierLeague['Swansea City'] = ["Swansea City", "Swansea", "The Swans", "SWA"]
PremierLeague['Tottenham Hotspur'] = ["Tottenham Hotspur", "Tottenham", "The Spurs", "TOT"]
PremierLeague['Watford'] = ["Watford", "Hornets", "Yellow Army", "WFC"]
PremierLeague['West Bromwich Albion'] = ["West Bromwich" "Albion", "West Bromwich", "The Baggies", "WBA"]
PremierLeague['West Ham United'] = ["West Ham United", "West Ham",  "The Hammers", "WHU"]



import nltk
import random
from nltk.corpus import movie_reviews

#remove function used inside cleanTweets
def remove_pattern(tweet_text, pattern):
 r = re.findall(pattern, tweet_text)
 for i in r:
  tweet_text = re.sub(i, '', tweet_text)   
 return tweet_text     


#accessing the newTweet value in the tweetObject dictionary 
def cleanTweet(tweetObject):
 print(tweet) # prints keys with no values
 print(tweet['new_tweet']) #prints class 'TypeError' 
 tweet = str(tweetObject['new_tweet'])
 tweet = np.vectorize(remove_pattern)(tweet, "RT @[\w]*:")
 tweet = np.vectorize(remove_pattern)(tweet, "@[\w]*")
 tweet = np.vectorize(remove_pattern)(tweet, "https?://[A-Za-z0-9./]*")
 tweet = np.core.defchararray.replace(tweet, "[^a-zA-Z#]", " ")
 tweetObject['new_tweet'] = tweet
 #sent(tweetObject)
 #eventTime(tweetObject)
    #naive(tweetObject)
    #text(tweetObject)

#not called 
def text(tweetObject):
 analysis = TextBlob(tweetObject)
 print(analysis.sentiment) 
#giving a sentiment value to each tweet text
def sent(tweetObject):
 
 print("HELLO")
 rate = (len(tweetObject))
 pos = int() 
 neg = int()
 neut = int()
 TeamA = PremierLeague['Arsenal']
 TeamB = PremierLeague['Manchester United']
 TeamAPos = int()
 TeamBPos = int()
 TeamANeut = int()
 TeamBNeut = int()
 TeamANeg = int()
 TeamBNeg = int()
 #for tweet in tweetObject:
 tweet = tweetObject['new_tweet']
 print(tweet)
 tweet = ''.join(str(tweet))
      #text(item)
      #naive(item)
 score = analyser.polarity_scores(tweet)
 lb = score['compound']
 if lb >= 0.05:
  print("Positive")
  for teamNames in TeamA:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamAPos = TeamAPos + 1
              
   if TeamAPos == 0:
    for teamNames in TeamB:
      string_you_are_searching_for = r"\b" + teamNames + r"\b"
      if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
       TeamBPos = TeamBPos + 1
       if TeamAPos == 0 and TeamBPos == 0:
        pos = pos + 1

 elif (lb > -0.05) and (lb < 0.05):
  print("Neutral")
  for teamNames in TeamA:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamANeut = TeamANeut + 1
              
  if TeamANeut == 0:
   for teamNames in TeamB:
    string_you_are_searching_for = r"\b" + teamNames + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     TeamBNuet = TeamBNeut + 1
     if TeamANeut == 0 and TeamBNeut == 0:
      neut = neut + 1 
   else:
    print("Negitive")
    for teamNames in TeamA:
     string_you_are_searching_for = r"\b" + teamNames + r"\b"
     if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
      TeamANeg = TeamANeg + 1
              
    if TeamANeg == 0:
     for teamNames in TeamB:
      string_you_are_searching_for = r"\b" + teamNames + r"\b"
      if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
       TeamBNeg = TeamBNeg + 1
       if TeamANeg == 0 and TeamBNeg == 0:
        neg = neg + 1
 print("GE")
 tweetCount = tweetCount + 1 
 
 try:
 
  print((pos/tweetCount) *100,"% of people tweeted postivly")
  print((neg/tweetCount) *100,"% of people tweeted negitivly")
  print((neut/tweetCount) *100,"% of people tweeted Neutral")
  print("out of ",tweetCount)
  total = (pos - neg / pos + neg + neut)
  totalA = (TeamApos - TeamAneg / TeamApos + TeamAneg + TeamAneut)
  totalB = (TeamBpos - TeamBneg / TeamBpos + TeamBneg + TeamBneut)
  print( TeamA[1] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
  print( TeamB[1] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
 
 except ZeroDivisionError:
  total = float('Inf')
  totalA = float('Inf')
  totalB = float('Inf')
  print( TeamA[1] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
  print( TeamB[1] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
    
def plotting():
 plt.plot([totalA,totalB])
 plt.ylabel('Level of Sentiment')
 plt.xlabel('Minutes in the game')
 plt.show()
 
def eventTime(tweetObject):
 events = {}
 incEvents = {}
 incEvents['goal'] = [int()]
 incEvents['redCard'] = [int()]
 incEvents['penalty'] = [int()]
 incEvents['substitution'] = [int()]
 incEvents['injury'] = [int()]
 incEvents['freeKick'] = [int()]
 incEvents['offside'] = [int()]
 incEvents['assist'] = [int()]
 incEvents['yellowcard'] = [int()]

 events['goal'] = ["goal", "score", "point", "shot", "strike", "kick", "on target"]
 events['redCard'] = ["red card", "sent off", "foul", "sending off", "straight red"]
 events['penalty'] = ["penalty", "pen"]
 events['substitution'] = ["substitution", "sub", "injury", "subbed", "bench"]
 events['injury'] = ["injured", "injury"]
 events['freeKick'] = ["free-kick", "sub", "injury", "subbed", "bench"]
 events['offside'] = ["offside"]
 events['assist'] = ["assist", "pass", "knocked on"]
 events['yellowcard'] = ["yellow", "foul", "warning", "caution"]

 for event in events:
  tweet = tweetObject['new_tweet']
  if re.search(event, tweet, re.IGNORECASE):
   incEvents['event'] = +1 

    #if count in incEvents if it is exceeded average by 400%
          
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
twitterStream.filter(track=["#ARSMUN"])











