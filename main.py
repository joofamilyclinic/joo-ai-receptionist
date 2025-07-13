
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
    if client and TWILIO_PHONE_NUMBER:
        client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=body)

@app.route("/", methods=["GET"])
def index():
    return "✅ Joo Family Clinic Webhook is running."

@app.route("/webhook/voice", methods=["POST"])
def voice():
    r = VoiceResponse()
    g = Gather(num_digits=1, action="/webhook/language", method="POST")
    g.say("Welcome to Zoo Family Clinic. For English press 1. For Korean press 2. For Spanish press 3.", language="en-US")
    r.append(g)
    r.redirect("/webhook/voice")
    return Response(str(r), mimetype="text/xml")

@app.route("/webhook/language", methods=["POST"])
def language():
    digit = request.form.get("Digits", "")
    r = VoiceResponse()
    if digit == "1":
        g = Gather(num_digits=1, action="/webhook/english", method="POST")
        g.say("Press 1 to schedule. 2 to ask a question. 3 to speak to our staff.", language="en-US")
        r.append(g)
    elif digit == "2":
        g = Gather(num_digits=1, action="/webhook/korean", method="POST")
        g.say("1번: 예약. 2번: 질문. 3번: 직원 연결.", language="ko-KR")
        r.append(g)
    elif digit == "3":
        g = Gather(num_digits=1, action="/webhook/spanish", method="POST")
        g.say("Presione 1 para cita. 2 para pregunta. 3 para hablar con personal.", language="es-ES")
        r.append(g)
    else:
        r.say("Invalid input.", language="en-US")
        r.hangup()
    return Response(str(r), mimetype="text/xml")

@app.route("/webhook/english", methods=["POST"])
def english():
    digit = request.form.get("Digits", "")
    caller = request.form.get("From", "")
    r = VoiceResponse()
    if digit == "1":
        r.say("We will text you the link to schedule.", language="en-US")
        send_sms(caller, "📅 Schedule: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360")
    elif digit == "2":
        r.say("Please ask your question.", language="en-US")
        r.pause(length=2)
        send_sms(caller, "❓ Thank you! We’ll reply soon.")
    elif digit == "3":
        r.say("Connecting to staff.", language="en-US")
        r.dial("+14254099247")
    else:
        r.say("Invalid.", language="en-US")
    r.hangup()
    return Response(str(r), mimetype="text/xml")

@app.route("/webhook/korean", methods=["POST"])
def korean():
    digit = request.form.get("Digits", "")
    caller = request.form.get("From", "")
    r = VoiceResponse()
    if digit == "1":
        r.say("예약 링크를 문자로 보내드리겠습니다.", language="ko-KR")
        send_sms(caller, "📅 예약 링크: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360")
    elif digit == "2":
        r.say("질문해 주세요. 문자로 답변드릴게요.", language="ko-KR")
        send_sms(caller, "❓ 질문 감사합니다. 곧 답변 드릴게요.")
    elif digit == "3":
        r.say("직원에게 연결합니다.", language="ko-KR")
        r.dial("+14254099247")
    else:
        r.say("잘못된 입력입니다.", language="ko-KR")
    r.hangup()
    return Response(str(r), mimetype="text/xml")

@app.route("/webhook/spanish", methods=["POST"])
def spanish():
    digit = request.form.get("Digits", "")
    caller = request.form.get("From", "")
    r = VoiceResponse()
    if digit == "1":
        r.say("Le enviaremos el enlace por mensaje de texto.", language="es-ES")
        send_sms(caller, "📅 Reserve aquí: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360")
    elif digit == "2":
        r.say("Gracias por su pregunta. Le responderemos por mensaje.", language="es-ES")
        send_sms(caller, "❓ Gracias por su pregunta.")
    elif digit == "3":
        r.say("Transfiriendo ahora.", language="es-ES")
        r.dial("+14254099247")
    else:
        r.say("Selección inválida.", language="es-ES")
    r.hangup()
    return Response(str(r), mimetype="text/xml")
