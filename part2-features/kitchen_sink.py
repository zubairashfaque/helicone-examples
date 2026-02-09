"""
Kitchen Sink Example - All Features Combined

Demonstrates using multiple Helicone features in a single request
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is diabetes?"}],
    max_tokens=200,
    temperature=0,
    extra_headers={
        # Session tracing
        "Helicone-Session-Id": "kitchen-sink-001",
        "Helicone-Session-Path": "/demo",
        
        # User tracking
        "Helicone-User-Id": "demo-user",
        
        # Custom properties
        "Helicone-Property-Environment": "demo",
        "Helicone-Property-Feature": "kitchen-sink",
        
        # Caching
        "Helicone-Cache-Enabled": "true",
        "Cache-Control": "max-age=3600",
        
        # Rate limiting
        "Helicone-RateLimit-Policy": "100;w=3600;s=user",
        
        # Prompt versioning
        "Helicone-Prompt-Id": "diabetes-query-v1",
    }
)

print("✅ Request with ALL features enabled!")
print(f"Response: {response.choices[0].message.content[:100]}...")
print("\nFeatures active:")
print("  ✓ Session tracing")
print("  ✓ User tracking") 
print("  ✓ Custom properties")
print("  ✓ Caching")
print("  ✓ Rate limiting")
print("  ✓ Prompt versioning")
