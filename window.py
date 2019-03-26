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
pd.set_option('display.expand_frame_repr', False)

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

dictionary = {
    "TeamA": ["Chelsea", "Blues","Pensioners", "CHE", "CFC"],
    "TeamB": ["Everton", "Toffees",  "EVE", "EFC"]
    }


dictionary2 = {
    "Chelsea": "TeamA",
    "Blues": "TeamA",
    "Pensioners": "TeamA",
    "CHE": "TeamA",
    "CFC": "TeamA",
    "Everton": "TeamB",
    "Toffees": "TeamB",
    "EVE": "TeamB",
    "EFC": "TeamB"
    }


def sent(tweetObject, engl=True):
 for row in group[1:]:
  tweetObject = row[1]
  print(type(tweetObject), tweetObject)
  tweetObject = str(tweetObject)
  tweet = tweetObject#['new_tweet']
  tweet = row[1].to_string(index=False)
  tweet = ''.join(str(tweet))

  score = analyser.polarity_scores(tweet)
  lb = score['compound']
  if lb >= 0.05:
   print("Positive")
   #for value in dict.items():
   for value in dictionary.values():
    for item in value:
     string_you_are_searching_for = r"\b" + str(item) + r"\b"
     if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
      if 'TeamA' in dictionary.keys():
       global TeamAPos
       TeamAPos +=1
       #print(tweet)
       if live == True:
        global TeamAPosLive		  
        TeamAPosLive +=1
      if 'TeamB' in dictionary.keys():
       global TeamBPos
       TeamBPos +=1
       if live == True:
        global TeamBPosLive	  
        TeamBPosLive +=1
    global pos 
    pos = pos + 1
   
  elif (lb > -0.05) and (lb < 0.05):
   print("Neutral")
   for value in dictionary.values():
    #print(type(value))
    for item in value:
     string_you_are_searching_for = r"\b" + str(item) + r"\b"
     if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
      if 'TeamA' in dictionary.keys():
       global TeamANeut
       TeamANeut +=1
       if live == True:
        global TeamANegLive	  
        TeamANeutLive +=1
      if 'TeamB' in dictionary.keys():
       global TeamBNeut 
       TeamBNeut +=1
       if live == True:
        global TeamBNeutLive	  
        TeamBNeutLive +=1
    global neut
    neut = neut + 1
    
  else:
   print("Negative")
   for value in dictionary.values():
    #print(type(value))
    for item in value:
     string_you_are_searching_for = r"\b" + str(item) + r"\b"
     if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
      if 'TeamA' in dictionary.keys():
       global TeamANeg
       TeamANeg +=1
       if live == True:
        global TeamANegLive	  
        TeamANegLive +=1
      if 'TeamB' in dictionary.keys():
       global TeamBNeg
       TeamBNeg +=1
       if live == True:
        global TeamBNegLive	  
        TeamBNegLive +=1
    global neg
    neg = neg + 1
   global tweetCount 
   tweetCount = tweetCount + 1 
  
  try:
   #print("pos",pos,"neg",neg,"neut",neut,"TeamAPos", TeamAPos,"TeamBPos", TeamBPos)
   #print("TeamANeut",TeamANeut,"TeamBNeut",TeamBNeut,"TeamANeg",TeamANeg,"TeamBNeg",TeamBNeg)  

   #print(((pos + TeamAPos + TeamBPos) /(tweetCount)) *100,"% of people tweeted positively")
   #print(((neg + TeamANeg + TeamBNeg)/(tweetCount)) *100,"% of people tweeted negatively")
   #print(((neut + TeamANeut + TeamBNeut)/(tweetCount)) *100,"% of people tweeted Neutral")
   #print("out of ",tweetCount)
   total = ((pos - neg) / (pos + neg + neut))
   print("d")
   totalACount = (TeamAPos + TeamANeut + TeamANeg)
   totalBCount = (TeamBPos + TeamBNeut + TeamBNeg)
   print("P")
   global TeamATotalLive
   global TeamBTotalLive
   #TeamATotalLive = (TeamAPosLive - TeamANegLive) //(TeamAPosLive + TeamANeutLive + TeamANegLive)
   #TeamBTotalLive = (TeamBPosLive - TeamBNegLive) //(TeamBPosLive + TeamBNeutLive + TeamBNegLive) 
   print("f")
   global totalA 
   global totalB
   #print(TeamATotalLive)
   #print(TeamBTotalLive)
   #totalA = ((pos - neg) / (pos + neg + neut))
   print("s")
   totalA = ((TeamAPos - TeamANeg) // (TeamAPos + TeamANeg + TeamANeut))
   totalB = ((TeamBPos - TeamBNeg) // (TeamBPos + TeamBNeg + TeamBNeut))
   print("g")
  #plotting(totalA,totalB)
   #print( TeamA[0] ,"tweets: Positive",TeamAPos,"Neutral",TeamANeut,"Negative",TeamANeg)
   #print( TeamB[0] ,"tweets: Positive",TeamBPos,"Neutral",TeamBNeut,"Negative",TeamBNeg)
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
  tweetObject = row[1]#.values
  tweetObject = str(tweetObject)
  for event in events:
   for x in events[event]:
    if re.search(x, tweetObject, re.IGNORECASE):
     incEvents[event] +=1
  return(True)
  
  

with open('eveche2019-03-17-rt1.csv', 'r') as csvfile:
 readCSV = csv.reader(csvfile, delimiter=',')
 for row in readCSV:
  data.append(row)
 #group is a tuple and then row is a panda 
 df = pd.DataFrame(data)
 df = df.set_index(pd.DatetimeIndex(df[2]))
 grouped = df.groupby(df.index.map(lambda t: (t.hour, t.minute)))
 for group in grouped:
  for row in group:
    print(row)
   #print(type(row),row)
   #print(len(row.index))
   #new = next(row.iterrows())[1] 
  #for line in row:
    #print(type(line), line)
   #tweetTime = row[2].to_string(index=False)
   #if start < tweetTime < finish:
    #sent(group)
    #eventTime(group)
    #live = True
   #else:
    #live = False
   
    

    #print(group[0])
   #eventTime(group)
   #sent(group)
   # sent(group)
  #average(TeamAPosLive, TeamBPosLive, TeamANeutLive, TeamBNeutLive, TeamANegLive, TeamBNegLive)



  #x = group[1]
  #new = x.head(1)
  #xaies1 = new[2]
  #each = [TeamATotalLive, TeamBTotalLive, xaies1]
