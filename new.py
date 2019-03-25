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
#pd.set_option('display.max_colwidth', -1)

data = []
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
plothot = []

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



dict = {"TeamA":"Chelsea", "TeamA": "Blues","TeamA":"Pensioners","TeamA":"CHE","TeamA":"CFC", "TeamB":"Everton", "TeamB": "Toffees","TeamB":"EVE","TeamB":"EFC" }

incEvents = {}
incEvents['goal'] = int()
incEvents['redCard'] = int()
incEvents['penalty'] = int()
incEvents['substitution'] = int()
incEvents['injury'] = int()
incEvents['freeKick'] = int()
incEvents['offside'] = int()
incEvents['assist'] = int()
incEvents['yellowcard'] = int()


wordCloudNegB = []
wordCloudPosA = []
wordCloudPosB = []
wordCloudNegA = []
xaies = []



def sent(tweetObject, engl=True):
 for row in group[1:]:
  tweetObject = row[1]
  tweetObject = str(tweetObject)
  tweet = tweetObject#['new_tweet']
  tweet = ''.join(str(tweet))

  score = analyser.polarity_scores(tweet)
  lb = score['compound']
  if lb >= 0.02:
   print("Positive")
   for value in dict.items():
    string_you_are_searching_for = r"\b" + str(value) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if dict.key["TeamA"]:
      TeamAPos +=1
     if dict.key["TeamB"]:
      TeamBPos +=1
   global pos 
   pos = pos + 1
   
  elif (lb > -0.05) and (lb < 0.02):
   print("Neutral")
   for value in dict.items():
    string_you_are_searching_for = r"\b" + str(value) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if dict.key["TeamA"]:
      TeamANeut +=1
     if dict.key["TeamB"]:
      TeamBNeut +=1
   global neut
   neut = neut + 1
    
  else:
   print("Negitive")
   for value in dict.items():
    string_you_are_searching_for = r"\b" + str(value) + r"\b"
    if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
     if dict.key["TeamA"]:
      TeamANeg +=1
     if dict.key["TeamB"]:
      TeamBNeg +=1
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
   print("d")
   totalACount = (TeamAPos + TeamANeut + TeamANeg)
   totalBCount = (TeamBPos + TeamBNeut + TeamBNeg)
   print("P")
   global TeamATotalLive
   global TeamBTotalLive
   TeamATotalLive = (TeamAPosLive - TeamANegLive) //(TeamAPosLive + TeamANeutLive + TeamANegLive)
   TeamBTotalLive = (TeamBPosLive - TeamBNegLive) //(TeamBPosLive + TeamBNeutLive + TeamBNegLive) 
   print("f")
   global totalA 
   global totalB
   #print(TeamATotalLive)
   #print(TeamBTotalLive)
   #totalA = ((pos - neg) / (pos + neg + neut))
   print("s")
   totalA = ((TeamAPos - TeamANeg) / (TeamAPos + TeamANeg + TeamANeut))
   totalB = ((TeamBPos - TeamBNeg) / (TeamBPos + TeamBNeg + TeamBNeut))
   print("g")
  #plotting(totalA,totalB)
   #print( TeamA[0] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negitive",TeamANeg)
   #print( TeamB[0] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negitive",TeamBNeg)
   #print(totalA)
   #print(totalB)
  except ZeroDivisionError:
   print("Error")

def eventTime(group): # want to increment a count of the occurrence of any of the events types
 events = {}
 

 events['goal'] = ["goal", "score", "point", "shot", "strike", "kick", "on target", "net"]
 events['redCard'] = ["red card", "sent off", "foul", "sending off", "straight red"]
 events['penalty'] = ["penalty", "pen"]
 events['substitution'] = ["substitution", "sub", "injury", "subbed", "bench"]
 events['injury'] = ["injured", "injury"]
 events['freeKick'] = ["free-kick", "sub", "injury", "subbed", "bench"]
 events['offside'] = ["offside"]
 events['assist'] = ["assist", "pass", "knocked on"]
 events['yellowcard'] = ["yellow", "foul", "warning", "caution"]
 for row in group[1:]:
  tweetObject = row[1].values
  tweetObject = str(tweetObject)
  for event in events:
   for x in events[event]:
    if re.search(x, tweetObject, re.IGNORECASE):
     incEvents[event] +=1
  return(True)
  
  

with open('eveche2019-03-17.csv', 'r') as csvfile:
 readCSV = csv.reader(csvfile, delimiter=',')
 for row in readCSV:
  print("HELLO")
  data.append(row)
 
  df = pd.DataFrame(data)
  df = df.set_index(pd.DatetimeIndex(df[2]))
  grouped = df.groupby(df.index.map(lambda t: (t.hour, t.minute)))

 for group in grouped:
  if start < time1 < finish:
   eventTime(group)
   sent(group)
  sent(group)
  #average(TeamAPosLive, TeamBPosLive, TeamANeutLive, TeamBNeutLive, TeamANegLive, TeamBNegLive)



  x = group[1]
  new = x.head(1)
  xaies1 = new[2]
  #each = [TeamATotalLive, TeamBTotalLive, xaies1]

