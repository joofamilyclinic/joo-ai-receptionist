
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic Webhook is running."

@app.route("/webhook/voice", methods=["POST"])
def voice_webhook():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/language", method="POST", timeout=5)
    gather.say("Welcome to Jew Family Clinic. For English, press 1. For Korean, press 2. For Spanish, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/voice")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/language", methods=["POST"])
def language_handler():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()
    if digit == "1":
        response.redirect("/webhook/english")
    elif digit == "2":
        response.redirect("/webhook/korean")
    elif digit == "3":
        response.redirect("/webhook/spanish")
    else:
        response.say("Invalid input.")
        response.redirect("/webhook/voice")
    return Response(str(response), mimetype="text/xml")

def send_sms(body):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        to_number = os.getenv("TARGET_PHONE_NUMBER")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"✅ Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ SMS failed: {str(e)}")

@app.route("/webhook/english", methods=["POST"])
def english_handler():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/english-menu", method="POST", timeout=5)
    gather.say("For scheduling an appointment, press 1. To ask a question, press 2. To speak to our staff, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english-menu", methods=["POST"])
def english_menu():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()
    if digit == "1":
        response.say("We will text you the appointment link shortly.", language="en-US")
        send_sms("📅 Schedule: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360")
    elif digit == "2":
        response.say("Thank you. We will reply to your question by text.", language="en-US")
        send_sms("❓ Thank you for your question. We'll respond soon.")
    elif digit == "3":
        response.say("Connecting you to a staff member.", language="en-US")
        dial = Dial()
        dial.number("4254099247")
        response.append(dial)
    else:
        response.say("Invalid input.")
        response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")
