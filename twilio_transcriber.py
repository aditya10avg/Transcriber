#This file transcribes the audio from twilio and prints it on the console.
import os
import assemblyai as aai 
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")  #Set the api key by retreiving from .env file. 

TWILIO_SAMPLE_RATE = 8000  #Twilio sample rate is 8000 Hz.

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)   #This will be called when our application connects to assemble ai real time speech to text.and
  
    
def on_data(transcipt: aai.RealtimeTranscript):
    if not transcript.text:
        return
    
    if isinstance(transcipt, aai.RealtimeFinalTranscript):
        print(transcipt.text , end='\r\n')  # when we receive the final transcript we will go to new line and at the beginnin and start printing the utterence.
    else:
        print(transcipt.text) # when we receive the interim transcript we will just print it and return to new line.
        

def on_error(error: aai.RealtimeError):
    print("An error has occured:", error)

def on_close():
    print("Closing Session...")
    
class TwilioTranscriber(aai.Transcriber):
    def __init__(self):
        super().__init__(
            on_open=on_open,
            on_data=on_data,
            on_error=on_error,
            on_close=on_close,
            sample_rate=TWILIO_SAMPLE_RATE,
            encoding=aai.AudioEncoding.pcm_mulaw
           )
        
 
        
        
        
        
        