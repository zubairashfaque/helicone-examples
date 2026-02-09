"""
Complete AutoGen Multi-Agent Healthcare System with Helicone

Demonstrates production-grade multi-agent workflow:
- Triage Agent: Initial patient assessment
- Emergency Specialist: Handles urgent cases
- Routine Specialist: Handles non-urgent cases
- Report Generator: Creates final medical report

Full Helicone instrumentation with session tracing and cost attribution.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

# Initialize Helicone-enabled client
client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),
)

def triage_agent(patient_symptoms, session_id, patient_id):
    """Agent 1: Triage - Assess severity and route to appropriate specialist"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical triage nurse. Assess symptom severity and classify as EMERGENCY or ROUTINE."},
            {"role": "user", "content": f"Patient reports: {patient_symptoms}"}
        ],
        max_tokens=150,
        temperature=0,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage",
            "Helicone-Property-Agent": "triage",
            "Helicone-Property-Department": "emergency-dept",
            "Helicone-User-Id": patient_id,
            "Helicone-Cache-Enabled": "true",
            "Cache-Control": "max-age=3600",
        }
    )
    return response.choices[0].message.content

def emergency_specialist(triage_assessment, session_id, patient_id):
    """Agent 2: Emergency Specialist - Handle urgent cases"""
    response = client.chat.completions.create(
        model="gpt-4o",  # Use more capable model for emergency
        messages=[
            {"role": "system", "content": "You are an emergency medicine specialist. Provide immediate diagnostic recommendations."},
            {"role": "user", "content": f"Triage assessment: {triage_assessment}"}
        ],
        max_tokens=300,
        temperature=0,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/emergency-specialist",
            "Helicone-Property-Agent": "emergency-specialist",
            "Helicone-Property-Department": "emergency-dept",
            "Helicone-User-Id": patient_id,
        }
    )
    return response.choices[0].message.content

def routine_specialist(triage_assessment, session_id, patient_id):
    """Agent 2: Routine Specialist - Handle non-urgent cases"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cost-effective for routine cases
        messages=[
            {"role": "system", "content": "You are a general practice physician. Provide diagnostic recommendations for routine cases."},
            {"role": "user", "content": f"Triage assessment: {triage_assessment}"}
        ],
        max_tokens=250,
        temperature=0,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/routine-specialist",
            "Helicone-Property-Agent": "routine-specialist",
            "Helicone-Property-Department": "primary-care",
            "Helicone-User-Id": patient_id,
            "Helicone-Cache-Enabled": "true",
            "Cache-Control": "max-age=7200",
        }
    )
    return response.choices[0].message.content

def report_generator(specialist_diagnosis, session_id, patient_id):
    """Agent 3: Report Generator - Create final medical report"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical report writer. Create a structured patient report."},
            {"role": "user", "content": f"Specialist diagnosis: {specialist_diagnosis}"}
        ],
        max_tokens=400,
        temperature=0,
        extra_headers={
            "Helicone-Session-Id": session_id,
            "Helicone-Session-Path": "/triage/report",
            "Helicone-Property-Agent": "report-generator",
            "Helicone-Property-Department": "medical-records",
            "Helicone-User-Id": patient_id,
        }
    )
    return response.choices[0].message.content

# Example workflow
if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    patient_id = "patient_12345"

    # Patient presents with symptoms
    symptoms = "Severe chest pain radiating to left arm, shortness of breath, started 20 minutes ago"

    print("🏥 Healthcare Multi-Agent Workflow\n")

    # Step 1: Triage
    print("1️⃣ Triage Agent assessing...")
    triage_result = triage_agent(symptoms, session_id, patient_id)
    print(f"   Result: {triage_result[:100]}...\n")

    # Step 2: Route to specialist based on severity
    if "EMERGENCY" in triage_result.upper():
        print("2️⃣ Routing to Emergency Specialist...")
        diagnosis = emergency_specialist(triage_result, session_id, patient_id)
    else:
        print("2️⃣ Routing to Routine Specialist...")
        diagnosis = routine_specialist(triage_result, session_id, patient_id)
    print(f"   Diagnosis: {diagnosis[:100]}...\n")

    # Step 3: Generate report
    print("3️⃣ Generating Medical Report...")
    report = report_generator(diagnosis, session_id, patient_id)
    print(f"   Report: {report[:100]}...\n")

    print(f"✅ Workflow complete! Session ID: {session_id}")
    print(f"📊 View session tree in Helicone dashboard:")
    print(f"   /triage → /triage/emergency-specialist → /triage/report")
