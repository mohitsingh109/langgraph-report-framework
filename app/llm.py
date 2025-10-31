from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from .config import settings


def llm_complete(prompt: str) -> str:
    print("GEMINI Request:", prompt)
    llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL)
    response = llm.invoke(prompt)
    response_text  =response.text or "(no response 🥺)"
    print("GEMINI Response:", response_text)
    return response_text



def get_llm():
    return init_chat_model(model=settings.GEMINI_MODEL, model_provider="google_genai")