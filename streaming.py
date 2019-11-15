#This is a simple example of the Tweepy streaming functinallity. It will listen to
#all tweets containing "android" and will keep track of the hashtags used in the tweets.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import oauthHandler
import ws
import hashtag_updater
from helper import set_interval


#Basic listener which parses the json, creates a tweet, and sends it to parseTweet
class TweetListener(StreamListener):
	def on_data(self, data):
		ws.send_tweet(data)
		return not is_ht_updated

	def on_error(self, status):
		print (status)



def updateFilter():
	global ht_list
	global is_ht_updated

	ht_list_updated = hashtag_updater.sheet_job()
	if set(ht_list) == set(ht_list_updated):
		is_ht_updated = False
	else :
		ht_list = ht_list_updated
		is_ht_updated = True


# if __name__ == '__main__':
def start_stream():
	listener = TweetListener()
	auth = oauthHandler.getAuth()
	stream = Stream(auth, listener)	
	while True:
		stream.filter(track=ht_list) #This will start the stream and make callbacks to the listener for all tweets containing "android"

global ht_list
ht_list = ['yanggang']
global is_ht_updated
updateFilter()
set_interval(updateFilter, 600)
is_ht_updated = False
start_stream()




