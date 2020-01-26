import tweepy
from config import create_api
import re

from sendSMS import send_message
import configparser

contacts = configparser.ConfigParser()
contacts.read('contacts.ini')


def extractUrl(str):
    ur = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str)
    return ur


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")
        try:
            image_url = f"{tweet.entities['media'][0]['media_url']}"
            for k, v in contacts.items('CONTACTS'):
                if(k.lower() in tweet.text.lower()):
                    send_message(v, image_url)
                    print(image_url)
            if('cc' in tweet.text.lower()):
                send_message(contacts.get('CONTACTS', 'SENDER'), image_url)
        except Exception as e:
            print(e)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.


# api = create_api()

# myStreamListener = MyStreamListener(api)
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
# user = myStreamListener.me
# myStream.filter(follow=[str(user.id)])


def main():
    api = create_api()
    myStreamListener = MyStreamListener(api)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    user = myStreamListener.me
    myStream.filter(follow=[str(user.id)], is_async=True)


if __name__ == "__main__":
    main()
