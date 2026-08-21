import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

# Ensure environment variables are loaded from the backend folder or the virtualenv folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))
load_dotenv()

def transcribe_audio_with_azure(file_path: str) -> str:
    """
    Takes a local audio file path, sends it to Deepgram Nova, 
    and returns the transcribed text. 
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")

    print("Sending audio to Deepgram...")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPGRAM_API_KEY is not set. Add it to the backend .env file.")

    # 1. Initialize the client with the API key from the environment.
    deepgram = DeepgramClient(api_key=api_key)

    # 2. Read the file and send it using the new v1 Media API
    with open(file_path, "rb") as file:
        response = deepgram.listen.v1.media.transcribe_file(
            request=file.read(),
            model="nova-2",
            smart_format=True
        )

    # 3. Extract the transcript
    transcript = response.results.channels[0].alternatives[0].transcript
    
    if not transcript:
        raise Exception("Deepgram returned an empty transcript.")
        
    print("Deepgram transcription successful!")
    return transcript