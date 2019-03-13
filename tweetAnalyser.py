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
import nltk
import random
from nltk.corpus import movie_reviews
import traceback
from nltk.tokenize import word_tokenize
#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""
fullTweets = []
cleanTweets = []
tweetCount = 0
TeamAPos = int()
TeamBPos = int()
TeamANeut = int()
TeamBNeut = int()
TeamANeg = int()
TeamBNeg = int()
totalA = 0 
totalB = 0
pos = int() 
neg = int()
neut = int()

PremierLeague = {}
PremierLeague['Arsenal'] = ["Arsenal", "The Gunners", "ARS", "Gunners"]
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
PremierLeague['FC Schalke 04'] = ["FC Schalke 04", "Schalke", "The Royal Blues", "S04"]



class listener(StreamListener):
#obtaining full tweet object, parsing and creating dictionary to sort are per tweet 
 def inTweetAPos(self, TeamA, tweetObject):
  tweet = tweetObject['new_tweet']
  posWordsTeamA = {}
  for teamNames in TeamA:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamAPos
    TeamAPos = TeamAPos + 1
    #posWordsTeamA.append(word_tokenize(tweet))
    wordCloudPosA = nltk.FreqDist(word_tokenize(tweet)) 
    return(True)
 
 def inTweetBPos(self, TeamB, tweetObject):
  tweet = tweetObject['new_tweet']
  posWordsTeamB = []
  for teamNames in TeamB:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamBPos
    TeamBPos = TeamBPos + 1
    posWordsTeamB.append(word_tokenize(tweet))
    wordCloudPosB = nltk.FreqDist(word_tokenize(tweet)) 
    return(True)

 def inTweetANeut(self, TeamA, tweetObject):
  tweet = tweetObject['new_tweet']
  for teamNames in TeamA:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamANeut
    TeamANeut = TeamANeut + 1
    #neutWordsTeamA.append(word_tokenize(tweet))
    return(True)
 
 def inTweetBNeut(self, TeamB, tweetObject):
  tweet = tweetObject['new_tweet']
  for teamNames in TeamB:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamBNeut
    TeamBNeut = TeamBNeut + 1
    #neutWordsTeamB.append(word_tokenize(tweet)) dont feel its worth mentioning
    return(True)

 def inTweetANeg(self,TeamA, tweetObject):
  tweet = tweetObject['new_tweet']
  for teamNames in TeamA:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamANeg
    TeamANeg = TeamANeg + 1
    wordCloud = nltk.FreqDist(negWordsTeamA) 
    return(True)
 
 def inTweetBNeg(self, TeamB, tweetObject):
  tweet = tweetObject['new_tweet']
  for teamNames in TeamB:
   string_you_are_searching_for = r"\b" + teamNames + r"\b"
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamBNeg
    TeamBNeg = TeamBNeg + 1
    negWordsTeamB.append(word_tokenize(tweet))
    wordCloud = nltk.FreqDist(negWordsTeamB)
    return(True)

 def word_cloud(wordCloud):
  stopwords = set(STOPWORDS)
  all_words = ' '.join([text for text in wordCloud])
  wordcloud = Word_Cloud(
   background_color='white',
   stopwords=stopwords,
   width=1600,
   height=800,
   random_state=21,
   colormap='jet',
   max_words=50,
   max_font_size=200).generate(all_words)
  plt.figure(figsize=(12, 10))
  plt.axis('off')
  plt.imshow(wordcloud, interpolation="bilinear");


 def sent(self, tweetObject):
  #pos = int() 
  #neg = int()
  #neut = int()
  TeamA = PremierLeague['FC Schalke 04']
  TeamB = PremierLeague['Manchester City']
  #TeamAPos = int()
  #TeamBPos = int()
  #TeamANeut = int()
  #TeamBNeut = int()
  #TeamANeg = int()
  #TeamBNeg = int()
  tweet = tweetObject['new_tweet']
  tweet = ''.join(str(tweet))

  score = analyser.polarity_scores(tweet)
  lb = score['compound']
  if lb >= 0.05:
   print("Positive")
   self.inTweetAPos(TeamA, tweetObject)
   self.inTweetBPos(TeamB, tweetObject)
  
   
   global pos 
   pos = pos + 1

  elif (lb > -0.05) and (lb < 0.05):
   print("Neutral")
   self.inTweetANeut(TeamA, tweetObject)
   self.inTweetBNeut(TeamB, tweetObject)
   global neut
   neut = neut + 1
    
  else:
   print("Negitive")
   self.inTweetANeg(TeamA, tweetObject)
   self.inTweetBNeg(TeamB, tweetObject)
   global neg
   neg = neg + 1
  global tweetCount 
  tweetCount = tweetCount + 1 
 
  try:
   print("pos",pos,"neg",neg,"neut",neut,"TeamAPos", TeamAPos,"TeamBPos", TeamBPos)
   print("TeamANeut",TeamANeut,"TeamBNeut",TeamBNeut,"TeamANeg",TeamANeg,"TeamBNeg",TeamBNeg)

   #print(((pos + TeamAPos + TeamBPos) /(tweetCount)) *100,"% of people tweeted postivly")
   #print(((neg + TeamANeg + TeamBNeg)/(tweetCount)) *100,"% of people tweeted negitivly")
   #print(((neut + TeamANeut + TeamBNeut)/(tweetCount)) *100,"% of people tweeted Neutral")
   #print("out of ",tweetCount)
  #total = (pos - neg / pos + neg + neut)
   totalACount = (TeamAPos + TeamANeut + TeamANeg)
   totalBCount = (TeamBPos + TeamBNeut + TeamBNeg)
 
   global totalA 
   global totalB
   #totalA = ((pos - neg) / (pos + neg + neut))
   totalA = ((TeamAPos - TeamANeg) / (TeamAPos + TeamANeg + TeamANeut))
   totalB = ((TeamBPos - TeamBNeg) / (TeamBPos + TeamBNeg + TeamBNeut))
   #print( TeamA[0] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
   #print( TeamB[0] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
   #print(totalA)
   #print(totalB)
  except ZeroDivisionError:
   print("Error")


  #traceback.print_exc()

 def on_data(self, data):
  #try:

  all_data = json.loads(data)
  tweet_text = all_data['text']
  user_id = all_data['id']
  user = all_data['user']
  time = all_data['created_at']
  f_count = user['followers_count']
  retweet_count = all_data['retweet_count']
  favorite_count = all_data['favorite_count']

  newTweet = (tweet_text.encode('ascii', 'ignore')).decode("utf-8")
  newTweet = re.sub('RT @[\w]*:',  '',    newTweet)
  newTweet = re.sub('@[\w]*',  '',    newTweet)
  newTweet = re.sub('https?://[A-Za-z0-9./]*',  '',    newTweet)


  if all_data['truncated'] == True:
   extended_tweet = all_data['extended_tweet']
   tweet_text = extended_tweet['full_text']
    #newTweet = tweet_text.encode('utf-8')
   newTweet = (tweet_text.encode('ascii', 'ignore')).decode("utf-8")
   newTweet = re.sub('RT @[\w]*:',  '',    newTweet)
   newTweet = re.sub('@[\w]*',  '',    newTweet)
   newTweet = re.sub('https?://[A-Za-z0-9./]*',  '',    newTweet)
       

  if all_data['coordinates'] == True:
   location = all_data['coordinates']
   tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : location}

  else: 
   tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : ''}
    
  self.sent(tweetObject)
    

   #threading.Timer(60.0, cleanTweet(tweetObject)).start()
   #print(tweetObject.keys())

   #return(True)

  #except:
   #print(sys.exc_info()[0])
 
 def on_error(self, status):
  print(status)

 def text(self, tweetObject):
  analysis = TextBlob(tweetObject)
  print(analysis.sentiment) 

 
 def plotting():
  plt.plot([totalA,totalB])
  plt.ylabel('Level of Sentiment')
  plt.xlabel('Minutes in the game')
  plt.show()

  #for word.value in wordCloud: #cause its a dictionary
   # if eventWord in events:

 

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
twitterStream.filter(track=["#UCL"])
