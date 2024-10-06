# Real-Time Call Transcription with Twilio and Assembly AI

This project provides a local Flask application that transcribes real-time phone calls made through the Twilio API. It uses Assembly AI for speech-to-text transcription, Ngrok for tunneling, and Flask to handle incoming calls and web socket connections.

## Table of Contents
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [How It Works](#how-it-works)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [License](#license)

## Tech Stack

- **Twilio API**: For making calls and managing voice interactions.
- **Assembly AI**: For converting speech to text.
- **Ngrok**: To create a secure tunnel to your localhost server.
- **Flask**: To create a local development server.
- **Base64**: For decoding incoming audio by converting it into mu-law bytes.
- **Flask-Sock**: To handle WebSocket connections.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aditya10avg/Transcriber.git
   cd Transcriber.git
   ```
2. Create a virtual environment and activate it: (Preferred but optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

``` bash
pip install Flask flask-sock assemblyai python-dotenv ngrok twilio
```

4. Ensure you have an account with Twilio and Assembly AI, and sign up for Ngrok.

5. Usage
Set your environment variables in a .env file:

Create file named .env
```bash
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_API_KEY_SID=your_twilio_api_key_sid
TWILIO_API_SECRET=your_twilio_api_secret
TWILIO_NUMBER=your_twilio_phone_number
NGROK_AUTHENTICATION=your_ngrok_auth_token
```

Run the Flask application:
```bash
python stream.py
```

Make a call to your Twilio number and speak to see your speech being transcribed in the console.

## Code Overview
stream.py: This file contains the main logic for receiving calls, handling audio streams via WebSocket, and integrating with Twilio and Assembly AI.

twilio_transcriber.py: This file handles the connection to Assembly AI and manages the transcription process. Ensure this file is in the same folder as stream.py.

## How It Works
The Flask application listens for incoming POST requests from Twilio at the / endpoint.
Upon receiving a call, it responds with TwiML instructions to connect the call audio to a WebSocket.
The audio stream is sent over the WebSocket connection and processed in real-time.
The audio payload is received in mu-law format, decoded from base64, and then streamed to Assembly AI for transcription.


## Environment Variables
TWILIO_ACCOUNT_SID: Your Twilio account SID.
TWILIO_API_KEY_SID: Your Twilio API Key SID.
TWILIO_API_SECRET: Your Twilio API Secret.
TWILIO_NUMBER: Your Twilio phone number.
NGROK_AUTHENTICATION: Your Ngrok authentication token.


## Dependencies
Flask
Flask-Sock
Twilio
Assembly AI
Ngrok
python-dotenv


### Notes:

- Ensure that `twilio_transcriber.py` is well-documented to provide additional context about its functionality.
- You may want to add more detailed instructions or sections depending on your audience's technical knowledge.
