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
output_row = pd.DataFrame(columns=['Username','Follower','Time'])
output_row.index.name = 'Id'
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
with open('output/nodes.csv', 'a') as n, open('output/edges.csv', 'a') as e, open('output/output.csv', 'a') as o:
    user = ['acrocephalus']
    depth = 2
    batch_items = 100
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
                try:
                    for page in tweepy.Cursor(config.api.followers_ids, screen_name=username).pages():
                        ids = []
                        ids.append(page)
                        #Getting followers' followers                    
                        groups = grouper(ids[0],batch_items)
                        #Iterate over to IDs list to get each username                
                        for u in range(len(ids)):
                            print '#Retrieving users\' followers\n'
                            #followers = []
                            #Iterate over the IDs list in batches of 100 Ids
                            for m in range(len(groups)):
                                    batch = groups[m]      
                                    try:                                                                                                            
                                        ids2 = config.api.lookup_users(user_ids=[batch])
                                        #time.sleep(60)
                                        for u in ids2:
                                            followers = []
                                            followers.append(str(u.screen_name))
                                            for i in range(len(followers)):
                                                t = datetime.now()                                            
                                                output_row.loc[i] = [username,followers[i],("%s-%s-%s %s:%s:%s" % (t.year,t.month,t.day, t.hour, t.month, t.second))]
                                                output = pd.concat([output, output_row], ignore_index=True)
        
                                                output.to_csv(o, mode='a', header=False)
                                                #Add data to the nodes data frame
                                                data_nodes = {'Node': list(pd.unique(output_row.Follower.ravel())), 'Label': list(pd.unique(output_row.Follower.ravel()))}
                                                nodes = pd.concat([nodes,pd.DataFrame(data_nodes)],ignore_index=True)
                                                nodes.to_csv(n, mode='a', header=False)
                                                #Add data to the edges data frame
                                                data_edges =  {'Source': list(output_row.Username),'Target': list(output_row.Follower), 'Type': Type,'Label': (output_row.Username + ' - ' + output_row.Follower)}                                        
                                                edges = pd.concat([edges,pd.DataFrame(data_edges)],ignore_index=True)                                       
                                                edges.to_csv(e, mode='a', header=False)
                                                edges = edges[['Source','Target','Type','Label','Weight']] 
                                                #Reset output_row dataframe to accept more data
                                                output_row = output_row.drop(output_row.index[:])                                                                                                                                                                 
                                    except:
                                        print 'The user has changed, moved or deleted his/her account. He/She may also be suspended.'
                except:
                    continue                                                  
    #Reset users list    
        user = output.Follower.tolist()          
    #Reset depth value        
        depth = depth-1
    
o.close()
n.close()
e.close