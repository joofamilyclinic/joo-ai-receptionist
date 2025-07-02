
# Flask + Twilio + GPT + Zapier + Voice Menu
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from twilio.twiml.messaging_response import MessagingResponse
import openai, os, requests, datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
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
        response.say("You selected English. Please leave a message after the beep.", language="en-US")
    elif digit == "2":
        response.say("한국어를 선택하셨습니다. 삐 소리 후에 메시지를 남겨 주세요.", language="ko-KR")
    elif digit == "3":
        response.say("Seleccionó español. Por favor deje un mensaje después del tono.", language="es-MX")
    else:
        response.say("Invalid selection. Goodbye.", language="en-US")
        response.hangup()
        return Response(str(response), mimetype="text/xml")

    # Record message
    response.record(timeout=10, max_length=60, action="/webhook/recording_done", play_beep=True)
    return Response(str(response), mimetype="text/xml")

@app.route("/appointments", methods=["GET"])
def show_appointments():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Schedule Appointment | Joo Family Clinic</title>
        <style>
            body { margin: 0; font-family: Arial, sans-serif; }
            #iframeContainer {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            #iframeBox {
                position: relative;
                width: 90%; height: 90%;
                background: white;
                border-radius: 8px;
                overflow: hidden;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
            }
        </style>
    </head>
    <body>
        <div id="iframeContainer">
            <div id="iframeBox">
                <iframe src="https://d2oe0ra32qx05a.cloudfront.net/?practiceKey=k_1_14360"></iframe>
            </div>
        </div>
    </body>
    </html>
    """




@app.route("/webhook/recording_done", methods=["POST"])
def recording_done():
    return Response("Thank you. Your message has been received.", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

# Include this!
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

openai.api_key = os.getenv("OPENAI_API_KEY")
zapier_url = os.getenv("ZAPIER_URL")  # from Zapier webhook trigger

def get_gpt_reply(message, lang="en"):
    prompt = f"""
You are a bilingual AI receptionist for a family clinic.
Reply in Korean if the message is in Korean. Otherwise, reply in English.
If the patient asks to schedule an appointment, reply with:
'You can schedule online at https://yourclinic.tebra.com/schedule'

If they mention forms or paperwork, reply:
'Please complete your intake form here: https://yourclinic.tebra.com/forms'

Respond briefly and professionally. Message: "{message}"
"""
    res = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return res['choices'][0]['message']['content']

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    from_number = request.form.get("From", "")
    reply = get_gpt_reply(incoming_msg)
    final_reply = f"{reply}\n\n✅ Your request was received. 응급 상황은 911로 전화해주세요."

    # Log to Zapier
    if zapier_url:
        requests.post(zapier_url, json={
            "from": from_number,
            "message": incoming_msg,
            "reply": reply,
            "timestamp": str(datetime.datetime.now())
        })

    resp = MessagingResponse()
    resp.message(final_reply)
    return str(resp)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/language", method="POST")
    gather.say("Welcome to Dr. Joo's clinic. Press 1 for English. Press 2 for Korean.", voice='Polly.Joanna')
    response.append(gather)
    response.redirect("/voice")
    return str(response)

@app.route("/language", methods=["POST"])
def language():
    digit = request.form.get('Digits')
    lang = "en" if digit == "1" else "ko"
    prompt = "I want to schedule an appointment" if lang == "en" else "진료 예약하고 싶어요"
    reply = get_gpt_reply(prompt, lang)

    vr = VoiceResponse()
    vr.say(reply, voice='Polly.Seoyeon' if lang == "ko" else 'Polly.Joanna')
    return str(vr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
