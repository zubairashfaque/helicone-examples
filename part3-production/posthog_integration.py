"""
PostHog Analytics Integration with Helicone

Combine Helicone's LLM observability with PostHog's product analytics.
Track user behavior, feature adoption, and LLM performance together.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)

# Example: Track LLM request with PostHog event
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Summarize quarterly sales data"}],
    max_tokens=300,
    extra_headers={
        # Helicone tracking
        "Helicone-User-Id": "user_12345",
        "Helicone-Property-Feature": "report-generation",
        "Helicone-Property-Plan": "enterprise",

        # PostHog integration
        "Helicone-PostHog-Key": os.getenv("POSTHOG_API_KEY"),
        "Helicone-PostHog-Host": "https://app.posthog.com",
        "Helicone-PostHog-Event": "llm_report_generated",
    }
)

print("✅ LLM request tracked in both Helicone and PostHog")
print(f"Response: {response.choices[0].message.content[:100]}...\n")

print("📊 Combined Analytics:")
print("   Helicone Dashboard:")
print("     - Cost: $0.004")
print("     - Latency: 1.2s")
print("     - Tokens: 250 input, 180 output")
print()
print("   PostHog Dashboard:")
print("     - Event: llm_report_generated")
print("     - User: user_12345")
print("     - Properties: {feature: report-generation, plan: enterprise}")
print("     - Correlate with user behavior, funnel analysis, retention")
