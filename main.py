
# Flask + Twilio + GPT + Zapier + Voice Menu
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
import openai, os, requests, datetime

app = Flask(__name__)

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
