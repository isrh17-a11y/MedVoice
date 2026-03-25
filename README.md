# 🩺 MedVoice

MedVoice is an AI-powered medical report assistant designed for elderly patients. The application takes complex medical reports—such as CBC and chemistry panels—and translates them into simple, warm, plain-language text. To make it even more accessible, MedVoice automatically generates high-quality text-to-speech (TTS) audio of the summary so patients can just hit "play."

## 🚀 Features
- **PDF Extraction**: Instantly pulls text out of standard medical PDF uploads.
- **AI Simplification**: Utilizes the Google Gemini API (`gemini-flash`) to generate empathetic, jargon-free explanations formatted into color-coded urgency sections (Normal, Attention, Urgent).
- **Audio Generation**: Connects to the Murf AI API to generate incredibly realistic AI voices to read the report directly to the user.
- **Conversational QA**: Users can ask natural-language follow-up questions via text or microphone (Web Speech API integration), complete with audio answers.
- **Clean UI**: A fully self-contained HTML/CSS/JS frontend built natively without heavyweight frameworks, styled perfectly for high readability.

---

## 🛠️ Tech Stack
- **Backend**: Python + Flask
- **LLM/AI Engine**: Google Gemini API (`gemini-flash-latest` via REST transport)
- **Voice/TTS Engine**: Murf AI (`v1/speech/generate`)
- **PDF Parsing**: `pdfplumber`
- **Frontend**: Vanilla HTML / JS / CSS
- **Deployment**: Render (Backend) + Vercel (Frontend)

---

## 📥 Setup Instructions (Local Development)

### 1. Prerequisites
- Python 3.10+
- A [Google Gemini API Key](https://aistudio.google.com/)
- A [Murf AI API Key](https://murf.ai/)

### 2. Environment Variables
Create a `.env` file in the root directory (the same level as `backend/`) and populate it with your keys:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
MURF_API_KEY=your_murf_api_key_here
FLASK_PORT=5000
```

### 3. Backend Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run the development server (make sure you are in the `/backend` directory):
   ```bash
   python run main.py
   # Or using gunicorn: gunicorn wsgi:app
   ```

### 4. Frontend Setup
The frontend is a completely self-contained file (`frontend/index.html`). 
Open `frontend/index.html` in an Editor, ensure the `API_BASE` inside the `<script>` tag points to your local Flask backend `http://localhost:5000`, and then simply open `index.html` in a web browser.

---

## 📡 API Usage & Documentation

If you wish to interact with the backend directly or build your own frontend, here are the accessible endpoints:

### 1. `GET /health`
Returns the status of the Flask application.
**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "MedVoice is running"
}
```

### 2. `GET /voices`
Fetches the hardcoded list of available Murf AI profile voices that a user can select.
**Response (200 OK):**
```json
{
  "voices": [
    { "id": "en-US-natalie", "name": "Natalie (Female)" },
    { "id": "en-US-marcus", "name": "Marcus (Male)" }
  ]
}
```

### 3. `POST /process-report`
The core engine. Give it a PDF or a text string, and it yields a fully simplified JSON report complete with generated MP3 audio base64 payload.
**Request Body (`multipart/form-data`):**
- `file` (optional): Uploaded PDF File path
- `text` (optional): Plain text extracted from an external source
- `language` (optional, default `"english"`)
- `voice_id` (optional, default `"en-US-natalie"`)

**Response (200 OK):**
```json
{
  "success": true,
  "audio_available": true,
  "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2Zj...",
  "report": {
    "summary": "This report shows your recent blood test results. Some levels are a bit outside the normal range.",
    "sections": [
      {
        "title": "Hemoglobin",
        "plain_text": "This measures oxygen in your blood. Yours is lower than normal.",
        "urgency": "attention"
      }
    ],
    "action_items": [
      "Get some extra rest today.",
      "Talk to your doctor soon."
    ],
    "reassurance": "We are here to help you feel your best."
  }
}
```

### 4. `POST /ask-followup`
Allows the user to ask questions regarding the generated summary or items inside the report.
**Request Body (`application/json`):**
```json
{
  "question": "What happens if hemoglobin is low?",
  "context": "This report shows your recent blood test results..."
}
```

**Response (200 OK):**
```json
{
  "answer": "If hemoglobin is low, your body isn't getting enough oxygen. This can make you tired or dizzy. Your doctor will help fix this.",
  "audio_available": true,
  "audio_base64": "SUQzBAAAAAA..."
}
```

---
*Created dynamically for the MedVoice project.*
