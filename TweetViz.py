 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
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
output = pd.DataFrame(columns=['Username','Follower','Time'])
output.index.name = 'Id'

#Create a data frame where to store nodes data
nodes = pd.DataFrame(columns=['Nodes','Label'])
nodes.index.name = 'Id'

#Set starting Twitter handle
ids = ['moixera']

#Set depth
depth = 1
with open('nodes.csv', 'a') as n:
    with open('output.csv', 'a') as f:
    #Initialize output file            
        output.to_csv(f, mode='a')
        while depth > 0:
            for i in range(len(ids)):
                username = ids[i]
    #Check if username has been already processed
                if username in output.Username.values:
                    continue
                else:
    #Start extracting each level followers
                    for user in tweepy.Cursor(api.followers, screen_name=username).items():
                        ids.append(str(user.screen_name))                                  
    #Add data to the data frame
                for i in range(len(ids)):
                    t = datetime.now()
                    output.loc[i] = [username,ids[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]
            output.to_csv(f, mode='a', header=False)
            depth = depth-1
f.close()
n.close()