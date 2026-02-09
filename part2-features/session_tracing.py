"""
Session Tracing - Multi-Agent Workflow Example

This example demonstrates:
- Hierarchical session paths for multi-step workflows
- Parent-child agent relationships
- Per-agent cost attribution
- Session trees in Helicone dashboard

Part 2 of the Helicone tutorial series: https://zubairashfaque.github.io/
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)


def multi_agent_healthcare_workflow(patient_id: str, symptoms: str):
    """
    Demonstrate multi-agent workflow with hierarchical session tracing.

    Workflow:
    1. Triage agent (root) - Initial assessment
    2. Analysis agent (child) - Detailed analysis
    3. Lab review agent (grandchild) - Lab data review
    4. Report generator (child) - Final report
    """

    session_id = f"healthcare-session-{patient_id}"

    print(f"Starting multi-agent workflow for patient {patient_id}")
    print("=" * 70)

    # Step 1: Triage Agent (Root)
    print("\n[1/4] Triage Agent - Initial Assessment")
    triage_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a triage nurse. Assess urgency level."},
            {"role": "user", "content": f"Patient symptoms: {symptoms}"}
        ],
        max_tokens=150,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage",
            "Helicone-Session-Name": "Healthcare Multi-Agent Workflow",
            "Helicone-Property-Agent": "triage",
            "Helicone-User-Id": patient_id,
        }
    )

    triage_result = triage_response.choices[0].message.content
    print(f"Triage: {triage_result[:100]}...")
    print(f"Cost: ${triage_response.usage.total_tokens * 0.00015 / 1000:.6f}")

    # Step 2: Analysis Agent (Child of triage)
    print("\n[2/4] Analysis Agent - Detailed Analysis")
    analysis_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a diagnostic specialist. Provide detailed analysis."},
            {"role": "user", "content": f"Triage says: {triage_result}. Provide detailed analysis."}
        ],
        max_tokens=300,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/analysis",  # Child of /triage
            "Helicone-Property-Agent": "analysis",
            "Helicone-User-Id": patient_id,
        }
    )

    analysis_result = analysis_response.choices[0].message.content
    print(f"Analysis: {analysis_result[:100]}...")
    print(f"Cost: ${analysis_response.usage.total_tokens * 0.0025 / 1000:.6f}")

    # Step 3: Lab Review Agent (Grandchild - child of analysis)
    print("\n[3/4] Lab Review Agent - Lab Data Analysis")
    lab_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a lab data analyst. Review hypothetical lab results."},
            {"role": "user", "content": "Review lab results for the analysis above."}
        ],
        max_tokens=200,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/analysis/lab-review",  # Grandchild
            "Helicone-Property-Agent": "lab-review",
            "Helicone-User-Id": patient_id,
        }
    )

    lab_result = lab_response.choices[0].message.content
    print(f"Lab Review: {lab_result[:100]}...")
    print(f"Cost: ${lab_response.usage.total_tokens * 0.0025 / 1000:.6f}")

    # Step 4: Report Generator (Child of triage, sibling of analysis)
    print("\n[4/4] Report Generator - Final Report")
    report_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate a concise medical report."},
            {"role": "user", "content": f"Compile: Triage={triage_result}, Analysis={analysis_result}"}
        ],
        max_tokens=200,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/report",  # Sibling of /analysis
            "Helicone-Property-Agent": "report-generator",
            "Helicone-User-Id": patient_id,
        }
    )

    report_result = report_response.choices[0].message.content
    print(f"Report: {report_result[:100]}...")
    print(f"Cost: ${report_response.usage.total_tokens * 0.00015 / 1000:.6f}")

    # Calculate total cost
    total_cost = (
        triage_response.usage.total_tokens * 0.00015 / 1000 +
        analysis_response.usage.total_tokens * 0.0025 / 1000 +
        lab_response.usage.total_tokens * 0.0025 / 1000 +
        report_response.usage.total_tokens * 0.00015 / 1000
    )

    print("\n" + "=" * 70)
    print(f"✅ Workflow Complete!")
    print(f"Total Cost: ${total_cost:.6f}")
    print(f"\nView session tree in Helicone:")
    print(f"https://helicone.ai/dashboard/sessions/{session_id}")
    print("\nSession hierarchy:")
    print("  /triage (root)")
    print("  ├── /triage/analysis")
    print("  │   └── /triage/analysis/lab-review")
    print("  └── /triage/report")


if __name__ == "__main__":
    if not os.getenv("HELICONE_API_KEY"):
        print("❌ Error: HELICONE_API_KEY not found")
        exit(1)

    multi_agent_healthcare_workflow(
        patient_id="patient-9876",
        symptoms="Persistent fever, cough, fatigue for 5 days"
    )
