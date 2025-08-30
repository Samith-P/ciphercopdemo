import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:/volume E/ciphercop-2025/gemini-clone/.env")

api_key = os.environ.get("GEMINI_API_KEY")
print("Gemini key found:", bool(api_key))

genai.configure(api_key=api_key)

# Try a lighter model if quota exceeded
model = genai.GenerativeModel("gemini-1.5-flash")

resp = model.generate_content("Hello from Gemini test")
print("Gemini response:", resp.text[:200])
