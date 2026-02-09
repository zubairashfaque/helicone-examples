"""
LangChain Integration with Helicone

This example demonstrates:
- Using Helicone with LangChain ChatOpenAI
- Session tracing for multi-step chains
- Custom properties for workflow tracking
- User tracking in LangChain applications

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_helicone_llm(session_id: str = None, user_id: str = None):
    """
    Create a LangChain LLM with Helicone observability.

    Args:
        session_id: Optional session ID for tracing
        user_id: Optional user ID for per-user analytics

    Returns:
        ChatOpenAI instance configured with Helicone
    """

    headers = {
        "Helicone-Property-Framework": "langchain",
    }

    if session_id:
        headers["Helicone-Session-Id"] = session_id

    if user_id:
        headers["Helicone-User-Id"] = user_id

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("HELICONE_API_KEY"),
        base_url="https://ai-gateway.helicone.ai/v1",
        default_headers=headers,
    )

    return llm


def medical_diagnosis_chain():
    """
    Example: Multi-step medical diagnosis workflow with LangChain.

    Demonstrates:
    - Chaining multiple LLM calls
    - Session tracking across chain steps
    - Automatic cost/latency tracking per step
    """

    print("LangChain Medical Diagnosis Chain")
    print("=" * 60)
    print()

    session_id = "langchain-diagnosis-001"

    # Step 1: Symptom analysis
    print("Step 1: Analyzing symptoms...")
    symptom_prompt = ChatPromptTemplate.from_template(
        "You are a medical assistant. Analyze these symptoms and list possible conditions:\n{symptoms}"
    )

    symptom_llm = create_helicone_llm(session_id=session_id, user_id="doctor-smith")
    symptom_chain = symptom_prompt | symptom_llm | StrOutputParser()

    symptoms = "Patient reports: severe headache, fever, stiff neck, sensitivity to light"
    analysis = symptom_chain.invoke({"symptoms": symptoms})

    print(f"Analysis: {analysis[:200]}...")
    print()

    # Step 2: Recommendation generation
    print("Step 2: Generating recommendations...")
    recommendation_prompt = ChatPromptTemplate.from_template(
        "Based on this medical analysis, provide treatment recommendations:\n{analysis}"
    )

    recommendation_llm = create_helicone_llm(session_id=session_id, user_id="doctor-smith")
    recommendation_chain = recommendation_prompt | recommendation_llm | StrOutputParser()

    recommendations = recommendation_chain.invoke({"analysis": analysis})

    print(f"Recommendations: {recommendations[:200]}...")
    print()

    print("=" * 60)
    print("✅ LangChain workflow complete!")
    print()
    print("View the full chain trace in Helicone:")
    print(f"https://helicone.ai/dashboard/sessions/{session_id}")
    print()
    print("You can see:")
    print("  • Both LLM calls in the session timeline")
    print("  • Individual costs and latencies per step")
    print("  • Total session cost and duration")
    print("  • Per-user (doctor-smith) analytics")
    print()


def simple_invoke_example():
    """Simple single-call example with Helicone."""

    print("Simple LangChain Invoke Example")
    print("=" * 60)
    print()

    llm = create_helicone_llm(user_id="doctor-jones")

    response = llm.invoke("Summarize the latest diabetes treatment guidelines in 2 sentences.")

    print(f"Response: {response.content}")
    print()
    print("✅ Single call logged to Helicone")
    print("   View at: https://helicone.ai/dashboard")
    print()


def main():
    """Run LangChain examples."""

    # Simple example first
    simple_invoke_example()

    # Multi-step chain example
    medical_diagnosis_chain()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        print("Please create a .env file with your Helicone API key")
        exit(1)

    main()
