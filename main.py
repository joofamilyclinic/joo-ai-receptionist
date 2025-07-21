
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from send_sms import send_sms

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic Webhook is running."

@app.route("/webhook/voice", methods=["POST"])
def voice_webhook():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/language", method="POST", timeout=5)
    gather.say("Welcome to Joo Family Clinic. For English, press 1. For Korean, press 2. For Spanish, press 3.", language="en-US")
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

@app.route("/webhook/english", methods=["POST"])
def english():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/english_option", method="POST", timeout=5)
    gather.say("For scheduling, press 1. For a question, press 2. To talk to a staff member, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english_option", methods=["POST"])
def english_option():
    digit = request.form.get("Digits", "")
    from_number = request.form.get("To", "")
    user_number = request.form.get("From", "")
    response = VoiceResponse()

    if digit == "1":
        send_sms(user_number, "📅 Schedule: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360")
        response.say("We will text you the appointment link shortly.", language="en-US")
        response.hangup()
    elif digit == "2":
        send_sms(user_number, "❓Thank you. Please reply to this message with your question.")
        response.say("Thank you. We will text you shortly.", language="en-US")
        response.hangup()
    elif digit == "3":
        response.say("Connecting you to a staff member.", language="en-US")
        response.dial("+14254099247")
    else:
        response.say("Invalid option.")
        response.redirect("/webhook/english")

    return Response(str(response), mimetype="text/xml")

# More routes (korean, spanish, etc.) can be added here following the same pattern.
