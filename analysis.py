
from __future__ import division
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time 
import csv
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
from textblob import TextBlob
#from collections import defaultdict
#from text.blob import TextBlob, Word, Blobber
#from text.classifiers import NaiveBayesClassifier
#from text.taggers import NLTKTagger
import threading
import matplotlib.pyplot as plt
import nltk
import random
from nltk.corpus import movie_reviews
import traceback
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from googletrans import Translator
translator = Translator()
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import ast 

#consumer key, consumer secret, access token, access secret.
ckey="WLntuQkpDe25sCSpwdLYWidI5"
csecret="KxbCDrEJqRBs7gjc64bIuJL4dzfvklNtk6UWUN1hviPv0AVble"
atoken="263661193-2OVxXqpHP6xqRzNymLK9ACh9XbeCtIfz0bp42WCu"
asecret="WejuT8bdw9U7zLA1RNH2QC2t1rziocwgJBGlkTV47r2qL"
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
data = []

PremierLeague = {}
PremierLeague['Arsenal'] = ["Arsenal", "The Gunners", "ARS", "Gunners"]
PremierLeague['Aston Villa'] = [ "Aston Villa", "The Villains", "Villa", "AST"]
PremierLeague['Burnley'] = [ "The Clarets", "Burnley"]
PremierLeague['Chelsea'] = ["Chelsea", "The Blues", "The Pensioners", "CHE", "CFC"]
PremierLeague['Crystal Palace'] = ["Crystal Palace","Crystal", "Palace", "The Eagles", "CRY"]
PremierLeague['Everton'] =[ "Everton", "The Toffees", "EVE"]
PremierLeague['Hull City'] = ["Hull City", "Hull", "The Tigers"]
PremierLeague['Leicester City'] = ["Leicester City", "Leicester", "The Foxes", "LEI"]
PremierLeague['Liverpool'] = ["Liverpool", "The Reds", "LIV", "YNWA", "Reds", "LFC", "LFCFamily"]
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
PremierLeague['Atletico Madrid'] = ["Atletico Madrid", "ATM"]
PremierLeague['Juventus'] = ["Juventus", "JUVE" ,"JUV"]
PremierLeague['Bayern Munich'] = ["Bayern Munich", "Bayern" ,"Munich", "FCB"]
PremierLeague['Dynamo Kyiv'] = ["dynamo kyiv", "FC Dynamo Kyiv", "DYN"]

TeamA = PremierLeague['Chelsea']
TeamB = PremierLeague['Everton']

wordCloudNegB = []
wordCloudPosA = []
wordCloudPosB = []
wordCloudNegA = []


class Name:

 



