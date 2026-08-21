# llm_service.py
import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))
load_dotenv()


def _build_fallback_summary(transcript: str) -> dict:
    """
    Intelligently extract meeting summary, decisions, and action items
    from the transcript without using Gemini.
    """
    cleaned = " ".join(transcript.split())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
    
    # Summary: First 1-2 sentences
    summary = " ".join(sentences[:2]) if sentences else "Meeting transcript received."
    if len(summary) > 250:
        summary = summary[:247] + "..."
    
    # Extract decisions (look for keywords like "decided", "will", "should", "must")
    decision_keywords = ["decided", "will", "should", "must", "agreed", "determined", "chose"]
    decisions = []
    for sentence in sentences:
        lower_sent = sentence.lower()
        if any(keyword in lower_sent for keyword in decision_keywords):
            if len(decisions) < 3 and sentence not in decisions:
                decisions.append(sentence[:150] + ("..." if len(sentence) > 150 else ""))
    
    if not decisions:
        decisions = ["Review the meeting discussion points for key decisions."]
    
    # Extract action items (look for keywords like "assign", "task", "responsible", "owner", "need to")
    action_keywords = ["assign", "task", "responsible", "owner", "need to", "will do", "will handle", "responsible for", "will take"]
    action_items = []
    for sentence in sentences:
        lower_sent = sentence.lower()
        if any(keyword in lower_sent for keyword in action_keywords):
            if len(action_items) < 3 and sentence not in action_items:
                action_items.append(sentence[:150] + ("..." if len(sentence) > 150 else ""))
    
    if not action_items:
        action_items = ["Follow up on discussed topics and track progress."]
    
    return {
        "summary": summary,
        "decisions": decisions,
        "actionItems": action_items,
    }


def generate_meeting_summary(transcript: str) -> dict:
    """
    Takes a raw meeting transcript, passes it to Gemini,
    and returns a structured JSON dictionary.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("GEMINI_API_KEY is missing; using fallback summary.")
        return _build_fallback_summary(transcript)

    genai.configure(api_key=gemini_key)
    
    # Try multiple model names in order of preference
    models_to_try = [
        'gemini-2.0-flash',
        'gemini-2.0-flash-exp',
        'gemini-pro',
        'gemini-1.5-flash',
    ]

    prompt = f"""
    You are an expert executive assistant. Analyze the following meeting transcript.
    Return a strict JSON object containing exactly three keys:
    1. "summary": A concise summary of the overall discussion.
    2. "decisions": An array of strings detailing the final decisions made.
    3. "actionItems": An array of strings detailing specific tasks assigned.

    Do not include any markdown formatting (like ```json) or extra text outside of the JSON.

    Transcript:
    {transcript}
    """

    print("Sending transcript to Gemini for summarization...")
    
    for model_name in models_to_try:
        try:
            print(f"  Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            # Force Gemini to return JSON
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                ),
            )
            
            # Convert the JSON string into a Python dictionary
            result_dict = json.loads(response.text)
            print(f"✅ Gemini summarization successful with model: {model_name}")
            return result_dict

        except Exception as e:
            error_msg = str(e)
            print(f"  ✗ {model_name} failed: {error_msg[:100]}...")
            continue
    
    print(f"\n⚠️ All Gemini models failed. Using fallback summary.\n")
    return _build_fallback_summary(transcript)