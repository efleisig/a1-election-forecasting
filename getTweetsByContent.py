import config
import tweepy
from streamListener import StreamListener

# OAuth2 authentication
# auth = tweepy.AppAuthHandler(config.api_key, config.api_secret_key)

#OAuth1 authentication
auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

# Set parameters for tweepy API here
HTTP_RETRY_ERRORS = [420, 429, 500, 502, 503, 504]
api = tweepy.API(auth,
                 retry_errors=HTTP_RETRY_ERRORS,
                 wait_on_rate_limit_notify=True)

streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)
stream.filter(track=['tweepy'])



# auth = tweepy.AppAuthHandler(config.api_key, config.api_secret_key)
#
# api = tweepy.API(auth)
#
# for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
#     print(tweet.text)
#
# streamListener = StreamListener()
# stream = tweepy.Stream(auth=api.auth, listener=streamListener)

#######################
# TWITTERAPI
# Application authentication
# api = TwitterAPI(config.api_key,
#                  config.api_secret_key,
#                  auth_type='oAuth2')
#
# search_endpoint = 'search/tweets'

# r = api.request(search_endpoint, {'q':'biden'})
# for item in r:
#         print(item)

# QUERY = "biden"
# r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
# print(f'[{r.status_code}] RULE ADDED: {r.text}')
# if r.status_code != 201: exit()
#
# # GET STREAM RULES
#
# r = api.request('tweets/search/stream/rules', method_override='GET')
# print(f'[{r.status_code}] RULES: {r.text}')
# if r.status_code != 200: exit()
