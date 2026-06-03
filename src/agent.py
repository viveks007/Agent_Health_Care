import os

from dotenv import load_dotenv
from google import genai

from src.prompts import PATIENT_ANALYSIS_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GENAI_API_KEY")
)

def analyze_patient(patient_data):

    prompt = PATIENT_ANALYSIS_PROMPT.format(
        patient_data=patient_data
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# Create Agent Orchestrator
def run_patient_review(patient):

    print(f"Analyzing patient: {patient['patient_id']}")

    analysis = analyze_patient(patient)

    return {
        "patient_id": patient['patient_id'],
        "patient_name": patient['patient_name'],
        "analysis": analysis
    }


from src.tools import get_high_risk_patients

def run_high_risk_agent():

    high_risk_patients = get_high_risk_patients(df)

    results = []

    for _, patient in high_risk_patients.iterrows():
        result = run_patient_review(patient.to_dict())

        results.append(result)

    return results


#Missed Appointment Agent
from src.tools import get_missed_appointments

def run_missed_appointment_agent():
    missed_appointments = get_missed_appointments(df)

    results = []

    for _, patient in missed_appointments.iterrows():
        result = run_patient_review(patient.to_dict())

        results.append(result)

    return results

