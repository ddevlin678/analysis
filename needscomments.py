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
import json
import pandas as pd
from matplotlib.animation import FuncAnimation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import timedelta
import threading

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
import statistics 
from astropy.stats import median_absolute_deviation
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.expand_frame_repr', False)
#%matplotlib.pyplot as plt
data = []
TeamAPos = int()
TeamBPos = int()
TeamANeut = int()
TeamBNeut = int()
TeamANeg = int()
TeamBNeg = int()

pos = int() 
neg = int()
neut = int()
data = []
start = datetime.datetime(2019, 3, 17, 16, 30, 00)

incEvents = {}
wordCloudNegB = []
wordCloudPosA = []
wordCloudPosB = []
wordCloudNegA = []
listofDict = []


dictionary = {
    "TeamA": ["Chelsea", "Blues","Pensioners", "CHE", "CFC", "chelseafc"],
    "TeamB": ["Everton", "Toffees",  "EVE", "EFC"]
    }
dictionary2 = {
    "TeamA": ["Chelsea", "Blues","Pensioners", "CHE", "CFC", "chelseafc"],
    "TeamB": ["Clarets", "Burnley",  "BFC"]
    }
dictionary3 = {
    "TeamA": ["ManU", "United","Manchester", "MUFC", "Reds", ],
    "TeamB": ["Everton", "Toffees",  "EVE", "EFC"]
    }
dictionary4 = {
    "TeamA": ["Arsenal", "Gunners","ARS", "AFC", "COYG"],
    "TeamB": ["Crystal", "Palace",  "Eagles", "CRY"]
    }
def wordCloud(wordcloud, title = None):
 stopwords = set(STOPWORDS)
 i = -1
 for wC in wordcloud: 
  i += 1
  new = wC
  titleList= ['Positive WordCloud TeamA', 'Positive WordCloud TeamB', 'Negative WordCloud TeamA', 'Negative WordCloud TeamB' ]
  wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(new))
  fig = plt.figure(1, figsize=(12, 12))
  fig.canvas.set_window_title(titleList[i])
  plt.axis('off')
  plt.imshow(wordcloud)
  plt.title(titleList[i])
  plt.show()

def sentiment(row, live):
 tweetObject = row[1]
 tweetObject = str(tweetObject)
 tweet = tweetObject
 tweet = ''.join(str(tweet))
 score = analyser.polarity_scores(tweet)
 lb = score['compound']
 teamType = ""
 if lb >= 0.05:
  for value in dictionary.values():
   for item in value:
    string_you_are_searching_for = r"\b" + str(item) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if item in dictionary['TeamA']:
      teamType += "A"
      wordCloudPosA.append(word_tokenize(tweet))
      global TeamAPos
      TeamAPos +=1
     if item in dictionary['TeamB']:
      teamType += "B"
      wordCloudPosB.append(word_tokenize(tweet))
      global TeamBPos
      TeamBPos +=1
   global pos 
   pos = pos + 1
   
 elif (lb > -0.05) and (lb < 0.05):
  #print("Neutral")
  for value in dictionary.values():
   for item in value:
    string_you_are_searching_for = r"\b" + str(item) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if item in dictionary['TeamA']:
      teamType += "A"
      global TeamANeut
      TeamANeut +=1
     if item in dictionary['TeamB']:
      teamType += "B"
      global TeamBNeut 
      TeamBNeut +=1
   global neut
   neut = neut + 1
    
 else:
  #print("Negative")
  for value in dictionary.values():
   for item in value:
    string_you_are_searching_for = r"\b" + str(item) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if item in dictionary['TeamA']:
      teamType += "A"
      wordCloudNegA.append(word_tokenize(tweet))
      global TeamANeg
      TeamANeg +=1
     if item in dictionary['TeamB']:
      teamType += "B"
      wordCloudNegB.append(word_tokenize(tweet))
      global TeamBNeg
      TeamBNeg +=1
   global neg
   neg = neg + 1

 
 try:
   return (lb,teamType)
 except ZeroDivisionError:
  print("")

def eventTime(row): # want to increment a count of the occurrence of any of the events types
 events = {}
 events['goal'] = ["goal", "score", "point", "shot", "strike", "kick", "on target", "net"]
 events['redCard'] = ["red card", "sent off", "foul", "sending off", "straight red"]
 events['penalty'] = ["penalty", "pen"]
 events['substitution'] = ["substitution", "sub", "injury", "subbed", "bench"]
 events['injury'] = ["injured", "injury"]
 events['freeKick'] = ["free-kick"]
 events['offside'] = ["offside"]
 events['assist'] = ["assist", "pass", "knocked on"]
 events['yellowcard'] = ["yellow", "foul", "warning", "caution"]
 
 dictkeys = ["goal","redCard","penalty","substitution","injury","freeKick","offside","assist","yellowcard"]

 for event in events:
  for h in events[event]:
   tweetObject = row[1]#.values
   tweetObject = str(tweetObject)
   if re.search(h, tweetObject, re.IGNORECASE):
    incEvents[event] +=1

