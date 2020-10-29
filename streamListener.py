import tweepy
import json

class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None, name=None, outputFile=None, maxTweets=None):
        super(StreamListener, self).__init__()
        self.name = name
        self.file = open(outputFile, "w")
        self.maxTweets = maxTweets
        self.numTweets = 0

    def on_status(self, status):
        print(status.text)
        tweet = status._json
        self.file.write(json.dumps(tweet) + '\n' )
        self.numTweets += 1

        # Stops streaming when it reaches the set limit
        if self.numTweets <= self.maxTweets:
            if self.numTweets % 100 == 0:
                print('Number of tweets captured so far: {}'.format(self.numTweets))
            return True
        else:
            return False

        self.file.close()


    # StreamListener performs exponential backoff when return value is True
    # For error 420 (rate-limiting error), StreamListener performs exponential backoff starting at 1 min
    def on_error(self, status_code):
        print("Error. Status code=", status_code)
        if status_code == 420 or status_code == 429:
            print(name + ": getting rate limited. Trying again.")
            return True
        elif status_code % 500 < status_code:
            print(name + ": server error. Trying again")
            return True

        print(name + ": fatal error. Disconnecting stream")
        return False
