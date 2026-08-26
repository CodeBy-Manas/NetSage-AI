import os

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found in .env"
    )

# Create Gemini client
client = genai.Client(
    api_key=api_key
)

# Simple Gemini request
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Reply with exactly: NetSage connection successful."
)

print("Gemini response:")
print(response.text)