import tweepy
#Variables to access to Twitter's application
consumer_key ='Gfo2favWdKJLOHsEh1F3AXPyl'
consumer_secret='POuONd8rv6f33d8g8Z1WF4tEIRBI4CXyXVp9ngS6HvOeQJFB8u'
access_token='23743958-5P8DVu4zGjZv3IA0cfOten9i6vvl9UXPASG5AZWHu'
access_secret='Nw2Sgralb73sQmKaIWq7akPXS1GUClHWKipQdDgj3rgAU'

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)