import pandas as pd

def get_patient(df, patient_id):
    patient = df[df["patient_id"] == patient_id]

    if patient.empty:
        return None
    
    return patient.iloc[0].to_dict()

def get_high_risk_patients(df):

    return df[(df["days_since_last_visit"] > 180)
    |
    (df["vitals_bp_systolic"] > 160)
    |
    (df["vitals_spo2"] < 92)
    |
    (df["missed_last_appointment"] == "Yes")
    ]


def get_missed_appointments(df):
    return df[df["missed_last_appointment"] == "Yes"]

def get_upcoming_patients(df):
    """
    Patients with scheduled follow-up
    """

    return df[
        df["next_scheduled_visit"].notna()
    ]

