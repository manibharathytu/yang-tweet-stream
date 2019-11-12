#This is a simple example of the Tweepy streaming functinallity. It will listen to
#all tweets containing "android" and will keep track of the hashtags used in the tweets.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import oauthHandler
import json
import ws
#Tweet class with all the information we need for this program (Hashtags and the actual tweet text)
class Tweet:
        text = str()
	hashtags = []

        def __init__(self, json):
		self.text = json["text"] 
		self.username = json["user"]["screen_name"]
		self.hashtags = json["entities"]["hashtags"]

#Basic listener which parses the json, creates a tweet, and sends it to parseTweet
class TweetListener(StreamListener):
	def on_data(self, data):
		jsonData = json.loads(data)
		tweet = Tweet(jsonData)
		# print(tweet.text.encode('utf-8'))
		ws.send_all(tweet.text.encode('utf-8'))
		# print(tweet.username.encode('utf-8'))
		return True

	def on_error(self, status):
		print (status)


# if __name__ == '__main__':
def start_stream():
	listener = TweetListener()
	auth = oauthHandler.getAuth()
	stream = Stream(auth, listener)	
	filt = ['yanggang']
	stream.filter(track=filt) #This will start the stream and make callbacks to the listener for all tweets containing "android"
	
start_stream()




