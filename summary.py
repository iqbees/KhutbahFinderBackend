import google.generativeai as genai
from config import LANGUAGE_NAMES
import os

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_summary(text: str, language: str = "en") -> dict:
    if not text.strip():
        raise ValueError("Text cannot be empty")

    model = genai.GenerativeModel('gemini-2.5-flash')
    target_language = LANGUAGE_NAMES.get(language, "English")

    prompt = f"""
    Please analyze the following Islamic khutbah text and provide a comprehensive summary.

    TEXT TO SUMMARIZE:
    {text}

    IMPORTANT INSTRUCTIONS:
    1. Write the entire summary in {target_language} language
    2. Keep the summary clear, concise, and easy to understand
    3. Focus on the main religious teachings and practical lessons
    4. Structure the summary with these key elements:
       - Main themes and topics discussed
       - Key Islamic teachings and principles
       - Practical advice and recommendations for daily life
       - Spiritual benefits and lessons learned

    5. Make the summary helpful for someone who wants to quickly understand the khutbah's message
    6. Use appropriate religious terminology that resonates with Muslim audiences
    7. Ensure the summary flows naturally in {target_language}

    Write the summary now in {target_language}:
    """

    response = model.generate_content(prompt)
    if not response.text:
        raise RuntimeError("Failed to generate summary")

    return {
        "summary": response.text,
        "language": language,
        "target_language": target_language,
        "original_text_length": len(text),
        "summary_length": len(response.text)
    }
