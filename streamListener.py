import tweepy
import backoff
import requests

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_time=30)
    def on_error(self, status_code):
        print("Error. Status code=", status_code)
        if status_code == 420 or status_code == 429:
            print("App is getting rate limited. Trying again.")
            return True
        elif status_code % 500 < status_code:
            print("Server error. Trying again")
            return True

        print("Fatal error. Disconnecting stream")
        return False
