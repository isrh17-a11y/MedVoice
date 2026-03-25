import google.generativeai as genai
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")

SYSTEM_PROMPT = """
You are MedVoice, a compassionate assistant helping elderly 
patients understand their medical reports. Translate complex 
medical language into simple, warm words a 70-year-old with 
no medical background can understand.

Rules:
- Use short sentences, max 15 words each
- Never use jargon without explaining it immediately
- Be warm and reassuring, never alarming
- If something needs doctor attention say:
  "Your doctor will want to discuss this with you"
- Respond ONLY in this exact JSON format, no markdown, no extra text:
{
  "summary": "2-3 sentence plain English overview",
  "sections": [
    {
      "title": "section name",
      "plain_text": "simple explanation",
      "urgency": "normal"
    }
  ],
  "action_items": ["thing patient should do"],
  "reassurance": "one warm closing sentence"
}
- urgency must be exactly one of: normal, attention, urgent
- If language param is not english, respond in that language
"""

def simplify_report(medical_text: str, language: str = "english") -> dict:
    """
    Takes raw medical report text and returns a structured 
    plain-language dict using Gemini.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        
        user_message = f"Language: {language}\n\nMedical Report:\n{medical_text}"
        
        response = model.generate_content(user_message)
        raw_text = response.text.strip()
        
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()
        
        return json.loads(raw_text)
    
    except json.JSONDecodeError:
        return {
            "summary": response.text,
            "sections": [],
            "action_items": [],
            "reassurance": ""
        }
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")


def ask_followup(question: str, context: str) -> str:
    """
    Answers a patient follow-up question about their report.
    Returns a plain string response.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=(
                "You are MedVoice. Answer the patient's question about "
                "their report in simple language. Max 3 sentences. Be warm "
                "and reassuring. Never use medical jargon without explaining it."
            )
        )
        
        user_message = f"Report summary: {context}\n\nPatient question: {question}"
        response = model.generate_content(user_message)
        return response.text.strip()
    
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")
