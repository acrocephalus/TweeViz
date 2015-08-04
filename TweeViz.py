 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
import TwitterLogin
import time
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
ids = [raw_input('Username: ')]

#Set depth
depth = int(raw_input('Depth (defaults to 1): ') or '1')

with open('output/nodes.csv', 'a') as n:
    with open('output/output.csv', 'a') as o:
        with open('output/edges.csv', 'a') as e:
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
        #Start extracting followers' IDs
                        for page in tweepy.Cursor(config.api.followers_ids, screen_name=username).pages():
                            time.sleep(60)
                            ids = []
                            ids.append(page)
        #Getting followers' usernames
                        for u in range(len(ids)):
                            ids = config.api.lookup_users(user_ids=ids[u])
                            ids = [str(u.screen_name) for u in ids]
                            time.sleep(60)
        #Add data to the output data frame
                            for i in range(len(ids)):
                                t = datetime.now()
                                output.loc[i] = [username,ids[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]
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
                            edges.loc[i]['Type'] = Type
                            edges.loc[i]['Label'] = edges.Source[i] + ' - ' + edges.Target[i]
        #Write edges file
                        edges.to_csv(e, mode='a', header=False)
#Reset depth value        
                depth = depth-1

o.close()
n.close()
e.close()