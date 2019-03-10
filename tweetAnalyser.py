from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time 
import sys
import numpy as np
import re
import unicodedata
from __future__ import division
import numpy as np 
import re 
import json
import unicodedata 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import TextBlob
from collections import defaultdict


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""
fullTweets = []
cleanTweets = []

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
   tweetObject = []

   newTweet = tweet_text.encode('utf-8')

   if all_data['truncated'] == True:
    extended_tweet = all_data['extended_tweet']
    tweet_text = extended_tweet['full_text']
    newTweet = tweet_text.encode('utf-8', ignore)
   

   if all_data['coordinates'] == True:
    location = all_data['coordinates']
    tweetObject.append({"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : location})
   else: 
    tweetObject.append({"user_id" : user_id, "new_tweet" : newTweet, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "location" : ''})

   return(True)

  except:
   print(sys.exc_info()[0])
 
 def on_error(self, status):
  print(status)

pos = int() 
neg = int()
neut = int()
Chelsea = int()
cleanTweets = []
tweetObject = []
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

#removing any unicode characters 
def removeUnicode(tweetObject):
  for text in tweetObject[newTweet]:
    text = line.encode('utf-8')
    #print(new.decode('unicode-escape'))
    text = new.decode('unicode-escape')
    text = new.encode('utf-8')
    tweetObject['newTweet'].update(tweet)

#accessing the newTweet value in the tweetObject dictionary 
def cleanTweet(tweetObject):
    for tweet in tweetObject['newTweet']:
        tweet = np.vectorize(remove_pattern)(tweet, "RT @[\w]*:")
        tweet = np.vectorize(remove_pattern)(tweet, "@[\w]*")
        tweet = np.vectorize(remove_pattern)(tweet, "https?://[A-Za-z0-9./]*")
        tweet = np.core.defchararray.replace(tweet, "[^a-zA-Z#]", " ")
        tweetObject['newTweet'].update(tweet)
    sent(tweetObject)
    #naive(tweetObject)
    #text(tweetObject)

#not called 
def text(tweetObject):
    analysis = TextBlob(tweetObject)
    print(analysis.sentiment) 
#giving a sentiment value to each tweet text
def sent(tweetObject):
    rate = (len(tweetObject))
    pos = int() 
    neg = int()
    neut = int()
    TeamA = PremierLeague['Chelsea']
    TeamB = PremierLeague['Liverpool']
    TeamAPos = int()
    TeamBPos = int()
    TeamANeut = int()
    TeamBNeut = int()
    TeamANeg = int()
    TeamBNeg = int()
    for tweet in tweetObject['newTweet']:
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
                elif for teamNames in TeamB:
                          string_you_are_searching_for = r"\b" + teamNames + r"\b"
                          if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
                              TeamBPos = TeamBPos + 1
                else:
                    pos = pos + 1  
        elif (lb > -0.05) and (lb < 0.05):
            print("Neutral")
            for teamNames in TeamA:
                string_you_are_searching_for = r"\b" + teamNames + r"\b"
                if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
                    TeamANeut = TeamANeut + 1
                elif: for teamNames in TeamB:
                          string_you_are_searching_for = r"\b" + teamNames + r"\b"
                          if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
                              TeamBNeut = TeamBNeut + 1
                else:
                    neut = neut + 1  
        else:
            print("Negitive")
            for teamNames in TeamA:
                string_you_are_searching_for = r"\b" + teamNames + r"\b"
                if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
                    TeamANeg = TeamANeg + 1
                elif: for teamNames in TeamB:
                          string_you_are_searching_for = r"\b" + teamNames + r"\b"
                          if re.search(string_you_are_searching_for, tweet, re.IGNORECASE):
                              TeamBNeg = TeamBNeg + 1
                else:
                    neg = neg + 1   
    
    print((pos/rate) *100,"% of people tweeted postivly")
    print((neg/rate) *100,"% of people tweeted negitivly")
    print((neut/rate) *100,"% of people tweeted Neutral")
    print("out of ",rate)
    print( teamA ,"tweets: Positive",TeamAPos,"Neutral",TeamAPNeut,"Negitive",TeamANeg)
    print( teamB ,"tweets: Positive",TeamBPos,"Neutral",TeamBPNeut,"Negitive",TeamBNeg)


#not called 
def naive(tweetObject):
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]

    random.shuffle(documents)
    
    testing_set = tweetObject
    #print(documents[1])

    all_words = []
    for w in movie_reviews.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    #print(all_words.most_common(15))


    word_features = list(all_words.keys())[:3000]

    def find_features(document):
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)
            

        return features

    featuresets = [(find_features(rev), category) for (rev, category) in documents]
     
    training_set = featuresets[:1900]

    # set that we'll test against.
    testing_set = tweetObject
    
    print(type(testing_set))
    print(testing_set)

    classifier = nltk.NaiveBayesClassifier.train(training_set)

    print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)

    
#removing unicode characters from tweet text

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
twitterStream.filter(track=["#MCIvCHE"])



