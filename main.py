import emoji
import pandas as pd
import tweepy
import re
import mysql.connector
from mysql.connector import Error
from pip._internal.utils import datetime
from tweepy import API
from datetime import datetime
import time




CONSUMER_KEY = "Your credentials"
CONSUMER_SECRET = Your credentials
ACCESS_TOKEN = "Your credentials"
ACCESS_TOKEN_SECRET = "Your credentials"

auth_handler= tweepy.OAuthHandler(consumer_key= CONSUMER_KEY, consumer_secret = CONSUMER_SECRET)
auth_handler.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api= tweepy.API(auth_handler, wait_on_rate_limit=True)

db = mysql.connector.connect(host='localhost', database="assignment", user='root', password='')
if db.is_connected():
        print("Connection with database established")
        cur = db.cursor()

search_term = ('Basketball', 'Football', 'Volleyball')
for i in search_term:
        tweet_amount = 100
        tweets = tweepy.Cursor(api.search_tweets, q=i, lang='en').items(tweet_amount)



final_tweets = []
for tweet in tweets:
    if not tweet.retweet_count: # remove retweets
        tweetdict = {'user_account': tweet.user.screen_name,
                     'numofaccfol': tweet.user.followers_count,
                     'numofacctw': tweet.user.statuses_count,
                     'numofaccretew': tweet.retweet_count,
                     'tweettext': tweet.text,
                     'date': tweet.created_at,
                     'location': tweet.user.location,
                     'hashtags': tweet.entities['hashtags']}
        final_tweets.append(tweetdict)
for i in final_tweets:
            i["user_account"] = "@" + i["user_account"]
            i["tweettext"] = re.sub(r'@\S+|https?://\S+', '', i['tweettext'])
            i['tweettext'] = emoji.demojize(i['tweettext'])
            i['tweettext'] = i['tweettext'].replace(":", " ")
            i['tweettext'] = i['tweettext'].replace("?", " ")
            i['tweettext'] = i['tweettext'].replace("#", " ")
            i['tweettext'] = ' '.join(i['tweettext'].split())
            i['date'] = datetime.strftime(i["date"], '%Y-%m-%d')
            print(final_tweets)

            user_acc = i["user_account"]
            numofaccfol = i["numofaccfol"]
            numofacctw = i["numofacctw"]
            numofaccretew = i["numofaccretew"]
            tweettext = ''.join([c for c in str(i["tweettext"])])
            date = i["date"]
            location = ''.join([c for c in str(i["location"])])
            hashtags = ''.join([c for c in str(i["hashtags"])])
            qa = "INSERT INTO twitter(user_acc,numofaccfol,numofacctw,numofaccretew,tweettext,date,location,hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(qa, (user_acc, numofaccfol, numofacctw, numofaccretew, tweettext, date, location, hashtags))



db.commit()
db.close()



























