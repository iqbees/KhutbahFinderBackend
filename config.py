import os

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CACHE_DIR = "faiss_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

KHUTBAH_COLLECTION = "khutbahs"

LANGUAGE_MAP = {
    "ar": "ar-XA",
    "en": "en-US",
    "id": "id-ID",
    "ur": "ur-PK",
    "bn": "bn-BD",
    "tr": "tr-TR",
    "fa": "fa-IR",
    "ha": "ha-NG",
    "ps": "ps-AF",
    "ms": "ms-MY",
    "fr": "fr-FR"
}

LANGUAGE_NAMES = {
    "ar": "Arabic",
    "en": "English",
    "id": "Indonesian",
    "tr": "Turkish",
    "ur": "Urdu",
    "fa": "Farsi",
    "bn": "Bengali",
    "ha": "Hausa",
    "ps": "Pashto",
    "ms": "Malay",
    "fr": "French",
}
