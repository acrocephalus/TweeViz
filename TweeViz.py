 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
import TwitterLogin
import time
import config
from tweetools import grouper
from StringIO import StringIO
import sys

#Login into Twitter
TwitterLogin.login()

#Create a data frame where to store each user's data
output = pd.DataFrame(columns=['Username','Follower','Time'])
output.index.name = 'Id'

#Create a data frame where to store nodes data
nodes = pd.DataFrame(columns=['Nodes','Label'])
nodes.index.name = 'Id'
with open('output/nodes.csv', 'a') as n:
    nodes.to_csv(n, mode='a')
    n.close()
#Create a data frame where to store edges data
edges = pd.DataFrame(columns=['Source','Target','Type','Label','Weight'])
edges.index.name = 'Id'
Type = 'Undirected'
with open('output/edges.csv', 'a') as e:
    edges.to_csv(e, mode='a')
e.close

#Set starting Twitter handle
user = [raw_input('Username: ')]

#Set depth
depth = int(raw_input('Depth (defaults to 1): ') or '1')


while depth > 0:
    for i in range(len(user)):
        username = user[i]
#Check if username has been already processed
        if username in output.Username.values:
            continue
        else:        
#Start extracting followers' IDs
            print '#Retrieving users\' ids \n'
            for page in tweepy.Cursor(config.api.followers_ids, screen_name=username).pages():
                ids = []
                ids.append(page)
#Getting followers' usernames
            print '#Retrieving users\' usernames\n'
            for u in range(len(ids)):
                groups = grouper(ids,100)                       
                for t in range(len(groups[0])):
                    try:
                        for batch,v in enumerate(groups[0]):
                            print '#Retrieving usernames batch number ' + str(batch+1) + '\n'
                        
                        ids2 = config.api.lookup_users(user_ids=[groups[0][t]])
                        usernames = []
                        usernames.append([str(u.screen_name) for u in ids2])
                        usernames = usernames[0]
                    except:
                        print '#The user has changed, moved or deleted his/her account.\n\
                        #He/She may also be suspended.\n\
                        #Moving to the next user\n'
            #Add data to the output data frame
                    for i in range(len(usernames)):
                        t = datetime.now()
                        output.loc[i] = [username,usernames[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]
                        with open('output/output.csv', 'a') as o:
                            output.to_csv(o, mode='a', header=False)                                        
        #Add data to the nodes data frame
                    nodes.Nodes = list(pd.unique(output.Follower.ravel()))
                    nodes.Label = list(pd.unique(output.Follower.ravel()))
                    with open('output/nodes.csv', 'a') as n:
                        nodes.to_csv(n, mode='a', header=False)

    #Add data to the edges data frame
                    edges.Source = output.Username
                    edges.Target = output.Follower
                    for i in range(len(edges.Source)):
                        edges.loc[i]['Type'] = Type
                        edges.loc[i]['Label'] = str(edges.Source[i]) + ' - ' + str(edges.Target[i])
                    with open('output/edges.csv', 'a') as e:
                        edges.to_csv(e, mode='a', header=False)

#Reset depth value        
                depth = depth-1
                

n.close()    
o.close()    
e.close()


