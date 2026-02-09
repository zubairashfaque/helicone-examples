"""
Microsoft AutoGen Integration with Helicone

This example demonstrates:
- Using Helicone with AutoGen v0.4+
- Multi-agent conversation tracking
- Session path hierarchy for agent workflows
- Per-agent cost attribution

Part of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_helicone_autogen_client(
    agent_name: str,
    session_id: str,
    session_path: str = None
):
    """
    Create an AutoGen model client with Helicone observability.

    Args:
        agent_name: Name of the agent (for property tracking)
        session_id: Session ID for grouping multi-agent conversations
        session_path: Optional hierarchical path (e.g., "/triage/analysis")

    Returns:
        OpenAIChatCompletionClient configured with Helicone
    """

    headers = {
        "Helicone-Auth": f"Bearer {os.environ['HELICONE_API_KEY']}",
        "Helicone-Session-Id": session_id,
        "Helicone-Session-Name": "AutoGen Multi-Agent Workflow",
        "Helicone-Property-Framework": "autogen-v0.4",
        "Helicone-Property-Agent": agent_name,
    }

    if session_path:
        headers["Helicone-Session-Path"] = session_path

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://oai.helicone.ai/v1",
        default_headers=headers,
    )

    return model_client


def medical_multi_agent_example():
    """
    Example: Medical consultation multi-agent system.

    Demonstrates:
    - Triage agent → Specialist agent workflow
    - Hierarchical session paths
    - Per-agent cost tracking
    """

    print("AutoGen Medical Multi-Agent Example")
    print("=" * 60)
    print()

    session_id = "autogen-medical-consult-001"

    # Create triage agent client
    print("Setting up Triage Agent...")
    triage_client = create_helicone_autogen_client(
        agent_name="triage-agent",
        session_id=session_id,
        session_path="/medical-consult/triage"
    )
    print(f"✅ Triage agent configured")
    print(f"   Path: /medical-consult/triage")
    print()

    # Create specialist agent client
    print("Setting up Specialist Agent...")
    specialist_client = create_helicone_autogen_client(
        agent_name="specialist-agent",
        session_id=session_id,
        session_path="/medical-consult/specialist"
    )
    print(f"✅ Specialist agent configured")
    print(f"   Path: /medical-consult/specialist")
    print()

    # Create report generator client
    print("Setting up Report Generator...")
    report_client = create_helicone_autogen_client(
        agent_name="report-generator",
        session_id=session_id,
        session_path="/medical-consult/report"
    )
    print(f"✅ Report generator configured")
    print(f"   Path: /medical-consult/report")
    print()

    print("=" * 60)
    print("Multi-Agent System Ready!")
    print()
    print("When these agents communicate, Helicone will track:")
    print("  • Hierarchical session tree with 3 agents")
    print("  • Per-agent costs (filter by 'Agent' property)")
    print("  • Conversation timeline across agents")
    print("  • Total session duration and cost")
    print()
    print(f"View session trace at:")
    print(f"https://helicone.ai/dashboard/sessions/{session_id}")
    print()
    print("Session tree will look like:")
    print("  /medical-consult")
    print("  ├── /triage (triage-agent)")
    print("  ├── /specialist (specialist-agent)")
    print("  └── /report (report-generator)")
    print()


def simple_autogen_example():
    """Simple single-agent AutoGen example."""

    print("Simple AutoGen Example with Helicone")
    print("=" * 60)
    print()

    client = create_helicone_autogen_client(
        agent_name="assistant",
        session_id="autogen-simple-001"
    )

    print("✅ AutoGen client configured with Helicone")
    print("   Model: gpt-4o-mini")
    print("   Framework: autogen-v0.4")
    print("   Session ID: autogen-simple-001")
    print()
    print("All agent conversations will be automatically logged")
    print("View at: https://helicone.ai/dashboard")
    print()


def main():
    """Run AutoGen examples."""

    simple_autogen_example()
    print()
    medical_multi_agent_example()


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        exit(1)

    main()
