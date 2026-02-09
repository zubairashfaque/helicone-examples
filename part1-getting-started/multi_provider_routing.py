"""
Multi-Provider Routing with Helicone AI Gateway

This example demonstrates:
- Using the same client for OpenAI, Claude, and Gemini
- Switching providers by changing only the model string
- Automatic cost tracking across all providers
- No SDK changes required

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Single client works for ALL providers via AI Gateway
client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)


def ask_question(model: str, question: str) -> dict:
    """
    Ask a question to any LLM provider via Helicone AI Gateway.

    Args:
        model: Model identifier (e.g., "gpt-4o", "claude-sonnet-4", "gemini-2.0-flash")
        question: User question

    Returns:
        dict with response and metadata
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=300,
        extra_headers={
            "Helicone-Property-Example": "multi-provider",
        }
    )

    usage = response.usage

    return {
        "model": response.model,
        "response": response.choices[0].message.content,
        "tokens": {
            "input": usage.prompt_tokens,
            "output": usage.completion_tokens,
            "total": usage.total_tokens,
        }
    }


def main():
    """Test the same question across multiple providers."""

    print("Multi-Provider Routing with Helicone AI Gateway")
    print("=" * 70)
    print()

    question = "Explain the difference between Type 1 and Type 2 diabetes in 2-3 sentences."

    # Test across three providers with the SAME client
    providers = [
        ("gpt-4o-mini", "OpenAI"),
        ("claude-sonnet-4-20250514", "Anthropic Claude"),
        ("gemini-2.0-flash", "Google Gemini"),
    ]

    results = []

    for model, provider_name in providers:
        print(f"Testing: {provider_name} ({model})")
        print("-" * 70)

        try:
            result = ask_question(model, question)
            results.append((provider_name, result))

            print(f"Model: {result['model']}")
            print(f"Tokens: {result['tokens']['total']} (in: {result['tokens']['input']}, out: {result['tokens']['output']})")
            print(f"\nResponse:\n{result['response']}")
            print()

        except Exception as e:
            print(f"❌ Error with {provider_name}: {e}")
            print("Note: Make sure provider keys are configured in Helicone dashboard")
            print("https://helicone.ai/dashboard/developer/provider-keys")
            print()

    print("=" * 70)
    print("✅ Multi-provider routing complete!")
    print()
    print("Key Benefits:")
    print("  ✓ Same OpenAI-compatible client for all providers")
    print("  ✓ Switch models by changing one string")
    print("  ✓ Automatic cost tracking across all providers")
    print("  ✓ No provider-specific SDK learning curve")
    print()
    print("View cost comparison in Helicone dashboard:")
    print("https://helicone.ai/dashboard/analytics")
    print()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        print("Please create a .env file with your Helicone API key")
        exit(1)

    main()
