from twilio.rest import Client
import api.TWILIO_CREDS as TWILIO_CREDS

client = Client(TWILIO_CREDS.ACCOUNT_ID, TWILIO_CREDS.AUTH_TOKEN)

def notifyNumber(name, phone_number):
    message = client.messages.create(
        to=phone_number,
        from_=TWILIO_CREDS.TWILIO_NUMBER,
        body="Hey {}! We're interested in learning more about about you.  Come up and visit us at the desk!".format(name))