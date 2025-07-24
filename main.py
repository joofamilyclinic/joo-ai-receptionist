
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

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
        response.say("Invalid input.", language="en-US")
        response.redirect("/webhook/voice")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english", methods=["POST"])
def english_handler():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/english_menu", method="POST", timeout=5)
    gather.say("You selected English. For appointments, press 1. To ask a question, press 2. To talk to a staff member, press 3.", language="en-US")
    response.append(gather)
    response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/english_menu", methods=["POST"])
def english_menu():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()
    if digit == "1":
        response.say("We will text you the scheduling link.", language="en-US")
    elif digit == "2":
        response.say("Thank you. We will text you shortly.", language="en-US")
    elif digit == "3":
        response.say("Connecting you to a staff member.", language="en-US")
        response.dial("+14254099247")
    else:
        response.say("Invalid input.", language="en-US")
        response.redirect("/webhook/english")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/korean", methods=["POST"])
def korean_handler():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/korean_menu", method="POST", timeout=5)
    gather.say("한국어를 선택하셨습니다. 진료 예약은 1번, 질문은 2번, 직원 연결은 3번을 누르세요.", language="ko-KR")
    response.append(gather)
    response.redirect("/webhook/korean")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/korean_menu", methods=["POST"])
def korean_menu():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()
    if digit == "1":
        response.say("예약 링크를 문자로 보내드리겠습니다.", language="ko-KR")
    elif digit == "2":
        response.say("감사합니다. 곧 문자로 답변드리겠습니다.", language="ko-KR")
    elif digit == "3":
        response.say("직원에게 연결 중입니다.", language="ko-KR")
        response.dial("+14254099247")
    else:
        response.say("잘못된 입력입니다.", language="ko-KR")
        response.redirect("/webhook/korean")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/spanish", methods=["POST"])
def spanish_handler():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/webhook/spanish_menu", method="POST", timeout=5)
    gather.say("Has seleccionado español. Para programar una cita, presiona 1. Para hacer una pregunta, presiona 2. Para hablar con el personal, presiona 3.", language="es-ES")
    response.append(gather)
    response.redirect("/webhook/spanish")
    return Response(str(response), mimetype="text/xml")

@app.route("/webhook/spanish_menu", methods=["POST"])
def spanish_menu():
    digit = request.form.get("Digits", "")
    response = VoiceResponse()
    if digit == "1":
        response.say("Te enviaremos un enlace para programar una cita.", language="es-ES")
    elif digit == "2":
        response.say("Gracias. Te enviaremos un mensaje de texto pronto.", language="es-ES")
    elif digit == "3":
        response.say("Conectando con un miembro del personal.", language="es-ES")
        response.dial("+14254099247")
    else:
        response.say("Entrada inválida.", language="es-ES")
        response.redirect("/webhook/spanish")
    return Response(str(response), mimetype="text/xml")
