import os

from dotenv import load_dotenv
from google import genai
from groq import Groq

from src.prompts import PATIENT_ANALYSIS_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Agent Logic
def analyze_patient(patient_data):

    prompt = PATIENT_ANALYSIS_PROMPT.format(
        patient_data=patient_data
    )

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a healthcare care-coordination agent."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"Retry {attempt + 1}: {e}")

            time.sleep(5)

    return "Analysis unavailable"

# Create Agent Orchestrator
def run_patient_review(patient):

    print(f"Analyzing patient: {patient['patient_id']}")

    analysis = analyze_patient(patient)

    return {
        "patient_id": patient['patient_id'],
        "patient_name": patient['patient_name'],
        "analysis": analysis
    }

#Hight risk
from src.tools import get_high_risk_patients

def run_high_risk_agent(df):

    high_risk_patients = get_high_risk_patients(df)

    results = []

    for _, patient in high_risk_patients.iterrows():
        result = run_patient_review(patient.to_dict())

        results.append(result)

    return results


#Missed Appointment Agent
from src.tools import get_missed_appointments

def run_missed_appointment_agent(df):

    missed_patients = get_missed_appointments(df)

    results = []

    for _, patient in missed_patients.iterrows():

        result = run_patient_review(
            patient.to_dict()
        )

        results.append(result)

    return results