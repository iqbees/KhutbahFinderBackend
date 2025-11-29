# Khutbah API - Semantic Search, TTS, and Summary

This is a FastAPI-based backend that provides:

- **Semantic search** for khutbahs using multilingual embeddings (FAISS + Sentence Transformers).
- **Text-to-Speech (TTS)** generation using Google Cloud TTS.
- **Automated summary** generation using Google Gemini (Generative AI).

---

## Features

1. **Search Khutbahs**
   - Endpoint: `POST /search`
   - Request JSON:
     ```json
     {
       "query": "pray",
       "lang": "en",
       "k": 10
     }
     ```
   - Returns top `k` khutbahs matching the query.

2. **Text-to-Speech**
   - Endpoint: `POST /tts`
   - Request JSON:
     ```json
     {
       "text": "Sample khutbah text",
       "language_code": "en"
     }
     ```
   - Returns MP3 audio stream of the text.

3. **Generate Summary**
   - Endpoint: `POST /generate-summary`
   - Request JSON:
     ```json
     {
       "text": "Full khutbah text",
       "language": "en"
     }
     ```
   - Returns a concise summary in the requested language.

4. **Health Check**
   - Endpoint: `GET /`
   - Returns API status and available services.

---

## Setup Instructions

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-folder>

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GEMINI_API_KEY="your-gemini-api-key"

# 5. Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
