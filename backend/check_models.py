import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

models = [
    "models/gemini-3.5-flash",
    "models/gemini-flash-latest",
    "models/gemini-3-flash-preview",
    "models/gemini-pro-latest",
    "models/gemini-2.0-flash",
]

for model in models:
    print(f"\nTesting: {model}")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say hello in one sentence."
        )
        print("✅ SUCCESS")
        print(response.text)
        break
    except Exception as e:
        print("❌ FAILED")
        print(e)