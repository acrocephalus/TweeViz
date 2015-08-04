 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
import TwitterLogin
import config

#Login into Twitter
TwitterLogin.login()

#Create a data frame where to store each user's data
output = pd.DataFrame(columns=['Username','Follower','Time'])
output.index.name = 'Id'

#Create a data frame where to store nodes data
nodes = pd.DataFrame(columns=['Nodes','Label'])
nodes.index.name = 'Id'

#Create a data frame where to store edges data
edges = pd.DataFrame(columns=['Source','Target','Type','Label','Weight'])
edges.index.name = 'Id'
Type = 'Undirected'

#Set starting Twitter handle
ids = [raw_input('Enter the Twitter username for which to get data: ')]

#Set depth
depth = 1
with open('nodes.csv', 'a') as n:
    with open('output.csv', 'a') as o:
        with open('edges.csv', 'a') as e:
        #Initialize output file            
            output.to_csv(o, mode='a')
        #Initialize nodes file            
            nodes.to_csv(n, mode='a')
        #Initialize edges file            
            edges.to_csv(e, mode='a')
            while depth > 0:
                for i in range(len(ids)):
                    username = ids[i]
        #Check if username has been already processed
                    if username in output.Username.values:
                        continue
                    else:
        #Start extracting each level followers
                        for user in tweepy.Cursor(config.api.followers, screen_name=username).items():
                            ids.append(str(user.screen_name))                                  
        #Add data to the output data frame
                            for i in range(len(ids)):
                                t = datetime.now()
                                output.loc[i] = [username,ids[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]
                                output = output[output.Username != output.Follower]
    #Write output file
                output.to_csv(o, mode='a', header=False)
    #Add data to the nodes data frame
                nodes.Nodes = list(pd.unique(output.Follower.ravel()))
                nodes.Label = list(pd.unique(output.Follower.ravel()))
        #Write nodes file
                nodes.to_csv(n, mode='a', header=False)
        #Add data to the edges data frame
                edges.Source = output.Username
                edges.Target = output.Follower
                for i in range(len(edges.Source)):
                    edges.loc[i+1]['Type'] = Type
                    edges.loc[i+1]['Label'] = edges.Source[i+1] + ' - ' + edges.Target[i+1]
        #Write edges file
                edges.to_csv(e, mode='a', header=False)
        #Reset depth value        
                depth = depth-1

o.close()
n.close()
e.close()