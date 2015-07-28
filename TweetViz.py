 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import time
import pandas as pd
#insert your Twitter keys here
consumer_key ='Gfo2favWdKJLOHsEh1F3AXPyl'
consumer_secret='POuONd8rv6f33d8g8Z1WF4tEIRBI4CXyXVp9ngS6HvOeQJFB8u'
access_token='23743958-5P8DVu4zGjZv3IA0cfOten9i6vvl9UXPASG5AZWHu'
access_secret='Nw2Sgralb73sQmKaIWq7akPXS1GUClHWKipQdDgj3rgAU'
 
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
if(api.verify_credentials):
    print '-------------------------\n*** You are logged in ***\n-------------------------'


#Create a data frame where to store each user's data
columns = ['Username','Follower']
df = pd.DataFrame(columns=columns)

#Set starting Twitter handle
ids = ['moixera']

#Set depth
depth = 3

with open('output.csv', 'a') as f:
    while depth > 0:
        for i in range(len(ids)):
            username = ids[i]
    #Check if username hs been already processed
            if username in df.Username.values:
                continue
            else:
    #Start extracting each level followers
                for user in tweepy.Cursor(api.followers, screen_name=username).items():
                    ids.append(str(user.screen_name))
                          
    #Add data to the data frame
            for i in range(len(ids)):
                df.loc[i] = [username,ids[i]]
            depth = depth-1
            df.to_csv(f, mode='a', header=False)
f.close()
print ids
print df