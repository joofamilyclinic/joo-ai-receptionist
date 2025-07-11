from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic Webhook is running."

@app.route("/webhook/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/language", method="POST")
    gather.say("Welcome to Zoo Family Clinic. For English, press 1. For Korean, press 2. For Spanish, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/voice")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/language", methods=["POST"])
def language_handler():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()

    if digit == "1":
        gather = Gather(num_digits=1, action="/webhook/english", method="POST")
        gather.say("Thank you for calling. Press 1 to schedule an appointment. Press 2 to ask a question. Press 3 to speak to our staff.", language="en-US")
        response.append(gather)
    elif digit == "2":
        gather = Gather(num_digits=1, action="/webhook/korean", method="POST")
        gather.say("감사합니다. 1번: 진료 예약, 2번: 질문하기, 3번: 직원과 통화.", language="ko-KR")
        response.append(gather)
    elif digit == "3":
        gather = Gather(num_digits=1, action="/webhook/spanish", method="POST")
        gather.say("Gracias por llamar. Presione 1 para programar una cita. 2 para preguntar. 3 para hablar con nuestro personal.", language="es-ES")
        response.append(gather)
    else:
        response.say("Invalid input. Goodbye.", language="en-US")
        response.hangup()

    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english", methods=["POST"])
def english_menu():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()

    if digit == "1":
        response.say("Thank you for choosing the schedule option. We will text you a link to book your appointment.", language="en-US")
        response.hangup()
    elif digit == "2":
        response.say("Please ask a question. I will answer your question.", language="en-US")
        response.pause(length=4)
        response.say("Thank you. We will respond shortly by text.", language="en-US")
        response.hangup()
    elif digit == "3":
        response.say("Please hold while we transfer you to a staff member.", language="en-US")
        response.dial("+14254099247")
    else:
        response.say("Invalid input. Goodbye.", language="en-US")
        response.hangup()

    return Response(str(response), mimetype="text/xml")
