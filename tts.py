import io
from pydub import AudioSegment
from fastapi.responses import StreamingResponse
from google.cloud import texttospeech
from config import LANGUAGE_MAP

def split_text_bytes(text, max_bytes=5000):
    chunks = []
    start = 0
    encoded_text = text.encode("utf-8")
    while start < len(encoded_text):
        end = start + max_bytes
        if end >= len(encoded_text):
            chunks.append(encoded_text[start:].decode("utf-8", errors="ignore"))
            break
        while end > start and (encoded_text[end] & 0b11000000) == 0b10000000:
            end -= 1
        chunks.append(encoded_text[start:end].decode("utf-8", errors="ignore"))
        start = end
    return chunks

def generate_tts_stream(text: str, language_code: str) -> StreamingResponse:
    if language_code not in LANGUAGE_MAP:
        raise ValueError(f"Unsupported language: {language_code}")

    gcp_language_code = LANGUAGE_MAP[language_code]
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code=gcp_language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    chunks = split_text_bytes(text)
    combined_audio = None

    for chunk in chunks:
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=chunk),
            voice=voice,
            audio_config=audio_config
        )
        audio_segment = AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3")
        combined_audio = audio_segment if combined_audio is None else combined_audio + audio_segment

    mp3_buffer = io.BytesIO()
    combined_audio.export(mp3_buffer, format="mp3")
    mp3_buffer.seek(0)

    return StreamingResponse(
        mp3_buffer,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=tts_output.mp3"}
    )