with open('eveche2019-03-17-rt1.csv', 'r') as csvfile:
 readCSV = csv.reader(csvfile, delimiter=',')
 for row in readCSV:
  data.append(row)
 df = pd.DataFrame(data)
 df = df.set_index(pd.DatetimeIndex(df[2]))
 grouped = df.groupby(df.index.map(lambda t: (t.hour, t.minute)))

 teamATotalSentiment = 0
 teamBTotalSentiment = 0
 teamATotalTweets = 0
 teamBTotalTweets = 0

 myListA = []
 myListB = []
 for group in grouped:
  teamAMinuteSentiment = 0 
  teamBMinuteSentiment = 0 
  teamAMinuteTweets = 0
  teamBMinuteTweets = 0
  incEvents = {}
  incEvents['goal'] = 0
  incEvents['redCard'] = 0
  incEvents['penalty'] = 0
  incEvents['substitution'] = 0
  incEvents['injury'] = 0
  incEvents['freeKick'] = 0
  incEvents['offside'] = 0
  incEvents['assist'] = 0
  incEvents['yellowcard'] = 0
  aResult = 0
  bResult = 0
  checkLive = False
  for x in group[1:]:
   for row in x.values:
    tweetTime = row[2]

    tweetTime = datetime.datetime.strptime(tweetTime, '%Y-%m-%d  %H:%M:%S')
    firsthalf = start + timedelta(minutes=48)
    secondhalf = firsthalf + timedelta(minutes=15)
    finish = secondhalf + timedelta(minutes=48)
    live = (start <= tweetTime) and (tweetTime <= firsthalf) or (secondhalf <= tweetTime) and (tweetTime <= finish)

   #tweetSentiment refers to score between -1 and 1
    tweetTuple = sentiment(row,live)
    tweetSentiment = (tweetTuple[0])
    teamType = tweetTuple[1]

    if("A" in teamType):
     teamATotalSentiment += tweetSentiment
     teamATotalTweets += 1
     #print(teamATotalSentiment, teamATotalTweets)
   
    if("B" in teamType):
     teamBTotalSentiment += tweetSentiment
     teamBTotalTweets += 1
     #print(teamBTotalSentiment, teamBTotalTweets)

   #totalSentiment += tweetSentiment
    if (live):
     checkLive = True
     event = eventTime(row)

     tweetTuple = sentiment(row,live)
     tweetSentiment = (tweetTuple[0])
     teamType = tweetTuple[1]              
     if ("A" in teamType):
      teamAMinuteSentiment += tweetSentiment
      teamAMinuteTweets += 1
      
   
     if ("B" in teamType):
      teamBMinuteSentiment += tweetSentiment
      teamBMinuteTweets += 1
  

   #return after each minute is that still in scope

     if teamAMinuteTweets != 0:
      aResult = (teamAMinuteSentiment/teamAMinuteTweets)
     if teamBMinuteTweets != 0:
      bResult = (teamBMinuteSentiment/teamBMinuteTweets)
  if (checkLive):
   myListA.append(aResult)
   myListB.append(bResult)
   listofDict.append(incEvents)
   checkLive = False
 
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


 def plotting(myListA,myListB):
  y1= myListA[:96]
  y2= myListB[:96]
  x = [item + 1 for item in range(96)]
  x2 = [item + 1 for item in range(96)]
  plt.xlabel('Minutes during game')
  plt.ylabel('Sentiment Weight')
  plt.plot(x, y1, '-b', label='Chelsea')
  plt.plot(x2, y2, '-r', label='Everton')
  plt.legend(loc='upper left')
  plt.title('Sentiment throughout game')
  plt.show()

 def pie(TeamAPos,TeamBPos,TeamANeut, TeamBNeut,TeamANeg,TeamBNeg):
  plt.figure()
  values = [TeamAPos, TeamANeut, TeamANeg, TeamBPos, TeamBNeut, TeamBNeg] 
  labels = ['TeamAPos', 'TeamANeut', 'TeamANeg', 'TeamBPos', 'TeamBNeut', 'TeamBNeg' ] 
  plt.pie(values, labels=labels, autopct='%.2f')
  plt.show()


 plotting(myListA,myListB)
 pie(TeamAPos,TeamBPos,TeamANeut,TeamBNeut,TeamANeg,TeamBNeg)


 dictkeys = ["goal","redCard","penalty","substitution","injury","freeKick","offside","assist","yellowcard"]
 for event in dictkeys:
  eventList = []
  for i in range(0,96):#len(listofDict):
   eventList.append(listofDict[i][event])
  sd= statistics.stdev(eventList)
  median=statistics.median(eventList)
  mad = median_absolute_deviation(eventList)
  print("event",event,"sd",sd,"median",median,"mad",mad)
  for i in range(0,96):
   if eventList[i] > mad*10:#or median*1000
    print(str(event), "may of happened at minute", i) #row.index(x)
