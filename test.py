from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")
response = model.generate_content("Hello! Introduce yourself in one sentence.")

print(response.text)