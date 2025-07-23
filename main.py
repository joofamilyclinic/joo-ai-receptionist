# Placeholder main.py
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
app = Flask(__name__)
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
        response.say("Sorry, invalid input.")
        response.redirect("/webhook/voice")

    return Response(str(response), mimetype="text/xml")
