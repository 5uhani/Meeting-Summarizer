# Meeting Summarizer

Meeting Summarizer is a modern, full-stack web application designed to automatically transcribe meeting audio recordings and extract structured, actionable insights. By leveraging **Deepgram's Nova-2** model for lightning-fast speech-to-text conversion and **Google Gemini** for intelligent linguistic analysis, the platform transforms raw conversation into an executive summary, concrete decisions, and key action items instantly.

---

## Features

* **Seamless Audio Processing:** Drag-and-drop or browse to upload `.wav`, `.mp3`, or `.m4a` files with instant frontend extension validation.
* **High-Fidelity Transcription:** Uses Deepgram's native REST orchestration for accurate word-for-word transcripts with smart formatting (automatic punctuation and paragraph structures).
* **AI-Driven Analytics:** Automated breakdown of transcripts into structured blocks:
    *  **Executive Summary:** A high-level overview of the discussion.
    *  **Action Items:** Explicitly assigned tasks with designated owners.
    *  **Key Decisions:** Critical conclusions reached during the session.
* **Intelligent Fallback Engine:** A local, rule-based keyword extraction system handles text processing seamlessly if external LLM APIs hit rate limits or quota caps.
* **Dynamic Response Compatibility:** The API provides dual-casing mappings (both `camelCase` and `snake_case`) to ensure native compatibility with varied frontend implementations.
* **Modern Responsive Dashboard:** A tailored interface featuring colored data cards, micro-animations, and an interactive, collapsible monospace transcript viewer.

---

##  Technology Stack

### Frontend
* **Framework:** React 19.2.7
* **Build Tool & Bundler:** Vite 8.1.1 (Fast HMR & optimized builds)
* **Styling:** Tailwind CSS 4.3.2 + `@tailwindcss/vite`
* **Linting:** ESLint with native React hooks enforcement

### Backend
* **Framework:** FastAPI (Python)
* **ASGI Server:** Uvicorn
* **Environment Management:** `python-dotenv`
* **HTTP Client:** `requests` for robust REST interaction

### Core Services & APIs
* **Transcription:** Deepgram API (`nova-2` model)
* **LLM Analysis:** Google Generative AI SDK (Multi-model fallback strategy)

---

##  Project Architecture & File Structure

```text
meeting-summarizer-workspace/
├── meeting-summarizer/          # Frontend Application (React + Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx  # Drag-and-drop landing area
│   │   │   ├── Loader.jsx      # Async processing spinner
│   │   │   └── Results.jsx     # Analytics & transcript dashboard
│   │   ├── App.jsx             # State orchestration & layout view
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styling
│   ├── package.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── index.html
│
└── summarizer-backend/          # Backend Service (FastAPI)
    ├── venv/                    # Python virtual environment
    │   ├── main.py             # FastAPI app & REST endpoints
    │   ├── speech_service.py   # Deepgram audio streaming logic
    │   ├── llm_service.py      # Gemini integration & keyword fallback
    │   └── .env                # Local secrets configuration
    ├── temp_audio/             # Transient storage for active uploads
    ├── requirements.txt        # Python dependencies
    └── venv/                   # Python dependencies location
```

---

##  API Documentation

### **POST** `/api/summarize`

Processes a binary or multi-part meeting audio recording, translates the file into formatted text, and applies intelligent parsing.

#### Request Details
- **Content-Type:** `multipart/form-data`
- **Parameter:** `file` (Binary file data matching `.wav`, `.mp3`, or `.m4a`)
- **Response Status:** `200 OK`

#### Example Response Schema

```json
{
  "summary": "The engineering team evaluated modern frontend styling utilities and scheduled upcoming API credential provisioning.",
  "executive_summary": "The engineering team evaluated modern frontend styling utilities and scheduled upcoming API credential provisioning.",
  "decisions": [
    "Adopted Tailwind CSS v4.0 for the production web app layout architecture.",
    "Decided to phase out legacy cloud provider configurations entirely."
  ],
  "key_decisions": [
    "Adopted Tailwind CSS v4.0 for the production web app layout architecture.",
    "Decided to phase out legacy cloud provider configurations entirely."
  ],
  "actionItems": [
    "Sarah to update code dependencies and verify styling build pipes by tomorrow.",
    "John to rotate active backend credentials before Friday's standup."
  ],
  "action_items": [
    "Sarah to update code dependencies and verify styling build pipes by tomorrow.",
    "John to rotate active backend credentials before Friday's standup."
  ],
  "transcript": "Alright team, let's sync up. For the layout styling, we will use Tailwind v4. Sarah, can you finalize that setup by tomorrow? Also, John, make sure the API keys are rotated before Friday."
}
```

---

##  Setup & Installation

### Prerequisites

- Node.js (v18+ recommended)
- Python 3.10+
- A Deepgram API Key
- A Google Gemini API Key

### 1. Backend Configuration

