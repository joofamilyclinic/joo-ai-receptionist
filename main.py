
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic AI receptionist is live."

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
        response.redirect("/webhook/voice")
    return Response(str(response), mimetype="text/xml")
