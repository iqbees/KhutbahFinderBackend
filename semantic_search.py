import os
import pickle
from google.cloud import firestore
from sentence_transformers import SentenceTransformer
import faiss
from config import MODEL_NAME, CACHE_DIR, KHUTBAH_COLLECTION

model = SentenceTransformer(MODEL_NAME)
db = firestore.Client()

language_indexes = {}
language_metadata = {}

def load_khutbahs():
    docs = db.collection(KHUTBAH_COLLECTION).stream()
    khutbahs = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = data.get("id", doc.id)
        khutbahs.append(data)
    return khutbahs

def get_or_build_index(lang, texts, meta):
    index_path = f"{CACHE_DIR}/{lang}.index"
    meta_path = f"{CACHE_DIR}/{lang}_meta.pkl"

    if os.path.exists(index_path) and os.path.exists(meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            metadata_list = pickle.load(f)
        return index, metadata_list

    embeddings = model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(meta, f)

    return index, meta

def initialize_indexes():
    all_khutbahs = load_khutbahs()
    langs = set()
    for k in all_khutbahs:
        langs.update(k.get("translations", {}).keys())
    langs.add("ar")

    for lang in langs:
        texts = []
        metadata_list = []

        for k in all_khutbahs:
            if lang == "ar":
                title = k.get("title", "")
                text = f"{title}\n{k.get('text', '')}".strip()
            else:
                trans = k.get("translations", {}).get(lang)
                if not trans:
                    continue
                title = trans.get("title", "")
                text = f"{title}\n{trans.get('text', '')}".strip()

            if not text:
                continue

            texts.append(text)
            metadata_list.append({
                "id": k["id"],
                "title": title,
                "speaker": k.get("speaker", ""),
                "mosque": k.get("mosque", ""),
                "date": k.get("date", "")
            })

        if not texts:
            continue

        index, saved_meta = get_or_build_index(lang, texts, metadata_list)
        language_indexes[lang] = index
        language_metadata[lang] = saved_meta

def search(query: str, lang: str = "ar", k: int = 5):
    if lang not in language_indexes:
        return []

    index = language_indexes[lang]
    meta = language_metadata[lang]

    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(meta[idx])

    return results
