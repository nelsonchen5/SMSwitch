import tweepy
import logging
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
logger = logging.getLogger()


def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


# def create_twilio_client():
    # account_sid = "ACe125e2892a1397d47779bab6b689ce17"
    # auth_token = "aa8d2251402671ea4d1d372dcc5ae510"

    # twilio_client = Client(account_sid, auth_token)
