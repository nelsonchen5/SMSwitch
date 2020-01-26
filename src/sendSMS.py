import os
from dotenv import load_dotenv
from twilio.rest import Client
import logging
load_dotenv()


def send_message(recipient, image):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_='+19492006864',
            to=recipient,
            media_url=[image]
        )
    print(message.sid)
