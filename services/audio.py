import os
from groq import Groq #groq library good for transcribing

#1. initialize the client and grab the API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(file_path: str):
    #open the uploaed audio file in read binary mode
    with open(file_path, 'rb') as file:
        # Send the file to grok's whisper model
        # We give it 3 arguments
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),# send the file name and the data
            model = "whisper-large-v3",#the free model anme
            response_format="text" #we just want raw text back
        )

    # Last step is to return the transcribed text
    return transcription