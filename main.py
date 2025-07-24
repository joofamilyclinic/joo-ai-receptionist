
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic Webhook is running."

# Voice, language, English, Korean, Spanish routes follow...
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
        response.say("Sorry, invalid input.")
        response.redirect("/webhook/voice")

    return Response(str(response), mimetype="text/xml")
@app.route("/webhook/english", methods=["POST"])
def english_handler():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/english-option", method="POST", timeout=5)
    gather.say("Welcome to Jew Family Clinic. For appointments, press 1. To ask a question, press 2. To speak with staff, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")
