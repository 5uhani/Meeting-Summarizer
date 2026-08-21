# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from dotenv import load_dotenv

from speech_service import transcribe_audio_with_azure
from llm_service import generate_meeting_summary  # <-- 1. Import the new service

load_dotenv()

app = FastAPI(title="Meeting Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/summarize")
async def summarize_meeting(file: UploadFile = File(...)):
    if not file.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(status_code=400, detail="Invalid file format.")

    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Transcribe with Deepgram
        transcript = transcribe_audio_with_azure(file_path)
        
        # 2. Summarize with Gemini
        ai_data = generate_meeting_summary(transcript)
        
        # 3. Combine the results and send them to React
        final_response = {
            # Summary keys (both naming conventions)
            "summary": ai_data.get("summary", "No summary available."),
            "executive_summary": ai_data.get("summary", "No summary available."),
            
            # Decisions keys (both naming conventions)
            "decisions": ai_data.get("decisions", []),
            "key_decisions": ai_data.get("decisions", []),
            
            # Action items keys (both naming conventions)
            "actionItems": ai_data.get("actionItems", []),
            "action_items": ai_data.get("actionItems", []),
            
            # Transcript key
            "transcript": transcript
        }

        return final_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)