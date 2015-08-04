#Welcome to TweeViz v1.0b!!

TweeViz is a command line crossplatform tool written in Python. It will retrieve all users for a given user.

#Parameters
There are just two parameters to be passed by the user:
Username: the user for whom we wish to get the followers
Depth: the number of follower levels to scan. For example, if we want to get the followers for a given user and then we use the followers list as an input for a subsequent iteration, we must set depyh = 2. Defaults to depth = 0.

#About the output files
The program returns three files:
output.csv: contains three columns labeled 'Username', 'Follower', 'Time'. Its purpose is to be used as a log file to keep track of the program process.
nodes.csv: it is a file formatted according to the Gephi specifications so it can be directly imported.
edges.csv: it is a file formatted according to the Gephi specifications so it can be directly imported.

#Caution
This program uses the Twitter's API so it is subject to its ToS. For more information on Twitter's API check https://dev.twitter.com/rest/public/rate-limiting
