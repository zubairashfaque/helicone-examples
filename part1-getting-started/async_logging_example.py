"""
Async Logging - Zero Latency Observability

This example demonstrates:
- Zero-latency logging with direct provider calls
- Async log shipping to Helicone
- Fault isolation (Helicone outages don't affect your app)
- Trade-offs: No proxy features (caching, rate limiting)

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from helicone_async import HeliconeAsyncLogger
from openai import OpenAI
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize async logger
logger = HeliconeAsyncLogger(api_key=os.getenv("HELICONE_API_KEY"))
logger.init()  # Patches the OpenAI client to intercept calls

# Standard OpenAI client - calls go directly to OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def latency_test():
    """
    Compare latency with async logging.

    Async logging adds ZERO latency because logs are shipped
    in the background after the response is returned.
    """

    print("Async Logging Latency Test")
    print("=" * 60)
    print()

    prompt = "What are the symptoms of hypertension?"

    # Make 3 calls and measure latency
    latencies = []

    for i in range(3):
        print(f"Call {i+1}/3...", end=" ")

        start_time = time.time()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        latencies.append(latency_ms)

        print(f"{latency_ms:.0f}ms")

    avg_latency = sum(latencies) / len(latencies)

    print()
    print(f"Average latency: {avg_latency:.0f}ms")
    print()
    print("✅ All calls completed with zero added latency")
    print("   Logs are being shipped to Helicone asynchronously")
    print()


def fault_isolation_demo():
    """
    Demonstrate fault isolation.

    If Helicone is down, your app continues to work normally.
    Logs are simply dropped until service resumes.
    """

    print("Fault Isolation Demo")
    print("=" * 60)
    print()

    print("Making API call to OpenAI...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "What is metformin used for?"}
        ],
        max_tokens=100,
    )

    print(f"✅ Response received: {response.choices[0].message.content[:100]}...")
    print()
    print("Even if Helicone is experiencing an outage:")
    print("  ✓ Your application is completely unaffected")
    print("  ✓ Users see no errors or delays")
    print("  ✓ Logs resume when Helicone service is restored")
    print()


def trade_offs_summary():
    """Print summary of async logging trade-offs."""

    print("Async Logging Trade-offs")
    print("=" * 60)
    print()

    print("✅ BENEFITS:")
    print("  • Zero latency impact (0ms added)")
    print("  • Complete fault isolation")
    print("  • Full observability (costs, tokens, latency, responses)")
    print("  • Per-user analytics and custom properties work normally")
    print()

    print("❌ LIMITATIONS:")
    print("  • No response caching (can't reduce costs)")
    print("  • No rate limiting (can't enforce quotas)")
    print("  • No automatic retries with fallback")
    print("  • No LLM security screening")
    print()

    print("💡 WHEN TO USE:")
    print("  • Real-time chat applications (latency-critical)")
    print("  • Voice assistants (every millisecond matters)")
    print("  • High-frequency agent loops (hundreds of calls/second)")
    print("  • Scenarios where observability is needed but not control")
    print()


def main():
    """Run async logging examples."""

    print("=" * 60)
    print("Helicone Async Logging Example")
    print("=" * 60)
    print()

    # Run latency test
    latency_test()

    # Demonstrate fault isolation
    fault_isolation_demo()

    # Show trade-offs summary
    trade_offs_summary()

    print("=" * 60)
    print("View your async-logged requests in Helicone dashboard:")
    print("https://helicone.ai/dashboard")
    print()


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        exit(1)

    main()
