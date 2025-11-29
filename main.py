from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from semantic_search import initialize_indexes, search
from tts import generate_tts_stream
from summary import generate_summary
from pydantic import BaseModel

app = FastAPI(title="Khutbah API - Search + TTS + Summary")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize FAISS indexes at startup
initialize_indexes()


# ---------- Pydantic Models ----------
class SearchRequest(BaseModel):
    query: str
    lang: str = "ar"
    k: int = 5


class TTSRequest(BaseModel):
    text: str
    language_code: str


class SummaryRequest(BaseModel):
    text: str
    language: str = "en"


# ---------- Routes ----------
@app.post("/search")
def search_endpoint(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = search(request.query, request.lang, request.k)
    if not results:
        raise HTTPException(status_code=404, detail="No results found or language not available")

    return JSONResponse({"results": results})


@app.post("/tts")
def tts_endpoint(request: TTSRequest):
    try:
        return generate_tts_stream(request.text, request.language_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-summary")
def summary_endpoint(request: SummaryRequest):
    try:
        result = generate_summary(request.text, request.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def health_check():
    return {"status": "healthy", "services": ["search", "tts", "summary"]}
