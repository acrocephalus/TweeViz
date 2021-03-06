#Welcome to TweeViz v1.0b!!

TweeViz is a command line crossplatform tool written in Python. It will retrieve all users for a given user.

#Parameters
There are three parameters to be passed by the user:
Username: the user for whom we wish to get the followers
Depth: the number of follower levels to scan. For example, if we want to get the followers for a given user and then we use the followers list as an input for a subsequent iteration, we must set depyh = 2. Defaults to depth = 0.
Method: the program first retrieves users' IDs and then runs a lookup call to get the users' username. Sometimes there is an ID without associated username. This can be because the user has moved, changed or deleted the account or it has been suspended. In this case, the program would exit with an error and no more users would be retrieved. To overcome this problem we have designed two methods. The 'Secure' method will run the lookup at one user at a time. This ensures that you get more data but it is slower. The 'Fast' method runs the lookup in batches containing 100 users. This allows to get more data for each API call, but if it throws an error all the batch will be lost. This method is faster but more prone to data lose.

#About the output files
The program returns three files:
output.csv: contains three columns labeled 'Username', 'Follower', 'Time'. Its purpose is to be used as a log file to keep track of the program process.
nodes.csv: it is a file formatted according to the Gephi specifications so it can be directly imported.
edges.csv: it is a file formatted according to the Gephi specifications so it can be directly imported.

#Caution
This program uses the Twitter's API so it is subject to its ToS. In order not to hit its rate limits, a sleeping time of 60 seconds is placed before making a new request for both ids and lookup processes. For more information on Twitter's API check https://dev.twitter.com/rest/public/rate-limiting
