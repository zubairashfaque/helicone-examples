"""
Caching Examples - Reduce Costs by 20-30%

Demonstrates:
- Basic caching with TTL
- Bucket caching for non-deterministic prompts
- Cache seeds for per-user namespaces

Part 2 of the Helicone tutorial series
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)


def basic_caching_example():
    """Enable caching with 24-hour TTL"""
    print("Example 1: Basic Caching (24-hour TTL)")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is Type 2 diabetes?"}],
        max_tokens=200,
        temperature=0,  # Deterministic for caching
        extra_headers={
            "Helicone-Cache-Enabled": "true",
            "Cache-Control": "max-age=86400",  # 24 hours
        }
    )

    print(f"Response: {response.choices[0].message.content[:100]}...")
    print(f"Cache Status: {response.headers.get('Helicone-Cache', 'MISS')}")
    print("\nRun again within 24 hours to see CACHE HIT")
    print()


def bucket_caching_example():
    """Bucket caching for non-deterministic prompts"""
    print("Example 2: Bucket Caching (Non-deterministic)")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Give me 3 healthy breakfast ideas"}],
        max_tokens=200,
        temperature=0.7,  # Non-deterministic
        extra_headers={
            "Helicone-Cache-Enabled": "true",
            "Helicone-Cache-Bucket-Max-Size": "5",  # Store 5 variations
            "Cache-Control": "max-age=3600",
        }
    )

    print(f"Response: {response.choices[0].message.content[:100]}...")
    print("Bucket caching stores 5 variations, returns random on hit")
    print()


def cache_seed_example():
    """Per-user cache namespaces"""
    print("Example 3: Cache Seeds (Per-User Namespaces)")
    print("=" * 60)

    user_id = "user-123"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "My personalized health tips"}],
        max_tokens=150,
        temperature=0,
        extra_headers={
            "Helicone-Cache-Enabled": "true",
            "Helicone-Cache-Seed": user_id,  # Per-user cache
            "Cache-Control": "max-age=7200",
        }
    )

    print(f"Response for {user_id}: {response.choices[0].message.content[:80]}...")
    print("Each user gets their own cached responses")
    print()


if __name__ == "__main__":
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    basic_caching_example()
    bucket_caching_example()
    cache_seed_example()

    print("✅ All caching examples complete!")
    print("Check Helicone dashboard for cache hit rates")
