
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import os

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, body):
    try:
        if client and TWILIO_PHONE_NUMBER:
            print(f"📤 Sending SMS to {to}: {body}")
            message = client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=body)
            print(f"✅ Message SID: {message.sid}")
        else:
            print("⚠️ Twilio client not initialized or missing TWILIO_PHONE_NUMBER")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")

@app.route("/", methods=["GET"])
def index():
    return "✅ SMS debug version running."
