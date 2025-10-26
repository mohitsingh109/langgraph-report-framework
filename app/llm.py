import google.generativeai as genai
from .config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

def llm_complete(prompt: str) -> str:
    print("GEMINI Request:", prompt)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    response = model.generate_content(prompt)
    response_text  =response.text or "(no response 🥺)"
    print("GEMINI Response:", response_text)
    return response_text
