from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize pyttsx3 (text to speech engine)
engine = pyttsx3.init()

# Function to convert text to speech
def text_to_speech(text):
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()
    return 'output.mp3'

# Function to summarize text
def summarize_text(text):
    parser = PlaintextParser.from_string(text, PlaintextParser.from_string(text, ''))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize the text to 2 sentences
    return ' '.join([str(sentence) for sentence in summary])

# Root route to display instructions
@app.route('/')
def home():
    instructions = """
    # Text to Speech API

    ## Description
    This API converts text to speech and provides a summarized version of the text.

    ## Endpoints

    ### POST /convert
    - **Request**: Send a JSON object with the `text` field.
      Example request body:
      ```json
      {
        "text": "This is a test message."
      }
      ```

    - **Response**:
      The API will return the original text and a summarized version of it.
      ```json
      {
        "original_text": "This is a test message.",
        "summary": "This is a test message."
      }
      ```

    ## How to Run Locally
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

    - Run the app:
      ```bash
      python app.py
      ```

    ## How to Deploy on Vercel
    - Push your code to GitHub.
    - Link the repository to Vercel for automatic deployment.
    """
    return instructions

# Convert text to speech and summarize the text
@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Convert text to speech
    audio_file = text_to_speech(text)

    # Summarize the text
    summary = summarize_text(text)

    return jsonify({
        'original_text': text,
        'summary': summary,
        'audio_file': audio_file  # This would point to the audio file generated
    })

if __name__ == '__main__':
    app.run(debug=True)
