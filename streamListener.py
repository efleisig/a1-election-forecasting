import tweepy
import json

class StreamListener(tweepy.StreamListener):
    # Override parent constructor
    def __init__(self, api=None, name=None,
                 outputFile=None, maxTweets=None, excludedWords=None):
        super(StreamListener, self).__init__()
        self.name = name
        self.file = open(outputFile, "w")
        self.maxTweets = maxTweets
        self.excludedWords = excludedWords
        print("excludedWords ", excludedWords)

        self.numTweets = 0

    # Executes whenever a new status is received
    def on_status(self, status):
        tweet = status._json

        # Check that the tweet doesn't contain any of the excluded words
        if self.has_words(tweet["text"], self.excludedWords):
            return True
        # Some tweets contain the full (extended) text
        elif ("extended_tweet" in tweet and "full_text" in tweet["extended_tweet"] and
             self.has_words(tweet["extended_tweet"]["full_text"], self.excludedWords)):
            return True

        # Otherwise, count this tweet and write to output
        print(status.text)
        self.file.write(json.dumps(tweet) + '\n' )
        self.numTweets += 1

        # Stop streaming when it reaches the set limit
        if self.numTweets <= self.maxTweets:
            if self.numTweets % 100 == 0:
                print('Number of tweets captured so far: {}'.format(self.numTweets))
            return True
        else:
            print("Hit max number of tweets to capture. Stopping stream")
            return False

        self.file.close()

    # Executes whenever an error is received
    # StreamListener performs exponential backoff when return value is True
    def on_error(self, status_code):
        print("Error. Status code=", status_code)

        # For error 420 (rate-limiting error), StreamListener performs exponential backoff starting at 1 min
        if status_code == 420 or status_code == 429:
            print(self.name + ": getting rate limited. Trying again.")
            return True
        elif status_code % 500 < status_code:
            print(self.name + ": server error. Trying again")
            return True

        print(self.name + ": fatal error. Disconnecting stream")
        return False

    # Check if string contains any of words
    def has_words(self, string, words):
        return any(word in string for word in words)
