 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from datetime import datetime
import TwitterLogin
import time
import config
from tweetools import grouper, add_to_file
from setproctitle import setproctitle
from textwrap import dedent as dedent
 
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
depth = int(raw_input('Depth (defaults to 1): ') or '1')
#Set username lookup method
is_valid = 0
while not is_valid:
    try:
        ask_input = '''\
        Please choose the method to be used on the user lookup calls:\n\
        [1] Secure\n\
        [2] Fast'''
        print dedent(ask_input)
        method = int(raw_input('Enter an integer corresponding to your choice [1,2]: '))
        is_valid = 1
    except ValueError, e :
        print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
if method == 1:
    method = 'Secure'
else:
    method = 'Fast'
while depth > 0:
    #Iterate over the followers list
    for i in range(len(user)):
        username = user[i]
        #Check if username has been already processed
        if username in output.Username.values:
            continue
        else:
            remaining_id_calls = 15
            endtime = time.time() + 15*60        
            #Start extracting followers' IDs
            print '#Retrieving users\' ids \n'
            for page in tweepy.Cursor(config.api.followers_ids, screen_name=username).pages():
                #Check if there are IDs calls left not to hit the rate limit
                if remaining_id_calls > 0:
                    ids = []
                    ids.append(page)
                    #Getting followers' followers                    
                    groups = grouper(ids[0],100)
                    #Iterate over to IDs list to get each username                
                    for u in range(len(ids)):
                        print '#Retrieving users\' followers\n'
                        followers = []
                        remaining_lookup_calls = 60
                        endtime = time.time() + 15*60
                        #Iterate over the IDs list in batches of 100 Ids 
                        for t in range(len(groups)):
                            batch = groups[t]
                            #Check if there are user lookup calls left within the 15 minutes time window
                            if method == 'Secure':
                                for z in range(len(batch)):
                                    if remaining_lookup_calls > 0:
                                        id_lookup = [str(batch[z])]
                                        try:
                                            ids2 = config.api.lookup_users(user_ids = id_lookup)
                                            followers.append([str(u.screen_name) for u in ids2])
                                            #Reset the remaining user lookup calls counter
                                            remaining_lookup_calls = remaining_lookup_calls - 1
                                        except:
                                            print 'The user has changed, moved or deleted his/her account. He/She may also be suspended.'
                                    else:
                                        remaining_time = endtime - time.time()
                                        print 'Going to sleep for ' + str(remaining_time) + ' seconds to avoid hitting the rate limits'
                                        add_to_file()                                       
                                        time.sleep(remaining_time)
                                        #Reset time and calls counter
                                        remaining_lookup_calls = 60
                                        endtime = time.time() + 15*60                                                                                        
                            #Get the IDs in batches of 100 IDs
                            else:         
                                for z in range(len(batch)):
                                    if remaining_lookup_calls > 0:
                                        try:                                                                                                            
                                            ids2 = config.api.lookup_users(user_ids=[batch[z]])
                                            followers.append([str(u.screen_name) for u in ids2])
                                            #Reset the remaining user lookup calls counter
                                            remaining_lookup_calls = remaining_lookup_calls - 1
                                        except:
                                            print 'The user has changed, moved or deleted his/her account. He/She may also be suspended.'
                                    #When reached the maximum allowed lookup calls, go to sleep for the remaining time
                                    else:
                                        remaining_time = endtime - time.time()
                                        print 'Going to sleep for ' + str(datetime.timedelta(seconds=remaining_time)) + ' seconds to avoid hitting the rate limits'                                    
                                        add_to_file()
                                        time.sleep(remaining_time)
                                        #Reset time and calls counter
                                        remaining_lookup_calls = 60
                                        endtime = time.time() + 15*60                                                        
                    #Reset the remaining ID calls counter
                    remaining_id_calls = remaining_id_calls - 1
                #When reached the maximum allowed lookup calls, go to sleep for the remaining time
                else:
                    remaining_time = endtime - time.time()
                    print 'Going to sleep for ' + remaining_time + ' seconds to avoid hitting the rate limits'
                    time.sleep(remaining_time)
                    #Reset time and calls counter
                    remaining_id_calls = 15
                    endtime = time.time() + 15*60                                
#Reset users list    
    user = output.Follower.tolist()          
#Reset depth value        
    depth = depth-1