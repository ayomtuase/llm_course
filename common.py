import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPEN_AI_SECRET_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

try:
    openai_client = openai.OpenAI(api_key=openai_api_key)
    print("OpenAI client initialized successfully.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    # You might want to exit or raise the error here depending on desired behavior
    raise
