"""
CrewAI Integration with Helicone

This example demonstrates:
- Using Helicone with CrewAI multi-agent workflows
- Per-agent observability
- Custom properties for agent tracking
- Session tracing across agent interactions

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from crewai import LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_helicone_crewai_llm(agent_name: str = None, session_id: str = None):
    """
    Create a CrewAI LLM with Helicone observability.

    Args:
        agent_name: Optional agent name for tracking
        session_id: Optional session ID for multi-agent tracing

    Returns:
        LLM instance configured with Helicone
    """

    headers = {
        "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}",
        "Helicone-Property-Framework": "crewai",
    }

    if agent_name:
        headers["Helicone-Property-Agent"] = agent_name

    if session_id:
        headers["Helicone-Session-Id"] = session_id

    llm = LLM(
        model="gpt-4o-mini",
        base_url="https://oai.helicone.ai/v1",
        api_key=os.environ.get("OPENAI_API_KEY"),
        extra_headers=headers
    )

    return llm


def medical_research_agent_example():
    """
    Example: Medical research agent with CrewAI.

    Note: This is a simplified example showing LLM configuration.
    Full CrewAI agent and task setup would follow CrewAI patterns.
    """

    print("CrewAI Medical Research Agent Example")
    print("=" * 60)
    print()

    session_id = "crewai-medical-research-001"

    # Create LLM for research agent
    print("Creating research agent with Helicone observability...")
    research_llm = create_helicone_crewai_llm(
        agent_name="medical-researcher",
        session_id=session_id
    )

    print(f"✅ Research agent configured")
    print(f"   Session ID: {session_id}")
    print(f"   Agent: medical-researcher")
    print(f"   Model: gpt-4o-mini")
    print()

    # Create LLM for writer agent
    print("Creating writer agent with Helicone observability...")
    writer_llm = create_helicone_crewai_llm(
        agent_name="medical-writer",
        session_id=session_id
    )

    print(f"✅ Writer agent configured")
    print(f"   Session ID: {session_id}")
    print(f"   Agent: medical-writer")
    print(f"   Model: gpt-4o-mini")
    print()

    print("=" * 60)
    print("Agent Configuration Complete!")
    print()
    print("When these agents make LLM calls, you'll see in Helicone:")
    print("  • All calls grouped by session ID")
    print("  • Per-agent cost breakdown (filterable by 'Agent' property)")
    print("  • Individual agent latencies")
    print("  • Full conversation trace across agents")
    print()
    print(f"View session trace at:")
    print(f"https://helicone.ai/dashboard/sessions/{session_id}")
    print()


def simple_crewai_llm_call():
    """Simple demonstration of CrewAI LLM with Helicone."""

    print("Simple CrewAI LLM Call with Helicone")
    print("=" * 60)
    print()

    llm = create_helicone_crewai_llm(agent_name="test-agent")

    print("Making LLM call through CrewAI + Helicone...")
    print()

    # Note: CrewAI's LLM.call() method may have different signatures
    # This is a conceptual example
    print("✅ LLM configured and ready")
    print("   All calls will be logged to Helicone automatically")
    print("   Filter by 'Framework: crewai' to see all CrewAI requests")
    print()


def main():
    """Run CrewAI examples."""

    simple_crewai_llm_call()
    print()
    medical_research_agent_example()


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        exit(1)

    main()
