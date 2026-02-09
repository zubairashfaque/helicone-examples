"""
Rate Limiting Examples - Cost Control and Quota Management

Demonstrates:
- Global rate limiting
- Per-user rate limiting
- Cost-based rate limiting (in cents)
- Per-property rate limiting

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


def global_rate_limit():
    """Global limit: 1000 requests per hour"""
    print("Example 1: Global Rate Limit")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Test message"}],
        max_tokens=50,
        extra_headers={
            "Helicone-RateLimit-Policy": "1000;w=3600",  # 1000 req/hour
        }
    )

    remaining = response.headers.get("Helicone-RateLimit-Remaining", "N/A")
    print(f"Remaining requests: {remaining}")
    print()


def per_user_rate_limit():
    """Per-user limit: 100 requests per day"""
    print("Example 2: Per-User Rate Limit")
    print("=" * 60)

    user_id = "user-456"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "User-specific query"}],
        max_tokens=50,
        extra_headers={
            "Helicone-RateLimit-Policy": "100;w=86400;s=user",  # 100/day per user
            "Helicone-User-Id": user_id,
        }
    )

    remaining = response.headers.get("Helicone-RateLimit-Remaining", "N/A")
    print(f"User {user_id} remaining: {remaining}")
    print()


def cost_based_rate_limit():
    """Cost-based limit: $5 per day per user"""
    print("Example 3: Cost-Based Rate Limit ($5/day)")
    print("=" * 60)

    user_id = "user-789"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Another query"}],
        max_tokens=50,
        extra_headers={
            "Helicone-RateLimit-Policy": "500;w=86400;u=cents;s=user",  # $5/day
            "Helicone-User-Id": user_id,
        }
    )

    remaining_cents = response.headers.get("Helicone-RateLimit-Remaining", "N/A")
    print(f"User {user_id} budget remaining: {remaining_cents} cents")
    print()


def department_rate_limit():
    """Per-department limit: 5000 requests per hour"""
    print("Example 4: Department Rate Limit")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Department query"}],
        max_tokens=50,
        extra_headers={
            "Helicone-RateLimit-Policy": "5000;w=3600;s=property",
            "Helicone-Property-Department": "cardiology",
        }
    )

    remaining = response.headers.get("Helicone-RateLimit-Remaining", "N/A")
    print(f"Cardiology dept remaining: {remaining}")
    print()


if __name__ == "__main__":
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    global_rate_limit()
    per_user_rate_limit()
    cost_based_rate_limit()
    department_rate_limit()

    print("✅ All rate limiting examples complete!")
    print("\nRate Limit Policy Syntax:")
    print("  [quota];w=[window];u=[unit];s=[segment]")
    print("  quota: Number of requests or cents")
    print("  window: Time in seconds")
    print("  unit: 'requests' (default) or 'cents'")
    print("  segment: 'user', 'property', or omit for global")
