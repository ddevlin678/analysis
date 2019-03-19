
from __future__ import division
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time 
import datetime
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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
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


fullTweets = []
cleanTweets = []
tweetCount = 0
TeamAPos = int()
TeamBPos = int()
TeamANeut = int()
TeamBNeut = int()
TeamANeg = int()
TeamBNeg = int()
TeamAPosLive = int()
TeamBPosLive = int()
TeamANegLive = int()
TeamBNegLive = int()
TeamANeutLive = int()
TeamBNeutLive = int()
TeamATotalLive = 0 
TeamBTotalLive = 0 
totalA = 0 
totalB = 0
pos = int() 
neg = int()
neut = int()
data = []
start = ('2019-03-17 16:30:00')
finish = ('2019-03-17 18:30:00')
fig = plt.figure() 
ax1 = fig.add_subplot(1,120,1) # need grid y 1(positive sentiment), 0, -1(negitive sentiment) by 120 minutes 
live = False


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

def inTweetAPos(TeamA, tweetObject):
 tweet = tweetObject#['new_tweet']
 hashtag = []
 for teamNames in TeamA:
  global TeamAPos
  global wordCloudPosA
  global TeamAPosLive
  string_you_are_searching_for = str(teamNames)
  if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
   TeamAPos = TeamAPos + 1
   if live == True:
    TeamAPosLive = TeamAPosLive + 1 
   wordCloudPosA.append(word_tokenize(str(tweet)))
   ht = re.findall(r"#(\w+)", tweet)
   hashtag.append(ht) 
   return(True)
 
def inTweetBPos(TeamB, tweetObject):
 tweet = tweetObject#['new_tweet']
 hashtag = []
 global TeamBPos
 global wordCloudPosB
 global TeamBPosLive
 for teamNames in TeamB:
  string_you_are_searching_for = str(teamNames)
  if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
   TeamBPos = TeamBPos + 1
   if live == True:
    TeamBPosLive = TeamBPosLive + 1  
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
   global TeamANeutLive
   print(tweet)
   TeamANeut = TeamANeut + 1
   if live == True:
    TeamANeutLive = TeamANeutLive + 1
   return(True)
 
def inTweetBNeut(TeamB, tweetObject):
 tweet = tweetObject#['new_tweet']
 for teamNames in TeamB:
  string_you_are_searching_for = str(teamNames)
  if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
   global TeamBNeut
   global TeamBNeutLive
   print(tweet)
   TeamBNeut = TeamBNeut + 1
   if live == True:
    TeamBNeutLive = TeamBNeutLive + 1
   return(True)

def inTweetANeg(TeamA, tweetObject):
 tweet = tweetObject#['new_tweet']
 hashtag = []
 global TeamANeg
 global wordCloudNegA
 global TeamANegLive
 for teamNames in TeamA:
  string_you_are_searching_for = str(teamNames)
  if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
   TeamANeg = TeamANeg + 1
   if live == True:
    TeamANegLive = TeamANegLive + 1 
   wordCloudNegA.append(word_tokenize(tweet)) 
   ht = re.findall(r"#(\w+)", tweet)
   hashtag.append(ht)
   return(True)
 
def inTweetBNeg(TeamB, tweetObject):
 tweet = tweetObject#['new_tweet']
 hashtag = []
 global TeamBNeg
 global wordCloudNegB
 global TeamBNegLive
 for teamNames in TeamB:
  string_you_are_searching_for = str(teamNames)
  if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
   TeamBNeg = TeamBNeg + 1
   if live == True:
    TeamBNegLive = TeamBNegLive + 1 
   wordCloudNegB.append(word_tokenize(tweet)) 
   ht = re.findall(r"#(\w+)", tweet)
   hashtag.append(ht)
   return(True)

def animate(i):
 xs = TeamATotalLive
 ys = TeamBTotalLive
 #xs.append(TeamATotalLive)
 #ys.append(TeamBTotalLive)
 ax1.clear()
 ax1.plot(xs, ys) #both teams average level of sentiment 

def wordCloud(wordcloud, title = None):
 stopwords = set(STOPWORDS)
 for wC in wordcloud: 
  new = wC
  wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(new))
  fig = plt.figure(1, figsize=(12, 12))
  plt.axis('off')
  if title: 
   fig.suptitle(title, fontsize=20)
   fig.subplots_adjust(top=2.3)
  plt.imshow(wordcloud)
  plt.show()



def sent(tweetObject, engl=True):
 tweet = tweetObject#['new_tweet']
 if engl:
  trans = tweet
 else: 
  trans = translator.translate(tweet).text #doesnt work 
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
  global TeamATotalLive
  global TeamBTotalLive
  TeamATotalLive = (TeamAPosLive - TeamANegLive) /(TeamAPosLive + TeamANeutLive + TeamANegLive)
  TeamBTotalLive = (TeamBPosLive - TeamBNegLive) /(TeamBPosLive + TeamBNeutLive + TeamBNegLive) 
  global totalA 
  global totalB
   #totalA = ((pos - neg) / (pos + neg + neut))
  totalA = ((TeamAPos - TeamANeg) / (TeamAPos + TeamANeg + TeamANeut))
  totalB = ((TeamBPos - TeamBNeg) / (TeamBPos + TeamBNeg + TeamBNeut))
  #plotting(totalA,totalB)
   #print( TeamA[0] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
   #print( TeamB[0] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
   #print(totalA)
   #print(totalB)
 except ZeroDivisionError:
  print("Error")

 
  #traceback.print_exc()

 
def text(tweetObject): #double checking 
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

 
def plotting(totalA, totalB): # havnt got working
 plt.plot([totalA,totalB])
 plt.ylabel('Level of Sentiment')
 plt.xlabel('Minutes in the game')
 plt.show()


def eventTime(tweetObject): # want to increment a count of the occurance of any of the events types
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
  happening = str(event)
  if re.search(happening, tweet, re.IGNORECASE):
   incEvents[happening] = +1 
  



 
with open('eveche2019-03-17.csv', 'r') as csvfile:
 readCSV = csv.reader(csvfile, delimiter=',')
 for row in readCSV:
  tweetObject = row[1]
  time1 = row[2]
  print(time1)
  while start < time1 < finish:
   live = True
   sent(tweetObject)
   text(tweetObject)
   ani = animation.FuncAnimation(fig, animate, interval=60000)
   #eventTime(tweetObject)  
  sent(tweetObject)
  text(tweetObject)
 wordcloud = [] 
 
 flat_list1 = [item for sublist in wordCloudPosA for item in sublist]
 flat_list2 = [item for sublist in wordCloudPosB for item in sublist]
 flat_list3 = [item for sublist in wordCloudNegA for item in sublist]
 flat_list4 = [item for sublist in wordCloudNegB for item in sublist]
 wordcloud.append(nltk.FreqDist(flat_list1).most_common(150))
 wordcloud.append(nltk.FreqDist(flat_list2).most_common(150))
 wordcloud.append(nltk.FreqDist(flat_list3).most_common(150))
 wordcloud.append(nltk.FreqDist(flat_list4).most_common(150))
 wordCloud(wordcloud)
 plt.show() # show graph with teams sentiment over the 120 minutes of live playing/break




