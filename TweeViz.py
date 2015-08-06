 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
import TwitterLogin
import time
import config
from tweetools import grouper
from setproctitle import setproctitle
 
#Set process name
setproctitle('TweeViz')   
#Authenticate app on Twitter
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

is_valid = 0
while not is_valid:
    try:
        depth = int(raw_input('Depth (defaults to 1): ') or '1')
        int(depth)
        is_valid = 1
    except ValueError, e:
        print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
#Set batch items number
is_valid = 0
while not is_valid:
    try:
        batch_items = int(raw_input('Batch items [1-100] (Defaults to 100): ') or '100')
        is_valid = 1
        while batch_items < 1 or batch_items > 100:
            print 'Integer outside allowed range. Please enter a vualue between 1-100' 
            batch_items = int(raw_input('Batch items [1-100] (Defaults to 100): ') or '100')           
    except ValueError, e:
        print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
while depth > 0:
    #Iterate over the followers list
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
                #Getting followers' followers                    
                groups = grouper(ids[0],batch_items)
                #Iterate over to IDs list to get each username                
                for u in range(len(ids)):
                    print '#Retrieving users\' followers\n'
                    followers = []
                    #Iterate over the IDs list in batches of 100 Ids
                    for t in range(len(groups)):
                            batch = groups[t]      
                            try:                                                                                                            
                                ids2 = config.api.lookup_users(user_ids=[batch])
                                time.sleep(60)
                                for u in ids2:
                                    followers.append(str(u.screen_name))
                            except:
                                print 'The user has changed, moved or deleted his/her account. He/She may also be suspended.'                                     
                    for i in range(len(followers)):
                        t = datetime.now()
                        output.loc[i] = [username,followers[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]    
                    with open('output/output.csv', 'a') as o:
                        output.to_csv(o, mode='a', header=False)
                    o.close()                                                                   
                    #Add data to the nodes data frame
                    nodes.Nodes = list(pd.unique(output.Follower.ravel()))
                    nodes.Label = list(pd.unique(output.Follower.ravel()))
                    with open('output/nodes.csv', 'a') as n:
                        nodes.to_csv(n, mode='a', header=False)
                    n.close()        
                    #Add data to the edges data frame
                    edges.Source = output.Username
                    edges.Target = output.Follower
                    for i in range(len(edges.Source)):
                        edges.loc[i]['Type'] = Type
                        edges.loc[i]['Label'] = str(edges.Source[i]) + ' - ' + str(edges.Target[i])
                    with open('output/edges.csv', 'a') as e:
                        edges.to_csv(e, mode='a', header=False)                           
#Reset users list    
    user = output.Follower.tolist()          
#Reset depth value        
    depth = depth-1