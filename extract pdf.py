from dotenv import load_dotenv
import os
load_dotenv()
import pdfplumber
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

with pdfplumber.open("sample_statement.pdf.pdf") as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()

model = genai.GenerativeModel("gemini-flash-latest")

prompt = f"""
Extract all transactions from this bank statement text.
Return ONLY a JSON list, each item with: date, description, amount, balance.

Text:
{text}
"""

response = model.generate_content(prompt)

print(response.text)
import json
import pandas as pd

# Clean the response (remove markdown code blocks if present)
clean_text = response.text.strip()
if clean_text.startswith("```"):
    clean_text = clean_text.split("```")[1]
    if clean_text.startswith("json"):
        clean_text = clean_text[4:]

data = json.loads(clean_text)
df = pd.DataFrame(data)
df.to_csv("transactions.csv", index=False)
print("\nSaved to transactions.csv!")