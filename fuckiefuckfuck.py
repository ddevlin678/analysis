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
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.expand_frame_repr', False)
#%matplotlib.pyplot as plt
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
start = datetime.datetime(2019, 3, 17, 16, 30, 00)
#finish = datetime.datetime(2019, 3, 17, 18, 30, 00)
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
PremierLeague['Manchester City'] = ["Manchester City", "City", "Cityzens", "MCI", "CTID" ,"MCFC"]
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

dict = {"TeamA":"Chelsea", "TeamA": "Blues","TeamA":"Pensioners","TeamA":"CHE","TeamA":"CFC", "TeamB":"Everton", "TeamB": "Toffees","TeamB":"EVE","TeamB":"EFC" }



incEvents = {}
wordCloudNegB = []
wordCloudPosA = []
wordCloudPosB = []
wordCloudNegA = []
listofDict = []


dictionary = {
    "TeamA": ["Chelsea", "Blues","Pensioners", "CHE", "CFC"],
    "TeamB": ["Everton", "Toffees",  "EVE", "EFC"]
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
 #global tweetCount 
 #tweetCount = tweetCount + 1 
 
 try:
   #print("pos",pos,"neg",neg,"neut",neut,"TeamAPos", TeamAPos,"TeamBPos", TeamBPos)
   #print("TeamANeut",TeamANeut,"TeamBNeut",TeamBNeut,"TeamANeg",TeamANeg,"TeamBNeg",TeamBNeg)  

   #print(((pos + TeamAPos + TeamBPos) /(tweetCount)) *100,"% of people tweeted positively")
   #print(((neg + TeamANeg + TeamBNeg)/(tweetCount)) *100,"% of people tweeted negatively")
   #print(((neut + TeamANeut + TeamBNeut)/(tweetCount)) *100,"% of people tweeted Neutral")
   total = ((pos - neg) / (pos + neg + neut))
   totalACount = (TeamAPos + TeamANeut + TeamANeg)
   totalBCount = (TeamBPos + TeamBNeut + TeamBNeg)
   global TeamATotalLive
   global TeamBTotalLive
   #TeamATotalLive = (TeamAPosLive - TeamANegLive) //(TeamAPosLive + TeamANeutLive + TeamANegLive)
   #TeamBTotalLive = (TeamBPosLive - TeamBNegLive) //(TeamBPosLive + TeamBNeutLive + TeamBNegLive) 
   global totalA 
   global totalB
   totalA = ((TeamAPos - TeamANeg) // (TeamAPos + TeamANeg + TeamANeut))
   totalB = ((TeamBPos - TeamBNeg) // (TeamBPos + TeamBNeg + TeamBNeut))

   #meant to be a tuple of score and teamtype, may not be correct syntax

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
 events['freeKick'] = ["free-kick", "sub", "injury", "subbed", "bench"]
 events['offside'] = ["offside"]
 events['assist'] = ["assist", "pass", "knocked on"]
 events['yellowcard'] = ["yellow", "foul", "warning", "caution"]
 
 

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


 #Make two lists of size for teams a and b
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
  #event = eventTime(group)
  #listofDict.append(event)
  for x in group[1:]:
   for row in x.values:
    #print(x)
    
   #tweetTime = row[0].to_string()#index=False
    tweetTime = row[2]
    
    #print(type(tweetTime))
   #print(tweetTime)
   #from dateutil import parser
   #tweetTime = parser.parse(tweetTime[3:])
    tweetTime = datetime.datetime.strptime(tweetTime, '%Y-%m-%d  %H:%M:%S')
   #print(type(tweetTime))
   #start = datetime.datetime.strptime(start, '%Y-%m-%d  %H:%M:%S')
   #finish = datetime.datetime.strptime(finish, '%Y-%m-%d  %H:%M:%S')

    firsthalf = start + timedelta(minutes=48)
    secondhalf = firsthalf + timedelta(minutes=15)
    finish = secondhalf + timedelta(minutes=48)
    #live = (start < tweetTime) and (tweetTime < finish)
    live = (start <= tweet) and (tweet <= firsthalf) or (secondhalf <= tweet) and (tweet <= finish)

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
     #listofDict.append(event)



     #print(tweetSentiment, teamType)
     tweetTuple = sentiment(row,live)
     tweetSentiment = (tweetTuple[0])
     teamType = tweetTuple[1]               #do they need on or not? 
     if ("A" in teamType):
      #print(row)
      teamAMinuteSentiment += tweetSentiment
      teamAMinuteTweets += 1
      
   
     if ("B" in teamType):
      #print(row)
      teamBMinuteSentiment += tweetSentiment
      teamBMinuteTweets += 1
     #print(teamBMinuteSentiment, teamBMinuteTweets)
     #print(teamAMinuteSentiment, teamAMinuteTweets)
  

   #return after each minute is that still in scope

     if teamAMinuteTweets != 0:
      aResult = (teamAMinuteSentiment/teamAMinuteTweets)
     if teamBMinuteTweets != 0:
      bResult = (teamBMinuteSentiment/teamBMinuteTweets)
  if (checkLive):
   myListA.append(aResult)
   myListB.append(bResult)
   listofDict.append(incEvents)
   #print(myListB,myListA)
   checkLive = False


  
  #for each count on each minute see if it is 300% bigger if so print event may have happened at that minute of game
 
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
 #for x in verified:
  #x['@whover' tweeted, which gave a sentiment reading of 'score', and with these 'follower count', 'likes' on tweet]
  

 nDict = 0 
 n1Dict = nDict + 1
 minuten = listofDict[nDict]
 minuten1 = listofDict[n1Dict]
 events = listofDict[0].keys()
 #print(listofDict)
 #print(type(minuten), minuten)
 def compare (val1, val2): 
  #print(val1, val2)
  return True if val1*1000 < val2 else False
 #lst = map(compare, minuten.values(), minuten1.values())
 #for x in minuten:
  #for y in minuten1:
    #for k: x[k] for k in x if k in y and x[k] < y[k]
     #print("grouped")
 def plotting(myListA,myListB):
  y1= myListA[]
  y2= myListB[]
  x = [item + 1 for item in range(96)]
  x2 = [item + 1 for item in range(96)]
  plt.xlabel('Sentiment Weight')
  plt.ylabel('Live sentiment')
  plt.plot(x, y1)
  plt.plot(x2, y2)

 
  plt.title('Sentiment throughout game')
  #plt.legend()
  plt.show()

 def pie(TeamAPos,TeamBPos,TeamANeut, TeamBNeut,TeamANeg,TeamBNeg):

  plt.figure()
  values = [TeamAPos, TeamANeut, TeamANeg, TeamBPos, TeamBNeut, TeamBNeg] 
  labels = ['TeamAPos', 'TeamANeut', 'TeamANeg', 'TeamBPos', 'TeamBNeut', 'TeamBNeg' ] 
  plt.pie(values, labels=labels, autopct='%.2f')
  plt.show()
 #print(len(myListB))
 plotting(myListA,myListB)
 pie(TeamAPos,TeamBPos,TeamANeut,TeamBNeut,TeamANeg,TeamBNeg)


 
 #checking = []
 #for event in events:
 # for i in range(0,119):
  # if (compare(listofDict[i][event], listofDict[i+1][event])):
   # print(event, "may of happened at minute",i+1 )
  #range(0,120)
 
 eventList2 = []
 for event in events:
  eventList = []
  for i in range(0,96):#len(listofDict):
   eventList.append(listofDict[i][event])
  eventList2.append(eventList)

 #print(eventList2)
#scrapwebsite to see if event actually happened 

  for row in eventList2:
   sd= statistics.stdev(row)
   median=statistics.median(row)
   for x in row:
    if x > sd*5:#or median*1000
     print(str(event), "may of happened at minute", row.index(x))

   #or row
  #what minutes had median + standard dev *2 or 3 

 



