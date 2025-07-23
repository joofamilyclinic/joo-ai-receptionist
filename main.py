# main.py with corrected pronunciation for 'Joo' as 'Jew'
app = Flask(__name__)
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
import openai
from twilio.rest import Client

app = Flask(__name__)
