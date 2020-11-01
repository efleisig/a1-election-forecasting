import config
import tweepy
import json
import os

from datetime import datetime
from streamListener import StreamListener

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#OAuth1 authentication
auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

# Set parameters for tweepy API here
HTTP_RETRY_ERRORS = [420, 429, 500, 502, 503, 504]
api = tweepy.API(auth,
                 parser=tweepy.parsers.JSONParser(),
                 retry_errors=HTTP_RETRY_ERRORS,
                 wait_on_rate_limit_notify=True)
trumpOutputFileFormat = "trump_{state}_{date}.json"
bidenOutputFileFormat = "biden_{state}_{date}.json"


states = {
            'al': 'alabama',
            'ak': 'alaska',
            'az': 'arizona',
            'ar': 'arkansas',
            'ca': 'california',
            'co': 'colorado',
            'ct': 'connecticut',
            'de': 'delaware',
            'dc': 'district of columbia',
            'fl': 'florida',
            'ga': 'georgia',
            'hi': 'hawaii',
            'id': 'idaho',
            'il': 'illinois',
            'in': 'indiana',
            'ia': 'iowa',
            'kd': 'kansas',
            'ku': 'kentucky',
            'la': 'louisiana',
            'me': 'maine',
            'md': 'maryland',
            'ma': 'massachusetts',
            'mi': 'michigan',
            'mn': 'minnesota',
            'ms': 'mississippi',
            'mp': 'missouri',
            'mt': 'montana',
            'ne': 'nebraska',
            'nv': 'nevada',
            'nh': 'new hampshire',
            'nj': 'new jersey',
            'nm': 'new mexico',
            'ny': 'new york',
            'nc': 'north carolina',
            'nd': 'north dakota',
            'oh': 'ohio',
            'ok': 'oklahoma',
            'or': 'oregon',
            'pa': 'pennsylvania',
            'ri': 'rhode island',
            'sc': 'south carolina',
            'sd': 'south dakota',
            'tn': 'tennessee',
            'tx': 'texas',
            'ut': 'utah',
            'vt': 'vermont',
            'va': 'virginia',
            'wa': 'washington',
            'wv': 'west virginia',
            'wi': 'wisconsin',
            'wy': 'wyoming'
         }

def extract_place(status):
    if type(status) is tweepy.models.Status:
        status = status.__dict__
    #Try to get the place from the place data inside the status dict
    if status['place'] is not None:
        place = status['place']
        if place.country != 'United States':
            return place.country
        elif place.place_type == 'admin':
            return place.name
        elif place.place_type == 'city':
            return states.get(place.full_name.split(', ')[-1])
    #If the status dict has no place info, get the place from the user data
    else:
        place = status['user'].location
        try:
            place = place.split(', ')[-1].upper()
        except AttributeError:
            return None
        if place in states:
            return states[place]
        else:
            return place

class TrumpStreamListener(StreamListener):
    
    def on_status(self, status):
        place = extract_place(status)
        if place is None:
            return status
        if place.lower() in states.keys() or place.lower() in states.values():
            print 'Trump: ' + place
            outputFile = trumpOutputFileFormat.format(state=place.lower(), date=datetime.today().strftime('%Y-%m-%d'))
            outputFile = os.path.join(THIS_FOLDER, 'trump_tweets/' + outputFile)
            with open(outputFile, 'a') as tf:
                tf.write(json.dumps(status._json))
                tf.write('\n')
            return status

class BidenStreamListener(StreamListener):
    
    def on_status(self, status):
        place = extract_place(status)
        if place is None:
            return status
        if place.lower() in states.keys() or place.lower() in states.values():
            print 'Biden: ' + place
            outputFile = bidenOutputFileFormat.format(state=place.lower(), date=datetime.today().strftime('%Y-%m-%d'))
            outputFile = os.path.join(THIS_FOLDER, 'biden_tweets/' + outputFile)
            with open(outputFile, 'a') as tf:
                tf.write(json.dumps(status._json))
                tf.write('\n')
            return status

bidenStreamListener = BidenStreamListener(name="BidenStream",
        maxTweets=10000,
        outputFile='biden_tweets.txt',
        excludedWords=['Donald', 'Trump'])
bidenStream = tweepy.Stream(auth=api.auth, listener=bidenStreamListener)
bidenStream.filter(track=['Joe Biden'], is_async=True)

trumpStreamListener = TrumpStreamListener(name="TrumpStream",
        maxTweets=10000,
        outputFile='trump_tweets.txt',
        excludedWords=['Joe', 'Biden'])
trumpStream = tweepy.Stream(auth=api.auth, listener=trumpStreamListener)
trumpStream.filter(track=['Donald Trump'], is_async=True)
