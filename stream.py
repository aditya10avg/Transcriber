#  This file receives the audio from the call. Currently we are not getting POST request from twilio while calling.


import os
import base64   # We require this to decode incoming audio from twilio.
import json

from flask import Flask, request , Response  # This will help us to create a post request and also get the response.
from flask_sock import Sock
from twilio_transcriber import TwilioTranscriber
import ngrok
from twilio.rest import Client
from dotenv import load_dotenv


#Flask settings 
PORT=5001
DEBUG=False 
INCOMING_CALL_ROUTE='/'   #Endpoint in our app to receive twilio calls
WEBSOCKET_ROUTE='/realtime'   #Route to websocket to which the audio stream will be sent 

#Twilio authentication 
account_sid=os.environ["TWILIO_ACCOUNT_SID"]
api_key=os.environ["TWILIO_API_KEY_SID"]
api_secret=os.environ["TWILIO_API_SECRET"]
client = Client(account_sid,api_key,api_secret)
                

#Adding Twilio Number
Twilio_Number= os.environ["TWILIO_NUMBER"]


#ngrok authentication
ngrok.set_auth_token(os.environ["NGROK_AUTHENTICAITON"])    

app = Flask(__name__)
sock = Sock(app)

@app.route(INCOMING_CALL_ROUTE, methods=['GET', 'POST'])
def receive_call():
    if request.method == 'POST':
        xml = f"""
     <Response>
        <Say>
          Speak to see your speech being transcribed in the console.
        </Say>
        <Connect> 
          <Stream name="audio" url="wss://{request.host}{WEBSOCKET_ROUTE}"/>
        </Connect>
      </Response>""".strip()  
        return Response(xml, mimetype='text/xml')  # To return the flask response.
    else:
        return "Real-time phone call transcription"

@sock.route(WEBSOCKET_ROUTE)
def transcription_websocket(ws):
    while True:
        data= json.loads(ws.receive())
        match data['event']:
            case "connected":
                transcriber = TwilioTranscriber()
                transcriber.connect() # This connect this transciber to assembly ai transcriber.
                print("Twilio Connected")
            case "started":
                print("Twilio Started")    
            case "media":
                payload_b64= data["media"]["payload"]  #payload coming from twilio
                payload_mulaw=base64.b64decode(payload_b64)  #Decoding the payload
                transcriber.stream(payload_mulaw)  #Streaming the payload
            case "stop":
                print("Twilio Connection stopped")
                transciber.close()
                print("transcriber closed")
    

if __name__ == '__main__':     #This will run only when this file is run directly.
    try:
        #open ngrok tunnel
        listener = ngrok.forward(f"http://localhost:{PORT}")
        ngrok_url=listener.url()
        
        # Set ngrok url to be the webhook for twilio calls. 
        twilio_numbers = client.incoming_phone_numbers.list()
        twilio_numbers_sid= [num.sid for num in twilio_numbers if num.phone_number == Twilio_Number][0]    
        client.incoming_phone_numbers(twilio_numbers_sid).update(account_sid,voice_url=f"{ngrok_url}{INCOMING_CALL_ROUTE}")
    
        app.run(debug=DEBUG,host='0.0.0.0',port=PORT) 
    except:
        ngrok.disconnect()  #This will disconnect ngrok tunnel if any error occurs.
    
    
    



#How actually the payload section is working with mulaw ? Read here .... 
#Twilio takes the raw data, uses mulaw algo to do byte to byte mapping to convert the audio data from Twilio into mulaw format and encodes this bytes as base64 string. These mulaw bites are sent to assembly ai transcipt. 