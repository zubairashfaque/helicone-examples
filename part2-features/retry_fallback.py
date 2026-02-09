"""
Retry and Fallback Examples

Demonstrates automatic retries with exponential backoff and provider fallbacks
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)

# Example: Retry with exponential backoff + provider fallback
response = client.chat.completions.create(
    model="gpt-4o/claude-sonnet-4",  # Try GPT-4o, fallback to Claude
    messages=[{"role": "user", "content": "Critical query with fallback"}],
    max_tokens=100,
    extra_headers={
        "Helicone-Retry-Enabled": "true",
        "Helicone-Retry-Num": "3",
        "Helicone-Retry-Factor": "2",  # Exponential: 1s, 2s, 4s
        "Helicone-Fallback-Enabled": "true",
    }
)

print("✅ Request succeeded (possibly after retries/fallback)")
print(f"Model used: {response.model}")
