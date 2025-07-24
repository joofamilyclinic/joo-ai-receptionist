from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial, Say
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Joo Family Clinic AI Receptionist is running."

@app.route("/webhook/voice", methods=["POST"])
def voice_webhook():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/language", method="POST")
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
        response.say("Invalid selection. Goodbye.")
        response.hangup()
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english", methods=["POST"])
def english_menu():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/english_option", method="POST")
    gather.say("For scheduling, press 1. To ask a question, press 2. To talk to our staff, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/korean", methods=["POST"])
def korean_menu():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/korean_option", method="POST")
    gather.say("예약은 1번, 질문은 2번, 직원과 통화는 3번을 누르세요.", language="ko-KR")
    response.append(gather)
    response.redirect("/webhook/korean")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/spanish", methods=["POST"])
def spanish_menu():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/spanish_option", method="POST")
    gather.say("Para programar una cita, presione 1. Para hacer una pregunta, presione 2. Para hablar con el personal, presione 3.", language="es-ES")
    response.append(gather)
    response.redirect("/webhook/spanish")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english_option", methods=["POST"])
def english_option():
    return handle_option(request.form.get("Digits"), "en")

@app.route("/webhook/korean_option", methods=["POST"])
def korean_option():
    return handle_option(request.form.get("Digits"), "ko")

@app.route("/webhook/spanish_option", methods=["POST"])
def spanish_option():
    return handle_option(request.form.get("Digits"), "es")

def handle_option(digit, lang):
    response = VoiceResponse()
    if digit == "1":
        message = {
            "en": "Schedule link has been sent by text.",
            "ko": "예약 링크를 문자로 보냈습니다.",
            "es": "El enlace de programación fue enviado por mensaje de texto."
        }[lang]
        sms_body = {
            "en": "📅 Schedule: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360",
            "ko": "📅 예약 링크: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360",
            "es": "📅 Programar: https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360"
        }[lang]
        response.say(message, language={"en": "en-US", "ko": "ko-KR", "es": "es-ES"}[lang])
        from twilio.rest import Client
        client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        client.messages.create(to=os.environ["TARGET_PHONE_NUMBER"], from_=os.environ["TWILIO_PHONE_NUMBER"], body=sms_body)
    elif digit == "2":
        confirm = {
            "en": "Thank you for your question. We will reply soon by text.",
            "ko": "질문해 주셔서 감사합니다. 곧 문자로 답변드리겠습니다.",
            "es": "Gracias por su pregunta. Le responderemos por mensaje de texto pronto."
        }[lang]
        response.say(confirm, language={"en": "en-US", "ko": "ko-KR", "es": "es-ES"}[lang])
        from twilio.rest import Client
        client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        client.messages.create(to=os.environ["TARGET_PHONE_NUMBER"], from_=os.environ["TWILIO_PHONE_NUMBER"], body=confirm)
    elif digit == "3":
        response.say({
            "en": "Transferring you to our staff.",
            "ko": "직원에게 연결해드리겠습니다.",
            "es": "Le estamos transfiriendo a nuestro personal."
        }[lang], language={"en": "en-US", "ko": "ko-KR", "es": "es-ES"}[lang])
        response.dial("+14254099247")
    else:
        response.say("Invalid selection. Goodbye.")
        response.hangup()
    return Response(str(response), mimetype="text/xml")