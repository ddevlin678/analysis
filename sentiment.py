from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time 
import sys
import numpy as np
import re
import unicodedata
#"possibly_sensitive":true tweets which contain links 
#id is id of the tweet unique 
#pip install tweepy --user
#pip install -user nltk
#chcp 65001 for UTF-8

#consumer key, consumer secret, access token, access secret.
ckey="WLntuQkpDe25sCSpwdLYWidI5"
csecret="KxbCDrEJqRBs7gjc64bIuJL4dzfvklNtk6UWUN1hviPv0AVble"
atoken="263661193-2OVxXqpHP6xqRzNymLK9ACh9XbeCtIfz0bp42WCu"
asecret="WejuT8bdw9U7zLA1RNH2QC2t1rziocwgJBGlkTV47r2qL"
fullTweets = []
cleanTweets = []

class listener(StreamListener):

 def remove_pattern(tweet_text, pattern):
  r = re.findall(pattern, tweet_text)
  for i in r:
   tweet_text = re.sub(i, '', tweet_text)   
  return tweet_text

 sample = ('RT @reluctantnicko: LEEDS. Already looking at Harry Wilson at LIVERPOOL for a loan next season if they go up. Playing for DERBY. Must have\u2026')
 sample = np.vectorize(remove_pattern)(sample, "RT @[\w]*:")
 print(sample)

 def on_data(self, data):
  try:
   all_data = json.loads(data)
   #print(all_data.keys())
   #sys.exit()
   tweet_text = all_data['text']

   newTweet = tweet_text.encode('utf-8')
   #print(type(tweet_text))
   #sys.exit() # thought it was one instance of 


   if all_data['truncated'] == True:
    extended_tweet = all_data['extended_tweet']
    tweet_text = extended_tweet['full_text']
    newTweet = tweet_text.encode('utf-8', ignore)


    


   user = all_data['user']
   print(user['verified'])

   f_count = user['followers_count']
   retweet_count = all_data['retweet_count']
   favorite_count = all_data['favorite_count']


   if all_data['coordinates'] == True:
    location = all_data['coordinates']
    print(location)
   
   
   #print("Tweet received \n")

   fullTweets.append(newTweet)
   #print(tweet_text)
   
   
   #tweet = all_data["full_text"]
   #saveThis = str(time.time())+'::'+tweet
   #file = open("tweet.json" , "a") #appends to top of file
   #file.write(tweet + "\n") #was tweet 
   #file.close()
   with open('tweet2.json', 'a') as outfile:
    json.dump(newTweet, outfile)
    outfile.write('\n')
   print("saved")
   return(True)
  except:
   print(sys.exc_info()[0])

    #RuntimeError as re:
    #handle_runtime(re)
    #return(False)
 
 def on_error(self, status):
  print(status)

 def uptheRa(newTweet):
  for tweet in newTweet:
   tweet = np.vectorize(remove_pattern)(sample, "RT @[\w]*:")
   cleanTweets.append(tweet)
   print(cleanTweets)
  

 

 def remove_pattern(tweet_text, pattern):
  r = re.findall(pattern, tweet_text)
  for i in r:
   tweet_text = re.sub(i, '', tweet_text)   
  return tweet_text


 def cleanTweets(): #tweet_text
  #for rawTweet in fullTweets:
  print(type(tweet_text))
  
  tweet_text = str(tweet_text)
  #print(type(tweet_text))
  #print(tweet_text)
  print("We are reading in Tweets")
  tweet_text = np.vectorize(remove_pattern(tweet_text, "RT @[\w]*:"))
  #tweet_text = np.vectorize(remove_pattern(tweet_text, "@[\w]*"))
  #tweet_text = np.vectorize(remove_pattern(tweet_text, "https?://[A-Za-z0-9./]*"))
  #tweet_text = np.core.defchararray.replace(tweet_text, "[^a-zA-Z#]", " ")
  cleanTweets.append(tweet_text)
  #print(cleanTweets)
  return cleanTweets
  
   
 def sentiment_analyzer_scores(fullTweets):
  score = analyser.polarity_scores(fullTweets)
  lb = score['compound']
  if lb >= 0.05:
   return 1
  elif (lb > -0.05) and (lb < 0.05):
   return 0
  else:
   return -1
  
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
twitterStream.filter(track=["war"])

#UnicodeEncodeError: 'charmap' codec can't encode character '\u0130' in position 43: character maps to <undefined>