#obtaining full tweet object, parsing and creating dictionary to sort are per tweet 
 def inTweetAPos(TeamA, tweetObject):
  tweet = tweetObject['new_tweet']
  hashtag = []
  for teamNames in TeamA:
   global TeamAPos
   global wordCloudPosA
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamAPos = TeamAPos + 1
    wordCloudPosA.append(word_tokenize(tweet))
    ht = re.findall(r"#(\w+)", tweet)
    hashtag.append(ht) 
    return(True)

 def inTweetBPos(TeamB, tweetObject):
  tweet = tweetObject#['new_tweet']
  hashtag = []
  global TeamBPos
  global wordCloudPosB
  for teamNames in TeamB:
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamBPos = TeamBPos + 1 
    wordCloudPosB.append(word_tokenize(tweet))
    ht = re.findall(r"#(\w+)", tweet)
    hashtag.append(ht)
    return(True)

 def inTweetANeut(TeamA, tweetObject):
  tweet = tweetObject#['new_tweet']
  for teamNames in TeamA:
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamANeut
    print(tweet)
    TeamANeut = TeamANeut + 1
    return(True)
 
 def inTweetBNeut(TeamB, tweetObject):
  tweet = tweetObject#['new_tweet']
  for teamNames in TeamB:
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    global TeamBNeut
    print(tweet)
    TeamBNeut = TeamBNeut + 1
    return(True)

 def inTweetANeg(TeamA, tweetObject):
  tweet = tweetObject#['new_tweet']
  hashtag = []
  global TeamANeg
  global wordCloudNegA
  for teamNames in TeamA:
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamANeg = TeamANeg + 1
    wordCloudNegA.append(word_tokenize(tweet)) 
    ht = re.findall(r"#(\w+)", tweet)
    hashtag.append(ht)
    return(True)
 
 def inTweetBNeg(TeamB, tweetObject):
  tweet = tweetObject#['new_tweet']
  hashtag = []
  global TeamBNeg
  global wordCloudNegB
  for teamNames in TeamB:
   string_you_are_searching_for = str(teamNames)
   if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
    TeamBNeg = TeamBNeg + 1
    wordCloudNegB.append(word_tokenize(tweet)) 
    ht = re.findall(r"#(\w+)", tweet)
    hashtag.append(ht)
    return(True)

 def wordCloud(wordCloudPosA, wordCloudNegA, wordCloudPosB, wordCloudNegB):
  #threading.Timer(60.0, wordCloud(wordCloudPosA, wordCloudNegA, wordCloudPosB, wordCloudNegB)).start()

  new = nltk.FreqDist(wordCloudPosA).most_common(20)
  wordCloudPosA = nltk.FreqDist(wordCloudPosA).most_common(20)
  wordCloudNegA = nltk.FreqDist(wordCloudNegA).most_common(20)
  wordCloudNegB = nltk.FreqDist(wordCloudPosB).most_common(20)
  wordCloudNegB = nltk.FreqDist(wordCloudNegB).most_common(20)
  
 # stopWords = set(stopwords.words('english'))
  #for word in new:
  # word = ' '.join(str(word))
  #stopwords = set(STOPWORDS)
  unique_string=(" ").join(new)
  wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
  plt.figure(figsize=(15,8))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.savefig("your_file_name"+".png", bbox_inches='tight')
  plt.show()
  plt.close()
  #stopwords = set(STOPWORDS)
  #all_words = ' '.join([text for text in wordCloud])
 # wordCloudPosA = Word_Cloud(
 #  background_color='white',
 #  stopwords=stopwords,
 #  width=1600,
 #  height=800,
 #  random_state=21,
 #  colormap='jet',
 #  max_words=50,
 #  max_font_size=200).generate(all_words)
 # plt.figure(figsize=(12, 10))
  #plt.axis('off')
  #plt.imshow(wordCloudPosA, interpolation="bilinear");


 def sent(tweetObject, engl=True):
  tweet = tweetObject#['new_tweet']
  if engl:
   trans = tweet
  else: 
   trans = translator.translate(tweet).text
  tweet = trans
  tweet = tweetObject#['new_tweet']
  tweet = ''.join(str(tweet))

  score = analyser.polarity_scores(tweet)
  lb = score['compound']
  if lb >= 0.02:
   print("Positive")
   inTweetAPos(TeamA, tweetObject)
   inTweetBPos(TeamB, tweetObject)
   global pos 
   pos = pos + 1

  elif (lb > -0.05) and (lb < 0.02):
   print("Neutral")
   inTweetANeut(TeamA, tweetObject)
   inTweetBNeut(TeamB, tweetObject)
   global neut
   neut = neut + 1
    
  else:
   print("Negitive")
   inTweetANeg(TeamA, tweetObject)
   inTweetBNeg(TeamB, tweetObject)
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
   total = ((pos - neg) / (pos + neg + neut))
   totalACount = (TeamAPos + TeamANeut + TeamANeg)
   totalBCount = (TeamBPos + TeamBNeut + TeamBNeg)
   #120 index 
   global totalA 
   global totalB
   #totalA = ((pos - neg) / (pos + neg + neut))
   totalA = ((TeamAPos - TeamANeg) / (TeamAPos + TeamANeg + TeamANeut))
   totalB = ((TeamBPos - TeamBNeg) / (TeamBPos + TeamBNeg + TeamBNeut))
   plotting(totalA,totalB)
   #print( TeamA[0] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
   #print( TeamB[0] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
   #print(totalA)
   #print(totalB)
  except ZeroDivisionError:
   print("Error")


  #traceback.print_exc()

 
 def text(tweetObject):
  tweet = tweetObject#['new_tweet']
  analysis = TextBlob(tweet)
  print(analysis.sentiment)
  if analysis.sentiment[0]>0:
   print('Positive1')
  elif analysis.sentiment[0]<0:
   print('Negative1')
  else:
   print('Neutral1')
  #analysis = TextBlob(tweet)

  #print(analysis.sentiment) 

 
 def plotting(totalA, totalB):
  #threading.Timer(60.0, plotting).start()
  plt.plot([totalA,totalB])
  plt.ylabel('Level of Sentiment')
  plt.xlabel('Minutes in the game')
  plt.show()

  #for word.value in wordCloud: #cause its a dictionary
   # if eventWord in events:

 def eventTime(tweetObject):
  #threading.Timer(60.0, eventTime).start() 
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

  events['goal'] = ["goal", "score", "point", "shot", "strike", "kick", "on target", "net"]
  events['redCard'] = ["red card", "sent off", "foul", "sending off", "straight red"]
  events['penalty'] = ["penalty", "pen"]
  events['substitution'] = ["substitution", "sub", "injury", "subbed", "bench"]
  events['injury'] = ["injured", "injury"]
  events['freeKick'] = ["free-kick", "sub", "injury", "subbed", "bench"]
  events['offside'] = ["offside"]
  events['assist'] = ["assist", "pass", "knocked on"]
  events['yellowcard'] = ["yellow", "foul", "warning", "caution"]
  

  for event in events:
   tweet = tweetObject#['new_tweet']
   if re.search(event, tweet, re.IGNORECASE):
    incEvents['event'] = +1 
  print(incEvents)
    #if count in incEvents if it is exceeded average by 400%
 
 with open('eveche7.csv', 'r') as csvfile:
  readCSV = csv.reader(csvfile, delimiter=',')
  #data = ast.literal_eval(csvfile.read())
  for row in readCSV:
  
   tweetObject = row[1]
   #tweetObject = dict(itertools.zip_longest(*[iter(row)] * 2, fillvalue=""))   
   #print(tweetObject)
   sent(tweetObject)
   text(tweetObject)
   eventTime(tweetObject)



