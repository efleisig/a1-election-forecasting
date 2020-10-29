import config
import tweepy
from streamListener import StreamListener

#OAuth1 authentication
auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

# Set parameters for tweepy API here
HTTP_RETRY_ERRORS = [420, 429, 500, 502, 503, 504]
api = tweepy.API(auth,
                 parser=tweepy.parsers.JSONParser(),
                 retry_errors=HTTP_RETRY_ERRORS,
                 wait_on_rate_limit_notify=True)
query = "Donald Trump"
outputFile = "trumpTweets.txt"

trumpStreamListener = StreamListener(name="trumpStream",
                                     outputFile=outputFile,
                                     maxTweets=10)
trumpStream = tweepy.Stream(auth=api.auth, listener=trumpStreamListener)
trumpStream.filter(track=[query])
