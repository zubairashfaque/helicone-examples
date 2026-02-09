"""
Healthcare AI Triage Assistant - Complete Example

This example demonstrates:
- AI Gateway integration with Helicone
- Custom property tagging (department, environment)
- User tracking (per-patient analytics)
- Prompt versioning for reproducibility
- Full observability: cost, latency, tokens

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize with Helicone AI Gateway
client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)


def triage_patient(patient_id: str, symptoms: str, department: str) -> dict:
    """
    Classify patient symptoms using LLM with full Helicone observability.

    Args:
        patient_id: Unique patient identifier
        symptoms: Patient-reported symptoms
        department: Hospital department (cardiology, emergency, etc.)

    Returns:
        dict with classification, rationale, and metadata
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical triage assistant. Classify the urgency "
                    "of patient symptoms as: EMERGENCY, URGENT, STANDARD, or "
                    "LOW-PRIORITY. Provide a brief rationale (2-3 sentences)."
                ),
            },
            {
                "role": "user",
                "content": f"Patient symptoms: {symptoms}"
            },
        ],
        max_tokens=200,
        temperature=0.1,  # Low temperature for consistent triage decisions
        extra_headers={
            # Track which user (patient) this request is for
            "Helicone-User-Id": patient_id,

            # Custom properties for analytics and filtering
            "Helicone-Property-Department": department,
            "Helicone-Property-App": "triage-assistant",
            "Helicone-Property-Environment": "production",

            # Associate with a versioned prompt for prompt management
            "Helicone-Prompt-Id": "triage-classifier-v1",
        },
    )

    # Extract response content
    classification = response.choices[0].message.content

    # Calculate metrics (these are automatically logged by Helicone)
    usage = response.usage

    return {
        "classification": classification,
        "patient_id": patient_id,
        "department": department,
        "tokens_used": {
            "input": usage.prompt_tokens,
            "output": usage.completion_tokens,
            "total": usage.total_tokens,
        },
        "model": response.model,
    }


def main():
    """Run example triage scenarios."""

    print("Healthcare AI Triage Assistant")
    print("=" * 60)
    print()

    # Example 1: Emergency case
    print("Example 1: EMERGENCY CASE")
    print("-" * 60)
    result = triage_patient(
        patient_id="patient-7829",
        symptoms="Severe chest pain, shortness of breath, sweating, radiating pain to left arm",
        department="cardiology"
    )
    print(f"Patient ID: {result['patient_id']}")
    print(f"Department: {result['department']}")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['tokens_used']['total']} (in: {result['tokens_used']['input']}, out: {result['tokens_used']['output']})")
    print(f"\nClassification:\n{result['classification']}")
    print()

    # Example 2: Routine case
    print("Example 2: ROUTINE CASE")
    print("-" * 60)
    result = triage_patient(
        patient_id="patient-3421",
        symptoms="Mild headache for 2 days, no fever, no visual disturbances",
        department="general-practice"
    )
    print(f"Patient ID: {result['patient_id']}")
    print(f"Department: {result['department']}")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['tokens_used']['total']} (in: {result['tokens_used']['input']}, out: {result['tokens_used']['output']})")
    print(f"\nClassification:\n{result['classification']}")
    print()

    # Example 3: Urgent case
    print("Example 3: URGENT CASE")
    print("-" * 60)
    result = triage_patient(
        patient_id="patient-5612",
        symptoms="High fever (103°F), persistent cough for 5 days, difficulty breathing",
        department="respiratory"
    )
    print(f"Patient ID: {result['patient_id']}")
    print(f"Department: {result['department']}")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['tokens_used']['total']} (in: {result['tokens_used']['input']}, out: {result['tokens_used']['output']})")
    print(f"\nClassification:\n{result['classification']}")
    print()

    print("=" * 60)
    print("✅ All examples completed!")
    print()
    print("View your requests in the Helicone dashboard:")
    print("https://helicone.ai/dashboard")
    print()
    print("Filter by:")
    print("  - Property 'Department' to see per-department analytics")
    print("  - User ID to track individual patient request history")
    print("  - Prompt ID 'triage-classifier-v1' to analyze this prompt's performance")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found in environment variables")
        print("Please create a .env file with your Helicone API key")
        print("See .env.example for template")
        exit(1)

    main()
