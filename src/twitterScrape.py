import tweepy
from config import create_api
import re

from sendSMS import send_message
import configparser
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SMSwitch')

response = table.scan()

contacts = response['Items']


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
            for k in contacts:
                if(k['Contact'].lower() in tweet.text.lower()):
                    send_message(k['Phone Number'], image_url)
                    print(image_url)
            # if('cc' in tweet.text.lower()):
                # send_message(contacts.get('CONTACTS', 'SENDER'), image_url)
            if('*add' in tweet.text.lower()):
                name = tweet.text.lower().split("*add")[1].split(" ")[1]
                number = tweet.text.lower().split("*add")[1].split(" ")[2]
                table.put_item(
                    Item={
                        'Contact': name,
                        'Phone Number': number
                    }
                )
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