Navigate to the backend directory, initialize your Python environment, and configure secrets:

```bash
cd summarizer-backend

# Create and activate virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

Create a `.env` file in the root of the `summarizer-backend/` directory:

```env
DEEPGRAM_API_KEY="your_deepgram_api_key"
GEMINI_API_KEY="your_google_gemini_api_key"
```

Start the FastAPI application server:

```bash
uvicorn main:app --reload
```

The backend server will instantiate locally at `http://localhost:8000`.

### 2. Frontend Configuration

Open a secondary terminal window, navigate into the frontend directory, and launch the development server:

```bash
cd meeting-summarizer

# Install project dependencies
npm install

# Start the Vite HMR server
npm run dev
```

The interface will be accessible via your browser at `http://localhost:5173`.

---

##  Core Engineering Protocols

### System Data Flow

```
[User File Upload] ──> (React Frontend) ──> [HTTP POST /api/summarize]
                                                     │
                                             (FastAPI Validation)
                                                     │
                                    (Deepgram Transcription)
                                                     │
                                    (Gemini LLM Analysis / Fallback)
                                                     │
[JSON Data Payload] <── (React Dashboard) <── (Structured JSON Response)
```

### Intelligent Fallback Architecture

To circumvent standard sandbox API limits or potential third-party network outages, `llm_service.py` features a multi-tiered fallback schema:

1. **Sequential Model Cascade:** System attempts available models in priority order:
   - `gemini-2.0-flash`
   - `gemini-2.0-flash-exp`
   - `gemini-pro`
   - `gemini-1.5-flash`

2. **API Failure Handling:** If total API failure occurs or rate caps trigger, the local keyword matching engine activates.

3. **Keyword Extraction:** The backup system inspects the transcript string via programmatic token queries:
   - **Decisions:** Looks for terms like `decided`, `agreed`, `determined`, `chose`
   - **Action Items:** Looks for terms like `assigned`, `responsible`, `will handle`, `owner`

4. **Local Structuring:** Extracted sentences are formatted into a clean JSON structure locally, avoiding service downtime.

### Memory & Lifecycle Optimization

- **Stateless Operation:** The API acts as a pure stream transformation pipeline—no underlying disk space is tied up by databases.
- **Storage Sanitization:** Uploaded files stream down into `temp_audio/` using standard async buffered chunks. A strict `finally` completion block triggers right after execution, ensuring the temporary audio file is deleted even if the downstream transcription fails.

---

##  Usage Guide

### Step 1: Start the Backend
```bash
cd summarizer-backend
.\venv\Scripts\activate  # Windows
python -m uvicorn main:app --reload
```

### Step 2: Start the Frontend
```bash
cd meeting-summarizer
npm run dev
```

### Step 3: Upload Audio
1. Navigate to `http://localhost:5173`
2. Click or drag-and-drop an audio file (`.wav`, `.mp3`, or `.m4a`)
3. Wait for the spinner to complete
4. View your meeting summary, decisions, and action items
5. Expand the transcript viewer to see the full transcription

---

##  Development

### Building for Production

**Frontend:**
```bash
cd meeting-summarizer
npm run build    # Creates optimized dist/ folder
npm run preview  # Preview production build locally
```

**Backend:**
The backend is production-ready with Uvicorn. Deploy using:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Linting & Code Quality

**Frontend:**
```bash
npm run lint     # Run ESLint checks
```

---

##  Environment Variables

Create a `.env` file in `summarizer-backend/` with:

```env
# Deepgram API Configuration
DEEPGRAM_API_KEY=your_api_key_here

# Google Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
```

> ** Security Note:** Never commit `.env` files to version control. Add `.env` to your `.gitignore`.

---

##  Supported Audio Formats

- `.wav` (Waveform Audio File Format)
- `.mp3` (MPEG Audio)
- `.m4a` (MPEG-4 Audio)

All formats are validated server-side before processing.

---

##  Performance & Optimization

- **Frontend:** Vite provides fast HMR for rapid development iteration
- **Backend:** Uvicorn async server handles concurrent requests efficiently
- **Transcription:** Deepgram processes audio with minimal latency
- **LLM:** Multi-model strategy ensures fast response times
- **Fallback:** Local keyword extraction provides instant processing without network I/O

---

##  Troubleshooting

### Backend Won't Start
- Verify Python 3.10+ is installed: `python --version`
- Check virtual environment is activated
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check port 8000 is not in use: `netstat -ano | findstr :8000`

### Frontend Won't Start
- Verify Node.js 18+ is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 5173 is not in use

### API Key Issues
- Verify `.env` file exists in `summarizer-backend/`
- Check API keys are correct (no extra quotes or spaces)
- Test Deepgram and Gemini keys on their respective platforms

### Transcription Quality
- Ensure audio file is clear and audible
- Try shorter audio files initially for testing
- Check Deepgram dashboard for usage quota

---

