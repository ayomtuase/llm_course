import os

import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_AI_SECRET_KEY")

try:
    client = openai.OpenAI(api_key=api_key)
    print("OpenAI client initialized successfully.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    # You might want to exit or raise the error here depending on desired behavior
    raise
