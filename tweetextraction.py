import tweepy
import csv
import pandas as pd
import re
import json
import socket
import pytz
####input your credentials here
ckey=""
csecret=""
atoken=""
asecret=""
counter = 0 
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
with open('chebur1345.csv', 'a', newline='') as output:
 for all_data in tweepy.Cursor(api.search,q="#CHEBUR -filter:retweets",
                           lang = "en",
                           tweet_mode = "extended",
                           since = "2019-04-22",
                           until = "2019-04-23").items():

  try:
   tweet_text = all_data.full_text
   print(tweet_text)
   user_id = all_data.id
   user = all_data.user
   tweetTime = all_data.created_at
   screen_name = user.screen_name 
   f_count = user.followers_count
   retweet_count = all_data.retweet_count
   favorite_count = all_data.favorite_count
   entities = all_data.entities
   verified = user.verified
   hashtags = all_data.entities.get('hashtags')
#data preprocessing- removal of unwanted characters
   newTweet = (tweet_text.encode('ascii', 'ignore')).decode("utf-8")
   newTweet = re.sub('RT @[\w]*:',  '',    newTweet)
   newTweet = re.sub('@[\w]*',  '',    newTweet)
   newTweet = re.sub('https?://[A-Za-z0-9./]*',  '',    newTweet)
   print(newTweet)
   
   if all_data.coordinates == True:
    location = all_data.coordinates
    tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "time" : tweetTime, "verified" : verified, "hashtags" : hashtags,  "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count,"hashtags": 'hashtags', "location" : location}
    dict_writer = csv.DictWriter(output, tweetObject)
    dict_writer.writerow(tweetObject)
    counter = counter + 1 
    print(counter)

   else: 
    tweetObject = {"user_id" : user_id, "new_tweet" : newTweet, "time" : tweetTime, "verified" : verified, "hashtags" : hashtags, "f_count" : f_count, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "hashtags": 'hashtags', "location" : ''}
    dict_writer = csv.DictWriter(output, tweetObject)
    dict_writer.writerow(tweetObject)
    counter = counter + 1
    print(counter)
  except socket.timeout: 
   print("error")

  
    
